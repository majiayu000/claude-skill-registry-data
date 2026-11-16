---
name: reproducible-ml-experiments
description: Implement, run, and compare ML experiments with traceable configurations and artifacts. Use when training, fine-tuning, evaluating, or reproducing a model.
---

# Reproducible ML Experiments

1. Convert the approved experiment design into explicit configuration files and runnable commands.
2. Pin code revision, dependencies, model/tokenizer versions, dataset snapshot, preprocessing, seeds, and hardware details where feasible.
3. Validate the data path, split logic, labels, batch shapes, loss, and metric implementation before long runs.
4. Run a smoke test on a small sample; confirm checkpointing, logging, and resume behavior.
5. Log configuration, environment, run ID, random seeds, resource use, metrics, and artifact locations.
6. Compare models under the same data, split, metric, and budget. Run multiple seeds when variance matters.
7. Keep validation-driven choices separate from final test evaluation.
8. Report failed, interrupted, and incomplete runs; preserve enough state to reproduce results.

Never invent metrics or present simulated values as measured. A checkpoint existing does not prove a run completed. Do not launch expensive or remote jobs without the user's approval and a clear budget/resource plan.
