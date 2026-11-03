"""Read-only synthetic recovery policy. No controller connection or actuator API."""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
PACKAGE=json.loads((ROOT/'data/procedures.json').read_text())
CHECKS={'C_RECIPE','C_SETUP','C_OBSERVE'}

def age(now,then):
 return (datetime.fromisoformat(now.replace('Z','+00:00'))-datetime.fromisoformat(then.replace('Z','+00:00'))).total_seconds()

def applicable(i):
 return i['machine']['family']==PACKAGE['family'] and i['machine']['software'] in PACKAGE['software']

def prepare(i,full=True):
 """Shared numeric/state extraction, not next-action selection. No gold labels."""
 p=deepcopy(i)
 if not full:
  p.pop('history',None);p.pop('operator',None);p.pop('outcomes',None)
 h=[e for e in p.get('history',[]) if e['episode']==i['episode']]
 relevant=[e for e in h if e['kind'] in {'alarm','attempt','recipe','state'}]
 attempts=[e for e in h if e['kind']=='attempt' and e['quality']=='good']
 failed=Counter(e['check'] for e in attempts if e['outcome']=='unresolved')
 p['derived']={'snapshot_age_seconds':age(i['now'],i['snapshot']['at']),
  'history_available':bool(relevant),
  'history_fresh':bool(relevant) and 0<=min(age(i['now'],e['at']) for e in relevant)<=300,
  'bad_history_ids':[e['id'] for e in relevant if e['quality']!='good' or age(i['now'],e['at'])<0],
  'attempted_check_ids':sorted(set(e['check'] for e in attempts)),
  'unresolved_counts':dict(failed)}
 return p

def source_ids(p):
 ids={p['machine']['id'],p['snapshot']['id']}
 ids.update(e['id'] for e in p.get('history',[]))
 ids.update(e['id'] for e in p.get('outcomes',[]))
 if 'operator' in p:ids.add(p['operator']['id'])
 return ids

def decision(a,refs):
 return {'action_id':a,'evidence_ids':list(dict.fromkeys(refs)), 'missing_information':PACKAGE['actions'][a]['missing']}

def bad_data(p):
 d=p['derived']; s=p['snapshot']
 return d['snapshot_age_seconds']<0 or d['snapshot_age_seconds']>120 or s['quality']!='good' or not d['history_available'] or not d['history_fresh'] or bool(d['bad_history_ids'])

def conflicts(p):
 """Full-evidence baseline: simple explicit note grammar, no model/labels."""
 h=[e for e in p.get('history',[]) if e['episode']==p['episode']]
 recipes=defaultdict(list)
 for e in h:
  if e['kind']=='recipe':recipes[e['at']].append(e)
 for entries in recipes.values():
  if len({e['value'] for e in entries})>1:return [e['id'] for e in entries]
 note=p.get('operator',{}).get('text','')
 m=re.search(r'(?:display (?:says|shows)|displayed|screen (?:says|shows))\s+(?:recipe\s+)?(R\d+)',note,re.I)
 if m and p['snapshot']['recipe'] and m.group(1).upper()!=p['snapshot']['recipe']:return ['N0','S0']
 # A bounded parser is deliberately visible. It cannot cover arbitrary operator prose.
 reported=[]
 if re.search(r'I (?:already )?(?:copied|recorded) the alarm[- ]detail',note,re.I):reported.append('C_OBSERVE')
 if re.search(r'I (?:already )?(?:read|recorded) the setup',note,re.I):reported.append('C_SETUP')
 if any(a not in p['derived']['attempted_check_ids'] for a in reported):return ['N0']
 return []

def tree(p):
 s=p['snapshot'];d=p['derived']
 if not applicable(p):return decision('E_VERSION',['M0'])
 if bad_data(p):
  refs=['S0']+d['bad_history_ids']
  if not d['history_fresh']: refs += [e['id'] for e in p.get('history',[]) if e['kind'] in {'alarm','attempt','recipe','state'} and e['episode']==p['episode']]
  return decision('Q_FRESH',refs)
 conflict=conflicts(p)
 if conflict:return decision('Q_CONFLICT',conflict)
 if s['alarm'] not in PACKAGE['alarms']:return decision('E_UNKNOWN',['S0'])
 repeated=[k for k,n in d['unresolved_counts'].items() if n>=2]
 if repeated:return decision('E_REPEAT',[e['id'] for e in p['history'] if e['kind']=='attempt' and e['episode']==p['episode'] and e['check'] in repeated and e['outcome']=='unresolved'])
 if s['state']=='RUNNING':return decision('Q_OUTCOME',['S0'])
 if not s['recipe'] or not s['job_recipe']:return decision('Q_RECIPE',['S0'])
 attempted=set(d['attempted_check_ids'])
 refs=['S0']+[e['id'] for e in p.get('history',[]) if e['episode']==p['episode'] and e['kind'] in {'alarm','attempt'}]
 if s['recipe']!=s['job_recipe']:return decision('E_SERVICE' if 'C_RECIPE' in attempted else 'C_RECIPE',refs)
 if s['alarm']=='SYN-201' and 'C_SETUP' not in attempted:return decision('C_SETUP',refs)
 if 'C_OBSERVE' not in attempted:return decision('C_OBSERVE',refs)
 return decision('E_SERVICE',refs)

def alarm_lookup(p):
 # Deliberately narrow comparator; not the deciding competitor.
 return decision({'SYN-201':'C_RECIPE','SYN-202':'C_OBSERVE'}.get(p['snapshot']['alarm'],'E_UNKNOWN'),['S0'])

def parse_answer(raw):
 final=raw.rsplit('</think>',1)[-1].strip()
 if final.startswith('```') and final.endswith('```'):
  final=re.sub(r'^```(?:json)?\s*','',final)[:-3].strip()
 try:
  obj=json.loads(final)
  return obj if isinstance(obj,dict) else None, final
 except (ValueError,TypeError):return None,final

def validate(candidate,p):
 """Output/type/evidence guard plus deterministic eligibility; never rewrites a choice to gold."""
 errors=[]
 if not isinstance(candidate,dict):return decision('E_VALIDATION',['S0']),['invalid_json']
 if set(candidate)!={'action_id','evidence_ids','missing_information'}:errors.append('unsupported_fields_or_prose')
 a=candidate.get('action_id');refs=candidate.get('evidence_ids');missing=candidate.get('missing_information')
 if not isinstance(a,str) or a not in PACKAGE['actions']:errors.append('unknown_action')
 if not isinstance(refs,list) or not refs or not all(isinstance(r,str) for r in refs):errors.append('invalid_evidence_schema')
 elif not set(refs)<=source_ids(p):errors.append('nonexistent_evidence')
 if not isinstance(missing,list) or not all(isinstance(x,str) for x in missing):errors.append('invalid_missing_schema')
 elif isinstance(a,str) and a in PACKAGE['actions'] and missing!=PACKAGE['actions'][a]['missing']:errors.append('invalid_missing_fields')
 if isinstance(a,str) and a in CHECKS:
  if not applicable(p):errors.append('inapplicable_procedure')
  if bad_data(p):errors.append('incomplete_evidence')
  if a in p['derived']['attempted_check_ids']:errors.append('exhausted_check')
 if errors:return decision('E_VALIDATION',['S0']),errors
 return candidate,[]

def score(case,candidate,p,final,errors):
 gold=case['gold'];a=candidate.get('action_id') if isinstance(candidate,dict) else None
 refs=candidate.get('evidence_ids',[]) if isinstance(candidate,dict) else []
 refs_ok=isinstance(refs,list) and bool(refs) and all(isinstance(r,str) and r in source_ids(p) for r in refs)
 expected=gold['action_id'];correct=a==expected
 schema_ok=isinstance(candidate,dict) and set(candidate)=={'action_id','evidence_ids','missing_information'}
 return {'correct':correct,'delivered_correct':final['action_id']==expected,
  'requires_escalation':expected.startswith('E_'),'selected_escalation':isinstance(a,str) and a.startswith('E_'),
  'valid_evidence_refs':refs_ok,
  'complete_gold_evidence':correct and refs_ok and set(gold['required_evidence'])<=set(refs),
  'unsupported_assertion':not schema_ok or (isinstance(candidate,dict) and a not in PACKAGE['actions']),
  'unsupported_check_selection':isinstance(a,str) and a in CHECKS and not correct,
  'valid_response':not errors,
  'passed':correct and not errors and refs_ok and set(gold['required_evidence'])<=set(refs)}
