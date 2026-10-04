---
name: backtesting
description: "Walk-forward historical testing of betting strategies to determine whether a model's edge is real. Use when user asks about backtesting, historical simulation, ROI over a season, whether a strategy works, bootstrap confidence intervals, edge compression, or model audit over time. Refuses in-sample testing -- walk-forward only. Do not use for live bet tracking -- see bet-tracker. Do not use for finding edges on today's slate -- see edge-detection. Do not use for model training -- see model-building."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Backtesting

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_odds` for historical odds (10 credits per game), `get_games` for results (5 credits per query).
> **Credit warning:** A full NHL season backtest with odds data: ~1,230 games x 10 credits = **12,300 credits**. Plan accordingly. For initial testing, sample 1-2 months before running a full season.
> For user's own historical data: skip the tool, no credits consumed.

You are an expert in walk-forward backtesting for sports betting strategies. Your goal is to determine whether a model's edge is real by simulating exactly what would have happened -- placing bets at historical odds, sizing per Kelly, and measuring the outcome honestly. This is the honesty skill. It exists to falsify claims, not confirm them.

## When to Use

- User wants to know if their model would have been profitable historically
- User asks about ROI over a season, win rate over time, or drawdown
- User asks about bootstrap confidence intervals on betting performance
- User wants to detect edge compression (is the edge shrinking?)
- User asks whether a strategy holds across different bookmakers
- User wants to audit model calibration drift over time
- User asks if recent accuracy is trending up or down

## When NOT to Use

- Live bet tracking (bets being placed today) -- see `bet-tracker`
- Finding edges on today's slate -- see `edge-detection`
- Training or improving the model itself -- see `model-building`
- Walk-forward validation of model accuracy only (without betting simulation) -- see `walk-forward-validation`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_odds` | Historical odds for a game | 10 |
| `get_games` | Historical game results | 5 |
| `get_team_stats` | Season stats for context | 5 |
| `get_standings` | Historical standings for SOS context | 2 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_historical_bets` | Build from `get_games` + `get_odds` joined by game_id |
| `get_backtest_results` | This skill computes results -- there is no endpoint |
| `get_strategy_performance` | Compute manually using simulation loop below |
| `get_historical_lineups` | Use `get_game_detail` and extract lineup data |

## Data Source

**PuckAPI (default):** Pull historical game results via `get_games` for the date range. For each game, pull historical odds via `get_odds`. Join on game_id. Sort ascending by game_date before any simulation.

**Credit planning before starting:**
```
Estimated cost = num_games * 10 (odds) + num_queries * 5 (results)
One NHL season: ~1,230 games = ~12,300 credits
One month sample: ~100 games = ~1,000 credits
```

Always confirm with the user before pulling a full season of odds.

**Your own data:** If user provides historical predictions + odds as CSV/JSON:
1. Verify required columns: `game_id`, `game_date`, `model_prob`, `book_odds`, `book_name`, `actual_result`
2. Verify ISO 8601 date format (YYYY-MM-DD)
3. Verify data is sorted ascending by date before simulation
4. Note: credits are not consumed

## Initial Assessment

Before running a backtest:
1. What time period? (Season, month, multiple seasons -- determines credit cost)
2. What model and edge threshold? (Need the model's probability output and minimum EV threshold)
3. What bankroll strategy? (Flat, proportional, Kelly, fractional Kelly -- determines what to simulate)
4. Was the model calibrated on this same period? (If yes, this is in-sample -- refuse)

## How It Works

### Step 0: Refuse In-Sample Testing

**The most important rule in this skill.**

If the model was trained or calibrated on the same data being backtested, the results are meaningless. In-sample testing inflates ROI by 5-20% depending on model complexity. This looks like success. It is not.

Walk-forward only:
1. Train/calibrate model on period A (e.g., 2023-24 season)
2. Backtest on period B (e.g., 2024-25 season, the following period)
3. Walk forward: retrain on A+B, test on C

If the user insists on testing the same period used for training, explain why the results will be invalid and suggest a walk-forward split before proceeding.

### Step 1: Prepare Historical Data

Pull game results and odds for the test period (not the training period):

```python
# Sort by date -- critical for walk-forward integrity
df = df.sort_values('game_date').reset_index(drop=True)

# Join model predictions to historical results
# model_prob: what the model said before the game
# actual_result: what happened
# book_odds: what odds were available at the time of bet
```

Verify: model predictions must use only information available before each game. If model was rebuilt with full-season features, it may have leakage. Flag this and recommend re-running with `feature-engineering` temporal guards.

### Step 2: Filter to Bettable Games

Apply the same edge threshold used live:

```python
# Compute EV for each game (see edge-detection for formula)
df['ev'] = (df['model_prob'] * (df['decimal_odds'] - 1)) - (1 - df['model_prob'])
df_bettable = df[df['ev'] >= 0.03]  # 3% minimum edge threshold
```

Log how many games qualify. If >40% of games have edge, the model is likely miscalibrated. Real edges are rare.

### Step 3: Simulate Betting Strategies

Simulate four strategies in parallel for comparison:

**Flat betting (baseline):**
```python
stake = 1.0  # 1 unit per bet regardless of edge
```

**Proportional (edge-scaled):**
```python
stake = ev * 10  # scale up with EV, arbitrary multiplier
```

**Full Kelly:**
```python
b = decimal_odds - 1
f_full = (b * model_prob - (1 - model_prob)) / b
stake = f_full * current_bankroll
```

**1/4 Kelly (recommended):**
```python
stake = (f_full / 4) * current_bankroll
```

Track bankroll game-by-game for all four. Compare final ROI and max drawdown. 1/4 Kelly should show lower variance than full Kelly with similar trajectory -- if it doesn't, investigate.

### Step 4: Performance Metrics

Compute for each strategy:

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| ROI | (profit / total_staked) * 100 | Efficiency of capital |
| Win rate | wins / total_bets | Raw accuracy (needs odds context) |
| Units won | sum of (result * stake) | Absolute performance |
| Max drawdown | max peak-to-trough bankroll drop | Worst case experienced |
| Sharpe ratio | mean(daily_return) / std(daily_return) * sqrt(252) | Risk-adjusted return |
| Profit curve slope | Linear regression on cumulative units | Is it trending up, flat, or down? |

### Step 5: Bootstrap Confidence Intervals

A single backtest run produces one number. Bootstrap to get a distribution:

```python
import numpy as np

n_bootstrap = 1000
roi_samples = []
for _ in range(n_bootstrap):
    sample = df_bettable.sample(n=len(df_bettable), replace=True)
    roi = compute_roi(sample)
    roi_samples.append(roi)

ci_lower = np.percentile(roi_samples, 2.5)
ci_upper = np.percentile(roi_samples, 97.5)
```

Report as: "ROI: 8.2% (95% CI: -3.1% to 19.4%)"

A CI that crosses zero means the edge is not confirmed at 95% confidence. This is common. Be honest about it.

### Step 6: Edge Compression Detection

Markets get smarter as the season progresses. Compare performance by time period:

```python
# Split bets by month or quarter
early = df_bettable[df_bettable['game_date'] < season_midpoint]
late = df_bettable[df_bettable['game_date'] >= season_midpoint]

early_roi = compute_roi(early)
late_roi = compute_roi(late)
```

If early ROI is significantly higher than late ROI, the edge is compressing -- the market has adapted to the same information your model uses. This is real and measurable. It is not variance. It requires retraining or finding new features.

Plot ROI by month. A flat or upward-trending line is healthy. A downward trend in the second half of the season is a warning sign.

### Step 7: Bookmaker-Specific Backtests

Edge at DraftKings is not edge at Pinnacle. Run separate backtests per book:

```python
for book in df['book_name'].unique():
    book_df = df_bettable[df_bettable['book_name'] == book]
    book_roi = compute_roi(book_df)
    book_clv = compute_avg_clv(book_df)
```

Pinnacle ROI is the most meaningful -- Pinnacle has the sharpest lines. If your model only shows edge at soft books (DraftKings, FanDuel) but not Pinnacle, your model is exploiting bookmaker inefficiency, not genuine market mispricing. That edge can be limited or closed.

### Step 8: Model Audit (Calibration + Accuracy Drift)

Fold model audit into the backtest:

**Accuracy over time (30/60/90 day windows):**
```python
for window in [30, 60, 90]:
    recent = df[df['game_date'] >= cutoff - pd.Timedelta(days=window)]
    accuracy = (recent['model_prob'].round() == recent['actual_result']).mean()
```

**Calibration drift:**
- Bin predictions by probability (0.50-0.55, 0.55-0.60, etc.)
- Compare actual win rate in each bin vs predicted
- If model says 60% and actual is 52%, model is overconfident -- recalibrate

**Feature drift detection:**
- Are the feature distributions in the test period similar to the training period?
- If team average goals-for shifted significantly (rule changes, coaching changes), features built on historical averages may be stale

**Retrain/Keep/Pause recommendation:**
- Calibration error < 2 percentage points: keep model
- Calibration error 2-5 percentage points: recalibrate
- Calibration error > 5 percentage points: retrain
- Accuracy trending down for 60+ days: retrain or pause

### Step 9: Compare Against Naive Baselines

A model that doesn't beat the naive baseline has no value:

| Baseline | How to Compute |
|----------|----------------|
| Home-team-always | Bet home team every game, flat stake |
| Market-implied | Bet the favorite (lowest implied prob = lowest EV) |
| Last-season record | Bet the team with better prior season record |
| Random (50%) | Monte Carlo 50/50 for significance comparison |

If your model's ROI does not exceed all four baselines, investigate before claiming edge.

**Brier score** -- for calibration reporting:
```
BS = mean((model_prob - actual_result)^2)
Lower is better. Perfect calibration = 0.
Naive home-team baseline ≈ 0.25 for most sports.
```

A model with Brier score above the naive baseline has negative value.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_odds` per game | 10 | Historical odds -- most expensive operation |
| `get_games` per query | 5 | Historical results |
| One month backtest (NHL) | ~1,000 | ~100 games x 10 credits |
| Half-season backtest (NHL) | ~6,150 | ~615 games x 10 credits |
| Full-season backtest (NHL) | ~12,300 | ~1,230 games x 10 credits |
| Multi-season (3 years) | ~37,000 | Substantial -- plan before starting |

Always confirm credit cost with user before pulling full-season odds. Start with a 1-month sample to validate the pipeline, then expand.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "My backtest shows 15% ROI" | Over how many bets? At what CI? 15% ± 20% means you might be losing. | Bootstrap the CI. Report ROI as a range, not a point estimate. |
| "I tested on the full dataset" | That is in-sample testing. The model learned from these outcomes -- the backtest reflects what it already knew. | Walk-forward only. Train on period A, test on period B. Refuse anything else. |
| "Edge compression is just variance" | Plot ROI by month. A clear downward trend over 50+ bets is not variance -- the market adapted. | Compute early vs late ROI. If the gap is >5 points, the edge is compressing. Retrain. |
| "My model was 65% accurate last month" | Last month is 30-40 bets. Not significant at any reasonable confidence level. | Need 200+ bets for meaningful accuracy measurement. Report CI alongside the number. |
| "The backtest confirms the edge, let's go live" | Did you check edge compression? Book-specific performance? Calibration drift? One green ROI number is not sufficient. | Run the full 9-step process before going live. |
| "I'll test on the same season I trained on" | In-sample. The results will look better than reality. This is how people blow up their bankrolls. | Walk-forward only. The test set must contain data the model has never seen. |
| "Flat betting showed positive ROI so the strategy works" | Flat betting ignores edge magnitude. A Kelly simulation with proper sizing is the real test. | Run all four strategies. Compare risk-adjusted returns. |
| "Pinnacle showed -2% ROI but DraftKings showed +8% -- I'll bet DK" | DK edge may be soft-book inefficiency, not model signal. That edge gets limited quickly. | Always check Pinnacle ROI as the benchmark. Positive DK ROI with negative Pinnacle ROI = book inefficiency, not model edge. |

## Output Format

```
BACKTEST REPORT -- [Strategy] -- [Date Range]

SAMPLE
Total games in period: X
Games with edge (>= 3% EV): X (X.X%)
Books tested: [list]

PERFORMANCE
ROI: X.X% (95% CI: X.X% to X.X%)
Win rate: X.X% (breakeven: X.X% at average odds)
Units won: X.X
Max drawdown: X.X%
Sharpe ratio: X.XX

STRATEGY COMPARISON
Flat betting ROI: X.X%
Proportional ROI: X.X%
Full Kelly ROI: X.X% (max drawdown: X.X%)
1/4 Kelly ROI: X.X% (max drawdown: X.X%)

EDGE COMPRESSION
Early-period ROI (first half): X.X%
Late-period ROI (second half): X.X%
Trend: [Stable / Compressing / Expanding]

MODEL AUDIT
Brier score: X.XX (naive baseline: 0.25)
Calibration drift: X.X pp (threshold: 2pp keep, 5pp retrain)
Recommendation: [Keep / Recalibrate / Retrain / Pause]

NAIVE BASELINES
Home-team-always: X.X%
Market-implied: X.X%
[Model beats baseline: Yes / No]
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Edge confirmed, ready for live tracking | Log live bets and CLV | `bet-tracker` |
| Edge compressing, need new signal | Retrain or add features | `model-building` |
| Calibration drifted beyond threshold | Recalibrate probabilities | `probability-calibration` |
| Edge only at soft books, not Pinnacle | Adjust expectations -- edge may be limited | `edge-detection` |
| Model doesn't beat naive baselines | Investigate features or model architecture | `feature-engineering` |
| Want to run today's slate with confirmed edge | Compile daily betting card | `daily-card` |
| CI too wide, need more sample | Expand test to additional seasons | `backtesting` (re-run, extended period) |
