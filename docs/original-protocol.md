# Recovery Replay

A synthetic incident-replay evaluator for the Liquid AI product take-home. Open `output/replay.html` for the combined interactive replay, evaluation and failure ledger. It is standalone and works without a network connection. It displays recorded local model runs; choosing an incident does not run live inference. All machine identities, faults, logs and procedures are fabricated. No manufacturer approved these instructions. There is no machine connection or actuation capability.

## Run

The saved replay and results are portable. Reproducing MLX inference requires an Apple Silicon Mac. The recorded machine was an M4 Pro with 24 GB unified memory.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.lock
# Download the pinned checkpoint (about 1.5 GB); no API key required.
.venv/bin/python reproduce.py --prepare
# Verify the frozen inputs, then rerun in a new result directory.
.venv/bin/python evaluate.py --split heldout --name heldout-reproduction --model
# Deterministic baselines only; no model needed after dependency setup.
.venv/bin/python evaluate.py --split heldout --name baselines-reproduction
.venv/bin/python -m unittest discover -s tests -v
```

Do not overwrite the original frozen runs. `evaluate.py --freeze` is the original protocol operation and refuses to replace an existing freeze. `make_scenarios.py` documents fixture authorship; it is not needed for reproduction. Source code and labels were authored together, so the benchmark is not independently blind. It tests adherence to a small artificial policy, not engineering diagnosis or packaging demand.

## Files

- `data/procedures.json`: exact version applicability, ordered policy, original mock instructions and output IDs.
- `data/dev.json`, `data/heldout.json`: 12 and 24 scenarios with explicit labels and required source IDs. Counterfactual pairs stay within a split; task categories necessarily overlap.
- `engine.py`: deterministic ages/counts, full-evidence rule baseline, validation and scoring. Note parsing is intentionally visible and limited to a small grammar; no claim of robust free-text interpretation.
- `prompts/system.txt`: final model instruction. Rendered prompts and complete generated text are saved per response.
- `evaluate.py`: four-condition evaluator with a persistent inference worker and a hard 60-second per-call timeout. It terminates and restarts the worker if necessary. Download and model load are separate from decision latency.
- `results/freeze.json`: hashes and decoding configuration frozen before held-out inference.
- `results/dev-v1`, `results/dev-v2`, `results/heldout-final`: raw rows, summaries and runtime metadata. Initial and revised development results are both retained.
- `results/EXPERIMENT.md`: interpretation, failures and limitations.
- `output/replay.html`: combined artifact; browser-only demo outcome entries can be exported and never modify the evaluation.

## What is compared

1. Current-alarm lookup (intentionally weak comparator).
2. A decision tree with **all** the information available to the full model, including the original operator note.
3. LFM with snapshot and procedure only.
4. LFM with full history, operator observations, outcomes and procedure.

The current-only ablation omits history needed by this policy. It is expected to ask for evidence and cannot establish the model's value. The full-evidence tree is the consequential comparator. All methods share output validation. Scores use the **raw choice**, with delivered/fallback scores separate; fallback does not turn an incorrect model output into a successful model decision.

The deterministic guard rejects malformed output, unsupported fields/IDs, fabricated evidence IDs, inapplicable procedures, incomplete/stale input for checks and already-attempted checks. It does not prove semantic correctness. A valid check can still be the wrong next step; that failure remains visible.

## Measures and limits

- Exact next-ID correctness includes checks, questions and escalation subtypes.
- Escalation recall counts any escalation on an escalation-required case; wrong subtypes still fail exact correctness. False escalations are reported.
- Reference validity means an ID exists in the method's input. Complete supporting evidence requires a correct choice and all manually required source IDs. This is a limited evidence test, not general entailment.
- Unsupported assertion is a conservative **contract-violation proxy**: malformed output, extra prose/fields or unknown action. It is not a direct factual hallucination rate. Wrong permitted checks are counted separately. No free-form diagnosis is allowed or assessed.
- Strict pass = correct raw next ID, accepted output contract and complete required evidence.
- Latency includes prompt template construction, tokenization, prompt processing, reasoning and final generated answer. It excludes shared preprocessing, guard/UI time, model download and loading. First generation is included; no warm-up or cross-case KV reuse. p95 is a descriptive nearest-rank statistic from a small sample, not a reliable deployment tail estimate.
- MLX peak allocation includes weights/tensors. Process RSS is sampled every 20 ms; it can miss short spikes and overlaps unified memory. Do not sum them. Nothing here measures system-wide peak usage, thermal soak, IPC application contention, power or cloud/plant-server alternatives.
- Greedy temperature 0 and no repetition penalty differ from the model card's recommended temperature 0.1 and repetition penalty 1.1. The single allowed revision changed the prompt only. These results characterize this harness and output budget; they do not establish the model's best achievable quality. A different decoder or schema constrained interface would require a fresh, separately reported experiment.
- The author wrote the synthetic procedure, labels and tree. No independent OEM labeler or production logs were available. The tree implements the procedure almost directly; this construction can favor rules. A further comparison would need independently labeled real incidents, especially genuinely varied operator language, and measured update/onboarding effort.

## Product scope

Read-only incident evidence → exact-version procedure → next permitted check / evidence question / escalation → original instruction plus sources → human-confirmed outcome record. No autonomous reset, parameter writes, motion control, electrical repair or robot recovery. Resumption is not proof of root cause.

A future collector would map OEM events to this incident contract (PackML can help but does not supply alarm semantics). This prototype implements replay input, not an OPC UA client, signed content/update distribution or production HMI integration. Customer procedures, security review, update ownership and contention testing remain prerequisites.

The source bundle contains synthetic/public material only. Private interview notes and proprietary data are excluded. Third-party model/runtime licensing is governed by its original terms; no broader commercial permission is asserted here.

For timeouts, exact input prompts are reconstructed separately from the frozen code and pinned tokenizer, with byte equality verified against completed calls. Partial generated text from killed workers is unavailable.
