---
name: xg-model-building
description: "Builds expected goals (xG) models from NHL play-by-play shot event data using XGBoost or LightGBM. Use when user asks about expected goals, xG model, shot quality, building an xG model, xGF%, xGA, rebound detection, rush shot detection, or shot probability. Do not use for applying pre-built xG values to team or game analysis -- see team-analysis or hockey-analytics. Do not use for general game prediction models -- see model-building. Do not use for goalie evaluation using xGA -- see goalie-analysis."
metadata:
  version: 1.1.0
  author: PuckAPI
---

# xG Model Building

> **Important: PuckAPI does NOT have play-by-play data.** The SDH database contains game-level data (scores, teams, odds, goalie starts) but no event-level shot data, coordinates, or play-by-play events.
>
> **Primary data source for xG:** The NHL Stats API at `api-web.nhle.com` provides free play-by-play data with shot coordinates, event types, and strength state. No API key or credits required.
>
> **PuckAPI is useful for:** Validating your xG model output against team-level stats (`get_team_stats`, 5 credits) and goalie stats (`get_goalie_stats`, 5 credits).
>
> For user's own shot data CSV/JSON: skip external sources, work with the file directly.

You are an expert in hockey expected goals modeling. Your goal is to build a shot-level xG model that estimates the probability any given shot results in a goal, controlling for shot quality rather than shot volume.

## When to Use

- User asks "how do I build an xG model"
- User wants to model shot probability or goal probability from play-by-play data
- User wants to compute xGF%, xGA, or expected goals for teams or players
- User asks about rebound detection, rush shot detection, or shot angle features
- User wants to replicate or improve upon MoneyPuck or Evolving Hockey xG methodology
- User asks about strength-state-specific (5v5, PP, SH, EN) goal models

## When NOT to Use

- Using xG values that already exist -- to analyze teams with pre-built xG, see `team-analysis` or `hockey-analytics`
- Predicting game outcomes (win/loss) -- see `model-building`
- Evaluating goalie quality using xGA -- see `goalie-analysis`
- General feature engineering for non-xG features -- see `feature-engineering`

## Data Sources

### NHL Stats API (primary, free)

The NHL Stats API provides play-by-play event data for every game:

```
https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play
```

Each play-by-play response includes shot events with:
- Event type (SHOT, GOAL, MISS, BLOCK)
- x/y coordinates (NHL coordinate system, feet, center ice = 0,0)
- Shot type (wrist, slap, snap, backhand, tip, deflection, wrap-around)
- Strength state (5v5, PP, SH, EN)
- Period and game time
- Shooter and goalie IDs

This is the same data that MoneyPuck and Evolving Hockey use. No credits consumed.

### PuckAPI (validation only)

SDH endpoints useful for validating your xG model output:

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_team_stats` | Team-level shot and goal summaries (compare your xGF% to team performance) | 5 |
| `get_goalie_stats` | Goalie save totals (for xGA validation) | 5 |
| `get_games` | Game list to get game IDs for NHL API play-by-play pulls | 5 |

SDH does NOT provide: play-by-play events, shot coordinates, event types, shot-level data.

### Your Own Data

If user provides CSV/JSON:
1. Verify required columns: `x_coord`, `y_coord`, `shot_type`, `strength_state`, `period`, `game_seconds`, `event_type` (SHOT/GOAL/MISS/BLOCK), `shooter_id`, `goalie_id`
2. Verify coordinate system is consistent (NHL uses feet, center ice = 0,0)
3. Flag missing coordinates -- do not silently drop
4. No credits consumed

## Commands That Do NOT Exist (in PuckAPI)

| Not Available in SDH | Where to Get It |
|---------------------|-----------------|
| Play-by-play events | NHL Stats API (`api-web.nhle.com`) -- free |
| Shot coordinates | NHL Stats API -- free |
| Shot event types | NHL Stats API -- free |
| Pre-computed xG values | Build the model yourself, or reference MoneyPuck/Evolving Hockey |
| Bulk shot coordinate export | Pull NHL API per game and aggregate |

## Initial Assessment

Before building, establish:
1. What is the data source? (NHL Stats API free, or user's own data)
2. How many seasons? (1 season minimum; 3+ seasons produces more stable coefficients)
3. What is the end use? (team-level xGF%, player-level scoring, goalie evaluation -- determines how to aggregate shot-level predictions)

## How It Works

### Step 1: Collect Shot Events

Pull play-by-play from the NHL Stats API and filter to shot events:
- `SHOT` (on goal, saved)
- `GOAL`
- `MISS` (missed net)
- `BLOCK` (blocked before reaching goalie)

Set target: `is_goal = 1` if event_type is GOAL, else 0.

**Important:** Include blocked shots in the model but treat them carefully -- some public models exclude blocks (MoneyPuck excludes, Evolving Hockey includes). Document the choice.

### Step 2: Compute Core Features

See `xg-features.md` for the complete feature table with formulas. Core features:

**Location:**
- `shot_distance`: Euclidean distance from shot coordinates to net center
- `shot_angle`: Absolute angle from net-center axis

**Shot type:** One-hot encode: wrist, slap, snap, backhand, tip, deflection, wrap-around. Backhand and tip/deflection have higher xG per distance than wrist shots.

**Strength state:** One-hot encode: 5v5, PP, SH, EN. Train separate models per strength state (Step 4).

**Time context:**
- `seconds_since_last_event`: time elapsed since the prior event
- `distance_from_last_event`: Euclidean distance between shot coordinates and prior event coordinates

### Step 3: Derive Rebound and Rush Features

These are the features that separate public xG models from naive distance-only models.

**Rebound detection:**
```python
df['is_rebound'] = (
    (df['seconds_since_last_event'] < 3) &
    (df['last_event_type'].isin(['SHOT', 'GOAL', 'MISS']))
).astype(int)
```

**Rush detection (zone entry proxy):**
```python
df['is_rush'] = (
    (df['seconds_since_last_event'] < 4) &
    (df['distance_from_last_event'] > 30)  # feet -- large spatial jump = transition
).astype(int)
```

**Shot angle change rate (MoneyPuck's "shotAnglePlusReboundSpeed"):**
```python
df['rebound_angle_speed'] = df['is_rebound'] * df['shot_angle_change'] / df['seconds_since_last_event'].clip(lower=0.1)
```

### Step 4: Train Separate Models Per Strength State

Train four separate XGBoost (or LightGBM) classifiers:
1. **5v5** (largest sample, most stable)
2. **PP** (power play -- angle matters more, distance less because shots cluster high slot)
3. **SH** (shorthanded -- small sample, may need regularization)
4. **EN** (empty net -- high conversion; EN shots are nearly deterministic by distance)

```python
from xgboost import XGBClassifier

models = {}
for state in ['5v5', 'PP', 'SH', 'EN']:
    subset = df[df['strength_state'] == state]
    X = subset[FEATURE_COLS]
    y = subset['is_goal']
    models[state] = XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='logloss',
        random_state=42
    )
    models[state].fit(X, y)
```

### Step 5: Evaluate the Model

**Shot-level evaluation:**
- **Brier score**: lower is better. A distance-only logistic baseline scores ~0.055. A good xG model scores ~0.048-0.050.
- **Calibration curve**: plot predicted xG decile vs actual goal rate. A well-calibrated model's curve should lie on the diagonal.
- **Log loss**: compare to public benchmarks.

**Team-level validation:**
```python
# Sum shot-level xG per team per game -- compare to actual goals
df['xg'] = df.apply(lambda r: models[r['strength_state']].predict_proba([r[FEATURE_COLS]])[0][1], axis=1)
team_xg = df.groupby(['game_id', 'team'])['xg'].sum()
```

Compare `xGF/xGA` per team against public values from MoneyPuck or Evolving Hockey. Correlation should exceed 0.85.

You can also validate against SDH team stats: pull `get_team_stats` (5 credits) to compare your team-level xG aggregates against the xG values in the standings data.

### Step 6: Aggregate to Team Level

```python
# xGF% (5v5 only -- standard)
xg_5v5 = df[df['strength_state'] == '5v5'].groupby(['game_id', 'team'])['xg'].sum()
team_xgf_pct = xg_5v5 / (xg_5v5.groupby('game_id').transform('sum'))
```

`xGF%` is the primary team-level output. Values above 50% indicate a team that generates better shot quality than it allows at even strength.

## Season Resolution

- October through December: current calendar year is the season start (e.g., 2026-27 season)
- January through September: previous calendar year is the season start (e.g., 2025-26 season)
- "This season" = season currently in progress or most recently completed
- NHL regular season: October to April. Playoffs: April to June.
- Play-by-play is available within hours of game completion.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| NHL Stats API play-by-play | 0 | Free -- no credits consumed |
| Full NHL regular season PBP | 0 | ~1,312 game API calls, all free |
| `get_team_stats` (validation) | 5 | Compare your xGF% to SDH team stats |
| `get_goalie_stats` (validation) | 5 | Compare your xGA to SDH goalie stats |
| `get_games` (get game IDs) | 5 | Pull game list, then use IDs for NHL API |

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "One model for all strength states is simpler" | PP and SH have fundamentally different shot distributions; a combined model learns the average and is wrong for both | Train separate models per strength state |
| "Distance alone is good enough" | Distance-only models miss rebound and rush context, which account for ~15% of xG variance | Include rebound flag and rush flag at minimum |
| "k-fold cross-validation is fine for shot data" | Shots within a game are correlated; k-fold leaks game-level context across folds | Group k-fold by game_id or season |
| "Blocked shots should be included the same as saved shots" | Blocked shots are a different event with different outcome distribution; mixing them without a flag distorts calibration | Either exclude blocks or include a `is_blocked` indicator |
| "I'll validate against total goals only" | Total goals validation misses calibration problems at the shot level | Validate Brier score at shot level AND team-level xGF% correlation |
| "Screen/traffic data isn't available so skip it" | Acknowledging the gap is correct -- just document it as a known model limitation | Note it as a known gap; NHL EDGE tracking may expose it in future data |
| "I'll use PuckAPI get_game_detail for shot data" | SDH has game-level data only (scores, odds, goalies) -- no play-by-play or shot coordinates | Use the NHL Stats API for play-by-play data (free) |

## Output Format

The xG model produces:

1. **Shot-level xG values**: DataFrame with `game_id`, `event_id`, `shooter_id`, `team`, `strength_state`, `xg` (float 0-1), and all computed features.
2. **Team-game xG aggregates**: `xGF` and `xGA` per team per game per strength state.
3. **Season xGF%** (5v5): one value per team, used as input to `team-analysis` or `feature-engineering`.
4. **Model artifacts**: serialized XGBoost models per strength state (`.pkl` or `.json`), feature names, and Brier score per strength state.
5. **Calibration report**: predicted vs actual goal rate by decile for each strength state model.

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| xG model built, want to use it as a prediction model feature | Add xGF% as a lag feature | `feature-engineering` |
| Team xGF% computed, want to analyze team quality | Use xGF% alongside Corsi and PDO | `team-analysis` |
| Goalie xGA computed, want to evaluate goalie quality | xGA is the input to GSAA calculation | `goalie-analysis` |
| Model is built, want to find betting edges using xG | Compare xG-implied win probability vs market odds | `edge-detection` |
| Want to validate the model with proper temporal splits | Hold out full seasons for out-of-sample testing | `walk-forward-validation` |
| Calibration curve is off | Recalibrate probabilities with isotonic regression or Platt scaling | `probability-calibration` |
