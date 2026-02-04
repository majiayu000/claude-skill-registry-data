---
name: elo-ratings-math
description: Explains the mathematical principles behind Elo rating systems, including expected score calculation, rating updates, and the K-factor. Use when implementing or understanding competitive rating systems.
---

# Elo Ratings Mathematics

## Overview

The Elo rating system is a method for calculating the relative skill levels of players in competitor-versus-competitor games. Originally developed by Arpad Elo for chess, it's now used in many competitive contexts including sports, video games, and online platforms.

## Core Mathematical Principles

### 1. Expected Score Formula

The expected score for a player is the probability of winning based on the rating difference between two players.

**Formula:**
```
E_A = 1 / (1 + 10^((R_B - R_A) / 400))
```

Where:
- `E_A` = Expected score for player A (between 0 and 1)
- `R_A` = Current rating of player A
- `R_B` = Current rating of player B
- `10^x` = 10 raised to the power of x

**Interpretation:**
- E_A = 1.0 means player A is expected to win with certainty
- E_A = 0.5 means both players are equally matched (50% win probability)
- E_A = 0.0 means player A is expected to lose with certainty

**Example:**
If player A has rating 1600 and player B has rating 1400:
```
E_A = 1 / (1 + 10^((1400 - 1600) / 400))
E_A = 1 / (1 + 10^(-200 / 400))
E_A = 1 / (1 + 10^(-0.5))
E_A = 1 / (1 + 0.316)
E_A ≈ 0.76
```
Player A is expected to score 0.76 (76% chance of winning).

### 2. Rating Update Formula

After a game, ratings are updated based on the actual outcome compared to the expected outcome.

**Formula:**
```
R'_A = R_A + K × (S_A - E_A)
```

Where:
- `R'_A` = New rating for player A
- `R_A` = Old rating for player A
- `K` = K-factor (determines rating volatility)
- `S_A` = Actual score (1 for win, 0.5 for draw, 0 for loss)
- `E_A` = Expected score (from formula above)

**The Update Difference:**
```
ΔR_A = K × (S_A - E_A)
```

This difference represents:
- Positive value: Player performed better than expected (rating increases)
- Negative value: Player performed worse than expected (rating decreases)
- Zero: Player performed exactly as expected (no rating change)

### 3. The K-Factor

The K-factor controls how much ratings can change after each game.

**Common K-factor values:**
- **K = 32**: High volatility, used for beginners or provisional ratings
- **K = 24**: Medium volatility, used for intermediate players
- **K = 16**: Low volatility, used for established/expert players
- **K = 10**: Very stable, used for top-level players

**Adaptive K-factor example (FIDE chess system):**
```
K = 40  if games_played < 30
K = 20  if rating < 2400
K = 10  if rating >= 2400
```

### 4. Rating Difference and Win Probability

The relationship between rating difference and expected win probability:

| Rating Difference | Expected Score | Win Probability |
|-------------------|----------------|-----------------|
| 0 | 0.50 | 50% |
| 50 | 0.57 | 57% |
| 100 | 0.64 | 64% |
| 200 | 0.76 | 76% |
| 300 | 0.85 | 85% |
| 400 | 0.91 | 91% |
| 500 | 0.95 | 95% |
| 600 | 0.97 | 97% |

**Formula for any rating difference:**
```
Win_Probability = 1 / (1 + 10^(-ΔR / 400))
```

Where `ΔR = R_A - R_B`

### 5. Two-Player Zero-Sum Property

In a two-player game, the rating changes are equal and opposite:

```
ΔR_A = -ΔR_B
```

This is because:
```
E_A + E_B = 1
S_A + S_B = 1 (for decisive games)
```

Therefore:
```
ΔR_A = K × (S_A - E_A)
ΔR_B = K × (S_B - E_B) = K × ((1 - S_A) - (1 - E_A)) = -K × (S_A - E_A) = -ΔR_A
```

## Comprehensive Example

**Scenario:** Player A (rating 1800) plays Player B (rating 1700), K = 32

**Step 1: Calculate Expected Scores**
```
E_A = 1 / (1 + 10^((1700 - 1800) / 400))
E_A = 1 / (1 + 10^(-0.25))
E_A = 1 / (1 + 0.562)
E_A ≈ 0.64

E_B = 1 - E_A ≈ 0.36
```

**Step 2: Actual Outcome - Player B Wins (upset!)**
```
S_A = 0 (loss)
S_B = 1 (win)
```

**Step 3: Calculate Rating Changes**
```
ΔR_A = 32 × (0 - 0.64) = 32 × (-0.64) = -20.48 ≈ -20
ΔR_B = 32 × (1 - 0.36) = 32 × (0.64) = 20.48 ≈ +20
```

**Step 4: New Ratings**
```
R'_A = 1800 + (-20) = 1780
R'_B = 1700 + 20 = 1720
```

Player B gained 20 points for the upset victory, while player A lost 20 points.

## Multi-Player Extensions

For games with more than two players, the Elo system can be extended:

**Pairwise Comparison Method:**
Each player's rating change is the sum of their changes against all opponents:

```
ΔR_i = K × Σ(S_ij - E_ij)
```

Where:
- `i` = player being rated
- `j` = each opponent
- `S_ij` = actual score against opponent j
- `E_ij` = expected score against opponent j

## Mathematical Properties

**1. Conservation of Rating Points:**
In a closed system with only two-player games, the total rating points remain constant.

**2. Logistic Distribution:**
The expected score formula uses a logistic curve, which creates smooth probability transitions.

**3. Rating Scale Calibration:**
The choice of 400 in the formula means a 400-point difference corresponds to a 10:1 odds ratio (91% vs 9% win probability).

**4. Convergence:**
Over many games, ratings converge toward players' true skill levels, with convergence speed determined by K-factor.

## Implementation Considerations

When implementing Elo ratings:

1. **Initial Ratings:** Typically start players at 1200, 1500, or 1600
2. **Minimum Ratings:** Consider setting a floor (e.g., 100) to prevent negative ratings
3. **Rating Inflation/Deflation:** Monitor average ratings over time
4. **Provisional Periods:** Use higher K-factors for new players
5. **Inactivity Decay:** Consider rating decay for inactive players
6. **Draw Handling:** Use S = 0.5 for both players in draws

## Extensions and Variants

**Glicko and Glicko-2:**
Adds rating deviation (RD) to account for uncertainty:
```
RD² = rating variance (higher = more uncertain)
```

**TrueSkill:**
Microsoft's system using Bayesian inference with skill mean (μ) and skill standard deviation (σ).

**Elo with Home Advantage:**
Add a constant to the home player's rating in expected score calculation:
```
E_home = 1 / (1 + 10^((R_away - (R_home + H)) / 400))
```
Where H is the home advantage (typically 30-100 points).

## References

- Elo, A. E. (1978). *The Rating of Chessplayers, Past and Present*
- FIDE Handbook: Rating Regulations
- Glickman, M. E. (1999). "Parameter estimation in large dynamic paired comparison experiments"
