# NeuroAgentBench

`neuroagentbench evaluate` scores a **recorded** run with L0–L5 functions. A file can exist and still be a `false_success`. No GPT judge.

Not the first neuroimaging agent bench.

## Go

```bash
git clone https://github.com/phindagijimana/neuroagentbench.git
cd neuroagentbench && pip install -e .
neuroagentbench evaluate \
  --task tasks/connectome/nab-atlas-wrong.yaml \
  --run examples/runs/atlas-wrong/
```

Python 3.11+. No MRI. No model API. `neuroagentbench run` without a recorded tree exits.

```bash
pytest tests
```

[Methods](docs/NeuroAgentBench_Methods.md) · [Handbook](docs/handbook.md) · Apache-2.0
