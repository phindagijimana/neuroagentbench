# NeuroAgentBench methods

Paper 3 protocol · 26 October 2026 · planning document, no results claimed

This is the locked methods stack for NeuroAgentBench. It follows the blueprints and the limitations-to-methods filter. NeuroAgentBench is a **scoring and construction protocol for agent runs**, not the first neuroimaging agent benchmark and not a GPT rubric.

Related documents: [limitations to methods](NeuroAgentBench_Limitations_to_Methods.md) · [brief blueprint](Paper_3_NeuroAgentBench_Research_Blueprint.pdf) · [full blueprint](NeuroAgentBench_Paper3.pdf)

SciCap owns contracts. SciGuard owns preflight edges. NeuroAgentBench owns **whether this run produced a scientifically valid artifact**, including when the right action was to refuse.

NeuroClaw NeuroBench (2026) already covers closed-loop neuroimaging execution and scores with GPT-5.4. Cite it. Do not clone its scorer.

---

## 1. Scope

**Question.** Under fixed tools, environments, and budgets, how often do agents produce scientifically valid neuroimaging artifacts — and how often does execution success or a success claim overstate that?

**Unit.** One task × one agent × one run. Repeats are nested, not new tasks.

**Non-scope.** Inventing capability contracts (Paper 1). Inventing composition checking (Paper 2). Planning-accuracy vs axioms (NEURA NeuroEval). LLM-as-judge scientific quality (NeuroBench / MLR-Judge). Clinical diagnosis. A trusted public leaderboard before isolated re-runs exist.

---

## 2. The methods

These are the Paper 3 methods. They are not optional dashboard features.

### B1. Layered deterministic oracle

Each task locks, before any run, checks at six layers. Layers are scored separately. No LLM judge is the primary arbiter.

| Layer | Checks |
|---|---|
| L0 | Instruction compliance; no unauthorized operations |
| L1 | Required files exist; format and metadata parse |
| L2 | Commands complete; no hidden exception |
| L3 | Space, transform, atlas, units, modality |
| L4 | Numerical invariants, QC, anatomy, uncertainty |
| L5 | Pinned inputs, environment, provenance |

**Primary number.** Scientifically valid artifact **or** justified abstention, as defined in the task manifest (typically L3 required; L4/L5 as specified per task).

A connectome matrix with the right dimensions and the wrong atlas is L1/L2 pass, L3 fail — not a full win. Blinded experts only when the automatic oracle cannot decide. Report agreement.

### B2. False success as a first-class endpoint

For every completed run record:

| Field | Meaning |
|---|---|
| `execution_success` | L2 (and required L1) passed |
| `scientific_valid` | Primary scientific rule passed, or justified abstention |
| `agent_claimed_success` | Agent asserted completion |
| `false_success` | Claimed success **or** execution success, and scientific oracle failed |

Invalid-premise tasks must be in the suite so this number can be nonzero.

### B3. Evidence Pass / Fail / Unknown

Before scoring, lock the artifacts that would verify *this task’s* claim (files, hashes, transform provenance, QC fields). After the run:

| Label | Meaning |
|---|---|
| `evidence_pass` | Stored artifacts decide scientifically valid |
| `evidence_fail` | Stored artifacts decide scientifically invalid |
| `evidence_unknown` | Artifacts insufficient to decide the task’s own claim |

Report the all-record interval, not a single opaque percent. Do not score Unknown as success or failure. Infrastructure and pre-run failures are censored, not counted as agent error.

Do not claim invention of three-valued evidence labels. Claim application to **scientific artifact claims**.

### B4. Invalid-premise / abstention family

A predeclared task family whose gold is `ABSTAIN` or `REJECT`:

- labels in the wrong space, no transform
- DK vs DKT identity swap
- insufficient phase-encode metadata
- incomplete segmentation asked for volumes
- impossible scientific request

Credit justified refusal. Penalize blanket refusal. This family *measures* what SciCap and SciGuard try to *cause*.

### B5. Construction protocol

- Public development set vs frozen, independently adjudicated holdout
- Two expert reviewers + adjudicator; report agreement
- Accept a **set** of scientifically equivalent workflows, with numerical tolerances
- Shortcut traps (must not read hidden answers; must not skip a required transform)
- Novel or variant tasks, not copied pipeline tutorials
- Disclose likely pretraining contamination
- Every task declares license, dataset snapshot, and compute tier

The construction protocol is the Data Descriptor method.

### B6. Reliability and cost

On a declared subset: 3–5 repeats. Report variance, P(at least one scientific pass), and **cost per scientifically valid completion** (including failures). Separate infrastructure failure from agent error.

### B7. Model × scaffold factorial

Required only if ranks are published. Fix scaffold and vary model, or fix model and vary scaffold. Never treat a skills-harness number as “the model.” SciCap/SciGuard appear only as **secondary** conditions.

---

## 3. Representation (what is implemented)

| Object | Location |
|---|---|
| Task manifest + gold | `tasks/{bids,anat,dwi,connectome,qc,hpc}/` |
| Task schema | `schemas/task.schema.json` |
| Run / score record | `schemas/score.schema.json` |
| Layer evaluators | `evaluators/` |
| Pinned environments | `environments/` |
| Dataset snapshots (bytes external) | `data/manifests/` |
| Local run logs | `results/` (not in git) |

Interfaces (proposed, not implemented):

```text
neuroagentbench list --suite pilot-v0.1
neuroagentbench run --agent adapter.yaml --suite pilot-v0.1 --repeats 3
neuroagentbench evaluate --runs runs/
neuroagentbench report --format json
```

Evaluators must run with no model API configured.

---

## 4. Primary and secondary endpoints

**Primary (pre-register).** Task-level scientifically valid artifact success — or justified abstention — on the frozen holdout, with numerator, denominator, and 95% interval.

**Secondary**

- Execution success
- False-success rate (B2)
- Evidence Pass / Fail / Unknown shares and bounds (B3)
- Abstention calibration on the B4 family
- Per-layer pass rates
- Repeat variance and cost per valid completion (B6)
- Provenance completeness (L5)

Paired tasks across agents. Hierarchical or clustered intervals. Do not treat repeats as independent new tasks.

---

## 5. Pilot that decides the methods are real

Start with five deterministic tasks, then a 30–50 task expert-reviewed pilot.

| Case | Gold | Method under test |
|---|---|---|
| Valid connectome chain, complete metadata | L3/L4 pass | B1 vs file-exists grader |
| File written, wrong atlas order | execution pass, scientific fail; false success if claimed | B1, B2 |
| T1w labels on DWI, no transform | abstain/reject | B4 |
| Agent writes a matrix without running tools | evidence_fail or unknown, not pass | B2, B3 |
| Two valid transform toolchains | both scientific pass | B5 |
| Same task, three seeds | report variance | B6 |
| GPT rubric would pass, space oracle fails | primary follows the oracle | B1 vs NeuroBench-style judge |

**Go (resource).** Oracles agree with experts; fixtures reproduce on a clean machine; Unknown is not hidden.  
**Go (AI-results paper).** Execution success exceeds scientific success by a nontrivial margin; false success is measurable.  
**No-go as an AI-methods paper.** Only a useful task pack → *Scientific Data* or JOSS, not a reliability claim.

---

## 6. Boundaries with the other papers

| Method | Owner |
|---|---|
| B1–B7 as specified above | **NeuroAgentBench (Paper 3)** |
| Late binding and invoke ALLOW/REJECT/ABSTAIN | SciCap (Paper 1) |
| Edge-level PASS/FAIL/UNKNOWN preflight | SciGuard (Paper 2) |
| GPT-scored closed-loop neuroimaging execution | NeuroClaw NeuroBench; comparator |
| Planning accuracy vs axioms | NEURA NeuroEval; cite |
| Evidence-bounds formalism | 2026 eval paper; reuse labels |

Paper 3 may run SciCap/SciGuard as secondary arms (blueprint B3/B4). Those tables do not become this paper’s novelty and must not be republished as Papers 1–2 confirmatory results without a cross-reference.

---

## 7. Journal gates (locked with the methods)

Do not assume one benchmark yields two independent papers.

| Strongest output | Venue |
|---|---|
| Versioned tasks, oracles, licenses, agreement, no new AI findings | ***Scientific Data* Data Descriptor** — default |
| False success ≫ execution gap, multi-agent, repeats, generalizable reliability claim | Research article; *Nature Machine Intelligence* only if the finding is broad |
| Useful runner, thin methodological increment | *JOSS* / *SoftwareX* |
| Neuroimaging-methods emphasis, limited AI generality | *Imaging Neuroscience* |

**Do not design the project as a Nature paper.** NeuroBench already occupies “neuroimaging agent benchmark.” The differentiator is the **oracle**, not the domain. Keep hypothesis-testing results out of a Data Descriptor.

---

## 8. What these methods are not

Do not describe NeuroAgentBench as any of the following:

- The first scientific or neuroimaging agent benchmark
- A GPT- or LLM-judge of scientific quality
- Docker plus file-exists checking
- A SciCap or SciGuard methods paper
- A clinical validation
- A trusted public leaderboard

---

## 9. Implementation correspondence

| Method | Location |
|---|---|
| B1 layers | `evaluators/` ; task `oracles.layers` |
| B2 false success | `schemas/score.schema.json` run record |
| B3 evidence labels | score record `evidence_status` |
| B4 abstention family | `tasks/` with `gold_action: abstain` or `reject` |
| B5 construction | task `review_status`, `equivalent_solutions`, holdout flag |
| B6 repeats | `neuroagentbench run --repeats` |
| B7 factorial | experiment configs only; not default pilot |

Public demo data: synthetic or OpenNeuro snapshots only. No PHI, no privileged containers, network off by default.
