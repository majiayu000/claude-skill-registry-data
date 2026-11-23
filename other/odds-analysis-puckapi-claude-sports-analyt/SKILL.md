---
name: odds-analysis
description: "Converts betting odds between formats and removes bookmaker margin to find true implied probabilities. Use when user asks about devigging, vig removal, implied probability, no-vig lines, American/decimal/fractional odds conversion, Shin method, Power method, or bookmaker margin. Prerequisite for edge detection. Do not use for viewing current odds -- see odds-explorer instead. Do not use for model probability calibration -- see probability-calibration instead. Do not use for finding edges -- see edge-detection instead."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Odds Analysis

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_odds` (10 credits) for current odds data.
> Use `get_line_movement` (25 credits) for historical line movement -- most expensive operation.
> For your own odds CSV, skip the tool and work with the file directly.

You are an expert in betting odds mathematics. Your goal is to extract true implied probabilities from bookmaker odds by removing the embedded margin (vig). This is prerequisite knowledge for any downstream edge detection or expected value calculation.

## When to Use

- User has betting odds and wants to know the "true" implied probability
- User wants to compare odds across multiple sportsbooks
- User asks about vig, juice, margin, or overround
- User wants to build a no-vig line from two-sided market odds
- User needs odds in a different format (American, decimal, fractional)

## When NOT to Use

- Viewing or exploring current odds -- see `odds-explorer`
- Comparing model probabilities against market to find edges -- see `edge-detection`
- Model output calibration -- see `probability-calibration`
- Tracking line movement over time -- the `get_line_movement` endpoint covers that; this skill covers the math

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_odds` | Current odds snapshot for a game | 10/game |
| `get_line_movement` | Historical line movement for a game | 25/game |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_no_vig_line` | Compute from `get_odds` using devig methods below |
| `get_true_probability` | Compute from `get_odds` using Shin or multiplicative method |
| `get_historical_odds` | Use `get_odds` with a past game date |
| `compare_books` | Fetch `get_odds` per book and compare manually |

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Odds snapshot (one game) | 10 | Returns all available books |
| Line movement (one game) | 25 | Full price history, use sparingly |
| Full season odds (backtest) | ~820-1,230 | 82 NHL games * 10cr each |

## Initial Assessment

Before starting, establish:
1. Which odds format is the user working with? (American most common in US; decimal in Europe)
2. Is this a two-sided market (moneyline) or three-outcome market (soccer 1X2)?
3. How many books are available? (More books = better Shin method estimate)

## Format Conversion

### American to Decimal

```
# Positive odds (underdog)
decimal = (american / 100) + 1
# Example: +150 -> (150/100) + 1 = 2.50

# Negative odds (favorite)
decimal = (100 / abs(american)) + 1
# Example: -180 -> (100/180) + 1 = 1.556
```

### Decimal to American

```
# Decimal >= 2.0 (underdog)
american = (decimal - 1) * 100
# Example: 2.50 -> (2.50 - 1) * 100 = +150

# Decimal < 2.0 (favorite)
american = -100 / (decimal - 1)
# Example: 1.556 -> -100 / (1.556 - 1) = -180
```

### American to Fractional

```
# Positive: american/100 = fractional
# +150 -> 150/100 = 3/2

# Negative: 100/abs(american) = fractional
# -180 -> 100/180 = 5/9
```

### Raw Implied Probability (with vig)

```
# From American positive
raw_prob = 100 / (american + 100)
# +150 -> 100 / 250 = 0.400

# From American negative
raw_prob = abs(american) / (abs(american) + 100)
# -180 -> 180 / 280 = 0.643

# From decimal
raw_prob = 1 / decimal
# 1.556 -> 1 / 1.556 = 0.643
```

## Vig Calculation

Vig (vigorish) is the bookmaker's margin. On a two-sided market, both raw probabilities sum to more than 1.0.

```
total_implied = raw_prob_home + raw_prob_away
vig = total_implied - 1.0
```

**Example:** DraftKings has Sabres +150 / Leafs -180.
- Raw prob Sabres: 100 / (150 + 100) = 0.400
- Raw prob Leafs: 180 / (180 + 100) = 0.643
- Total: 0.400 + 0.643 = 1.043
- Vig: 0.043 (4.3% margin)

Typical vig ranges:
- Moneyline main markets: 3-6%
- Totals main markets: 4-5%
- Props: 7-12%
- Live betting: 8-15%

## Four Devigging Methods

### 1. Multiplicative Method

Divide each raw probability by the total overround. Simple and fast.

```
true_prob_home = raw_prob_home / total_implied
true_prob_away = raw_prob_away / total_implied
```

**Example (continued):**
- True prob Sabres: 0.400 / 1.043 = 0.384
- True prob Leafs: 0.643 / 1.043 = 0.617
- Check: 0.384 + 0.617 = 1.001 (rounding)

**Use when:** Quick estimate is needed, books are balanced. Assumes vig is distributed proportionally across both sides.

### 2. Power Method

Assumes equal overround per outcome -- finds exponent p such that sum of probabilities^p = 1.

```
# Find p via numerical solve:
raw_prob_home^(1/p) + raw_prob_away^(1/p) = 1

true_prob_home = raw_prob_home^(1/p)
true_prob_away = raw_prob_away^(1/p)
```

Use scipy.optimize.brentq or similar to solve for p. More accurate than multiplicative on asymmetric markets (heavy favorites).

**Use when:** Moneyline markets with significant favorites where vig is likely tilted.

### 3. Shin Method

Accounts for the possibility of insider trading (informed bettors). The bookmaker widens lines beyond pure vig to protect against sharp action. Shin estimates the true probability plus the insider trading component.

```
# Shin's z parameter (fraction of bets from informed traders):
z = solve for: sum of (raw_prob_i^2 / (z + (1-z) * raw_prob_i)) = 1

# True probability:
true_prob_i = sqrt(z^2 + 4*(1-z)*raw_prob_i^2) / (2*(1-z)) - z / (2*(1-z))
```

The Shin calculation requires numerical methods. In practice:

```python
from scipy.optimize import brentq

def shin_z(z, raw_probs):
    return sum(p**2 / (z + (1-z)*p) for p in raw_probs) - 1

z = brentq(shin_z, 0, 0.5, args=(raw_probs,))
true_probs = [
    (math.sqrt(z**2 + 4*(1-z)*p**2) - z) / (2*(1-z))
    for p in raw_probs
]
```

**Use when:** You want the most accurate true probability estimate. Best for comparing against model. Gold standard for research.

**Limitation:** Requires at least two outcomes. For three-outcome markets (soccer), extend the formula to three sides.

### 4. Worst-Case Method

Assumes all vig is placed on one side -- the most conservative estimate.

```
# Assumes entire vig on favorite:
true_prob_favorite = raw_prob_favorite - vig
true_prob_underdog = raw_prob_underdog  # no adjustment

# Or alternatively: entire vig on underdog
true_prob_underdog = raw_prob_underdog - vig
true_prob_favorite = raw_prob_favorite
```

**Use when:** Conservative analysis, want to know the floor on underdog true probability. Not recommended for betting EV calculations -- too conservative.

## When to Use Each Method

| Method | Use Case | Sample Size | Accuracy |
|--------|----------|-------------|----------|
| Multiplicative | Quick estimates, balanced markets | Any | Moderate |
| Power | Favorites with significant lines | Any | Good |
| Shin | Research, model comparison, EV bets | Best with multiple books | Best |
| Worst-case | Conservative floor estimates | Any | Conservative |

**Default recommendation:** Shin for any research or betting application. Multiplicative only for quick sanity checks.

## Worked Example: Full Devig

**Market:** DraftKings Sabres +150 / Leafs -180

**Step 1: Raw implied probabilities**
- Sabres: 100 / (150+100) = 0.4000
- Leafs: 180 / (180+100) = 0.6429
- Total: 1.0429, Vig: 4.29%

**Step 2: Multiplicative method**
- True Sabres: 0.4000 / 1.0429 = 38.4%
- True Leafs: 0.6429 / 1.0429 = 61.7%

**Step 3: Power method**
- Solve for p: 0.4000^(1/p) + 0.6429^(1/p) = 1 -> p ≈ 1.041
- True Sabres: 0.4000^(1/1.041) = 38.5%
- True Leafs: 0.6429^(1/1.041) = 61.5%

**Step 4: Shin method**
- Solve for z: numerical result z ≈ 0.021
- True Sabres: 38.3%
- True Leafs: 61.7%

**Result comparison:**

| Method | Sabres True Prob | Leafs True Prob |
|--------|-----------------|-----------------|
| Multiplicative | 38.4% | 61.7% |
| Power | 38.5% | 61.5% |
| Shin | 38.3% | 61.7% |
| Raw (with vig) | 40.0% | 64.3% |

Note how raw probabilities sum to 104.3%. Using raw probabilities for EV calculation would make every bet look worse than it is -- you'd be comparing your model against an inflated baseline.

## No-Vig Line Construction

The no-vig line is the American odds equivalent of the true probability.

```
# True prob -> American odds:
# If true_prob > 0.5:
no_vig_american = -100 * true_prob / (1 - true_prob)

# If true_prob < 0.5:
no_vig_american = 100 * (1 - true_prob) / true_prob
```

**Example:** Shin says Sabres true prob = 38.3%
- 0.383 < 0.5, so: 100 * (0.617 / 0.383) = +161

DraftKings posts +150, no-vig line is +161. DraftKings is 11 cents short on the underdog side.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll just use the raw implied probability from the odds" | Raw implied probability includes the vig. For a -180 favorite, raw implied is 64.3% but true probability might be 61.7%. Using raw makes every underdog look worse than it is. | Always devig before comparing against model. One of the four methods above, Shin preferred. |
| "Multiplicative is close enough for moneyline" | On balanced markets (near -110/-110), yes. On heavy favorites (-300+), multiplicative and Shin diverge by 1-2%. On an edge that is already 2-3%, that's significant. | Use Shin for anything with significant implied probability asymmetry. |
| "Line movement means sharp action, I should follow it" | Line movement reflects many things: injury news, public betting, sharp action, or just book repositioning. It is evidence, not proof. | Use line movement as one signal. Cross-reference with injury reports and model output before acting. |
| "Props have the same vig as moneylines" | Props carry 7-12% vig vs 3-5% on moneylines. The no-vig probability for a prop at -115 is very different from a moneyline at -115. | Always calculate vig explicitly from the two-sided market before devigging. |

## Output Format

For a devigged market:

```
Game: Buffalo Sabres vs Toronto Maple Leafs
Book: DraftKings
Raw odds: Sabres +150 / Leafs -180

Raw implied: Sabres 40.0% / Leafs 64.3% (total: 104.3%, vig: 4.3%)

Devigged (Shin method):
  Sabres: 38.3%
  Leafs:  61.7%
  No-vig line: Sabres +161 / Leafs -161
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Devigged odds in hand, have model probability | Compare model vs market to find edge | `edge-detection` |
| Want to explore current lines across books | Browse available odds | `odds-explorer` |
| Need calibrated model probability first | Verify model output quality | `probability-calibration` |
| Building a backtest with historical odds | Fetch historical odds data | `backtesting` |
