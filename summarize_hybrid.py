"""Report the corrected experiment without rewriting the original record."""
from pathlib import Path
import json,csv
from engine import ROOT
from evaluate_hybrid import verify_freeze
verify_freeze()
d=ROOT/'results/hybrid-final';s=json.loads((d/'summary.json').read_text());m=json.loads((d/'metadata.json').read_text());rows=[json.loads(x) for x in (d/'rows.jsonl').read_text().splitlines()]
f=s['lfm_full'];t=s['decision_tree'];a=s['alarm_lookup'];full=[r for r in rows if r['method']=='lfm_full'];extract=sum(r['score']['extraction_correct'] for r in full)
with (d/'failures.csv').open('w') as out:
 w=csv.writer(out);w.writerow(['case','method','candidate','delivered','errors','strict_pass'])
 for r in rows:
  if not r['score']['passed']:w.writerow([r['case_id'],r['method'],r['candidate']['action_id'] if r['candidate'] else None,r['delivered']['action_id'],';'.join(r['validation_errors']),False])
report=f'''# Correction and revised product design

The final hybrid workflow passed {f['passed']} of {f['n']} fresh synthetic cases. The full evidence rule tree also passed {t['passed']} of {t['n']}. This repairs the unusable demonstration and establishes no advantage over rules. A model layer remains conditional on its ability to handle varied real operator language with less maintenance than forms and phrase rules.

## What changed

The original model tried to choose the procedure step directly. It returned zero usable responses on 24 held out cases. Those frozen inputs, outputs and results remain unchanged in `heldout-final`.

Corrective development exposed two separate problems. Repetitive reasoning exhausted the original answer budget. Simplifying the output interface and suppressing reasoning produced valid answers quickly but left action selection unreliable. Native tool calling completed in two diagnostic cases but did not reliably follow the procedure. These were development probes, not new performance claims.

The product design now gives the model a smaller task: extract a displayed recipe and explicitly completed checks from the operator note. The deterministic procedure tree uses those observations and the full incident history to choose the response. It owns action selection and citations. Model output never executes commands. The score is for the complete hybrid pipeline, not for model action selection.

An initial hybrid development run closed the reasoning block and incorrectly listed every available check as completed. Restoring the native reasoning template and using 1,024 generation tokens produced 12 of 12 strict development passes. The final configuration, code, procedure and 24 fresh combinations were then frozen before model inference. No further prompt or rule changes followed the fresh results.

## Fresh results

| Condition | Correct next step | Strict pass | Valid response |
| :--- | :--- | :--- | :--- |
| Alarm lookup | {a['correct']}/24 | {a['passed']}/24 | {a['valid_response']}/24 |
| Full evidence rules | {t['correct']}/24 | {t['passed']}/24 | {t['valid_response']}/24 |
| LFM observations plus rules | {f['correct']}/24 | {f['passed']}/24 | {f['valid_response']}/24 |

* Exact model observation extraction: {extract}/24.
* Appropriate escalation: {f['appropriate_escalations']}/{f['escalations_required']}; false escalation: {f['false_escalations']}.
* Wrong permitted checks: {f['unsupported_check_selection']}; contract violations: {f['unsupported_assertion']}.
* Valid evidence references: {f['valid_evidence_refs']}/24; complete required evidence: {f['complete_gold_evidence']}/24. Those citations come from the rule engine in the hybrid.
* Timeouts: {f['timeouts']}; generation budget reached: {f['truncated']}.
* Median model call: {f['latency_p50_seconds']:.2f} seconds; descriptive p95: {f['latency_p95_seconds']:.2f} seconds.
* Peak MLX allocation: {f['mlx_peak_bytes']/2**30:.2f} GiB. Separately sampled process footprint: {f['rss_peak_sampled_bytes']/2**30:.2f} GiB. They overlap.
* Prompt token range: {f['prompt_tokens_range']}. The total context budget was 8,192, with a maximum of 1,024 generated tokens including reasoning.

The current state ablation remains in the original and hybrid development records. It has no note or history to interpret and is omitted from the fresh comparison. All three fresh conditions use the same scored incidents. Rules and the hybrid receive the same full evidence; the model itself sees only the note. The rules read the structured evidence and extracted observations.

## Runtime and reproducibility

Official checkpoint: `{m['model']['repo']}`. Revision: `{m['model']['revision']}`. Hardware: {m['hardware']}. MLX {m['runtime_versions']['mlx']}; MLX LM {m['runtime_versions']['mlx-lm']}. Temperature 0.1, top k 50, repetition penalty 1.1 over 256 tokens, seed 17. Native reasoning template preserved. No grammar constraint, retry, candidate replacement or gold label access. A malformed extraction fails closed.

`hybrid-freeze.json` records hashes before inference. Each completed call records its exact prompt, raw answer and measured runtime. `hybrid-final/failures.csv` includes every failed strict comparison across all methods. Raw results and original failures are also available through the replay.

## Limits that matter

These are fresh combinations of an existing artificial policy, not independent industrial evidence. One author created the policy, labels and rule baseline. The baseline directly implements the policy and matches the hybrid. Two reported check examples use language that the visible rule parser already handles. The test does not demonstrate better language coverage, lower maintenance cost or buyer demand.

Fresh extraction labels cover only displayed recipe and reported checks. Correct extraction here does not prove arbitrary instruction resistance or correct interpretation of all possible notes. Grounding rejects a recipe absent from the note; check extraction still relies on the model. The application has no actuation capability.

Latency covers native reasoning, input processing and answer generation. It excludes deterministic preprocessing, validation and UI rendering. Loading is separate. The first call is included; no warm up or cross case cache. Memory is measured per call on a Mac with uncontrolled desktop activity. No industrial PC, hardware contention, thermal soak, power, plant server or cloud comparison was run.

The business pitch remains a hypothesis. The next funded step should qualify incident burden, procedure ownership and buyer value. Deployment of a model requires independently labeled real notes and measured maintenance advantage over the rule baseline. Keep the simpler implementation when it wins.
'''
(ROOT/'results/CORRECTION.md').write_text(report)
(ROOT/'results/hybrid-final/extraction-summary.json').write_text(json.dumps({'n':len(full),'exact_observation_extraction_correct':extract,'model_selects_action':False,'action_selection':'deterministic procedure tree'},indent=2)+'\n')
print('Final hybrid',f['correct'],f['passed'],'extraction',extract,'median',f['latency_p50_seconds'])
