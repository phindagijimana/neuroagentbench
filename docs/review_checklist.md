# Two-expert review checklist (unsigned)

Construction protocol for B5. This is **not a result**. Two humans plus an adjudicator apply [`handbook.md`](handbook.md) to each recorded tree. Leave this file unsigned until that happens. Do not invent names, dates, signatures, or agreement rates.

`llm_judge_primary` stays false. SciCap/SciGuard detections are secondary flags (`oracle: false`), not this paper’s score. Do not start an agent. Do not write MRI bytes. Do not write tasks into `tasks/holdout/`.

## Reviewers (leave blank)

| Role | Name | Date | Signature |
|---|---|---|---|
| Expert 1 | | | |
| Expert 2 | | | |
| Adjudicator | | | |

`review_status` on every pilot task stays `draft` until the three rows above are filled by people.

## How to mark one tree

For each item: score L0–L5 from the handbook, then the four B2 fields and B3 evidence. Use `pass` / `fail` / `not_applicable` for layers. Use `evidence_pass` / `evidence_fail` / `evidence_unknown` for evidence. Unknown is not fail.

Do not treat file-exists (B0) as scientific validity. Do not use a GPT rubric.

## Pilot items (five development tasks)

| Task | Recorded tree | Family | L0 | L1 | L2 | L3 | L4 | L5 | execution_success | scientific_valid | agent_claimed_success | false_success | evidence_status | Expert 1 | Expert 2 | Adjudicator |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `nab-valid-stub` | `examples/runs/valid-stub/` | complete gold | | | | | | | | | | | | | | |
| `nab-atlas-wrong` | `examples/runs/atlas-wrong/` | wrong atlas order | | | | | | | | | | | | | | |
| `nab-labels-on-dwi` | `examples/runs/labels-on-dwi/` | invalid premise, ran it | | | | | | | | | | | | | | |
| `nab-no-tools-matrix` | `examples/runs/no-tools-matrix/` | fabrication | | | | | | | | | | | | | | |
| `nab-register-001` | `examples/runs/missing-evidence/` | missing evidence | | | | | | | | | | | | | | |

## Extra recorded tree (not a sixth task)

Optional public-shaped JSON tree. Same task as the B4 family. No NIfTI.

| Task | Recorded tree | Family | L0 | L1 | L2 | L3 | L4 | L5 | execution_success | scientific_valid | agent_claimed_success | false_success | evidence_status | Expert 1 | Expert 2 | Adjudicator |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `nab-labels-on-dwi` | `examples/runs/labels-on-dwi-refuse/` | invalid premise, justified reject | | | | | | | | | | | | | | |
| `nab-valid-stub` | `examples/runs/s0-public-t1w/` | complete gold, S0 T1w pointer | | | | | | | | | | | | | | |

## What this file does not contain

- Signed expert names
- Agreement percentages
- A claimed review_status of `expert_reviewed` or `adjudicated`
- Evaluation numbers from a live agent
