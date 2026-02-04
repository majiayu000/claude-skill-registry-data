---
name: training-archive-gating
description: "Mandatory training archive with model gating (APPROVED/REVIEW/DROP). Trigger when: (1) training run completes, (2) need to decide which models to deploy, (3) want historical training reference, (4) need checkpoint recommendations for overfitting."
author: Claude Code
date: 2024-12-24
---

# Training Archive & Model Gating System (v2.4.1)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-24 |
| **Goal** | Create mandatory post-training archival with automatic model classification |
| **Environment** | alpaca_trading.training package, Colab/local training |
| **Status** | Success |

## Context

Training runs produce summaries with validation metrics, but there was no:
1. **Structured archival** - Summaries were ephemeral JSON files
2. **Model classification** - No clear criteria for deployment readiness
3. **Overfitting detection** - No automatic checkpoint recommendations
4. **Historical reference** - No way to track model improvements over time

The solution: `TrainingArchiveManager` with automatic gating based on fitness, profit factor, consistency, and drawdown thresholds.

## Verified Workflow

### Model Gating Thresholds

**NOTE (v2.4.1):** Thresholds are calibrated for `reward_scale=0.001`. MaxDD is a **proxy metric** reflecting reward volatility during validation, not actual equity drawdown. With conservative reward scaling:
- 8% proxy MaxDD = rewards staying mostly positive
- 15% proxy MaxDD = occasional negative reward streaks

| Classification | Fitness | PF | Consistency | MaxDD | Action |
|---------------|---------|-----|-------------|-------|--------|
| **APPROVED** | >= 0.70 | >= 1.8 | >= 85% | <= 8% | Deploy to production |
| **REVIEW** | 0.50-0.70 | 1.3-1.8 | 65-85% | 8-15% | Manual review required |
| **DROP** | < 0.50 | < 1.3 | < 65% | > 15% | Do not deploy |

### Overfitting Detection

```python
# Fitness decline from peak triggers checkpoint recommendation
fitness_decline_threshold = 0.05  # 5% decline from peak
fitness_oscillation_threshold = 0.10  # 10% swing = unstable training
```

### Archive Usage

```python
from alpaca_trading.training import TrainingArchiveManager

# Archive training run with automatic gating
archive_mgr = TrainingArchiveManager(archive_dir='training_archives')
archive = archive_mgr.archive_training_run(summary_data)

# Results
print(f"APPROVED: {archive.approved_count}")
print(f"REVIEW: {archive.review_count}")
print(f"DROP: {archive.dropped_count}")

# Get approved models for deployment
approved = archive_mgr.get_approved_models(archive.timestamp)
print(f"Ready for deployment: {approved}")

# Get symbol history across runs
history = archive_mgr.get_symbol_history('AAPL')
```

### Archive Structure

```
training_archives/
├── index.json                    # Master index of all runs
├── {timestamp}/
│   ├── summary.json              # Raw training summary
│   ├── model_assessments.json    # Per-model gating decisions
│   └── recommendations.md        # Human-readable report
```

### Gating Configuration

```python
from alpaca_trading.training import ModelGatingConfig

# Custom thresholds (stricter than v2.4.1 defaults)
config = ModelGatingConfig(
    approved_min_fitness=0.80,     # Default: 0.70
    approved_min_pf=2.0,           # Default: 1.8
    approved_min_consistency=0.90, # Default: 0.85
    approved_max_drawdown=0.05,    # Default: 0.08 (5% proxy MaxDD)
)

# Use custom config
classification, flags, use_checkpoint, best_idx = assess_model_quality(
    final_fitness=0.75,
    final_pf=1.9,
    final_consistency=0.88,
    final_max_dd=0.06,  # 6% proxy MaxDD
    fitness_history=[0.70, 0.75, 0.78, 0.75],
    config=config,
)
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Manual assessment | Inconsistent criteria, subjective | Use fixed thresholds in code |
| Single metric gating | Models with high PF but poor consistency slipped through | Require ALL thresholds met |
| No overfitting detection | Models deployed that had peaked earlier | Track fitness history, recommend checkpoints |
| ASCII-only reports | Unicode errors on Windows (emoji characters) | Use `encoding='utf-8'` on all file operations |

## Key Insights

### Why Multiple Thresholds

1. **Fitness alone is insufficient** - High fitness can mask poor profit factor
2. **Consistency matters** - A model with PF=5.0 but 50% consistency is risky
3. **Drawdown is critical** - High-equity models can still blow up
4. **All thresholds must pass** - A single weak metric can indicate problems

### Checkpoint Recommendations

When `use_checkpoint=True` is returned:
- Model's final fitness declined >5% from peak
- The `best_idx` indicates which validation point had peak fitness
- Calculate checkpoint update: `checkpoint_update = (best_idx + 1) * validation_interval`

### Flags Returned

| Flag | Meaning |
|------|---------|
| `FITNESS_DECLINE` | Final < peak by >5% |
| `UNSTABLE_TRAINING` | Fitness oscillation >10% |
| `LOW_FITNESS` | Below REVIEW threshold |
| `LOW_PF` | Profit factor below threshold |
| `LOW_CONSISTENCY` | Consistency below threshold |
| `HIGH_DRAWDOWN` | Max drawdown above threshold |

### Files Created

```
alpaca_trading/training/__init__.py    # Package exports
alpaca_trading/training/gating.py      # ModelGatingConfig, assess_model_quality()
alpaca_trading/training/archive.py     # TrainingArchiveManager
tests/test_training_archive.py         # 20 unit tests
```

## References
- `alpaca_trading/training/gating.py`: Lines 40-128 (gating logic)
- `alpaca_trading/training/archive.py`: Lines 55-393 (archive manager)
- `tests/test_training_archive.py`: Full test suite
- CLAUDE.md: Model Gating Standards section
