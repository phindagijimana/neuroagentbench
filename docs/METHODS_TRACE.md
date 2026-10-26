# NeuroAgentBench methods trace (wave 2)

Paper 3 · 26 October 2026 · planning document, no results claimed

This trace cites the public tool reused for each locked method and the literature residual. It does not replace [`NeuroAgentBench_Methods.md`](NeuroAgentBench_Methods.md). It does not invent B8. It does not add a GPT judge. Bibliographic metadata must be re-locked before any manuscript; do not treat author–year labels here as new DOIs or evaluation numbers.

**Residual (use this, not a priority claim).** Layered L0–L5 oracles, first-class `false_success`, evidence Unknown ≠ fail, and abstain/reject gold. Not the first neuroimaging agent benchmark.

`llm_judge_primary` stays **false** on every task.

---

## Public tool (B0)

SWE-bench (Jimenez et al., ICLR 2024) owns recorded fixtures and a fail-to-pass file/unit-test grader. NeuroAgentBench reuses that discipline as `evaluators/file_exists.py`: pass iff required artifact files exist. No space, atlas, QC, or scientific oracle.

When a recorded tree points at `shared/data/external/ds000003/sub-01/anat/sub-01_T1w.nii.gz`, B0 also reports whether that real gzip exists. Bytes stay outside this folder. Missing inputs do not change artifact status.

Atlas-wrong is the honest residual of that public tool: the matrix file exists, so B0 passes.

Do not copy MLR-Judge or NeuroClaw NeuroBench’s GPT-5.4 rubric.

---

## Locked methods B1–B7

| Method | Public tool reused | Literature residual | Test |
|---|---|---|---|
| B1 | SWE-bench recorded trees | L0–L5 functions, no LLM | `test_evaluate.py` |
| B2 | GroundEval / SciAgentArena invalid-premise | first-class `false_success` | atlas-wrong |
| B3 | — | evidence Unknown ≠ fail | missing-evidence |
| B4 | SciAgentArena invalid premise | abstain/reject gold | labels-on-dwi |
| B5–B7 | construction fields; SciCap/SciGuard secondary flags only | holdout empty; no factorial in v0; flags are not the oracle | schema tests; `test_wave4.py`; unsigned `docs/review_checklist.md` |

### Citations (what they own vs residual)

| Work | Owns | Residual used here |
|---|---|---|
| SWE-bench (Jimenez et al., ICLR 2024) | Recorded fixtures; fail-to-pass graders | File-exists is B0 only. Space/atlas/QC stay in L3–L5. |
| ScienceAgentBench (Chen et al., ICLR 2025) | Expert science tasks; success = program executes; contamination / shortcut-trap construction | Artifact validity and abstain gold, not code-file success. Split / equivalents / review status borrowed (B5). |
| SciAgentArena (Liu et al., 2026) | Interactive science tasks; agents execute invalid premises | Measure “they ran it anyway” as `false_success`; credit `gold_action: abstain` / `reject` (B2, B4). Do not claim discovery of invalid-premise execution. |
| MLR-Bench (2025) | Open-ended ML research; fabrication after failed runs; **MLR-Judge is an LLM judge** | Steal the fabrication failure mode (no-tools matrix). Do not copy an LLM judge. |
| NeuroClaw NeuroBench (Wang et al., 2026) | Closed-loop neuroimaging execution; GPT-5.4 rubric as primary | Cite it. Score artifacts with functions, not prompts. `llm_judge_primary: false`. |
| NEURA NeuroEval (2026) | Planning accuracy versus axioms | Different object. Paper 3 scores executed artifacts and justified refusal. |

GroundEval / false-success (2026) owns claim-versus-contradictory-state as a failure mode. The residual is a deterministic `false_success` field without a judge. Evidence-bounds (2026) owns three-valued Pass/Fail/Unknown labels; the residual is applying Unknown to *scientific* artifact claims (B3), not inventing the labels.

---

## What this folder does not claim

- First scientific or neuroimaging agent benchmark (NeuroClaw NeuroBench already occupies the domain).
- A GPT / LLM judge of scientific quality (NeuroBench / MLR-Judge).
- Docker plus file-exists as the scientific check (that is B0).
- A new B8.

Primary number remains scientifically valid artifact **or** justified abstention. Execution success and the agent’s claim sit beside it.
