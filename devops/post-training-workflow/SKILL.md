---
name: post-training-workflow
description: "Post-training model validation workflow: gating, backtesting, walk-forward validation, deployment decisions. Trigger after GPU training completes."
author: Claude Code
date: 2024-12-27
---

# Post-Training Model Validation Workflow

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-27 |
| **Goal** | Establish systematic workflow for validating trained models before deployment |
| **Environment** | Windows, Alpaca API, GPU-native PPO models |
| **Status** | Verified |

## Context

After completing GPU training (e.g., on Colab), models need systematic validation before deployment:
1. **Gating Assessment** - Does the model meet quality thresholds?
2. **Backtesting** - How does it perform on recent data?
3. **Walk-Forward Validation** - Is performance consistent across time periods?
4. **Deployment Decision** - Paper trading, live, or retrain?

## Verified Workflow

### Step 1: Extract Training Archive

Training runs produce a zip file with models and summary:

```bash
# Extract to training_archives/
unzip Alpaca_trading_trained_YYYYMMDD_HHMMSS.zip -d training_archives/YYYYMMDD_HHMMSS_extract/

# Key files:
# - training_summary_YYYYMMDD_HHMMSS.json  (metrics per symbol)
# - models/rl_symbols/*.pt                 (trained models)
```

### Step 2: Model Gating Assessment

Apply v2.4.5 thresholds to classify each model:

| Classification | Fitness | PF | Consistency | MaxDD |
|---------------|---------|-----|-------------|-------|
| **APPROVED** | >= 0.70 | >= 1.8 | >= 85% | <= 8% |
| **REVIEW** | >= 0.50 | >= 1.3 | >= 65% | <= 15% |
| **DROP** | < 0.50 | < 1.3 | < 65% | > 15% |

```python
from alpaca_trading.training.gating import assess_model_quality

classification, flags, use_checkpoint, cp_idx = assess_model_quality(
    final_fitness=metrics['fitness_score'][-1],
    final_pf=metrics['profit_factor'][-1],
    final_consistency=metrics['consistency'][-1],
    final_max_dd=metrics['max_drawdown'][-1],
    fitness_history=metrics['fitness_score'],
)
```

**IMPORTANT**: Training MaxDD is a PROXY metric (reward volatility), not actual equity drawdown. Old reward_scale=0.1 caused inflated values (35-80%). New reward_scale=0.001 produces realistic values (5-15%).

### Step 3: Copy Models for Testing

Copy approved/review models to models/rl_symbols/:

```bash
cp training_archives/YYYYMMDD_HHMMSS_extract/Alpaca_trading/models/rl_symbols/SYMBOL_1Hour.pt \
   models/rl_symbols/
```

### Step 4: Simple Backtest (30 days)

Quick sanity check on recent data:

```bash
# Set Alpaca API keys (NOT yfinance for crypto)
export ALPACA_KEYS_FILE=API_key_100kPaper.txt

python scripts/run_backtest.py \
    --model models/rl_symbols/SYMBOL_1Hour.pt \
    --days 30 \
    --capital 100000
```

Expected output:
- Total Return (%)
- Max Drawdown (%) - Should be much lower than training proxy MaxDD
- Win Rate (%)
- Profit Factor

### Step 5: Walk-Forward Validation (Critical)

Tests out-of-sample performance across multiple time periods:

```bash
python scripts/run_backtest.py \
    --model models/rl_symbols/SYMBOL_1Hour.pt \
    --days 180 \
    --capital 100000 \
    --walk-forward 5
```

**Interpretation:**

| Metric | Good | Marginal | Poor |
|--------|------|----------|------|
| Positive Folds | >= 4/5 (80%) | 3/5 (60%) | <= 2/5 (40%) |
| Sharpe Range | < 1.0 std dev | 1-2 std dev | > 2 std dev |
| Return Range | All positive | Mixed | Mostly negative |

**Example output from UNIUSD validation:**
```
PER-FOLD ANALYSIS
  Sharpe Range: -3.67 to 2.36
  Sharpe Mean: -1.18 (+/- 2.17)  # High variance = inconsistent
  Positive Folds: 2/5           # Only 40% profitable
```

This indicates the model performs well in some market regimes but poorly in others.

### Step 6: Deployment Decision

| Walk-Forward Result | Action |
|---------------------|--------|
| >= 4/5 positive folds, low variance | Deploy to LIVE |
| 3/5 positive folds, moderate variance | Deploy to PAPER for monitoring |
| <= 2/5 positive folds, high variance | RETRAIN with new parameters |
| Consistent losses | DROP model, investigate training data |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using yfinance for crypto | yfinance doesn't support UNIUSD, BTCUSD etc | Always use Alpaca API for all symbols |
| Trusting training MaxDD | Old reward_scale=0.1 caused 35-80% phantom MaxDD | Backtest shows real MaxDD (2-5%) |
| Simple backtest only | Overlaps with training data, not out-of-sample | Walk-forward validation is essential |
| Deploying after gating only | Gating uses proxy metrics from training | Real validation requires backtesting |

## Key Insights

1. **Proxy vs Real MaxDD** - Training MaxDD is from reward volatility, not equity. Real backtest MaxDD is typically 5-10x lower than training proxy.

2. **Walk-forward is essential** - A model can look good on aggregate metrics but fail in specific market regimes. Walk-forward reveals this.

3. **Fold consistency matters** - A model with 2/5 positive folds but high total return is being carried by one lucky period. Not reliable.

4. **Alpaca API for all data** - yfinance doesn't support crypto. Use `ALPACA_KEYS_FILE` environment variable to specify API credentials.

5. **Time per fold** - Each walk-forward fold takes ~7-8 minutes for 253 bars. 5-fold validation takes ~35-40 minutes total.

## Commands Reference

```bash
# Quick backtest (30 days, recent data)
ALPACA_KEYS_FILE=API_key_100kPaper.txt python scripts/run_backtest.py \
    --model models/rl_symbols/SYMBOL_1Hour.pt --days 30

# Walk-forward validation (180 days, 5 folds)
ALPACA_KEYS_FILE=API_key_100kPaper.txt python scripts/run_backtest.py \
    --model models/rl_symbols/SYMBOL_1Hour.pt --days 180 --walk-forward 5

# Extended validation (365 days, 10 folds)
ALPACA_KEYS_FILE=API_key_100kPaper.txt python scripts/run_backtest.py \
    --model models/rl_symbols/SYMBOL_1Hour.pt --days 365 --walk-forward 10
```

## References

- `scripts/run_backtest.py`: Backtest engine with walk-forward support
- `alpaca_trading/backtest/walk_forward.py`: Walk-forward validation implementation
- `alpaca_trading/training/gating.py`: Model quality assessment
- `alpaca_trading/training/archive.py`: Training archive management
- Training archive: `training_archives/YYYYMMDD_HHMMSS_extract/`
