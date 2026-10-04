---
name: bet-tracker
description: "Track predictions vs actuals in production: log bets, compute CLV, monitor ROI, detect edge decay, and run significance tests. Use when user asks about tracking bets, bet logging, closing line value, CLV, ROI tracking, win rate, drawdown monitoring, or whether their model has an edge right now. Do not use for finding today's bets -- see daily-card or edge-detection. Do not use for historical backtesting before live betting -- see backtesting. Do not use for model training or retraining -- see model-building."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Bet Tracker

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_games` (5 credits) to pull outcomes. Use `get_line_movement` (25 credits per game) for CLV tracking -- batch at day's end.
> For logging and metrics: local CSV or SQLite -- no credits consumed.

You are the honesty mechanism in the methodology chain. Your goal is to answer "do I actually have an edge right now?" with real numbers, not historical backtesting confidence. Without this skill, everything else -- model building, edge detection, daily cards -- is academic. The feedback loop that makes it matter.

## When to Use

- User wants to log a bet they placed (or are about to place)
- User asks whether their model has an edge based on live performance
- User asks about closing line value, CLV, or whether the market agreed with them
- User wants to see their running ROI, win rate, drawdown, or P&L
- User asks if their track record is statistically significant
- User wants to know when to stop or pause betting

## When NOT to Use

- Finding today's edges before betting -- see `daily-card` or `edge-detection`
- Historical backtesting with past data before going live -- see `backtesting`
- Rebuilding or retraining the model -- see `model-building`
- Checking calibration of model probabilities -- see `probability-calibration`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Pull game results to resolve open bets | 5 |
| `get_odds` | Pull closing odds for CLV tracking (if not stored at bet time) | 10 |
| `get_line_movement` | Opening to closing line for CLV computation | 25 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_bet_history` | Local CSV/SQLite is the store -- no cloud sync via API |
| `get_clv` | Compute from `get_line_movement` output manually |
| `get_roi` | Compute from local bet log |
| `get_outcomes` | Use `get_games` filtered to dates and teams |
| `log_bet` | Write to the local file directly |

## Initial Assessment

Before starting:
1. Is the user logging a new bet, resolving existing bets, or reviewing performance metrics?
2. Where is the bet log stored? (Default: `bets.csv` in working directory; or SQLite `bets.db`)
3. Does the user track CLV? If yes, `get_line_movement` will be needed at day's end (25 credits/game).

## Storage Schema

Recommend CSV for simplicity, SQLite for scale (200+ bets).

**CSV schema (`bets.csv`):**
```
date,game_id,sport,bet_type,selection,model_prob,market_odds,closing_odds,stake_pct,stake_units,result,pnl_units,clv,book,notes
```

**Field definitions:**
- `date` -- ISO 8601 (YYYY-MM-DD)
- `game_id` -- from `get_games` output; links to outcome resolution
- `sport` -- NHL (or other sport if applicable)
- `bet_type` -- ML, spread, total, prop
- `selection` -- Home ML, Away ML, Over 6.0, etc.
- `model_prob` -- decimal (0.0-1.0)
- `market_odds` -- American format at time of bet (-110, +135, etc.)
- `closing_odds` -- American format at game time (fill after close for CLV)
- `stake_pct` -- percentage of bankroll (e.g., 0.021 = 2.1%)
- `stake_units` -- units staked (e.g., 1.0 unit)
- `result` -- W, L, P (push), or OPEN
- `pnl_units` -- profit/loss in units (+0.91 for win at -110, -1.0 for loss)
- `clv` -- closing odds - market odds (positive = beat the close)
- `book` -- DraftKings, FanDuel, Pinnacle, etc.
- `notes` -- free text

## How It Works

### Step 1: Log a Bet

When user says they placed a bet, write a row immediately with result=OPEN.

Do not wait for the outcome. Capture at bet time: model_prob, market_odds, stake_pct, book.

Closing odds and result get filled in later.

### Step 2: Resolve Open Bets

Call `get_games` with the relevant dates and teams. Match by game_id or team names + date.

Update result (W/L/P) and compute pnl_units:
- Win at American odds +XXX: `pnl = stake_units * (odds/100)`
- Win at American odds -XXX: `pnl = stake_units * (100/abs(odds))`
- Loss: `pnl = -stake_units`
- Push: `pnl = 0`

### Step 3: Compute CLV

At end of day (not before bet placement), call `get_line_movement` for each game bet.

```python
# For a bet on Team A ML:
# clv = closing_team_a_odds - bet_team_a_odds (American)
# Positive CLV: you got better odds than close (beat the market)
# Negative CLV: market moved away from your number
```

Convert American to decimal for averaging across books:
```python
def american_to_decimal(odds):
    if odds > 0:
        return (odds / 100) + 1
    else:
        return (100 / abs(odds)) + 1

clv_decimal = american_to_decimal(closing_odds) - american_to_decimal(bet_odds)
```

**CLV interpretation:**
- Positive sustained CLV: model has real signal; the market confirmed your reads
- CLV near zero: you're betting at market consensus; no information advantage
- Negative CLV: market consistently disagrees with your model

### Step 4: Running Metrics

Compute from the bet log at any point:

**Win rate:**
```python
win_rate = wins / (wins + losses)  # exclude pushes
```

**ROI in units:**
```python
roi = total_pnl_units / total_stake_units
```

**Breakeven rate at average odds:**
```python
# For -110 average odds: breakeven = 110/210 = 52.38%
avg_decimal = mean([american_to_decimal(o) for o in market_odds])
breakeven_rate = 1 / avg_decimal
```

**Average CLV:**
```python
avg_clv = mean(clv_column)  # in decimal odds units
```

**Drawdown:**
```python
cumulative_pnl = pnl_units.cumsum()
peak = cumulative_pnl.cummax()
drawdown = cumulative_pnl - peak  # negative values = drawdown
max_drawdown = drawdown.min()
current_drawdown = drawdown.iloc[-1]
```

### Step 5: Edge Decay Detection

Plot CLV and ROI as rolling 20-bet windows over time.

Negative CLV for 3 consecutive weeks = pause, not persevere. Do not interpret a losing streak as variance without checking CLV first.

If CLV is positive but ROI is negative: good process, bad luck. Continue.
If CLV is negative and ROI is negative: the model has no real edge. Pause and audit with `backtesting`.
If CLV is positive and ROI is positive: keep going.

### Step 6: Significance Testing

**Chi-squared test on win rate:**
```python
from scipy.stats import binom_test

# H0: true win rate = breakeven rate
# H1: true win rate > breakeven rate
p_value = binom_test(wins, n_bets, breakeven_rate, alternative='greater')

# p < 0.05 = statistically significant at 95% confidence
```

**Minimum bets for significance by win rate (at -110 lines, breakeven = 52.38%):**

| Win Rate | Min Bets Needed |
|----------|----------------|
| 53% | ~900 |
| 55% | ~350 |
| 57% | ~180 |
| 60% | ~90 |
| 63% | ~50 |

State explicitly: "Your sample is N bets. At your win rate of X%, you need Y bets for statistical significance."

Never confirm an edge from fewer than 100 bets unless win rate is above 60%.

### Step 7: Safety Alerts

Fire automatic alerts when:

1. **Negative CLV 3 consecutive weeks:** "CLV has been negative for 3 weeks. Pause and audit with `backtesting` before continuing."
2. **Drawdown exceeds 20% of bankroll:** "Current drawdown is XX%. Recommend pausing at 20%. Review model calibration."
3. **Win rate drops below breakeven for 50+ bets:** "Win rate of X% is below breakeven of Y% over 50+ bets. Auditing the model is warranted."
4. **Staking above 1/4 Kelly:** "Recorded stake of X% exceeds 1/4 Kelly recommendation of Y%. Confirm this is intentional."

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_games` (outcome resolution) | 5 | Covers all games on a date |
| `get_line_movement` per game | 25 | Batch at end of day; don't pull before betting |
| `get_odds` (closing odds backup) | 10 | Only if closing odds not stored at bet time |
| Typical day (resolve + CLV for 3 bets) | ~80 | 5 + 3x25 |
| Logging and metrics | 0 | Local file operations |

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll track results later" | Survival bias: you remember wins more vividly than losses; logging after the fact skews records | Log at bet placement, not resolution |
| "My win rate is 58%, I clearly have an edge" | 58% over 40 bets has a confidence interval of ~15 percentage points; it could be 43%-73% | Run the significance test; state sample size requirements |
| "CLV doesn't matter if I'm profitable" | Profitability without CLV is indistinguishable from luck; CLV separates skill from variance | Track CLV; sustained positive CLV is the real edge signal |
| "I'll keep betting through the drawdown -- variance will correct" | A 20%+ drawdown in under 100 bets is a signal, not noise. Persevering is the gambler's fallacy | Pause at 20% drawdown; audit the model |
| "My model can't be wrong -- it backtested well" | Backtesting overfits; live performance is truth | CLV and live ROI override backtest confidence |
| "Record stakes in dollar amounts" | Dollar amounts shift with bankroll size; units and percentages are portable | Track stake_pct and stake_units; convert to dollars on display |

## Output Format

**Dashboard view:**
```
Bet Tracker Dashboard -- Updated [date]

Total bets: N | Open: X | Resolved: Y
Win rate: XX.X% (need X more for significance at current rate)
Breakeven rate: XX.X% (at avg odds)

ROI: +X.XX units (+XX.X%)
Current drawdown: -X.X units (-X.X% of bankroll)
Max drawdown (historical): -X.X units

CLV (avg): +X.X cents [POSITIVE / NEGATIVE]
CLV (last 20 bets): +X.X cents [TRENDING UP / DOWN]

Status: [EDGE CONFIRMED / EDGE UNCERTAIN / PAUSE RECOMMENDED]
[Safety alert if triggered]
```

**Single bet log:**
```
Logged: [Date] | [Game] | [Bet Type] | [Selection]
Model: XX.X% | Odds: [+/-XXX] | Stake: X.X%
Status: OPEN (result pending)
```

**Resolved bet:**
```
Resolved: [Date] | [Game] | [Selection]
Result: [W/L/P] | P&L: [+/-X.XX units]
CLV: [+/-X cents] | [Beat the close / Didn't beat the close]
Running ROI: [+/-XX.X%] over N bets
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| CLV negative for 3+ weeks | Audit model against historical data | `backtesting` |
| Edge confirmed, ready for today | Pull tonight's slate and rank edges | `daily-card` |
| Drawdown exceeded threshold | Check calibration of model probabilities | `probability-calibration` |
| Win rate significant, want to scale | Compute Kelly sizing for larger bankroll | `edge-detection` |
| Model needs retraining based on live data | Rebuild with corrected features | `model-building` |
| Want visual equity curve | Generate cumulative P&L chart with drawdown bands | `visualization` |
