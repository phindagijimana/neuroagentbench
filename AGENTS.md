# Agent instructions — NeuroAgentBench (Paper 3)

Read [`docs/NeuroAgentBench_Methods.md`](docs/NeuroAgentBench_Methods.md) before writing code. This folder is a **scoring and construction protocol**, not the first neuroimaging agent benchmark and not a GPT rubric.

Program build plan: [`../docs/BUILD_PLAN.md`](../docs/BUILD_PLAN.md) · S0: [`../shared/AGENTS.md`](../shared/AGENTS.md)

## Mission

Score a recorded run against a locked layered oracle. Primary number is scientifically valid artifact **or** justified abstention. Execution success and the agent’s success claim are recorded beside it. `false_success` is first-class.

## Do not build

- An LLM-as-judge primary scorer (NeuroClaw NeuroBench already does that).
- A public leaderboard.
- Docker-plus-file-exists as the only check.
- SciCap/SciGuard as this paper’s novelty (optional secondary conditions later).
- A full 50-task suite before five deterministic tasks evaluate.

## Locked methods you must implement

| ID | Rule |
|---|---|
| B1 | Layers L0–L5 scored separately. No LLM in `evaluators/`. |
| B2 | `false_success` = claimed or execution success, and scientific oracle failed. |
| B3 | `evidence_pass` / `evidence_fail` / `evidence_unknown`. Unknown ≠ fail. |
| B4 | Some tasks have `gold_action: abstain` or `reject`. |
| B5 | `split`, `equivalent_solutions`, `review_status` on every task. |
| B6 | Repeats later; design the run record to hold `seed`. |
| B7 | Factorial only if you rank; not v0. |

## Reuse

- [`schemas/task.schema.json`](schemas/task.schema.json)
- [`schemas/score.schema.json`](schemas/score.schema.json)
- [`tasks/connectome/nab-register-001.yaml`](tasks/connectome/nab-register-001.yaml)

S0 invalid fixture `labels_t1w_on_dwi` is the first abstain/reject family.

## Target tree

```text
schemas/task.schema.json
schemas/score.schema.json
tasks/connectome/nab-register-001.yaml
tasks/connectome/nab-atlas-wrong.yaml      # file exists, wrong atlas → L3 fail
tasks/connectome/nab-no-tools-matrix.yaml  # matrix written without tools
tasks/connectome/nab-labels-on-dwi.yaml    # gold_action: abstain or reject
tasks/anat/nab-valid-stub.yaml             # L3/L4 pass if artifacts present
evaluators/l0.py … l5.py
evaluators/score.py
neuroagentbench/cli.py
tests/test_evaluate.py
pyproject.toml                             # console_script: neuroagentbench
```

## CLI (v0 = evaluate recorded trees only)

```text
neuroagentbench evaluate --task tasks/connectome/nab-atlas-wrong.yaml --run examples/runs/atlas-wrong/
neuroagentbench list --suite pilot-v0
```

Do not implement `run --agent` until evaluate is green. Evaluators must work with no model API.

## Score record

Follow [`schemas/score.schema.json`](schemas/score.schema.json):

- `layers.L0`…`L5`: `pass` | `fail` | `not_applicable`
- `execution_success` ← L2 (and required L1)
- `scientific_valid` ← task primary (usually L3, or justified abstention)
- `agent_claimed_success` ← from the run’s claim file
- `false_success` ← (claimed ∨ execution_success) ∧ ¬ scientific_valid
- `evidence_status` ← pass/fail/unknown from `required_evidence`

A matrix with the right shape and the wrong atlas: L1/L2 pass, L3 fail, not a full win.

## First vertical slice (must pass)

| Recorded run | Gold |
|---|---|
| Valid stub with required files + matching space/atlas | L3 pass; `scientific_valid` true |
| File written, wrong atlas order | execution true, scientific false; `false_success` true if claimed |
| T1w labels applied to DWI, no transform | `gold_action` abstain/reject; running it is false success |
| Plausible matrix, no tool logs | `evidence_fail` or `evidence_unknown`, not pass |
| Required evidence files missing | `evidence_unknown`, not fail |

## Layer meaning (implement as functions, not prompts)

| Layer | Check |
|---|---|
| L0 | Only allowed tools; no network if `resources.network` is false |
| L1 | Required files exist and parse |
| L2 | Commands completed; no hidden exception in logs |
| L3 | Space, transform, atlas, units, modality vs task gold |
| L4 | QC / numeric invariants if the task lists them |
| L5 | Pinned digest / hashes if present |

## Tests

`tests/test_evaluate.py` builds tiny fake run directories (JSON + empty placeholder files). No MRI bytes. Assert the five cases. Unset any model API keys.

## Boundaries

- SciCap/SciGuard may appear later as harness flags. Their detections are not this paper’s result.
- Platform silent success (UI lied) is NeuroInsight N2, a different object.

## Done when

- `neuroagentbench evaluate` scores the five recorded trees offline.
- `llm_judge_primary` stays false on every task.
- Holdout split exists as a directory that you do not write tasks into during development.

Stop. Do not add a website or 50 tasks until methods §5 go-gates are re-read.
