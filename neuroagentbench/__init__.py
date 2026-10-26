"""NeuroAgentBench public API. Score a recorded run. No GPT judge."""

from evaluators.score import evaluate_paths as evaluate

__all__ = ["evaluate"]
__version__ = "0.1.0"
