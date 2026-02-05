---
name: experiment-analysis
description: Analyze GRPO training runs for learning dynamics and pipeline performance. Use when diagnosing training issues, reviewing Elo progression, checking throughput, or updating experiment results.
---

# Experiment Analysis

Diagnose GRPO training runs using WandB metrics and Axiom logs.

## Quick Reference

| Question | Command |
|----------|---------|
| **Full Elo analysis** | `uv run python .claude/skills/experiment-analysis/analyze_elo.py <run>` |
| **Compare sweep runs** | `uv run python .claude/skills/experiment-analysis/analyze_sweep.py --sweep <prefix>` |
| Is model learning? | `uv run python scripts/wandb_cli.py get-metrics -r <run> --all-metrics` |
| Rollout throughput? | `uv run python scripts/axiom_cli.py rollout-timing --last 6h` |
| Any errors? | `uv run python scripts/axiom_cli.py errors --last 1h` |
| Extraction rate? | `uv run python scripts/axiom_cli.py extraction-stats --last 24h` |
| System health? | `uv run python scripts/axiom_cli.py health --last 1h` |

## Tools Overview

### WandB CLI (`scripts/wandb_cli.py`)
Training metrics and Elo ratings. Use for:
- Elo trajectory analysis (learning signal)
- Reward/loss curves
- KL divergence and grad norm

### Axiom CLI (`scripts/axiom_cli.py`)
Real-time logs and events. Use for:
- Rollout timing and throughput
- Inference engine performance
- Error monitoring
- Order extraction stats

## Detailed Guides

- [Learning Dynamics](learning-dynamics.md) - Elo, rewards, KL analysis
- [Pipeline Performance](pipeline-performance.md) - Throughput, timing, errors
- [Experiment Tracker Guide](experiment-tracker-guide.md) - Updating docs/experiment-tracker.md
- [Examples](examples.md) - Real analysis walkthrough

## Key Metrics

### Learning Signal (Fixed Reference Analysis)

**Key insight:** Win rate against a dynamic league is meaningless. Use FIXED references.

| Metric | Good Sign | Bad Sign |
|--------|-----------|----------|
| base_model Elo | Declining | Stable/Rising |
| Baseline bot Elo | Declining (exploited) | Rising |
| Best checkpoint - base_model gap | Growing | Shrinking |
| Older checkpoint Elo | Declining | Stable |
| KL divergence | Stable <0.1 | Spikes >0.2 |

**Fixed references** (base_model, chaos_bot, etc.) don't change, so their Elo changes = learning.
**Elo gap** (best checkpoint - base_model) measures how much better trained model is.

### Performance
| Metric | Target | Action if Miss |
|--------|--------|----------------|
| Rollout p95 duration | <120s | Check inference engine |
| Extraction rate | >95% | Check logits processor |
| Error rate | <1% | Check Axiom errors |
| Grad norm | <50 | Policy may be unstable |
