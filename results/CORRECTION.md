# Correction and revised product design

The final hybrid workflow passed 24 of 24 fresh synthetic cases. The full evidence rule tree also passed 24 of 24. This repairs the unusable demonstration and establishes no advantage over rules. A model layer remains conditional on its ability to handle varied real operator language with less maintenance than forms and phrase rules.

## What changed

The original model tried to choose the procedure step directly. It returned zero usable responses on 24 held out cases. Those frozen inputs, outputs and results remain unchanged in `heldout-final`.

Corrective development exposed two separate problems. Repetitive reasoning exhausted the original answer budget. Simplifying the output interface and suppressing reasoning produced valid answers quickly but left action selection unreliable. Native tool calling completed in two diagnostic cases but did not reliably follow the procedure. These were development probes, not new performance claims.

The product design now gives the model a smaller task: extract a displayed recipe and explicitly completed checks from the operator note. The deterministic procedure tree uses those observations and the full incident history to choose the response. It owns action selection and citations. Model output never executes commands. The score is for the complete hybrid pipeline, not for model action selection.

An initial hybrid development run closed the reasoning block and incorrectly listed every available check as completed. Restoring the native reasoning template and using 1,024 generation tokens produced 12 of 12 strict development passes. The final configuration, code, procedure and 24 fresh combinations were then frozen before model inference. No further prompt or rule changes followed the fresh results.

## Fresh results

| Condition | Correct next step | Strict pass | Valid response |
| :--- | :--- | :--- | :--- |
| Alarm lookup | 4/24 | 4/24 | 11/24 |
| Full evidence rules | 24/24 | 24/24 | 24/24 |
| LFM observations plus rules | 24/24 | 24/24 | 24/24 |

* Exact model observation extraction: 24/24.
* Appropriate escalation: 9/9; false escalation: 0.
* Wrong permitted checks: 0; contract violations: 0.
* Valid evidence references: 24/24; complete required evidence: 24/24. Those citations come from the rule engine in the hybrid.
* Timeouts: 0; generation budget reached: 0.
* Median model call: 8.46 seconds; descriptive p95: 10.05 seconds.
* Peak MLX allocation: 1.97 GiB. Separately sampled process footprint: 1.91 GiB. They overlap.
* Prompt token range: [216, 228]. The total context budget was 8,192, with a maximum of 1,024 generated tokens including reasoning.

The current state ablation remains in the original and hybrid development records. It has no note or history to interpret and is omitted from the fresh comparison. All three fresh conditions use the same scored incidents. Rules and the hybrid receive the same full evidence; the model itself sees only the note. The rules read the structured evidence and extracted observations.

## Runtime and reproducibility

Official checkpoint: `LiquidAI/LFM2.5-2.6B-MLX-4bit`. Revision: `04efa23776ce61ec34ec95ec34c859854c89542b`. Hardware: Apple M4 Pro, 14 CPU cores, 24 GB unified memory. MLX 0.32.4; MLX LM 0.32.2. Temperature 0.1, top k 50, repetition penalty 1.1 over 256 tokens, seed 17. Native reasoning template preserved. No grammar constraint, retry, candidate replacement or gold label access. A malformed extraction fails closed.

`hybrid-freeze.json` records hashes before inference. Each completed call records its exact prompt, raw answer and measured runtime. `hybrid-final/failures.csv` includes every failed strict comparison across all methods. Raw results and original failures are also available through the replay.

## Limits that matter

These are fresh combinations of an existing artificial policy, not independent industrial evidence. One author created the policy, labels and rule baseline. The baseline directly implements the policy and matches the hybrid. Two reported check examples use language that the visible rule parser already handles. The test does not demonstrate better language coverage, lower maintenance cost or buyer demand.

Fresh extraction labels cover only displayed recipe and reported checks. Correct extraction here does not prove arbitrary instruction resistance or correct interpretation of all possible notes. Grounding rejects a recipe absent from the note; check extraction still relies on the model. The application has no actuation capability.

Latency covers native reasoning, input processing and answer generation. It excludes deterministic preprocessing, validation and UI rendering. Loading is separate. The first call is included; no warm up or cross case cache. Memory is measured per call on a Mac with uncontrolled desktop activity. No industrial PC, hardware contention, thermal soak, power, plant server or cloud comparison was run.

The business pitch remains a hypothesis. The next funded step should qualify incident burden, procedure ownership and buyer value. Deployment of a model requires independently labeled real notes and measured maintenance advantage over the rule baseline. Keep the simpler implementation when it wins.
