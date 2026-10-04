---
name: elo-engineering
description: "Builds multi-variant Elo rating systems for sports prediction. Use when user asks about Elo ratings, rating systems, team strength, K-factor, home field advantage, season carryover, margin-of-victory adjustments, or mentions 'Fading Elo', 'Form Elo', 'Component Elo'. Do not use for general feature construction -- see feature-engineering instead. Do not use for team stats without ratings -- see team-analysis instead."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Elo Engineering

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_games` (5 credits) for historical game results to build and update ratings.
> Use `get_team_stats` (5 credits) for goal/score data needed for Component Elo.
> For your own CSV of game results, skip the tool and work with the file directly.

You are an expert in Elo rating system construction for sports prediction. Your goal is to build, tune, and export multi-variant Elo systems that can serve as model features or standalone win probability estimators. PuckCast uses 5 Elo variants as features -- they rank among the most important predictors in the model.

## When to Use

- User wants to build an Elo rating system from scratch
- User wants to add Elo-based features to an existing model
- User asks about K-factor tuning, home advantage, or season regression
- User wants to track team momentum or recent form
- User needs separate offensive/defensive strength ratings

## When NOT to Use

- Adding non-Elo features to a model -- see `feature-engineering`
- Comparing team stats without building ratings -- see `team-analysis`
- Training a full prediction model -- see `model-building`
- Running season simulations -- see `playoff-simulation`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Historical results for building ratings | 5/query |
| `get_team_stats` | Goals for/against for Component Elo | 5/query |
| `get_standings` | Current season context | 2/query |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_elo_ratings` | Build ratings from `get_games` results |
| `get_team_strength` | Use `get_team_stats` + compute Elo |
| `get_historical_ratings` | Rebuild from game logs with carryover |

## Initial Assessment

Before building, establish:
1. Which sport? (determines K-factor, HFA, carryover defaults -- see `parameter-reference.md`)
2. How many seasons of history are available?
3. Single Elo variant or all 5? (all 5 recommended for model features)

## Data Source

**PuckAPI (default):** Use `get_games` with season and league filters. Returns home team, away team, final score, game date.

**Your own data:** Required columns: `game_id`, `date`, `home_team`, `away_team`, `home_score`, `away_score`. Sort ascending by date before processing. Flag games with missing scores -- do not silently drop.

## The 5 Variants

### 1. Standard Elo

The baseline. Ratings update after every game based on expected vs actual outcome.

```
expected_home = 1 / (1 + 10^((away_elo - home_elo - HFA) / 400))
new_home_elo = home_elo + K * MOV_multiplier * (actual - expected_home)
new_away_elo = away_elo + K * MOV_multiplier * ((1 - actual) - (1 - expected_home))
```

- `actual` = 1 (home win), 0 (away win), 0.5 (tie/OT loss handled by sport)
- `HFA` = home field advantage in Elo points (NHL default: 35)
- Initialize all teams at 1500

### 2. Fading Elo

Recent performance weighted more heavily via exponential decay. Useful when teams change significantly mid-season (trades, injuries).

```
weight = exp(-decay_rate * days_since_game)
weighted_K = K * weight
```

- Typical decay rate: 0.003-0.007 (tune via grid search)
- Apply the weighted K in place of standard K during update
- Higher decay = older games matter less

### 3. Form Elo

Short-term momentum. Only the last N games (default N=5, test N=7 and N=10) contribute to the rating. Ratings reset to a baseline each calculation.

**Process:**
1. For each team, take only their last N game results
2. Start from a shared baseline (league average at that date)
3. Apply standard Elo updates in chronological order
4. Output is a "form rating," not cumulative

- Best combined with Standard Elo as a second feature (captures different signal)
- Sensitive to N: run sensitivity across 5/7/10, keep all three in feature set initially

### 4. Component Elo

Separate offense and defense ratings per team. Offensive rating updates based on goals scored vs expected; defensive rating updates based on goals allowed vs expected.

```
expected_goals_for = f(home_off_elo, away_def_elo, HFA_goals)
off_update = K_component * (actual_goals_for - expected_goals_for)
def_update = K_component * (actual_goals_against - expected_goals_against)
```

- Requires goal data: use `get_team_stats` or score columns from `get_games`
- K_component is typically smaller than standard K (NHL: 6-8)
- Outputs 4 ratings per team: home_off, home_def, away_off, away_def
- Combine into win probability: use logistic function on (home_off + away_def) - (away_off + home_def)

### 5. Flat-K Elo

Standard Elo with fixed K-factor -- no margin-of-victory adjustment, no adaptation. Simpler and sometimes competitive when training data is limited.

```
new_elo = elo + K_flat * (actual - expected)
```

- K_flat is constant regardless of score margin
- Use as a baseline sanity check: if your tuned variants don't beat Flat-K, something is wrong
- Tune K_flat separately from Standard K (often 15-25 range)

## Margin-of-Victory Adjustment

Apply to Standard, Fading, and Component variants. Prevents a 5-0 blowout from updating ratings as much as a 5-0 game when the true gap is extreme.

```
MOV_multiplier = ln(abs(score_diff) + 1) * (2.2 / (win_elo_diff * 0.001 + 2.2))
```

- `score_diff` = absolute goal/point difference
- `win_elo_diff` = winner's Elo - loser's Elo before the game
- Cap MOV_multiplier at 1.8 to prevent extreme blowouts from dominating
- Do NOT apply to Form Elo (defeats the purpose of recency weighting)
- Do NOT apply to Flat-K Elo (it's intentionally simple)

## Tuning Process

Grid search to minimize log loss on held-out historical data.

**Parameters to tune (Standard Elo):**
- K-factor: test [5, 10, 15, 20, 25]
- HFA: test [20, 35, 50, 65, 80] (NHL) or sport-appropriate range
- MOV cap: test [1.5, 1.8, 2.0]

**Process:**
1. Train on seasons 1 through N-2
2. Validate on season N-1 (never season N -- future data)
3. Report log loss and Brier score on validation set
4. Pick params with lowest log loss; break ties by Brier score
5. Retrain on seasons 1 through N-1, apply to current season

See `parameter-reference.md` for published starting points by sport.

## Season Carryover

At the start of each new season, blend each team's end-of-season rating toward 1500 (league mean). This accounts for roster turnover and regression to the mean.

```
new_season_elo = carryover * end_elo + (1 - carryover) * 1500
```

- NHL carryover: 0.88 (12% regression)
- Higher regression for sports with more offseason change (see `parameter-reference.md` for other sports)

**Expansion teams:** Initialize at 1380-1400 (below mean) to reflect unknown quality.

## Season/Date Logic

- Process games in strict chronological order. Never process future games.
- "Current ratings" = ratings as of yesterday, using games through yesterday only
- When building features for a model: rating used for game on date D must be computed from games through D-1 (no leakage)
- Off-season: ratings stay frozen at end-of-season values until carryover is applied on opening day

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "Initialize all teams at 1000 for simplicity" | Scale doesn't matter, but 1500 is conventional and matches published benchmarks you'll want to compare against | Use 1500. Deviation gains nothing. |
| "Use the same K for all sports" | NHL teams play 82 games; other sports have very different schedules. K must reflect game frequency and score variance. | Use sport-specific defaults in parameter-reference.md. Tune from there. |
| "Skip MOV adjustment to keep it simple" | Without MOV, a 6-1 blowout and a 2-1 win shift ratings identically. Signal is lost. | Implement the logarithmic MOV multiplier. It's 3 lines of code. |
| "One Elo variant is enough" | PuckCast's feature importance shows each variant captures different signal. Standard and Form are often the top two features. | Build all 5. Use feature selection to prune later if needed. |
| "Don't regress ratings between seasons" | A team that went 60-22 in 2023 is not the same team in 2024. Over-confident carry-forward pollutes predictions. | Apply carryover. NHL uses 0.88 -- 12% regression. Other sports regress even more. |
| "Use end-of-season ratings for next season's opening day" | Without regression, teams that had lucky seasons (high PDO) stay overrated. | Apply carryover formula on day 1 of the new season. |

## Output Format

For each variant, produce a ratings table:

```
team         | elo_standard | elo_fading | elo_form | elo_off | elo_def | elo_flat | as_of_date
-------------|-------------|------------|----------|---------|---------|----------|----------
Buffalo Sabres| 1487.3      | 1491.2     | 1502.1   | 1495.6  | 1478.9  | 1489.1   | 2026-05-01
Toronto Leafs | 1534.8      | 1529.4     | 1518.7   | 1541.2  | 1528.3  | 1532.0   | 2026-05-01
```

For model features: output as one row per game with home/away ratings as of game date.

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Elo variants built, ready to add to model | Combine with other features | `feature-engineering` |
| Ratings built, want a full model | Train on Elo + other features | `model-building` |
| Model trained, need to verify calibration | Check probability output quality | `probability-calibration` |
| Want to simulate playoff bracket | Use Elo to seed simulations | `playoff-simulation` |
| Elo accuracy unclear | Backtest against market odds | `backtesting` |
