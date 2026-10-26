# NeuroAgentBench

`neuroagentbench evaluate` scores a **recorded** run with L0–L5 functions. A file can exist and still be a `false_success`. No GPT judge.

Not the first neuroimaging agent bench.

## Go

```bash
pip install git+https://github.com/phindagijimana/neuroagentbench.git
neuroagentbench evaluate \
  --task tasks/connectome/nab-atlas-wrong.yaml \
  --run examples/runs/atlas-wrong/
```

```python
from neuroagentbench import evaluate
evaluate("task.yaml", "run/")
```

Python 3.11+. No MRI. No model API. `neuroagentbench run` without a recorded tree exits. Optional SciCap/SciGuard flags land on `score.secondary` when those packages import; they are not this paper's oracle. `llm_judge_primary` stays false. Extra recorded JSON trees: `examples/runs/labels-on-dwi-refuse/` (justified reject; no NIfTI) and `examples/runs/s0-public-t1w/` (points at `shared/data/external/ds000003/.../sub-01_T1w.nii.gz`; bytes stay outside this folder). Two-expert form: [`docs/review_checklist.md`](docs/review_checklist.md) — unsigned until humans review.

Optional agent transport (evaluate only; does not start an agent): `python -m neuroagentbench.mcp`

```bash
pytest tests
```

[Methods](docs/NeuroAgentBench_Methods.md) · [Handbook](docs/handbook.md) · Apache-2.0
