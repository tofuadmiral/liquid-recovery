"""Model extracts note observations. The explicit procedure tree selects the next step.
Scores for this pipeline must never be attributed to model action selection.
"""
import json,re
from copy import deepcopy
from engine import ROOT,PACKAGE,tree,parse_answer,decision

def messages(p):
 return [{'role':'system','content':(ROOT/'prompts/extract.txt').read_text()},
 {'role':'user','content':json.dumps({'operator_note':p.get('operator',{}).get('text','')})}]

def normalize(raw,p):
 obj,final=parse_answer(raw)
 if not isinstance(obj,dict) or set(obj)!={'displayed_recipe','reported_check_ids'}:return None,final
 recipe=obj['displayed_recipe'];checks=obj['reported_check_ids'];note=p.get('operator',{}).get('text','')
 if recipe is not None and (not isinstance(recipe,str) or not re.fullmatch(r'R\d+',recipe) or recipe not in note):return None,final
 if not isinstance(checks,list) or any(not isinstance(x,str) or x not in {'C_SETUP','C_OBSERVE','C_RECIPE'} for x in checks) or len(checks)!=len(set(checks)):return None,final
 # Existing deterministic gates retain precedence. Replace only the limited baseline note parser.
 canonical=[]
 if recipe:canonical.append('The display says recipe '+recipe+'.')
 if 'C_SETUP' in checks:canonical.append('I recorded the setup status.')
 if 'C_OBSERVE' in checks:canonical.append('I copied the alarm detail text.')
 q=deepcopy(p)
 if 'operator' in q:q['operator']['text']=' '.join(canonical)
 selected=tree(q)
 # Baseline has no grammar for a reported recipe comparison. Preserve policy precedence.
 if 'C_RECIPE' in checks and 'C_RECIPE' not in p['derived']['attempted_check_ids'] and selected['action_id'] not in {'E_VERSION','Q_FRESH','Q_CONFLICT'}:
  selected=decision('Q_CONFLICT',['N0'])
 return selected,final
