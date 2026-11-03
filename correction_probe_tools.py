import json,time
from pathlib import Path
import mlx.core as mx
from mlx_lm import load,stream_generate
from mlx_lm.sample_utils import make_sampler,make_logits_processors
from engine import prepare,PACKAGE
from correction_adapter import messages
R=Path(__file__).resolve().parent
model,tok=load(json.loads((R/'results/model.json').read_text())['local_path'],trust_remote_code=False)
tools=[{'type':'function','function':{'name':'record_decision','description':'Record the next action ID and supporting evidence. This only records a recommendation and cannot control a machine.','parameters':{'type':'object','properties':{'action_id':{'type':'string','enum':list(PACKAGE['actions'])},'evidence_ids':{'type':'array','items':{'type':'string'}}},'required':['action_id','evidence_ids']}}}]
rows=[]
for c in json.loads((R/'data/dev.json').read_text())[:2]:
 msgs=messages(prepare(c['input']));msgs[0]['content']=msgs[0]['content'].replace('Return only JSON with exactly action_id and evidence_ids.', 'Call record_decision exactly once with action_id and evidence_ids.')
 prompt=tok.apply_chat_template(msgs,tools=tools,tokenize=False,add_generation_prompt=True)
 mx.random.seed(17);t=time.perf_counter();raw=''
 for x in stream_generate(model,tok,prompt,max_tokens=4096,sampler=make_sampler(temp=.1,top_k=50),logits_processors=make_logits_processors(repetition_penalty=1.1,repetition_context_size=1024)):
  raw+=x.text
  if '<|tool_call_end|>' in raw:break
  if time.perf_counter()-t>90:break
 print(c['id'],time.perf_counter()-t,x.finish_reason,raw[-2200:],flush=True)
 rows.append({'id':c['id'],'prompt':prompt,'raw':raw,'seconds':time.perf_counter()-t,'tokens':x.generation_tokens})
(R/'results/correction-probe-tools.json').write_text(json.dumps(rows,indent=2))
