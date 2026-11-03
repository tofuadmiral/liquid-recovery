"""Compact evidence adapter; arithmetic and eligibility only, never answer selection."""
import json
from engine import PACKAGE,ROOT,applicable,parse_answer

def compact(p):
 d=p['derived'];s=p['snapshot']; full='history' in p
 relation='MISSING' if not s['recipe'] or not s['job_recipe'] else 'SAME' if s['recipe']==s['job_recipe'] else 'DIFFERENT'
 return {'machine':{**p['machine'],'supported':applicable(p)},
 'snapshot':{**s,'age_seconds':d['snapshot_age_seconds'],'usable':0<=d['snapshot_age_seconds']<=120 and s['quality']=='good','recipe_relation':relation},
 'current_episode':p['episode'],
 'history':{'available':d['history_available'],'usable':d['history_available'] and d['history_fresh'] and not d['bad_history_ids'],
 'bad_record_ids':d['bad_history_ids'],'attempted_check_ids':d['attempted_check_ids'],'unresolved_count':d['unresolved_counts'],
 'records':p.get('history',[])},
 'operator':p.get('operator'), 'outcomes':p.get('outcomes',[]), 'history_and_notes_included':full}

def messages(p):
 return [{'role':'system','content':(ROOT/'prompts/correction.txt').read_text()}, {'role':'user','content':json.dumps(compact(p),separators=(',',':'))}]

def normalize(raw):
 obj,final=parse_answer(raw)
 if not isinstance(obj,dict) or set(obj)!={'action_id','evidence_ids'}:return None,final
 a=obj['action_id']
 if not isinstance(a,str) or a not in PACKAGE['actions']:return None,final
 # This constant is content retrieval, not model reasoning. Choice and citations remain untouched.
 return {**obj,'missing_information':PACKAGE['actions'][a]['missing']},final
