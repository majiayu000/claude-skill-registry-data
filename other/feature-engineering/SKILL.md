---
name: feature-engineering
description: "Transforms raw game, player, and goalie data into model-ready features with built-in leakage detection. Use when user asks about feature construction, rolling windows, home/away splits, SOS adjustment, goalie features, Elo as features, or opponent-adjusted metrics. Strictly enforces .shift(1) before any rolling calculation. Do not use for raw data exploration -- see game-lookup or team-analysis. Do not use for understanding hockey metrics -- see hockey-analytics. Do not use for xG feature construction -- see xg-model-building."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Feature Engineering

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_games` for game results (5 credits), `get_team_stats` for team-level stats (5 credits), `get_goalie_stats` for goalie data (5 credits).
> For user's own CSV/JSON: skip the tool, work with the file directly -- no credits consumed.

You are an expert in sports feature engineering. Your goal is to construct model-ready features from raw sports data while guaranteeing zero temporal leakage. This is where 80% of beginners fail.

## When to Use

- User wants to prepare data for a prediction model
- User asks about rolling windows, moving averages, or recent form metrics
- User asks about home/away splits, rest-day features, or back-to-backs
- User asks about strength-of-schedule adjustment
- User asks about goalie quality features (SV%, GSAA, recent form)
- User asks how to incorporate Elo ratings as model features
- User asks about opponent-adjusted metrics

## When NOT to Use

- Raw data exploration (looking up scores, stats) -- see `game-lookup` or `team-analysis`
- Understanding what Corsi, Fenwick, or PDO mean -- see `hockey-analytics`
- Building expected goals (xG) features specifically -- see `xg-model-building`
- Training or evaluating the model itself -- see `model-building` and `walk-forward-validation`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Historical game results for rolling calculations | 5 |
| `get_team_stats` | Season and split team stats | 5 |
| `get_goalie_stats` | Starter SV%, GSAA, recent starts | 5 |
| `get_head_to_head` | Head-to-head history for matchup features | 10 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_team_rolling_stats` | Compute rolling stats manually from `get_games` results |
| `get_sos` | Compute iterative SOS from `get_standings` + `get_team_stats` |
| `get_rest_days` | Compute from game date sequences in `get_games` output |
| `get_goalie_recent_form` | Compute from `get_goalie_stats` with manual window |

## Data Source

**PuckAPI (default):** Pull historical game log via `get_games` for the team and date range needed. Sort ascending by date before any calculation.

**Your own data:** If user provides CSV/JSON:
1. Verify required columns: `game_date`, `home_team`, `away_team`, result columns, and stat columns
2. Verify ISO 8601 date format (YYYY-MM-DD)
3. Flag missing rows -- do not silently drop
4. Note: credits are not consumed

## Initial Assessment

Before building features, establish:
1. What is the prediction target? (win/loss, goal differential, over/under)
2. What data is available? (game logs, team stats, player/goalie data)
3. What historical depth is available? (seasons of data determines valid window sizes)

## How It Works

### Step 0: Establish Temporal Ordering

Sort all data ascending by `game_date`. This is non-negotiable. Every calculation that follows depends on correct order. Verify sort before proceeding.

### Step 1: Apply `.shift(1)` Before ANY Rolling Calculation

**The single most important rule in this skill.**

For every stat column that will enter a rolling window:
```python
df['stat_shifted'] = df.groupby('team_id')['stat'].shift(1)
```

This ensures game N uses only games 1 through N-1. Without `.shift(1)`, game N includes its own outcome in its own feature -- that is leakage.

Even season-level aggregate stats must be lagged. If you join season stats as a static feature, those season stats include the current game's outcome. Lag them.

### Step 2: Rolling Window Statistics

Compute rolling windows at multiple sizes. The "right" window is an empirical question, not a convention.

Required windows to test: **5, 10, 20, 40, 82 games**

```python
for window in [5, 10, 20, 40, 82]:
    df[f'goals_for_roll{window}'] = (
        df.groupby('team_id')['goals_for_shifted']
        .transform(lambda x: x.rolling(window, min_periods=window//2).mean())
    )
```

Run sensitivity analysis: does the model's walk-forward accuracy change meaningfully when you swap window sizes? If 5-game and 20-game produce similar accuracy, prefer the shorter window (less data required, works earlier in season). Document which window was chosen and why.

### Step 3: Home/Away Splits and Rest-Day Features

Compute all features separately for home context and away context. A team's road performance is a different signal than home performance.

**Rest-day feature:**
```python
df['rest_days'] = df.groupby('team_id')['game_date'].diff().dt.days - 1
df['back_to_back'] = (df['rest_days'] == 0).astype(int)
df['rest_bucket'] = pd.cut(df['rest_days'], bins=[-1, 0, 1, 2, 99],
                            labels=['b2b', '1day', '2day', '3plus'])
```

Back-to-backs carry measurable performance impact in NHL (PuckCast: ~1.5 percentage point win rate drop). Always include.

### Step 4: Strength of Schedule Adjustment (Iterative)

Simple opponent win% is not SOS. It double-counts easy schedules. Use iterative SOS:

1. Initialize each team's strength rating as their win%
2. Each team's SOS = mean(opponents' current strength ratings)
3. Each team's adjusted rating = f(own record, SOS)
4. Repeat steps 2-3 until ratings converge (typically 10-20 iterations)

Do NOT use simple opponent win% as SOS. It underestimates the difficulty of facing strong opponents who themselves faced strong opponents.

Pull opponent records via `get_standings`. Recompute per-fold in walk-forward validation -- never use full-season SOS as a feature (that leaks final standings into early-season predictions).

### Step 5: Goalie Quality Features

Goalie variance is the single largest source of randomness in NHL game outcomes. Features:

- **Starter SV%** (season to date, lagged): from `get_goalie_stats`
- **Recent form SV%** (last 5 starts, lagged): rolling on starts, not games
- **GSAA (Goals Saved Above Average)** (season to date, lagged): measures goalie quality net of shot quality
- **Confirmed starter flag**: 1 if starter announced, 0 if uncertain

```python
# GSAA formula: (league_avg_sv_pct - goalie_sv_pct) * shots_faced_against
# Negative GSAA = goalie is below average (worse than expected)
```

### Step 6: Elo Ratings as Features

Reference `elo-engineering` skill for Elo calculation details. As a feature input:

- Use **pre-game Elo** (before the game's result updates the rating)
- Elo difference (home_elo - away_elo) is often more predictive than raw Elo values
- Elo captures recent form implicitly -- no need to separately include win streak if Elo is in the model

### Step 7: Opponent-Adjusted Metrics

Raw goals-for is partially a function of opponent quality. Subtract opponent average:

```python
df['adj_goals_for'] = df['goals_for_roll10'] - df['opp_goals_against_roll10']
```

This isolates the team's contribution from the matchup context. PuckCast uses home-minus-away differences for all 158 features -- this encodes opponent context directly.

### Step 8: Construct Home-Minus-Away Differences

For matchup prediction, compute the difference between home team feature and away team feature:

```python
df['goal_diff_feature'] = df['home_goals_for_roll10'] - df['away_goals_for_roll10']
```

All features become single signed values. This reduces dimensionality by half and encodes matchup context directly. PuckCast proved this representation across 158 features.

### Step 9: Leakage Audit

Before handing features to `model-building`, audit every feature:

1. Does it use data from the game being predicted? -> Leakage
2. Does it use data from after the game being predicted? -> Leakage
3. Was `.shift(1)` applied before any rolling calculation? -> If no, leakage
4. Were season-level stats lagged? -> If no, leakage

See `feature-catalog.md` for the full recommended feature list with leakage risk ratings.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_games` per season | 5 | Pull full season game log |
| `get_team_stats` | 5 | Season splits per team |
| `get_goalie_stats` | 5 | Per goalie per season |
| Full NHL season feature build | ~475 | 32 teams * 5 (stats) + 32 * 5 (goalies) + games |

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "k-fold is fine for feature selection" | k-fold on time series leaks future folds into training, inflating feature importance scores by 5-15% | Use walk-forward fold structure for all feature selection |
| "40-game window is standard" | 40 is arbitrary; the right window depends on your data | Test 5/10/20/40/82 windows, report sensitivity, pick empirically |
| "Elo is redundant with rolling win%" | Elo updates after every game and weights recent games more; win% is equally weighted across the season | Include Elo; it captures momentum that win% misses |
| "Don't need .shift(1) for season-level stats" | Season stats include the current game's outcome; that is leakage | Lag every stat, including season-level aggregates |
| "I'll add shift(1) at the end" | Rolling windows applied before shift include game N in game N's feature | Shift first, then roll. Order is not flexible. |
| "Opponent win% is a fine SOS proxy" | Simple opponent win% double-counts easy schedules | Use iterative SOS -- run convergence loop on opponent ratings |
| "More features can't hurt" | More features increase overfitting risk in small sports datasets | Use feature importance from walk-forward folds to prune aggressively |
| "I'll just use this season's stats for the whole season" | Future games in the season leak into early-season features | Rebuild SOS and aggregate stats per fold in walk-forward |

## Output Format

Feature engineering produces:

1. **Feature matrix** (`X`): rows = games, columns = home-minus-away feature differences. All numeric. No nulls (handle early-season NaN with fill strategy: season average or 0 with a "sufficient data" flag column).
2. **Target vector** (`y`): 1 = home win, 0 = away win. For totals modeling: total goals.
3. **Game index**: game_id and game_date for temporal sorting in walk-forward splits.
4. **Feature audit log**: each feature name, window size, shift applied (Y/N), leakage risk (from catalog).

Hand this output directly to `walk-forward-validation` or `model-building`.

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Features built, need to evaluate a model | Validate with temporal splits | `walk-forward-validation` |
| Features built, ready to train | Train with walk-forward methodology baked in | `model-building` |
| Suspect a feature has leakage | Audit shift/roll order, check leakage risk in catalog | `feature-engineering` (re-run Step 9) |
| Want to add Elo as a feature | Build Elo ratings first | `elo-engineering` |
| Want expected goals features | xG requires shot-level data and a separate process | `xg-model-building` |
| Features look good, want to backtest a strategy | Backtesting adds bankroll simulation on top | `backtesting` |
