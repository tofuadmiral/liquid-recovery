# Recovery

A packaging machine stops after a product change. The operator checks the recipe, but the same alarm returns. Recovery uses the machine history and the manufacturer's instructions to show the next useful check.

[Open the demo](https://liquid-recovery.vercel.app/) · [Read the memo](https://liquid-recovery.vercel.app/memo.pdf) · [Long term value](docs/long-term-value.md)

The demo opens with a short illustrated story. Play it or move through the steps yourself. You can also inspect all 24 synthetic incidents and compare the recorded results.

## What it does

* Reads machine events, operator notes and checks already attempted.
* Shows a check from the matching procedure, asks for missing information, or refers the case to service.
* Leaves the person in control. There is no machine connection, reset, parameter change or generated repair instruction.

LFM2.5 with 2.6B parameters reads the operator note. Rules use the extracted observations and machine history to choose the next step. The website displays saved local runs. Playback does not call a model, and animation timing is illustrative.

## What the test shows

The assistant passed all 24 fresh synthetic cases, including the expected supporting evidence. Rules alone also passed all 24. The model extracted the expected observations in 24 of 24 notes. The median model call took 8.46 seconds on an Apple M4 Pro.

This shows that the bounded workflow works on these examples. It does not establish that the model is needed, that factories would save money, or that the system would work on their hardware. One author created the mock policy, examples and labels. The rule baseline already understands the wording used in the notes.

All machines, alarms and instructions are invented. No manufacturer approved these procedures.

## How the value could grow

Each machine would accumulate reviewed service history: the product settings and software version, what the operator tried, and what a person confirmed afterward. Service staff could use recurring incidents to improve instructions and note interpretation.

Those incidents would also become tests for future updates. The useful asset is machine knowledge that has been reviewed and tested as the equipment changes. Customers would own and be able to export their records. Their service knowledge would stay separate.

The [long term value notes](docs/long-term-value.md) explain what could make this harder to replace and what would disprove that argument.

## Run the demo

Open `output/replay.html` directly, or serve the website locally:

```sh
python3 -m http.server 8080 --directory site
```

The public site is static. It requires no API key, database or model download. Demonstration outcomes are stored only in the current browser.

## Reproduce the evaluation

MLX inference requires an Apple Silicon Mac. The pinned model revision and runtime versions are in `results/hybrid-final/metadata.json`. No model weights are included.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.lock
.venv/bin/python reproduce.py --prepare
.venv/bin/python evaluate_hybrid.py --split correction-heldout --name hybrid-reproduction --model
```

Use a new result directory for each run. The evaluator verifies the frozen code, prompt and cases before the run. Models receive evidence, never expected answers. The preparation command writes a local cache path to `results/model.json`; keep that path out of published commits.

## Inspect or verify

* `data/correction-heldout.json` contains the evaluated incidents and explicit labels.
* `hybrid_adapter.py` reads model observations and passes them to the procedure rules.
* `engine.py` contains the rules, eligibility checks and scoring.
* `results/hybrid-final/` contains every response, summary and runtime detail.
* `results/hybrid-freeze.json` records the code and data hashes before evaluation.
* `EVIDENCE.md` links the public sources behind the product proposal.

```sh
npm ci
npm test
.venv/bin/python -m unittest discover -s tests -v
```

Vercel serves `site/`. The repository contains synthetic data and public research. Confidential interview notes are excluded. Codex helped with research, code, testing and writing under Fuad's direction. Third party model and runtime licenses retain their original terms.
