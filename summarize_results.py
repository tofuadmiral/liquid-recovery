"""Publish counts, failure rows and a bounded interpretation of the frozen experiment."""
import csv,json
from pathlib import Path
from engine import ROOT,PACKAGE
from evaluate import verify_freeze,summarize
verify_freeze()
d=ROOT/'results/heldout-final';rows=[json.loads(x) for x in (d/'rows.jsonl').read_text().splitlines()]
s=json.loads((d/'summary.json').read_text());m=json.loads((d/'metadata.json').read_text())
assert s==summarize(rows)
assert len(rows)==96 and len({(r['case_id'],r['method']) for r in rows})==96
cases={c['id']:c for c in json.loads((ROOT/'data/heldout.json').read_text())}
for r in rows:
 assert r['case_id'] in cases
 assert r['score']['correct']==(r['candidate'] is not None and r['candidate']['action_id']==cases[r['case_id']]['gold']['action_id'])
 assert r['delivered']['action_id'] in PACKAGE['actions']
f=s['lfm_full'];t=s['decision_tree']
with (d/'failures.csv').open('w') as out:
 w=csv.writer(out);w.writerow(['case','method','expected','raw_action','delivered','correct','complete_evidence','errors','timeout','finish_reason','seconds'])
 for r in rows:
  if not r['score']['passed']:
   w.writerow([r['case_id'],r['method'],cases[r['case_id']]['gold']['action_id'],r['candidate'].get('action_id') if r['candidate'] else '',r['delivered']['action_id'],r['score']['correct'],r['score']['complete_gold_evidence'],';'.join(r['validation_errors']),r['runtime'].get('timeout'),r['runtime'].get('finish_reason'),r['runtime']['latency_seconds']])
report=['# Frozen replay evaluation','',
 f'**Decision: hold the LFM product bet in this form.** The tree selected the expected next ID in {t["correct"]}/24 cases; the full model did so in {f["correct"]}/24. The full model returned {f["valid_response"]}/24 accepted decisions. The experiment did not establish a need for a model in this structured workflow, nor did it measure lower maintenance effort or buyer value. The model result characterizes this generation harness and budget. It does not establish the best achievable capability of LFM2.5.',
 '', '## Primary held out results','',
 '| Condition | Correct ID | Strict pass | Valid response | Escalation recall | False escalation | Valid refs | Complete gold evidence | Contract violations | Wrong checks | Timeouts | Token cap |',
 '| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
for k,v in s.items():
 report.append(f'| {k} | {v["correct"]}/24 | {v["passed"]}/24 | {v["valid_response"]}/24 | {v["appropriate_escalations"]}/{v["escalations_required"]} | {v["false_escalations"]}/{24-v["escalations_required"]} | {v["valid_evidence_refs"]}/24 | {v["complete_gold_evidence"]}/24 | {v["unsupported_assertion"]}/24 | {v["unsupported_check_selection"]}/24 | {v["timeouts"]}/24 | {v["truncated"]}/24 |')
report += ['', 'Contract violations are the evaluator\'s conservative unsupported assertion proxy: unparseable output, extra fields or unknown actions. They must not be described as 24 demonstrated factual hallucinations. Correct ID is scored before fallback. The guard can reject an output but does not prove that an accepted output is semantically correct. Gold evidence completeness is a limited manually specified support test.', '', '## Runtime','',
 f'Checkpoint: `{m["model"]["repo"]}` at revision `{m["model"]["revision"]}`. Official affine 4 bit artifact, group size 64; its embedding layer uses 6 bits, as recorded in the model config. Runtime versions: '+', '.join(f'{k} {v}' for k,v in m['runtime_versions'].items())+'.',
 '', f'Hardware: {m["hardware"]}. {m["os"]}. Configuration: '+json.dumps(m['config'])+'.', '',
 '| Condition | p50 seconds | p95 seconds | Maximum seconds | Peak MLX GiB | Sampled RSS GiB | Prompt token range on completed calls |',
 '| :--- | ---: | ---: | ---: | ---: | ---: | :--- |']
for k,v in s.items():
 completed=[r for r in rows if r['method']==k and 'prompt_tokens' in r['runtime']]
 token_range=f'{min(r["runtime"]["prompt_tokens"] for r in completed)} to {max(r["runtime"]["prompt_tokens"] for r in completed)}' if completed else 'not measured'
 report.append(f'| {k} | {v["latency_p50_seconds"]:.6f} | {v["latency_p95_seconds"]:.6f} | {v["latency_max_seconds"]:.6f} | {v["mlx_peak_bytes"]/2**30:.3f} | {v["rss_peak_sampled_bytes"]/2**30:.3f} | {token_range} |')
loads=m['model_loads']
report += ['',f'Initial model load: {loads[0]["load_seconds"]:.3f} seconds. Worker loads including timeout restarts: {len(loads)}. The initial download took {m["model"]["download_seconds"]:.1f} seconds and is excluded from latency.',
 '', 'Latency includes prompt construction, tokenization, prefill, reasoning and generation; shared preprocessing, validation and UI rendering are excluded. Timeout rows record the 60 second limit and lack partial output, token counts and memory telemetry. The model worker is killed and restarted. Raw output is preserved for completed calls; no partial text was recovered from timed out workers. Exact timeout input prompts are reconstructed separately from frozen code and the pinned tokenizer, after checking byte equality against completed prompts. Observed memory peaks therefore cover calls with returned telemetry. Baseline memory was not profiled; its zero values are placeholders for unavailable measurements.',
 '', 'MLX peak allocation includes weights and tensors. RSS is sampled every 20 ms and may miss brief spikes. These measures overlap in unified memory and cannot be added. Desktop activity and power conditions were not controlled. A spot check during the held out run reported battery power and no recorded OS thermal warning. This is not an industrial PC qualification or a cloud comparison. Actual input prompts are shorter than the 8K budget; no performance claim is made at a full 8K context.',
 '', '## Development and freeze','']
for name in ('dev-v1','dev-v2'):
 dev=json.loads((ROOT/f'results/{name}/summary.json').read_text())
 report.append(f'{name}: tree {dev["decision_tree"]["correct"]}/12 correct IDs; current model {dev["lfm_current"]["correct"]}/12; full model {dev["lfm_full"]["correct"]}/12. Full model accepted responses {dev["lfm_full"]["valid_response"]}/12, token cap {dev["lfm_full"]["truncated"]}/12, timeouts {dev["lfm_full"]["timeouts"]}/12.')
report += ['', 'The sole revision clarified classification labels versus callable tools, restated the ordered policy and reinforced the JSON contract. The initial responses often emitted function calls. The revision did not solve the generation contract within the fixed token budget. No calls were executed. Source snapshots for both development runs are preserved.',
 '', 'The final prompt, procedure, scenarios, evaluator and engine were hashed before held out inference. `results/freeze.json` records that point. Neither policy nor labels were changed after seeing held out results. Presentation and reporting code were completed later and do not affect scores.',
 '', 'Greedy decoding with no repetition penalty differs from the model card\'s recommended settings. A supported constrained output interface, recommended decoding or a different output budget could alter the result; each requires a separately declared experiment with fresh evaluation cases. The current result is insufficient to conclude that this model cannot do bounded selection.',
 '', '## Failure ledger','', 'Every failed case is listed in `heldout-final/failures.csv` and the HTML viewer. For quick review:','']
for k,v in s.items():report.append(f'- {k}: '+(', '.join(v['failure_ids']) or 'none')+'.')
report += ['', '## Evidence slices','', '| Slice | Cases | Tree correct | Full model correct |','| :--- | ---: | ---: | ---: |']
for tag in sorted(set(t for c in cases.values() for t in c['tags'])):
 ids={k for k,c in cases.items() if tag in c['tags']}
 counts={m:sum(r['score']['correct'] for r in rows if r['case_id'] in ids and r['method']==m) for m in ['decision_tree','lfm_full']}
 report.append(f'| {tag} | {len(ids)} | {counts["decision_tree"]}/{len(ids)} | {counts["lfm_full"]}/{len(ids)} |')
report += ['', 'Slices overlap. Same author bias, tiny sample size and the direct translation from procedure to tree limit interpretation. The note parser sees full text but handles only a bounded grammar. No actual onboarding or maintenance effort was measured.',
 '', '## What changes next','', 'Pause the proposed model selection workflow. Customer discovery can continue without treating this simulation as demand evidence. Obtain permitted historical incidents and an accountable procedure owner, reconstruct who paid for specialist effort, and compare the existing HMI, service workflow and rules. Only reopen model investment if real unstructured evidence creates a meaningful gap and a fresh evaluation shows the model can close it within a viable hardware and maintenance budget.',
 '', 'The proposed eight week pilot and prices remain conditional. No customer has agreed to them. A future pilot would target 25% fewer specialist minutes per eligible incident, with incident mix and all escalations in the denominator. The synthetic replay cannot estimate that outcome.',
 '', '## Verification','', 'Ten Python contract tests exercise correct and deliberately invalid outputs, evidence grounding, version applicability, exhausted checks, split isolation and parser handling. DOM tests iterate every saved case and method, check evidence targets and escaping, navigate views, and exercise local demonstration outcome storage. A browser visual check verified the development viewer and method/case selection. The final memo is rendered separately and checked for two pages and the requested prose style.']
(ROOT/'results/EXPERIMENT.md').write_text('\n'.join(report)+'\n')
print('Reconciled 96 held out rows, summaries, failure CSV and experiment report.')
