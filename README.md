# NeuroAgentBench

Scores **recorded** run trees with deterministic L0–L5 functions. File-exists can pass while the atlas oracle fails (`false_success`). `llm_judge_primary` is false.

Not the first neuroimaging agent bench. Not a GPT rubric (NeuroClaw NeuroBench already exists).

## Install

```bash
pip install -e .
```

Python 3.11+. No MRI bytes. No model API.

## Use

```bash
neuroagentbench list --suite pilot-v0
neuroagentbench evaluate \
  --task tasks/connectome/nab-atlas-wrong.yaml \
  --run examples/runs/atlas-wrong/ \
  --seed 0
neuroagentbench run --task tasks/connectome/nab-atlas-wrong.yaml
# exits: evaluate_first_no_agent
```

## Tests

```bash
pytest tests
```

## Docs

- [Methods](docs/NeuroAgentBench_Methods.md) (B1–B7)
- [Handbook](docs/handbook.md)
- [Literature map](docs/NeuroAgentBench_Literature_Map.md)

Apache-2.0.
