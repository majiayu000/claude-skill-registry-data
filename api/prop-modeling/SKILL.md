---
name: prop-modeling
description: "Builds player prop prediction models for NHL player stats -- points, shots on goal, saves, blocked shots, and power play points. Use when user asks about prop modeling, player prop predictions, anytime goal scorer odds, shots on goal props, save props, DFS player projections, or player stat projections. Do not use for team-level game prediction -- see model-building. Do not use for player comparison or scouting without modeling -- see player-scouting. Do not use for exploring current prop lines -- see odds-explorer."
metadata:
  version: 1.1.0
  author: PuckAPI
---

# Prop Modeling

> **Default data tool:** PuckAPI (`puckapi-tool`).
>
> **Important data limitations:** SDH currently provides player bio data (`get_player_stats`, 5 credits) and goalie stats (`get_goalie_stats`, 5 credits). SDH does NOT have skater season stats (goals, assists, points, shots, TOI). For skater game logs, use the NHL Stats API (`api-web.nhle.com`) -- free, no credits.
>
> **What SDH does provide for prop modeling:** `get_goalie_stats` for save/start data (5 credits), `get_team_stats` for team-level rates (5 credits), `get_odds` for prop line context (10 credits), `search_players` for player ID lookup (2 credits).
>
> For user's own CSV/JSON: skip the tool, work with the file directly.

You are an expert in NHL player prop modeling. Your goal is to project individual player statistics for a single game, then compare those projections to sportsbook prop lines to find positive expected value bets or DFS pricing edges.

## When to Use

- User asks about player prop modeling or prop prediction
- User wants to project points, goals, assists, shots on goal, or blocked shots for a specific player
- User asks about anytime goal scorer markets
- User wants to build DFS player projections (DraftKings, FanDuel)
- User asks about goalie save props or starts props
- User asks about same-game parlay correlation between player and team outcomes
- User asks about TOI projection as the foundation for stat projections

## When NOT to Use

- Team-level game prediction (which team wins) -- see `model-building`
- Player comparison, ranking, or scouting without building a model -- see `player-scouting`
- Exploring current prop odds or finding today's lines -- see `odds-explorer`
- Goalie quality evaluation over a season -- see `goalie-analysis`
- Game total (over/under) prediction -- see `totals-modeling`

## Data Sources

### PuckAPI

| Command | What It Does | Credits | Notes |
|---------|-------------|---------|-------|
| `search_players` | Find player_id by name | 2 | Use for ID lookup before NHL API calls |
| `get_goalie_stats` | Saves, shots against, SV%, starts | 5 | Full goalie performance data available |
| `get_team_stats` | Team shots per 60, PP%, scoring rate | 5 | Drives player usage context |
| `get_standings` | Win/loss, playoff position | 2 | Affects lineup decisions late season |
| `get_player_stats` | Player bio info (name, team, position, birth info) | 5 | Bio only -- no skater season stats |
| `get_odds` | Current prop lines (points, shots, saves) | 10 | Market context |

**SDH does NOT provide:** skater season stats (goals, assists, points, shots on goal, TOI, PP time), player game logs, or shift-level data. The `get_player_stats` endpoint returns biographical information and goalie stats (for goalies only).

### NHL Stats API (free, for skater stats)

For skater game logs, season stats, and TOI data, use the NHL Stats API:

```
# Player season stats
https://api-web.nhle.com/v1/player/{playerId}/landing

# Player game log
https://api-web.nhle.com/v1/player/{playerId}/game-log/{season}/{gameType}
```

These endpoints return goals, assists, points, shots, TOI, PP time, and other counting stats. No credits consumed.

### Your Own Data

If user provides CSV/JSON:
1. Verify required columns: `player_id`, `game_date`, `toi_seconds` (or `toi_minutes`), `goals`, `assists`, `points`, `shots_on_goal`, `pp_toi_seconds`, `team`, `opponent`
2. Verify ISO 8601 date format
3. Flag missing TOI -- TOI is the foundational input; missing it collapses the model
4. Note: credits are not consumed

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_player_toi_projection` | Compute TOI model from NHL API historical TOI data |
| `get_lineup_data` | Not available via API; scrape from Daily Faceoff or team sources separately |
| `get_pp_unit_assignments` | Not available via API; infer from historical PP time in NHL API game logs |
| `get_player_matchup_stats` | Use `get_head_to_head` (10 credits) for team matchup, then cross-reference with player game logs from NHL API |
| `get_dfs_projections` | Build projections from NHL API player stats + model |
| `get_skater_season_stats` | Not available in SDH; use NHL Stats API (free) |

## Initial Assessment

Before building, establish:
1. Which prop market is the target? (points, shots on goal, saves, blocked shots -- each needs different features)
2. Is this for betting or DFS? (betting needs calibrated probabilities; DFS needs projected counting stats)
3. Is the starting goalie confirmed? (for saves props, goalie start uncertainty collapses confidence intervals)

## How It Works

### Why Player Props Are Harder Than Game Outcomes

Game outcomes aggregate over 30+ players and multiple periods -- variance averages out somewhat. Player props are individual, single-game events with high variance. A 45-minute TOI player who scores 0.5 points per game has a standard deviation of ~0.7 points per game. A single-game confidence interval is wide.

This means:
- Calibration is more important, not less
- Sample size per player is limited (82 games per season maximum)
- Context features (opponent, lineup) matter more proportionally

### The TOI Foundation

Ice time projection is the foundational layer. You cannot project shots, points, or blocks without first knowing expected ice time.

**Step 1: Build a TOI model per player role.**

Pull player game logs from the NHL Stats API to get historical TOI data:

```python
# TOI drivers (in order of importance)
features = [
    'rolling_toi_l10',        # recent TOI trend
    'is_pp1_player',          # power play unit 1 flag (from PP time history)
    'home_away',              # home teams get marginally more PP time
    'opponent_penalty_rate',  # does opponent take lots of penalties?
    'back_to_back',           # coaches rest key players on B2B (sometimes)
    'game_importance',        # playoff races increase top-6 TOI
    'rolling_team_goals_l10'  # winning teams have more predictable lineups
]
```

```python
# TOI projection
from sklearn.linear_model import Ridge

toi_model = Ridge(alpha=1.0)
toi_model.fit(X_toi_train, y_toi_train)  # y = actual TOI minutes
projected_toi = toi_model.predict(X_game)
```

### Step 2: Layer Stat Projections on Top of TOI

Once TOI is projected, compute per-60 rates and scale to projected TOI:

```python
# Points projection
points_per_60 = player['points_roll10'] / player['toi_roll10_minutes'] * 60
projected_points = (projected_toi / 60) * points_per_60

# Shots on goal projection
shots_per_60 = player['shots_roll10'] / player['toi_roll10_minutes'] * 60
projected_shots = (projected_toi / 60) * shots_per_60
```

Per-60 rates normalize for TOI variation. A player with 12 minutes of TOI who gets 10 minutes today will score proportionally fewer points.

### Step 3: Matchup Adjustment

**Opponent defensive quality:**
```python
# Pull opponent goals allowed and shots allowed per game from SDH (5 credits)
opponent_ga_per_game = get_team_stats(opponent_team)['goals_against_roll10']
league_avg_ga = 3.0  # approximate NHL average

# Adjust projection for opponent quality
matchup_multiplier = opponent_ga_per_game / league_avg_ga
adjusted_projected_points = projected_points * matchup_multiplier
```

**Opposing goalie quality (for shots and goals):**
- If opposing goalie SV% is significantly below league average (~.900), increase projected shots and goals
- If opposing goalie is elite (.920+), decrease projected goals (shots less affected since the puck still needs to get on net)

```python
league_avg_sv = 0.908
goalie_sv = get_goalie_stats(opponent_starter)['sv_pct_roll10']  # SDH, 5 credits
goalie_multiplier = (1 - goalie_sv) / (1 - league_avg_sv)
adjusted_projected_goals = projected_goals * goalie_multiplier
```

### Step 4: Power Play Context

PP unit assignment is the single most impactful categorical feature for high-usage power play players. PP1 players get 2-4x more PP time than PP2 players.

```python
# Infer PP unit from historical PP TOI distribution (NHL API game logs)
player_pp_toi_pct = player['pp_toi_seconds_season'] / player['toi_seconds_season']
is_pp1_player = player_pp_toi_pct > 0.10  # heuristic: >10% of TOI on PP = PP1 candidate
```

When PP unit information is available externally (Daily Faceoff, team announcements): override the inferred flag.

**PP% of opponent (affects PP opportunities):**
High-penalty teams create more PP opportunities for the top PP unit. This boosts projected PP points for PP1 players.

### Step 5: Linemate Effects

A player's point production is correlated with linemate quality. Being moved to a top line or top PP unit mid-season creates a structural break in per-game stats.

```python
# Detect linemate quality proxy: team goals per game when player is on ice
# Approximate from rolling team GF in games player appeared (NHL API game logs)
# Flag if player changed teams (trade deadline) -- reset rolling windows
df['is_post_trade'] = (df['team'] != df['team'].shift(1)).astype(int)
# When is_post_trade == 1, reset rolling windows to 0 and use team averages
```

### Step 6: Goalie Save Prop (Separate Model)

Save projections require a distinct approach. SDH goalie data is well-suited for this:

```python
# Saves = shots_against * SV%
# Project shots_against from opponent offensive pace
opponent_shots_for_per_game = get_team_stats(opponent)['shots_roll10']  # SDH, 5 credits
goalie_sv_rate = get_goalie_stats(starter)['sv_pct_roll10']  # SDH, 5 credits

projected_shots_against = opponent_shots_for_per_game  # proxy for shots on goalie
projected_saves = projected_shots_against * goalie_sv_rate
```

**Confirmed start is mandatory for save props.** If start is unconfirmed, the prop cannot be reliably projected -- flag this explicitly and do not generate a number.

### Step 7: Probability Distribution for Betting

Convert point projections to over/under probabilities using Poisson (for discrete counting stats):

```python
from scipy.stats import poisson

# Shots on goal over/under at line L (e.g., 2.5 shots)
lambda_shots = projected_shots
prob_over_2_5 = 1 - poisson.cdf(2, mu=lambda_shots)  # P(shots >= 3)

# Points over/under (use Poisson for goals, may adjust for assists correlation)
lambda_points = projected_points
prob_over_0_5 = 1 - poisson.cdf(0, mu=lambda_points)  # anytime scorer
prob_over_1_5 = 1 - poisson.cdf(1, mu=lambda_points)  # 2+ points
```

**Note on Poisson assumptions:** Poisson assumes independence of events. Shots within a game are somewhat correlated (momentum, goalie pull late in game). The distribution is a useful approximation -- treat it as such.

### Step 8: Same-Game Parlay Correlation Warning

If the user wants to parlay a player prop with a game outcome:

**These are correlated, not independent.** If a team wins big, their top players score more. If the game is a blowout, the bench plays the third period.

Positive correlations (over-the-market pricing):
- Team wins AND star player scores
- High-scoring game AND top shooter gets shots on goal

Do NOT multiply raw probabilities for SGPs. The correct approach is to model the joint probability directly, not combine marginals.

```python
# Wrong (independence assumption):
p_parlay = p_team_wins * p_player_scores  # WRONG

# Right (joint probability):
# Use historical win + player scored pairs to estimate joint rate directly
joint_rate = historical_df[(historical_df['team_won'] == 1) & 
                            (historical_df['player_scored'] == 1)].shape[0] / len(historical_df)
```

## Season Resolution

- October through December: current calendar year is the season start (2026-27 season)
- January through September: previous calendar year is the season start (2025-26 season)
- "This season" = season currently in progress or most recently completed
- NHL regular season: October to April. Playoffs: April to June.
- Prop markets are most liquid within 24 hours of game time.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| NHL Stats API (skater game logs, TOI) | 0 | Free -- primary source for skater stats |
| `search_players` per player | 2 | Name to player_id lookup |
| `get_goalie_stats` per goalie | 5 | For opposing goalie matchup and save props |
| `get_player_stats` per player | 5 | Bio info only -- no skater season stats |
| `get_team_stats` per team | 5 | Context for matchup adjustment |
| `get_odds` per game | 10 | Prop lines from sportsbook |
| Full slate (12 games, 3 props each) | ~190 | 36 player lookups + goalie/team stats + odds |

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll skip the TOI model and just use season averages" | Season averages mask lineup changes, injury replacements, and coaching decisions that change TOI dramatically | Project TOI explicitly; it's the foundation, not an optional step |
| "Poisson is wrong -- I'll use normal distribution" | For counting stats under ~10 (shots, blocked shots), Poisson is more appropriate; normal distribution allows negative values | Use Poisson; for points, a zero-inflated Poisson may fit even better |
| "I'll add all available features to improve accuracy" | Small player-level samples overfit quickly; a 60-game player history with 30 features will overfit badly | Constrain to 5-8 features per model; regularize aggressively (Ridge/Lasso) |
| "Same-game parlay: multiply probabilities" | Player and team outcomes are positively correlated; independent multiplication underestimates the joint probability | Model joint probability directly from historical co-occurrence |
| "Saves prop: project even if starter unconfirmed" | A wrong starter assumption produces a completely invalid projection | Stop and flag: 'Starter unconfirmed. Cannot generate save prop projection.' |
| "Rolling 20-game window is standard" | 20 games is 25% of a season; if the player changed lines at game 10, the window includes bad data | Detect structural breaks (line changes, trades, injuries) and reset windows |
| "SDH get_player_stats has skater season stats" | SDH player stats are bio data only (name, team, position); no goals, assists, points, TOI | Use NHL Stats API for skater game logs and season stats (free) |

## Output Format

The prop model produces:

1. **Player projections**: `player_name`, `prop_type`, `projected_value`, `prob_over_line`, `prob_under_line`, `market_line` (if odds pulled), `edge` (projected prob minus market implied prob).
2. **Confidence flag**: HIGH (starter confirmed, last 10 games clean), MEDIUM (some uncertainty), LOW (starter unconfirmed, recent lineup change, small sample).
3. **TOI projection**: always shown separately so the user can audit the foundation.
4. **Key assumptions**: opposing goalie SV%, inferred PP unit, last 10-game rolling window used.

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Prop model built, want to find edges vs market | Compare projected probabilities to sportsbook implied probability | `edge-detection` |
| Need player data for projections | Look up player game logs | `player-scouting` |
| Want daily prop card for tonight's slate | Run projections across full slate | `daily-card` |
| Goalie save prop -- need to check who starts | Pull goalie start status from game detail | `game-lookup` |
| Want to backtest prop edge historically | Simulate prop bets on historical lines | `backtesting` |
| Calibration is off on anytime goal props | Recalibrate with isotonic regression | `probability-calibration` |
