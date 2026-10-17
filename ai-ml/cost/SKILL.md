---
name: cost
description: "Show cost tracking and ROI for this engagement."
disable-model-invocation: false
---
Show engagement cost data.

Run these in sequence:
1. `uv run python3 $CLAUDE_PROJECT_DIR/tools/cost.py summary`
2. `uv run python3 $CLAUDE_PROJECT_DIR/tools/cost.py roi`
3. Provide analysis: which agents consumed the most, whether the spend is justified by findings.

## Top-Tier ROI Review

Cost review is a hunting control, not accounting trivia.

- Segment spend by phase: recon, ranking, hunting, validation, reporting, rework.
- Flag any agent class with high spend and low durable output: no new surface, no killed hypotheses, no confirmed evidence.
- Compare spend to expected value: bounty range, report probability, duplicate risk, and remaining proof work.
- Recommend one concrete budget move: continue, pivot class, reduce parallelism, raise min-score, skip noisy targets, or run a focused chain pass.
- Treat repeated false positives as a training signal. Link the spend spike to `/learn`, `/brain`, or rules updates.
