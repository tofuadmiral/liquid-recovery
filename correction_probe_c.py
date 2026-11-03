import json,time
from pathlib import Path
import mlx.core as mx
from mlx_lm import load,stream_generate
from mlx_lm.sample_utils import make_sampler,make_logits_processors
from engine import prepare
from correction_adapter import messages
R=Path(__file__).resolve().parent
model,tok=load(json.loads((R/'results/model.json').read_text())['local_path'],trust_remote_code=False)
rows=[]
for c in json.loads((R/'data/dev.json').read_text())[::3]:
 prompt=tok.apply_chat_template(messages(prepare(c['input'])),tokenize=False,add_generation_prompt=True)
 mx.random.seed(17);t=time.perf_counter();raw=''
 for x in stream_generate(model,tok,prompt,max_tokens=384,sampler=make_sampler(temp=.1,top_k=50),logits_processors=make_logits_processors(repetition_penalty=1.1,repetition_context_size=1024)):
  raw+=x.text
  if '</think>' in raw:break
 thinking=raw
 if '</think>' not in raw:raw+='</think>'
 final=''
 for x in stream_generate(model,tok,prompt+raw,max_tokens=256,sampler=make_sampler(temp=.1,top_k=50),logits_processors=make_logits_processors(repetition_penalty=1.1,repetition_context_size=1024)):
  final+=x.text
 print(c['id'],time.perf_counter()-t,final,flush=True)
 rows.append({'id':c['id'],'prompt':prompt,'thinking':thinking,'final':final})
(R/'results/correction-probe-c.json').write_text(json.dumps(rows,indent=2))
