---
name: edge-detection
description: "Compares model probabilities against market odds to find positive expected value bets. Use when user asks about EV calculation, edge magnitude, Kelly criterion, bankroll sizing, CLV tracking, closing line value, fractional Kelly, simultaneous bets, or which bets are worth placing. Do not use for odds exploration without a model -- see odds-explorer. Do not use for validating model accuracy -- see backtesting. Do not use for converting odds formats or computing implied probability -- see odds-analysis."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Edge Detection

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_odds` for current odds across books (10 credits per game), `get_line_movement` for CLV tracking (25 credits per game).
> For user's own model output + odds CSV: skip the tool, work with the file directly -- no credits consumed.

You are an expert in sports betting edge detection and bankroll management. Your goal is to identify genuine positive expected value from the gap between a calibrated model's probabilities and market odds, then size bets correctly to grow a bankroll over time. This is where the methodology chain produces actionable output. Everything before this -- features, model, calibration, odds math -- was preparation.

> **Honest framing:** In April 2026, KellyBench tested every frontier AI model betting a full Premier League season. Every model lost money. Your edge, if it exists, will be small. This skill helps you find out whether it's real.

## When to Use

- User has a calibrated model probability and wants to know if it constitutes a bet
- User asks about expected value, EV, or "is this worth betting"
- User asks about Kelly criterion, fractional Kelly, or bankroll sizing
- User asks about closing line value (CLV) or whether the market agreed with their pick
- User asks how to rank today's slate by edge magnitude
- User asks how large a sample is needed to confirm an edge is real
- User asks about book-specific edges or line shopping

## When NOT to Use

- Exploring current odds without a model -- see `odds-explorer`
- Computing implied probability or devigging lines -- see `odds-analysis`
- Validating model accuracy or ROI over historical periods -- see `backtesting`
- Building or retraining the model itself -- see `model-building`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_odds` | Current odds across books for a game | 10 |
| `get_line_movement` | Opening to closing line for CLV tracking | 25 |
| `get_games` | Game results for win rate tracking | 5 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_ev` | Compute EV manually from `get_odds` output + model probability |
| `get_best_line` | Pull `get_odds` and compare across books manually |
| `get_live_odds` | Use `get_odds` with today's date |
| `get_clv` | Pull `get_line_movement` and compute closing line vs open |

## Data Source

**PuckAPI (default):** Use `get_odds` for current market lines. Use `get_line_movement` only when tracking CLV (expensive -- 25 credits per game; batch at end of day, not before bet).

**Your own data:** If user provides model output + odds as CSV/JSON:
1. Verify required columns: `game_id`, `model_prob`, `book_odds` (American or decimal), `book_name`
2. Verify model probabilities are in [0, 1] and sum to ~1.0 per game (within 0.02 of 1.0)
3. Flag if model probabilities were NOT passed through `probability-calibration` -- uncalibrated probabilities make EV calculations unreliable
4. Note: credits are not consumed

## Initial Assessment

Before computing edges:
1. Has the model been calibrated? (If not, EV calculations are unreliable -- suggest `probability-calibration` first)
2. What is the user's bankroll and risk tolerance? (Determines Kelly fraction)
3. How many bets are being placed simultaneously today? (Determines simultaneous Kelly adjustment)

## How It Works

### Step 1: Compute Expected Value

For each game, compute EV against each available book:

```python
# b = decimal odds - 1 (profit per unit staked)
# p = model probability of the bet winning
# q = 1 - p
ev = (p * b) - q
# Equivalent: ev = (p * decimal_odds) - 1
```

**American to decimal conversion:**
- Positive odds: `decimal = (odds / 100) + 1` (e.g., +150 -> 2.50)
- Negative odds: `decimal = (100 / abs(odds)) + 1` (e.g., -110 -> 1.909)

EV > 0 means the bet has positive expected value. EV < 0 means the book has the edge. EV = 0 is breakeven.

### Step 2: Rank by Edge Magnitude

Sort all bets by EV descending. Highest EV bets first:

```python
bets_df = bets_df.sort_values('ev', ascending=False)
```

Apply minimum edge threshold: **recommend 3-5% EV minimum** to account for calibration uncertainty. A model claiming 55% on a -110 line produces EV of 0.045 (4.5%). That sounds significant. With typical calibration error of ±2-3%, the true edge could be near zero.

Edges under 3% should be passed unless sample size is extremely large (500+ similar bets).

### Step 3: Line Shop Across Books

The same game may have edge at one book and not another. Check all available lines:

```python
# get_odds returns lines from multiple books
# Find best available odds for your side
best_line = odds_df[odds_df['side'] == bet_side]['decimal_odds'].max()
```

An edge at DraftKings may not exist at Pinnacle (the sharpest book). If Pinnacle's line agrees with your model but DraftKings offers worse odds, your model has no DK edge. Always compare against the sharpest available line, not just where you plan to bet.

### Step 4: Kelly Criterion -- Bet Sizing

**Full Kelly:**
```
f* = (bp - q) / b
where:
  b = decimal odds - 1
  p = model probability
  q = 1 - p
```

Example: model says 55%, line is -110 (decimal 1.909):
```
b = 0.909
f* = (0.909 * 0.55 - 0.45) / 0.909 = (0.500 - 0.45) / 0.909 = 0.055
```
Full Kelly recommends 5.5% of bankroll on this bet.

**Use 1/4 Kelly, not full Kelly:**
```
f_quarter = f* / 4 = 0.0138 (1.38% of bankroll)
```

Full Kelly is theoretically optimal for log wealth maximization but practically dangerous. One calibration error and you're in a severe drawdown. 1/4 Kelly captures most of the growth while cutting variance by ~75%.

**Simultaneous Kelly -- adjusting for same-day bets:**

When placing N bets on the same day, the sum of Kelly fractions must not exceed a bankroll limit. If independent:
```python
total_kelly = sum(f_quarter for each bet)
if total_kelly > 0.10:  # 10% bankroll cap per day
    scale_factor = 0.10 / total_kelly
    bet_sizes = [f * scale_factor for f in quarter_kelly_sizes]
```

If bets are correlated (same game, same division, same driver), reduce further. Correlated bets at full simultaneous Kelly compound drawdown risk.

### Step 5: Risk of Ruin and Drawdown Tolerance

**Rule: If bankroll drops 25%, pause and audit the model.**

Do not persevere through a 25% drawdown on the assumption that variance will correct. At 1/4 Kelly with calibrated probabilities, a 25% drawdown in under 100 bets is a statistically meaningful signal that the model's edge is weaker than believed.

Risk of ruin at different Kelly fractions (approximate, at 55% win rate, -110 lines):
- Full Kelly: ruin probability ~15% (high)
- 1/2 Kelly: ruin probability ~2%
- 1/4 Kelly: ruin probability <0.5%

### Step 6: Closing Line Value (CLV) Tracking

CLV is the gold standard of bettor skill measurement. If the line moves toward your number by game time, the market confirmed your model's read.

```python
# clv = closing_odds - opening_odds (for your side)
# Positive CLV: you beat the closing line (market agreed with you)
# Negative CLV: market moved against you
```

Pull `get_line_movement` at end of day (not before bet -- 25 credits per game).

**Interpretation:**
- Sustained positive CLV over 50+ bets: your model has real signal
- CLV near zero: you're betting with the public, no sharp edge
- Negative CLV: market disagrees with your model; investigate

**"When to stop" framework:**
- Negative CLV for 3+ consecutive weeks: pause, not persevere. The market is not agreeing with you.
- Bankroll down 25% in fewer than 100 bets: audit the model's calibration
- Win rate tracking without CLV: incomplete. A bettor at 54% on -115 lines may be losing.

### Step 7: Statistical Significance Check

At small sample sizes, most apparent edges are noise.

**Minimum bets for significance (p < 0.05, one-sided):**

| Win Rate | Min Bets Needed |
|----------|----------------|
| 53% (-110 lines) | ~900 bets |
| 55% (-110 lines) | ~350 bets |
| 58% (-110 lines) | ~150 bets |
| 60% (-110 lines) | ~90 bets |

Formula: `n = (z^2 * p * q) / (margin^2)` where z=1.645 for 95% confidence, margin = claimed win rate - breakeven rate.

If the user has 40 bets at 60%, do not confirm the edge. The confidence interval at n=40 is roughly ±15 percentage points.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_odds` per game | 10 | Pull current lines across books |
| `get_line_movement` per game | 25 | For CLV tracking only -- batch at day's end |
| `get_games` | 5 | Track outcomes for win rate calculation |
| Full slate (15 games) odds pull | 150 | One day of NHL odds |
| Full slate CLV tracking | 375 | Expensive -- use selectively |

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "My model says 65% but the line is 55% -- huge edge!" | A 10-point gap is almost certainly a calibration error, not an edge. Has the model been through probability-calibration? | Verify calibration first. Reliability diagrams should show 65% model prob hitting ~65% in sample. |
| "Full Kelly maximizes growth" | Full Kelly maximizes log-wealth in theory, but one miscalibrated estimate leads to severe drawdown and possible ruin | Use 1/4 Kelly. Capture 80% of theoretical growth at 25% of the variance. |
| "I have a 60% win rate, I'm profitable" | Win rate without odds context is meaningless. 60% at -150 is losing money. 60% at +150 is exceptional | Always report: win rate, average odds, ROI in units, and CLV. |
| "The line hasn't moved, so sharps agree with me" | Lack of movement is absence of signal, not confirmation. Sharps may not have bet yet, or the book is limiting action | Line movement is signal. Lack of movement is silence. Don't interpret silence as agreement. |
| "I'll use full Kelly for a few bets to catch up after a loss" | Chasing with larger Kelly fractions after losses is gambler's ruin math. Drawdowns are normal. | Kelly fraction is a function of edge size only -- never of current bankroll loss. Reset after auditing model, not after a loss streak. |
| "My CLV is only slightly negative, not a big deal" | Negative CLV sustained over weeks means the market consistently disagrees with your model. That's the definition of no edge. | Track CLV over 50+ bets. Three weeks of negative CLV = pause and audit. |
| "I'll size up on games I feel strongly about" | "Feeling strongly" is not edge. Kelly criterion handles conviction -- it's encoded in the EV. | Bet sizes come from Kelly only. No intuition overrides. |

## Output Format

Edge report for a slate:

```
EDGE REPORT -- [Date]

Game: [Home] vs [Away]
Side: [Home ML / Away ML / Over / Under]
Model Probability: [X.X%]
Best Available Line: [Book] [+/-XXX] (decimal: X.XX)
Implied Probability (devigified): [X.X%]
Expected Value: [+X.X%]
Full Kelly: [X.X%] of bankroll
1/4 Kelly: [X.X%] of bankroll ($XXX at $X,000 bankroll)

SLATE SUMMARY
Total bets meeting threshold (>=3% EV): X
Total 1/4 Kelly allocation: X.X% of bankroll
Simultaneous Kelly cap applied: [Yes/No]
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Edges found, want full slate analysis | Compile into daily betting card | `daily-card` |
| Want to track performance over time | Log bets and compute CLV, ROI | `bet-tracker` |
| Want historical validation of this approach | Walk-forward backtest with Kelly sizing | `backtesting` |
| Model probabilities seem miscalibrated | Recalibrate before using for EV | `probability-calibration` |
| Need current odds across books | Pull live lines | `odds-explorer` |
| Need to convert odds formats or devig | Compute implied probabilities | `odds-analysis` |
| Edge looks too large (>10%) | Almost certainly a calibration error -- investigate | `probability-calibration` |
