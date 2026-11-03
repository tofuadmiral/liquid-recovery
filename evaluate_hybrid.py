"""Frozen, reproducible replay evaluator. See README for protocol and limitations."""
import argparse,hashlib,importlib.metadata,json,multiprocessing as mp,os,platform,statistics,sys,time
from pathlib import Path
from datetime import datetime,timezone
from engine import ROOT,PACKAGE,prepare,tree,alarm_lookup,parse_answer,validate,score
METHODS=['alarm_lookup','decision_tree','lfm_full']
CONFIG={'temperature':0.1,'top_k':50,'max_tokens':1024,'context_budget':8192,'timeout_seconds':60,'seed':17,'repetition_penalty':1.1,'repetition_context_size':256,'reasoning_prefill':''}
FROZEN=['engine.py','evaluate_hybrid.py','hybrid_adapter.py','prompts/extract.txt','data/procedures.json','data/dev.json','data/correction-heldout.json']
def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FROZEN}
def freeze():
 p=ROOT/'results/hybrid-freeze.json'
 if p.exists():raise RuntimeError('Freeze exists; do not overwrite. Use a new experiment for changes.')
 p.write_text(json.dumps({'created_at':datetime.now(timezone.utc).isoformat(),'sha256':hashes(),'config':CONFIG,'development_process':'Original failure and all corrective direct selection probes retained. Separate hybrid design uses model note extraction and deterministic procedure selection. Two full hybrid development runs. The revision restores the native reasoning template and raises the output budget; fresh holdout frozen afterward.'},indent=2)+'\n')
 print('Frozen code, data, prompt and config before held-out inference.')
def verify_freeze():
 f=json.loads((ROOT/'results/hybrid-freeze.json').read_text())
 if f['sha256']!=hashes() or f['config']!=CONFIG:raise RuntimeError('Frozen inputs changed. This is not the original held-out experiment.')
 return f

def worker(conn,manifest):
 import mlx.core as mx
 from mlx_lm import load,stream_generate
 from mlx_lm.sample_utils import make_sampler,make_logits_processors
 import psutil,threading
 proc=psutil.Process()
 t=time.perf_counter()
 model,tokenizer=load(manifest['local_path'],trust_remote_code=False)
 mx.eval(model.parameters())
 conn.send({'ready':True,'load_seconds':time.perf_counter()-t,'rss_after_load_bytes':proc.memory_info().rss,'mlx_active_after_load_bytes':mx.get_active_memory()})
 while True:
  msg=conn.recv()
  if msg is None:break
  messages=msg['messages']
  mx.random.seed(CONFIG['seed'])
  mx.clear_cache();mx.reset_peak_memory()
  rss=[proc.memory_info().rss]; stop=threading.Event()
  def sample():
   while not stop.wait(.02):rss.append(proc.memory_info().rss)
  thread=threading.Thread(target=sample,daemon=True);thread.start()
  start=time.perf_counter();parts=[];first=None;last=None
  try:
   prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)+CONFIG['reasoning_prefill']
   n=len(tokenizer.encode(prompt))
   if n+CONFIG['max_tokens']>CONFIG['context_budget']:raise ValueError('Context budget exceeded')
   for chunk in stream_generate(model,tokenizer,prompt,max_tokens=CONFIG['max_tokens'],sampler=make_sampler(temp=CONFIG['temperature'],top_k=CONFIG['top_k']),logits_processors=make_logits_processors(repetition_penalty=CONFIG['repetition_penalty'],repetition_context_size=CONFIG['repetition_context_size'])):
    if first is None:first=time.perf_counter()-start
    parts.append(chunk.text);last=chunk
   mx.synchronize()
   result={'raw':''.join(parts),'rendered_prompt':prompt,'prompt_tokens':n,
    'generation_tokens':last.generation_tokens if last else 0,'finish_reason':last.finish_reason if last else None,
    'latency_seconds':time.perf_counter()-start,'first_token_seconds':first,
    'mlx_peak_bytes':mx.get_peak_memory(),'mlx_active_bytes':mx.get_active_memory(),
    'timeout':False,'error':None}
  except Exception as e:result={'raw':'','error':str(e),'latency_seconds':time.perf_counter()-start,'timeout':False}
  finally:stop.set();thread.join();rss.append(proc.memory_info().rss)
  result['rss_peak_sampled_bytes']=max(rss)
  conn.send(result)
 conn.close()

from hybrid_adapter import messages,normalize

class ModelRunner:
 def __init__(self):self.proc=None;self.loads=[];self.manifest=json.loads((ROOT/'results/model.json').read_text())
 def start(self):
  parent,child=mp.get_context('spawn').Pipe();self.conn=parent
  self.proc=mp.get_context('spawn').Process(target=worker,args=(child,self.manifest));self.proc.start();child.close()
  if not self.conn.poll(120):self.close();raise RuntimeError('Model failed to load in 120 seconds')
  self.loads.append(self.conn.recv());print('Model loaded:',round(self.loads[-1]['load_seconds'],2),'s',flush=True)
 def run(self,p):
  if self.proc is None:self.start()
  self.conn.send({'messages':messages(p)})
  if not self.conn.poll(CONFIG['timeout_seconds']):
   self.close();return {'raw':'','timeout':True,'error':'hard_timeout','latency_seconds':CONFIG['timeout_seconds']}
  return self.conn.recv()
 def close(self):
  if self.proc is not None:
   if self.proc.is_alive():self.proc.terminate()
   self.proc.join();self.conn.close();self.proc=None

def percentile(values,q):
 values=sorted(values)
 if not values:return None
 return values[max(0,min(len(values)-1,__import__('math').ceil(q*len(values))-1))]

def summarize(rows):
 out={}
 for method in METHODS:
  r=[x for x in rows if x['method']==method]
  if not r:continue
  s=[x['score'] for x in r]; lat=[x['runtime']['latency_seconds'] for x in r]
  esc=[x for x in s if x['requires_escalation']];non=[x for x in s if not x['requires_escalation']]
  out[method]={'n':len(r),**{k:sum(x[k] for x in s) for k in ['correct','delivered_correct','passed','valid_evidence_refs','complete_gold_evidence','unsupported_assertion','unsupported_check_selection','valid_response']},
   'escalations_required':len(esc),'appropriate_escalations':sum(x['selected_escalation'] for x in esc),'false_escalations':sum(x['selected_escalation'] for x in non),
   'timeouts':sum(x['runtime'].get('timeout',False) for x in r),'truncated':sum(x['runtime'].get('finish_reason')=='length' for x in r),
   'latency_p50_seconds':statistics.median(lat),'latency_p95_seconds':percentile(lat,.95),'latency_max_seconds':max(lat),
   'mlx_peak_bytes':max((x['runtime'].get('mlx_peak_bytes',0) for x in r),default=0),
   'rss_peak_sampled_bytes':max((x['runtime'].get('rss_peak_sampled_bytes',0) for x in r),default=0),
   'prompt_tokens_range':[min(x['runtime'].get('prompt_tokens',0) for x in r),max(x['runtime'].get('prompt_tokens',0) for x in r)],
   'failure_ids':[x['case_id'] for x in r if not x['score']['passed']]}
 return out

def run(args):
 if args.split=='correction-heldout':verify_freeze()
 cases=json.loads((ROOT/f'data/{args.split}.json').read_text())
 out=ROOT/'results'/args.name;out.mkdir(exist_ok=False)
 started=datetime.now(timezone.utc).isoformat();rows=[];runner=ModelRunner() if args.model else None
 methods=METHODS if args.model else METHODS[:2]
 try:
  for index,case in enumerate(cases):
   full=prepare(case['input']);current=prepare(case['input'],False)
   order=methods if index%2==0 else methods[:2]+list(reversed(methods[2:]))
   for method in order:
    p=current if method=='lfm_current' else full
    t=time.perf_counter()
    if method.startswith('lfm_'):
     runtime=runner.run(p);candidate,final_text=normalize(runtime['raw'],p)
    else:
     candidate=(tree if method=='decision_tree' else alarm_lookup)(p)
     runtime={'raw':json.dumps(candidate),'latency_seconds':time.perf_counter()-t,'timeout':False,'error':None};final_text=runtime['raw']
    delivered,errors=validate(candidate,p)
    scored=score(case,candidate,p,delivered,errors)
    if method.startswith('lfm_') and 'observations' in case['gold']:
     extracted,_=parse_answer(runtime['raw'])
     expected_observations=case['gold']['observations'] if method=='lfm_full' else {'displayed_recipe':None,'reported_check_ids':[]}
     scored['extraction_correct']=extracted==expected_observations
    row={'case_id':case['id'],'group':case['group'],'split':case['split'],'method':method,'candidate':candidate,
     'delivered':delivered,'validation_errors':errors,'score':scored,'runtime':runtime,'final_text':final_text}
    rows.append(row)
    with (out/'rows.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    print(f"{case['id']} {method}: {candidate.get('action_id') if candidate else 'INVALID'} gold={case['gold']['action_id']} correct={scored['correct']} {runtime['latency_seconds']:.3f}s",flush=True)
 finally:
  if runner:runner.close()
 metadata={'started_at':started,'ended_at':datetime.now(timezone.utc).isoformat(),'split':args.split,'config':CONFIG,'source_hashes':hashes(),
  'model':{k:v for k,v in json.loads((ROOT/'results/model.json').read_text()).items() if k!='local_path'},
  'runtime_versions':{k:importlib.metadata.version(k) for k in ['mlx','mlx-lm','transformers','huggingface-hub','psutil']},
  'hardware':'Apple M4 Pro, 14 CPU cores, 24 GB unified memory','os':platform.platform(),'python':sys.version,
  'model_loads':runner.loads if runner else [],'method_order':'alternates LFM order per case; baselines first','architecture':'hybrid_extraction_rules','notes':'Fresh evaluation compares alarm lookup, full evidence rules and the full hybrid. The current only ablation remains in the original experiment and hybrid development records; it is omitted from the fresh run because it has no note to interpret. Model extracts displayed recipe and reported completed checks only. Tree selects the action. Hybrid correctness is not model action selection accuracy. No warm-up; first inference included. No cross-case KV cache. Vendor sampling settings with repetition context 256. Native reasoning template preserved. 1024 token total generation budget including reasoning. Two field note extraction JSON. Deterministic tree selects the action using the extracted observations. Invalid extraction fails closed. No constrained decoder or retry. No gold substitution. RSS sampled every 20 ms; MLX peak includes model and tensors, not whole-system RAM. Download excluded. Desktop apps not controlled; no IPC or contention validation.'}
 (out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
 (out/'summary.json').write_text(json.dumps(summarize(rows),indent=2)+'\n')
 print(json.dumps(summarize(rows),indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--freeze',action='store_true');p.add_argument('--split',choices=['dev','correction-heldout'],default='dev');p.add_argument('--name',default='dev-v1');p.add_argument('--model',action='store_true');args=p.parse_args()
 if args.freeze:freeze()
 else:run(args)
