import json,time
from pathlib import Path
import mlx.core as mx
from mlx_lm import load,stream_generate
from mlx_lm.sample_utils import make_sampler,make_logits_processors
from hybrid_adapter import messages
from engine import prepare
R=Path(__file__).resolve().parent
model,tok=load(json.loads((R/'results/model.json').read_text())['local_path'],trust_remote_code=False)
rows=[]
for c in json.loads((R/'data/dev.json').read_text())[::4]:
 prompt=tok.apply_chat_template(messages(prepare(c['input'])),tokenize=False,add_generation_prompt=True)
 mx.random.seed(17);start=time.perf_counter();raw=''
 for x in stream_generate(model,tok,prompt,max_tokens=1024,sampler=make_sampler(temp=.1,top_k=50),logits_processors=make_logits_processors(repetition_penalty=1.1,repetition_context_size=256)):
  raw+=x.text
 print(c['id'],time.perf_counter()-start,x.finish_reason,raw[-1800:],flush=True)
 rows.append({'id':c['id'],'prompt':prompt,'raw':raw,'seconds':time.perf_counter()-start})
(R/'results/hybrid-probe.json').write_text(json.dumps(rows,indent=2))
