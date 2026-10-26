# Limitations that can become methods

NeuroAgentBench / Paper 3 · 26 October 2026

Same filter as SciCap and SciGuard: a limitation is a method only if it yields a scoring rule, task-construction rule, or reporting protocol that still stands after ScienceAgentBench, SciAgentArena, SWE-bench, MLR-Bench, and NeuroClaw NeuroBench are granted. The locked Paper 3 protocol is [`NeuroAgentBench_Methods.md`](NeuroAgentBench_Methods.md).

**Filter**

| Keep as a method | Discard as a feature gap |
|---|---|
| Score the artifact, not the claim | “First science-agent benchmark” |
| False success as a primary number | “More tasks than ScienceAgentBench” |
| Evidence Pass / Fail / Unknown | Docker + pass/fail |
| Invalid-premise tasks whose gold is abstain | A GPT rubric on planning quality |
| Frozen holdout + multiple valid solutions | A public leaderboard website |

SciCap owns **contracts**. SciGuard owns **preflight edges**. NeuroAgentBench owns **how agent runs are scored**. Do not republish M1–M4 or G1–G5 as Paper 3 methods. Secondary arms may *use* SciCap/SciGuard; they are not this paper’s novelty.

---

## 1. What the closest systems cannot do

| System | Limitation | Why it is not already NeuroAgentBench |
|---|---|---|
| SWE-bench | Fail-to-pass unit tests. Software correctness ≠ atlas/space/QC. | Steal fixtures and graders. Not the oracle. |
| ScienceAgentBench (ICLR 2025) | 102 expert tasks; success is a Python program that executes. Contamination/shortcut traps exist. Does not score neuroimaging scientific artifacts. | Closest general science bench. Residual: artifact validity, not code-file success. |
| SciAgentArena (2026) | ~200 interactive tasks; stepwise checks. **Finding:** agents execute invalid premises (sycophancy). Rankings unstable. | They *name* weak validity checking. Residual: measure it as a first-class endpoint. |
| MLR-Bench (2025) | Open-ended ML research. Agents fabricate results after failed runs (~80% in one coding-agent slice). LLM judge (MLR-Judge). | Steal the fabrication failure mode. Do not use an LLM judge as the primary oracle. |
| NeuroClaw NeuroBench (2026) | 100–500 neuroimaging tasks; expected artifacts, QC, checksums. **Scored by a GPT-5.4 rubric** (planning 30%, tool reasonableness 40%, code 30%). Closed-loop *execution* focus. | Highest domain overlap. Residual: deterministic scientific layers, false success, Unknown, invalid-premise gold, no LLM-judge primary. |
| NEURA NeuroEval (2026) | 110 tasks; **planning** accuracy vs axioms. | Different object: plans/claims, not executed artifacts. |
| BFCL / ToolBench / TOOLRET | Function-call / retrieval match. | Method lesson only. |
| Evidence-bounds (2026) | Native scores overstate when stored artifacts do not support the claim. Pass / Fail / **Unknown**. | Absorb the reporting rule. Residual: scientific checklists (space, atlas, QC) as the evidence, not UI state. |
| False-success / GroundEval (2026) | Agents assert completion when state contradicts; LLM judges miss it (AUROC ≤ 0.65). | False success is a measured endpoint. Deterministic oracles, not judges. |

NeuroBench is the 2026 paper that will be cited against you. Answer in one sentence: NeuroBench asks whether an agent can **run a neuroimaging loop** under a GPT rubric; NeuroAgentBench asks whether the **produced artifact is scientifically valid**, including when the right answer is to refuse.

---

## 2. Methods worth keeping (Paper 3)

### B1. Layered artifact scoring (not completion, not a GPT rubric)

**Limitation.** ScienceAgentBench scores an executed program. NeuroBench’s published scorer weights planning and “tool reasonableness” via GPT-5.4. GroundEval: judges score plausible traces that never retrieved the needed artifact.

**Method.** Each task declares, before any run, a layered oracle. Layers are scored separately:

| Layer | Checks |
|---|---|
| L0 | Instruction compliance; no unauthorized ops |
| L1 | Required files exist; format/metadata parse |
| L2 | Commands complete; no hidden exception |
| L3 | Space, transform, atlas, units, modality |
| L4 | Numerical invariants, QC, anatomy, uncertainty |
| L5 | Pinned inputs, environment, provenance |

**Primary number:** scientifically valid artifact **or** justified abstention, as defined in the task manifest. Execution success is reported beside it, never instead of it. A matrix with the right shape and the wrong atlas is L1/L2 pass, L3 fail — not a full win.

No LLM judge as sole arbiter. Blinded experts only when the automatic oracle cannot decide.

### B2. False success as a first-class endpoint

**Limitation.** MLR-Bench: agents synthesize results after failed execution. SciAgentArena: agents run invalid premises. Advani (2026): false success is common; judges miss it.

**Method.** For every run record:

- `execution_success`
- `scientific_valid`
- `agent_claimed_success`
- **`false_success`** = claimed or technically finished, scientific oracle failed

Invalid and incomplete tasks must be in the suite so false success can occur. This is the finding that could travel beyond neuroimaging if it is large and stable.

### B3. Evidence Pass / Fail / Unknown (no silent dropping)

**Limitation.** Evidence-bounds (2026): a binary leaderboard hides undecidable runs. Counting Unknown as fail or success biases agents that leave different traces.

**Method.** Before scoring, lock the artifacts that would verify *this task’s* claim (files, hashes, transform provenance, QC fields). After the run:

- Evidence Pass — artifacts decide valid
- Evidence Fail — artifacts decide invalid
- Unknown — artifacts insufficient to decide the task’s own claim

Report the all-record interval, not a single opaque percent. Infrastructure failures are censored, not scored as agent error.

Do not claim you invented three-valued evidence labels. Claim you applied them to **scientific artifact claims**.

### B4. Invalid-premise and abstention tasks

**Limitation.** SciAgentArena’s own result: agents execute scientifically invalid requests. Almost every bench is “do the thing.” Almost none score “do not do the thing.”

**Method.** A predeclared family whose gold is `ABSTAIN` or `REJECT`:

- labels in the wrong space, no transform
- DK vs DKT identity swap
- phase-encode metadata insufficient
- incomplete segmentation asked for volumes
- impossible scientific request

Credit justified refusal. Penalize blanket refusal. This family is how Paper 3 *measures* what SciCap/SciGuard try to *cause*.

### B5. Construction protocol: contamination, equivalents, hidden split

**Limitation.** ScienceAgentBench had to block label-reading shortcuts. Public tutorials leak. Single reference scripts reject valid alternatives. NeuroBench tasks sit next to the agent’s skill pack.

**Method.**

- Public development set vs frozen, independently adjudicated holdout
- Two expert reviewers + adjudicator; report agreement
- Accept a **set** of scientifically equivalent workflows, with numerical tolerances
- Shortcut traps (must not read hidden answers; must not skip a required transform)
- Novel or variant tasks, not copied fMRIPrep tutorials
- Disclose likely pretraining contamination

The construction protocol is part of the method. A Data Descriptor can carry this even if the AI-results paper is separate.

### B6. Reliability and cost, not one seed

**Limitation.** SciAgentArena: outcomes vary across identical runs. Nature-tier agent papers will ask for stability.

**Method.** 3–5 repeats on a declared subset. Report variance, P(at least one valid), and **cost per scientifically valid completion** (including failures). Separate infrastructure failure from agent error.

### B7. Model × scaffold factorial (optional but required for ranking claims)

**Limitation.** Leaderboards confound model and harness. NeuroBench’s main contrast is with-skills vs no-skills on *their* harness.

**Method.** If you rank agents, fix the scaffold and vary the model, or fix the model and vary the scaffold. Never treat a Claude+NeuroClaw-skills number as “Claude.” SciCap/SciGuard appear only as **secondary** conditions, not as this paper’s invention.

---

## 3. Methods that belong next door

| Method | Owner |
|---|---|
| Late binding, invoke ALLOW/REJECT/ABSTAIN | SciCap (Paper 1) |
| Edge-level PASS/FAIL/UNKNOWN preflight | SciGuard (Paper 2) |
| GPT-scored closed-loop neuroimaging execution | NeuroClaw NeuroBench; cite as comparator |
| Planning-accuracy vs axioms | NEURA NeuroEval; cite |
| Evidence-bounds formalism | 2026 eval paper; reuse the labels |
| “First scientific agent benchmark” | False; do not write it |

Paper 3 may run SciCap/SciGuard as ablations (blueprint B3/B4). Those results support Papers 1–2 or a joint supplement. They do not make Paper 3 a methods paper about contracts.

---

## 4. Feature gaps that look like methods but are not

- “Neuroimaging is missing from ScienceAgentBench.” Domain port.
- “We have 200 tasks and a website.”
- “We run Docker and check that a file exists.”
- “We use expert annotators.” ScienceAgentBench already did.
- “Stepwise verification.” SciAgentArena already did.
- “LLM-as-judge for scientific correctness.” That is NeuroBench’s weakness, not a method to copy.
- A trusted public leaderboard before isolated re-runs exist.

---

## 5. Recommended methods stack

1. **Oracle (B1 + B3):** layered deterministic checks; Evidence Pass/Fail/Unknown; no LLM-judge primary.
2. **Endpoints (B2 + B4):** scientific-valid rate **and** false-success rate; abstention family included.
3. **Construction (B5 + B6):** hidden split, equivalent solutions, repeats, cost per valid completion.
4. **Comparators:** reference non-agent pipeline; documentation+shell agent; typed MCP; optional SciCap/SciGuard as secondary.

**Venue split (do not conflate).**

| Strongest output | Venue |
|---|---|
| Versioned tasks, oracles, licenses, agreement | *Scientific Data* Data Descriptor — **no hypothesis results** |
| False success ≫ execution gap, multi-agent, repeats | Research article; *Nature Machine Intelligence* only if the finding is general |
| Useful runner, thin novelty | *JOSS* / *SoftwareX* |

Default: build the resource for **Scientific Data**. Do not design a Nature paper. NeuroBench already occupies “neuroimaging agent benchmark” in 2026; your differentiator is the **oracle**, not the domain.

---

## 6. Pilot that decides these are real methods

| Case | Gold | Method under test |
|---|---|---|
| Valid connectome chain, complete metadata | L3/L4 pass | B1 vs file-exists grader |
| File written, wrong atlas order | execution pass, scientific fail, **false success** if agent claims win | B1, B2 |
| T1w labels on DWI, no transform | abstain/reject; running it is false success | B4 |
| Agent writes a plausible matrix without running tools | Evidence Fail or Unknown, not Pass | B3, B2 (MLR fabrication) |
| Two valid transform toolchains | both Pass | B5 equivalents |
| Same task, three seeds | report variance | B6 |
| GPT rubric says Pass, space oracle says Fail | our primary follows the oracle | B1 vs NeuroBench-style judge |

**Go.** Execution success exceeds scientific success by a nontrivial margin; false success is measurable; Unknown is not hidden; two experts can agree.  
**No-go as an AI-methods paper.** Only a useful task pack. Then *Scientific Data* or JOSS, not a reliability claim.

---

## 7. Decision

Turn **layered non-LLM oracles**, **false success**, **evidence Unknown**, and **invalid-premise gold** into the Paper 3 methods. Leave contracts to SciCap, preflight graphs to SciGuard, and GPT-scored execution loops to NeuroBench. That is the limitation set this field will grant NeuroAgentBench.
