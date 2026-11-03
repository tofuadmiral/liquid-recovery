# Frozen replay evaluation

**Decision: hold the LFM product bet in this form.** The tree selected the expected next ID in 24/24 cases; the full model did so in 0/24. The full model returned 0/24 accepted decisions. The experiment did not establish a need for a model in this structured workflow, nor did it measure lower maintenance effort or buyer value. The model result characterizes this generation harness and budget. It does not establish the best achievable capability of LFM2.5.

## Primary held out results

| Condition | Correct ID | Strict pass | Valid response | Escalation recall | False escalation | Valid refs | Complete gold evidence | Contract violations | Wrong checks | Timeouts | Token cap |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| alarm_lookup | 3/24 | 3/24 | 15/24 | 0/7 | 0/17 | 24/24 | 3/24 | 0/24 | 21/24 | 0/24 | 0/24 |
| decision_tree | 24/24 | 24/24 | 24/24 | 7/7 | 0/17 | 24/24 | 24/24 | 0/24 | 0/24 | 0/24 | 0/24 |
| lfm_current | 0/24 | 0/24 | 0/24 | 0/7 | 0/17 | 0/24 | 0/24 | 24/24 | 0/24 | 5/24 | 19/24 |
| lfm_full | 0/24 | 0/24 | 0/24 | 0/7 | 0/17 | 0/24 | 0/24 | 24/24 | 0/24 | 2/24 | 22/24 |

Contract violations are the evaluator's conservative unsupported assertion proxy: unparseable output, extra fields or unknown actions. They must not be described as 24 demonstrated factual hallucinations. Correct ID is scored before fallback. The guard can reject an output but does not prove that an accepted output is semantically correct. Gold evidence completeness is a limited manually specified support test.

## Runtime

Checkpoint: `LiquidAI/LFM2.5-2.6B-MLX-4bit` at revision `04efa23776ce61ec34ec95ec34c859854c89542b`. Official affine 4 bit artifact, group size 64; its embedding layer uses 6 bits, as recorded in the model config. Runtime versions: mlx 0.32.4, mlx-lm 0.32.2, transformers 5.22.1, huggingface-hub 2.4.0, psutil 7.2.2.

Hardware: Apple M4 Pro, 14 CPU cores, 24 GB unified memory. macOS-26.7.2-arm64-arm-64bit. Configuration: {"temperature": 0.0, "top_k": 0, "max_tokens": 1536, "context_budget": 8192, "timeout_seconds": 60, "seed": 17, "repetition_penalty": 1.0}.

| Condition | p50 seconds | p95 seconds | Maximum seconds | Peak MLX GiB | Sampled RSS GiB | Prompt token range on completed calls |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| alarm_lookup | 0.000028 | 0.000095 | 0.000140 | 0.000 | 0.000 | not measured |
| decision_tree | 0.000094 | 0.000362 | 0.001410 | 0.000 | 0.000 | not measured |
| lfm_current | 44.343552 | 60.000000 | 60.000000 | 2.346 | 1.920 | 1423 to 1424 |
| lfm_full | 34.748366 | 60.000000 | 60.000000 | 2.489 | 1.724 | 1447 to 1962 |

Initial model load: 1.316 seconds. Worker loads including timeout restarts: 8. The initial download took 64.8 seconds and is excluded from latency.

Latency includes prompt construction, tokenization, prefill, reasoning and generation; shared preprocessing, validation and UI rendering are excluded. Timeout rows record the 60 second limit and lack partial output, token counts and memory telemetry. The model worker is killed and restarted. Raw output is preserved for completed calls; no partial text was recovered from timed out workers. Exact timeout input prompts are reconstructed separately from frozen code and the pinned tokenizer, after checking byte equality against completed prompts. Observed memory peaks therefore cover calls with returned telemetry. Baseline memory was not profiled; its zero values are placeholders for unavailable measurements.

MLX peak allocation includes weights and tensors. RSS is sampled every 20 ms and may miss brief spikes. These measures overlap in unified memory and cannot be added. Desktop activity and power conditions were not controlled. A spot check during the held out run reported battery power and no recorded OS thermal warning. This is not an industrial PC qualification or a cloud comparison. Actual input prompts are shorter than the 8K budget; no performance claim is made at a full 8K context.

## Development and freeze

dev-v1: tree 12/12 correct IDs; current model 0/12; full model 0/12. Full model accepted responses 0/12, token cap 6/12, timeouts 0/12.
dev-v2: tree 12/12 correct IDs; current model 0/12; full model 0/12. Full model accepted responses 0/12, token cap 12/12, timeouts 0/12.

The sole revision clarified classification labels versus callable tools, restated the ordered policy and reinforced the JSON contract. The initial responses often emitted function calls. The revision did not solve the generation contract within the fixed token budget. No calls were executed. Source snapshots for both development runs are preserved.

The final prompt, procedure, scenarios, evaluator and engine were hashed before held out inference. `results/freeze.json` records that point. Neither policy nor labels were changed after seeing held out results. Presentation and reporting code were completed later and do not affect scores.

Greedy decoding with no repetition penalty differs from the model card's recommended settings. A supported constrained output interface, recommended decoding or a different output budget could alter the result; each requires a separately declared experiment with fresh evaluation cases. The current result is insufficient to conclude that this model cannot do bounded selection.

## Failure ledger

Every failed case is listed in `heldout-final/failures.csv` and the HTML viewer. For quick review:

- alarm_lookup: H01b, H02a, H02b, H03a, H03b, H04a, H04b, H05a, H05b, H06a, H06b, H07a, H07b, H08a, H08b, H09a, H10b, H11a, H11b, H12a, H12b.
- decision_tree: none.
- lfm_current: H01a, H01b, H02a, H02b, H03a, H03b, H04a, H04b, H05a, H05b, H06a, H06b, H07a, H07b, H08a, H08b, H09a, H09b, H10a, H10b, H11a, H11b, H12a, H12b.
- lfm_full: H01a, H01b, H02a, H02b, H03a, H03b, H04a, H04b, H05a, H05b, H06a, H06b, H07a, H07b, H08a, H08b, H09a, H09b, H10a, H10b, H11a, H11b, H12a, H12b.

## Evidence slices

| Slice | Cases | Tree correct | Full model correct |
| :--- | ---: | ---: | ---: |
| contradiction | 6 | 6/6 | 0/6 |
| counterfactual | 20 | 20/20 | 0/20 |
| history | 4 | 4/4 | 0/4 |
| injection | 2 | 2/2 | 0/2 |
| missing | 6 | 6/6 | 0/6 |
| natural_language | 2 | 2/2 | 0/2 |
| noise | 6 | 6/6 | 0/6 |
| outcome | 2 | 2/2 | 0/2 |
| quality | 2 | 2/2 | 0/2 |
| repeat | 2 | 2/2 | 0/2 |
| stale | 4 | 4/4 | 0/4 |
| version | 2 | 2/2 | 0/2 |

Slices overlap. Same author bias, tiny sample size and the direct translation from procedure to tree limit interpretation. The note parser sees full text but handles only a bounded grammar. No actual onboarding or maintenance effort was measured.

## What changes next

Pause the proposed model selection workflow. Customer discovery can continue without treating this simulation as demand evidence. Obtain permitted historical incidents and an accountable procedure owner, reconstruct who paid for specialist effort, and compare the existing HMI, service workflow and rules. Only reopen model investment if real unstructured evidence creates a meaningful gap and a fresh evaluation shows the model can close it within a viable hardware and maintenance budget.

The proposed eight week pilot and prices remain conditional. No customer has agreed to them. A future pilot would target 25% fewer specialist minutes per eligible incident, with incident mix and all escalations in the denominator. The synthetic replay cannot estimate that outcome.

## Verification

Ten Python contract tests exercise correct and deliberately invalid outputs, evidence grounding, version applicability, exhausted checks, split isolation and parser handling. DOM tests iterate every saved case and method, check evidence targets and escaping, navigate views, and exercise local demonstration outcome storage. A browser visual check verified the development viewer and method/case selection. The final memo is rendered separately and checked for two pages and the requested prose style.
