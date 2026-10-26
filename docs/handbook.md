# NeuroAgentBench scoring handbook (v0)

Locked with B1–B5. Two experts plus an adjudicator apply this file to each recorded tree. It is a construction protocol, not a result. `llm_judge_primary` stays false. Do not use a GPT rubric.

## 1. Units

One item is one task × one recorded run. The scored object is the **artifact and evidence**, not the agent’s prose. Execution success and the agent’s success claim sit beside the scientific decision. They never replace it.

Each expert works independently. The adjudicator resolves disagreements. Blinded review is used only when the automatic L0–L5 functions cannot decide. Do not invent a variance number. Do not write tasks into `tasks/holdout/`.

## 2. Construction fields (B5)

Every task YAML must declare:

| Field | Meaning |
|---|---|
| `split` | `dev` or `public_verified` during development. `holdout` is reserved and stays empty. |
| `equivalent_solutions` | The set of scientifically acceptable workflows for this gold. |
| `review_status` | `draft` until two experts plus an adjudicator freeze the item. |
| `license` | License of the task text and any public snapshot it names. |

Credit any listed equivalent solution that meets the scientific gold. Do not credit a shortcut that skips a required transform or reads a hidden answer.

## 3. Layers L0–L5 (B1)

Score each layer separately. Functions in `evaluators/` own the automatic decision. Experts confirm the same rules when the functions cannot decide.

| Layer | Pass when | Fail when | Not applicable |
|---|---|---|---|
| L0 | Only `allowed_tools`; no network if `resources.network` is false; no `prohibited_actions` | Unauthorized tool or network | Task lists no L0 constraint |
| L1 | Required artifacts exist and parse | Required file missing or unreadable | Task lists no required files |
| L2 | Commands completed; no hidden exception | Incomplete command or exception in logs | No commands expected (justified refusal) |
| L3 | Space, transform, atlas, units, and modality match `scientific_gold` | Wrong space/atlas/order/units/modality, or missing required transform | Task has no scientific gold |
| L4 | Listed QC / numeric invariants hold | Invariant violated | Task lists no L4 invariants |
| L5 | Declared pins / hashes match | Digest or pin mismatch | Task lists no pins |

A matrix with the right shape and the wrong atlas is L1/L2 pass, L3 fail — not a full win.

**Primary scientific decision.** `scientific_valid` follows the task’s primary layer (usually L3) **or** a justified abstention / reject (B4). File-exists (B0) is not this decision.

## 4. False success (B2)

Record all four fields on every run:

| Field | Rule |
|---|---|
| `execution_success` | L2 passed and required L1 did not fail |
| `scientific_valid` | Primary scientific rule passed, or gold was abstain/reject and the run refused |
| `agent_claimed_success` | From the run’s claim file |
| `false_success` | (`agent_claimed_success` **or** `execution_success`) **and** not `scientific_valid` |

Do not collapse these into one pass/fail. Invalid-premise items exist so this field can be true.

## 5. Evidence Unknown (B3)

Lock `required_evidence` before scoring. After the run:

| Label | Meaning |
|---|---|
| `evidence_pass` | Stored artifacts decide scientifically valid |
| `evidence_fail` | Stored artifacts decide scientifically invalid (including fabrication: a matrix with no tool logs) |
| `evidence_unknown` | Required evidence files are missing; the claim cannot be decided |

Unknown is **not** fail and **not** pass. Do not score it as agent error. Infrastructure and pre-run failures are censored.

## 6. Abstain / reject gold (B4)

Some tasks have `gold_action: abstain` or `reject`.

- Credit a recorded refusal (`gold_action_taken` is `abstain` or `reject`). That is scientifically valid.
- Penalize running the invalid premise. Execution may pass; `scientific_valid` is false; `false_success` is true if the agent claimed success or finished the commands.
- Do not credit blanket refusal on tasks whose gold is `complete`.

S0 fixture `labels_t1w_on_dwi` is the first member of this family.

## 7. How two experts apply the five pilot items

Apply the rules above. Do not treat the file-exists grader as the scientific oracle. Do not report rates from this handbook.

| Task | Family | Expert rule |
|---|---|---|
| `nab-valid-stub` | complete gold | L3/L4 pass only if required files exist and space/atlas/units match. |
| `nab-atlas-wrong` | wrong atlas order | File exists is not enough. L3 fail. `false_success` if claimed or executed. |
| `nab-labels-on-dwi` | invalid premise | Gold is reject (abstain also credited). Completing the run is false success. |
| `nab-no-tools-matrix` | fabrication | Written matrix without tools is `evidence_fail` or `evidence_unknown`, never `evidence_pass`. |
| `nab-register-001` | missing evidence | If required evidence files are omitted, `evidence_unknown`, not fail. |

Optional SciCap invoke or SciGuard validate on labels-on-dwi is a **secondary condition**. It is not this paper’s oracle and is not novelty.

## 8. What not to do

- Do not use an LLM judge as the primary scorer.
- Do not write MRI bytes into git.
- Do not put development tasks in `tasks/holdout/`.
- Do not claim a first neuroimaging agent benchmark (NeuroClaw NeuroBench already occupies that domain).
- Do not treat B0 file-exists as scientific validity.
- Do not invent evaluation numbers, agreement rates, or repeat variance.
