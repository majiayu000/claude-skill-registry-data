---
name: experiment-design
description: Design a falsifiable, controlled experiment for software, ML, or computational research. Use before implementing a research experiment or committing scarce compute.
---

# Experiment Design

Design the experiment so the result can distinguish between the hypothesis and plausible alternatives.

1. State the hypothesis, target claim, and falsifiable prediction.
2. Define independent variables, outcomes, control conditions, and confounders.
3. Select meaningful baselines and ablations; justify dataset splits and prevent leakage.
4. Specify metrics, aggregation, uncertainty estimates, seeds, sample sizes, and stopping rules as appropriate.
5. Fix the evaluation protocol before inspecting test results. Keep validation and test data roles separate.
6. Estimate compute, memory, wall time, cost, and failure recovery. Run a small pilot before a large job.
7. Record software versions, environment, hardware, hyperparameters, data versions, and artifacts to preserve.
8. Plan negative-result interpretation and what would falsify the preferred explanation.

Deliver a protocol with a run matrix, metrics, resources, risks, and reproducibility requirements. Do not tune repeatedly on the final test set or change metrics after seeing outcomes without disclosing it.
