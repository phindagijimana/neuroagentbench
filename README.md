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

Python 3.11+. No MRI. No model API. `neuroagentbench run` without a recorded tree exits.

Optional agent transport (evaluate only; does not start an agent): `python -m neuroagentbench.mcp`

```bash
pytest tests
```

[Methods](docs/NeuroAgentBench_Methods.md) · [Handbook](docs/handbook.md) · Apache-2.0
