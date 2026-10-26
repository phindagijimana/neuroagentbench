# NeuroAgentBench literature map

Paper 3 — scoring and construction protocol · 26 October 2026 · planning document, no results claimed

This map states what closest systems already own and what residual NeuroAgentBench is allowed to implement. It is not a PRISMA review and not a finding that the bench works. **Do not invent DOIs or evaluation numbers.** Bibliographic metadata must be re-locked before any manuscript.

**Positioning sentence (use this, not a priority claim).** NeuroClaw NeuroBench asks whether an agent can run a neuroimaging loop under a GPT rubric. NeuroAgentBench asks whether the produced artifact is scientifically valid, including when the right action is to refuse.

**Do not write:** “first neuroimaging agent benchmark,” “first science-agent bench,” or “GPT-judge of scientific quality.”

**Residual that survives the closest systems:** deterministic L0–L5 layers, first-class `false_success`, evidence Pass/Fail/**Unknown**, and abstain/reject gold. No LLM in `evaluators/`. `llm_judge_primary` stays false on every task.

---

## 1. How this map was built

Sources are the locked methods and limitations memos in this folder, plus the program-wide SciCap map for shared 2025–2026 citations already recorded in-tree. No new quantitative scores are introduced here.

| Cluster | Meant to catch |
|---|---|
| Software-repair benches | SWE-bench fail-to-pass graders |
| General science-agent benches | ScienceAgentBench, SciAgentArena |
| Open-ended research + fabrication | MLR-Bench, MLR-Judge |
| Neuroimaging agent eval | NeuroClaw NeuroBench, NEURA NeuroEval |
| Claim vs state | GroundEval / false-success; evidence-bounds Unknown |

---

## 2. Five literature updates

These are the updates this v0 implementation is allowed to act on. Each grants the prior system its object, then names the residual.

### Update 1 — SWE-bench (Jimenez et al., ICLR 2024)

**Owns.** Fail-to-pass unit tests on recorded software patches. Fixture-and-grader discipline.

**Does not own.** Atlas identity, reference space, transform direction, modality, or QC as the oracle.

**Residual.** Steal recorded-tree fixtures and deterministic graders. Do not treat unit-test pass as scientific validity.

### Update 2 — ScienceAgentBench (Chen et al., ICLR 2025)

**Owns.** Expert-constructed general science tasks; success is a Python program that executes. Contamination and shortcut-trap construction already exist.

**Does not own.** Scoring of neuroimaging scientific artifacts (space, atlas, units, justified refusal).

**Residual.** Closest general science bench. Paper 3 residual is artifact validity, not code-file success. Construction protocol (split, equivalents, review status) is borrowed, not invented.

### Update 3 — SciAgentArena (Liu et al., 2026)

**Owns.** Interactive multi-domain science tasks and stepwise checks. **Finding already named:** agents execute invalid premises (sycophancy); rankings can be unstable.

**Does not own.** Invalid-premise gold as a first-class scored family, or false success as a primary endpoint.

**Residual.** Measure “they ran it anyway” as `false_success` and credit `gold_action: abstain` / `reject`. Do not claim we discovered invalid-premise execution.

### Update 4 — MLR-Bench (2025) and GroundEval / false-success (2026)

**Owns (MLR-Bench).** Open-ended ML research tasks; agents can fabricate results after failed runs; **MLR-Judge is an LLM judge**.

**Owns (GroundEval / false-success).** Agents assert completion when state contradicts; LLM judges miss false success.

**Does not own.** A deterministic scientific-artifact oracle that makes `false_success` a recorded field without a judge.

**Residual.** Steal the fabrication and false-success *failure modes*. Do not copy an LLM judge as the primary scorer. A matrix written without tool logs is `evidence_fail` or `evidence_unknown`, not pass.

### Update 5 — NeuroClaw NeuroBench (Wang et al., 2026) and NEURA NeuroEval (2026)

**Owns (NeuroBench).** Closed-loop neuroimaging execution; expected artifacts, QC, checksums; **primary score is a GPT-5.4 rubric** (planning / tool reasonableness / code). Highest domain overlap. Cite it. Do not clone its scorer.

**Owns (NeuroEval).** Planning accuracy versus axioms. Different object: plans and claims, not executed artifacts.

**Does not own.** Layered deterministic L0–L5, `false_success`, evidence Unknown, abstain/reject gold, and `llm_judge_primary: false`.

**Residual.** Score the artifact (and justified refusal) with functions, not prompts. Unknown is recorded and is not fail. Holdout stays empty during development.

---

## 3. Work-by-work matrix

| Work | Year | Object they own | Threat if we over-claim | Residual for Paper 3 |
|---|---|---|---|---|
| SWE-bench | 2024 | Fail-to-pass tests | “We invented recorded graders” | Space/atlas/QC oracle |
| ScienceAgentBench | 2025 | Expert science tasks; code executes | “First science-agent bench” | Artifact validity; abstain gold |
| MLR-Bench | 2025 | Fabrication after failed runs; LLM judge | Copying MLR-Judge | Deterministic `false_success` |
| SciAgentArena | 2026 | Invalid-premise execution, named | Claiming that finding | First-class abstain family + false success |
| NeuroClaw NeuroBench | 2026 | Neuroimaging closed-loop + GPT-5.4 rubric | “First neuroimaging bench”; GPT primary | L0–L5 functions; no LLM judge |
| NEURA NeuroEval | 2026 | Planning vs axioms | Treating plans as artifacts | Executed-artifact layers |
| Evidence-bounds | 2026 | Pass / Fail / Unknown on stored artifacts | Inventing three-valued labels | Apply Unknown to *scientific* claims |
| GroundEval / false-success | 2026 | Claim vs contradictory state | LLM-judge AUROC as our method | Deterministic B2 field |
| BFCL / ToolBench / TOOLRET | 2023–26 | Call / retrieval match | Function-call as science | Method lesson only |
| SciCap / SciGuard | this program | Contracts; preflight edges | Republishing M1–M4 / G1–G5 | Optional secondary arms later |

---

## 4. What would not be novel (do not write these)

- “The first scientific or neuroimaging agent benchmark.”
- “We score scientific quality with a GPT/LLM judge.”
- “Docker plus file-exists is the check.”
- “We have more tasks than ScienceAgentBench.”
- “Stepwise verification” as the contribution (SciAgentArena).
- “Expert annotators” as the contribution (ScienceAgentBench).
- A trusted public leaderboard before isolated re-runs.

---

## 5. Methods this folder implements (locked remainder)

From [`NeuroAgentBench_Methods.md`](NeuroAgentBench_Methods.md) B1–B7:

| ID | Implemented in v0 |
|---|---|
| B1 | `evaluators/l0.py` … `l5.py` — no LLM |
| B2 | `false_success` on every score record |
| B3 | `evidence_status` ∈ {pass, fail, unknown}; unknown ≠ fail |
| B4 | `nab-labels-on-dwi` gold `reject` |
| B5 | `split`, `equivalent_solutions`, `review_status`; `tasks/holdout/` empty |
| B6 | Score record holds `seed`; repeats not run in v0 |
| B7 | Not v0; no ranking |

Primary number: scientifically valid artifact **or** justified abstention. Execution success and the agent’s claim sit beside it.

---

## 6. Open questions (do not resolve by invention)

1. Re-lock NeuroClaw / NeuroBench / NeuroEval bibliographic metadata at submission.
2. Confirm GroundEval and evidence-bounds venue versions before citing page-level claims.
3. If NeuroBench later publishes a non-GPT primary oracle, re-read the go-gate before claiming residual.

**Decision.** Build the resource around the oracle. Default venue remains a *Scientific Data* descriptor if v0 only yields a useful task pack. Do not design a Nature paper around “neuroimaging agent benchmark.”
