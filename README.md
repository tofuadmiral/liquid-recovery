# Recovery

A product concept for an embedded recovery assistant on packaging machines, by Fuad Ali.

[Live replay](https://liquid-recovery.vercel.app/) · [Read the two page memo](https://liquid-recovery.vercel.app/memo.pdf) · [Editable memo](output/memo.md) · [Public evidence](EVIDENCE.md)

The replay shows why the same alarm can need a different next step when the incident history changes. Every machine, alarm and procedure is synthetic. The website displays recorded local inference. It does not run a model in your browser or connect to a machine.

## Product idea

* Sell to an OEM that carries substantial included support costs.
* Start with one case packer family and recurring stops after a changeover.
* Show the procedure instruction, ask for missing evidence, or escalate with the history attached.
* Keep resets, parameter writes, motion and generated repairs outside the product.
* Earn expansion through repeatable deployment and measurable support savings.

## What works and what remains open

The original direct model selection experiment failed to deliver usable answers on its 24 held out cases. Those results remain unchanged and inspectable. Repairs to the answer format alone did not make the decisions reliable.

The revised design gives LFM a narrower job: extract observations from the operator note. A deterministic procedure tree then selects the response. Hybrid results describe that complete pipeline, not model action selection accuracy. The fresh evaluation uses 24 new combinations under the same synthetic policy. The model must still justify its maintenance cost against rules on independently labeled real incidents.

Buyer demand, industrial hardware compatibility, deployment effort and support savings are unproved. The pricing and pilot described in the memo are hypotheses.

## Open the artifact

Open `output/replay.html` directly for an offline walkthrough, or serve `site/` with any static web server. The memo is linked from the replay header and footer. Local demonstration outcomes stay in your browser and never modify evaluation results.

```sh
python3 -m http.server 8080 --directory site
```

## Reproduce local inference

The recorded hardware is an Apple M4 Pro with 24 GB unified memory. MLX requires Apple Silicon. The source contains no model weights.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.lock
.venv/bin/python reproduce.py --prepare
# Fresh directory required; never overwrite a recorded result.
.venv/bin/python evaluate_hybrid.py --split correction-heldout --name hybrid-reproduction --model
# Reproduce the original frozen experiment separately.
.venv/bin/python evaluate.py --split heldout --name original-reproduction --model
```

`reproduce.py` downloads the pinned official checkpoint and adds its local cache path to `results/model.json`. Keep that local path out of published commits. Both frozen evaluators verify their code, prompts and cases before the held out run. Models receive incident evidence, never case labels.

## Verify and inspect

```sh
.venv/bin/python -m unittest discover -s tests -v
npm ci
npm test
```

* `results/EXPERIMENT.md` preserves the original interpretation and complete failure counts.
* `results/CORRECTION.md` explains the correction, changed model role and fresh results.
* `results/heldout-final/` contains the original raw responses, summaries and metadata.
* `results/hybrid-final/` contains the fresh hybrid evaluation.
* `results/freeze.json` and `results/hybrid-freeze.json` pin the two experiments.
* `engine.py` owns the procedure tree, eligibility checks, scoring and shared arithmetic.
* `hybrid_adapter.py` parses model observations and passes them to the procedure tree.
* `data/` contains explicit labels and supporting sources. Pairs remain within a split.
* `docs/original-protocol.md` preserves the original methodology and metric definitions.

All diagnostic runs are retained. The same author created the synthetic policy, labels and baseline. This is a bounded replay test, not an independent industrial benchmark. Valid evidence IDs are not a general factual entailment test. MLX allocation and process memory overlap and must not be added.

## Deployment

Vercel serves the static `site/` directory. No server inference, API keys, database, customer records or model weights are required. Public materials contain synthetic data and public research only. Confidential interview notes are excluded.

AI assistance: Codex supported research, code, evaluation and writing under Fuad's direction. Fuad will present the argument and its limits. Third party model and runtime licenses retain their original terms.
