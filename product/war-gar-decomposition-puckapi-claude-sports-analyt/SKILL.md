---
name: war-gar-decomposition
description: "Builds WAR (Wins Above Replacement) and GAR (Goals Above Replacement) from scratch using RAPM ridge regression on shift-level data. Use when user asks about WAR, GAR, RAPM, player value metrics, wins above replacement, contract surplus value, JFresh-style player cards, or all-in-one player evaluation. Do not use for simple player stats lookup -- see player-scouting. Do not use for goalie evaluation -- goalies use GSAA not WAR, see goalie-analysis. Do not use for team-level performance -- see team-analysis."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# WAR/GAR Decomposition

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_game_detail` for game-level data (10 credits per game) and `get_player_stats` for player biographical data (5 credits).
> Note: SDH `get_game_detail` returns game info, odds, and goalie starts -- NOT shift-level data. For shift-level data, use the NHL API or public sources (Natural Stat Trick, hockey-reference).
> Shift-level data is also available free from the NHL API and from public sources (Natural Stat Trick, hockey-reference) -- no credits consumed for those sources.
> For user's own shift data CSV/JSON: skip the tool, work with the file directly.

You are an expert in advanced hockey player evaluation. Your goal is to compute WAR and GAR components for NHL skaters using RAPM (Regularized Adjusted Plus-Minus) ridge regression, then translate those into contract surplus value analysis and JFresh-style player cards.

## When to Use

- User asks about WAR, GAR, RAPM, or wins above replacement for hockey players
- User wants to evaluate player value beyond box score stats
- User asks about contract surplus value or cap efficiency
- User wants to reproduce or extend Evolving Hockey's WAR/GAR methodology
- User wants to build a JFresh-style player card (radar chart of GAR components)
- User asks about regularized adjusted plus-minus or ridge regression for player evaluation

## When NOT to Use

- Simple player stats lookup without modeling -- see `player-scouting`
- Goalie evaluation -- goalies use GSAA (Goals Saved Above Average), not WAR. See `goalie-analysis`
- Team-level performance and standings analysis -- see `team-analysis`
- Game prediction or betting models (WAR is a player evaluation metric, not a game prediction feature directly) -- see `model-building` or `feature-engineering`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_game_detail` | Game metadata, team info, odds records, and goalie starts | 10 |
| `get_games` | Game list for bulk shift data pulls | 5 |
| `get_player_stats` | Player biographical data, salary reference | 5 |
| `get_team_stats` | Team-level validation of RAPM outputs | 5 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_shift_data` | Use the NHL API or public sources (Natural Stat Trick, hockey-reference) for shift-level data |
| `get_rapm` | No pre-computed RAPM. Run the ridge regression yourself |
| `get_war` | No pre-computed WAR. Compute from GAR components |
| `get_player_contract` | Pull AAV from CapFriendly or PuckPedia externally; not in PuckAPI |
| `get_on_ice_stats` | Use the NHL API or public sources for on-ice data; not available in PuckAPI |

## Data Source

**PuckAPI:** `get_game_detail` returns game metadata, team info, odds records, and goalie starts -- NOT shift-level data. For the shift-level data required by RAPM, use the NHL API or public sources below.

**Free alternatives (recommended for volume):**
- Natural Stat Trick (`naturalstattrick.com`): exports on-ice data by player, season, strength state. No credits.
- Hockey Reference (`hockey-reference.com`): player game logs. No credits.
- Evolving Hockey (`evolving-hockey.com`): publicly posts GAR component values for validation. No credits.

**Your own data:** If user provides shift-level CSV:
1. Verify required columns: `game_id`, `player_id`, `is_home` (binary), `strength_state`, `shift_duration_seconds`, `goals_for`, `goals_against`, `corsi_for`, `corsi_against`, `xg_for`, `xg_against`
2. Verify each row represents one player's contribution to one shift
3. Flag missing strength state -- RAPM must be run separately per state
4. Note: credits are not consumed

## Initial Assessment

Before building, establish:
1. What is the target metric? (raw GAR components, total WAR, or contract surplus value?)
2. How many seasons of data? (1 season produces noisy RAPM estimates; 3+ seasons produces stable values)
3. What is the end use? (player comparison, contract analysis, player card visualization)

## How It Works

### RAPM: The Foundation

RAPM (Regularized Adjusted Plus-Minus) is ridge regression at the shift level. It answers: "Controlling for every other player on the ice, how many more goals (or Corsi events, or xG) occurred per 60 minutes when this player was on ice?"

See `war-components.md` for the full mathematical formulation. The mechanism:

**Matrix construction:**
- Each row = one shift
- Columns = one column per player in the league (positive for home players, negative for away players)
- Target = outcome rate for that shift (goals/60, Corsi/60, or xG/60)

```python
# Simplified structure
# X: sparse matrix, shape (n_shifts, n_players)
# y: outcome per 60 for each shift (goals differential, weighted by shift duration)
# Ridge regression: beta = (X'X + lambda*I)^-1 X'y

from sklearn.linear_model import Ridge

rapm_model = Ridge(alpha=2500)  # regularization parameter; see war-components.md for selection
rapm_model.fit(X_shifts, y_goals_per_60, sample_weight=shift_durations)
player_rapm = dict(zip(player_ids, rapm_model.coef_))
```

The ridge penalty (alpha) shrinks each player's coefficient toward zero. This is necessary because players with limited ice time have too little data to produce stable estimates -- regularization pulls them toward the league mean.

### Step 1: Prepare the Shift Matrix

For each game, expand shift records into the player-indicator matrix:

```python
import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix

n_players = len(all_player_ids)
player_to_col = {pid: i for i, pid in enumerate(all_player_ids)}

X = lil_matrix((n_shifts, n_players))
for shift_idx, shift in enumerate(shifts):
    for player_id in shift['home_players']:
        col = player_to_col[player_id]
        X[shift_idx, col] = 1  # home = positive
    for player_id in shift['away_players']:
        col = player_to_col[player_id]
        X[shift_idx, col] = -1  # away = negative

X = X.tocsr()  # convert to compressed sparse row for Ridge
```

Target vector `y`:
```python
y = (shift['goals_for'] - shift['goals_against']) / shift['shift_duration_seconds'] * 3600  # goals per 60
sample_weight = shift['shift_duration_seconds']  # longer shifts weighted more
```

### Step 2: Run RAPM Per Strength State and Target

Run separate regressions for each combination:

| GAR Component | Strength State | Target | Public Model Equivalent |
|---------------|---------------|--------|------------------------|
| EV Offense | 5v5 | xGF per 60 | Evolving Hockey EVO |
| EV Defense | 5v5 | xGA per 60 (inverted) | Evolving Hockey EVD |
| PP Contribution | PP (5v4, 5v3) | xGF per 60 | Evolving Hockey PPO |
| PK Contribution | SH (4v5, 3v5) | xGA per 60 (inverted) | Evolving Hockey PKD |
| Penalties Drawn | All states | PD per 60 | Evolving Hockey PD |
| Penalties Taken | All states | PT per 60 (inverted) | Evolving Hockey PT |

```python
components = {}
for component, state, target_col in component_specs:
    state_mask = shifts['strength_state'] == state
    X_state = X[state_mask]
    y_state = shifts[target_col][state_mask]
    w_state = shifts['shift_duration'][state_mask]
    
    model = Ridge(alpha=ALPHA_BY_STATE[state])
    model.fit(X_state, y_state, sample_weight=w_state)
    components[component] = dict(zip(player_ids, model.coef_))
```

### Step 3: Aggregate to Total GAR

Sum the components for each player. Weight each component by its contribution to actual goals (derived from regression against actual goals per 60):

```python
# GAR = weighted sum of components
# Weights vary slightly by model; Evolving Hockey weights are public
EV_O_WEIGHT = 1.0   # reference weight
EV_D_WEIGHT = 1.0
PP_WEIGHT   = 0.65  # PP time is partial; adjust by average PP fraction
PK_WEIGHT   = 0.35
PD_WEIGHT   = 0.15
PT_WEIGHT   = -0.15

player_gar = (
    EV_O_WEIGHT * gar['ev_offense'] +
    EV_D_WEIGHT * gar['ev_defense'] +
    PP_WEIGHT   * gar['pp_contribution'] +
    PK_WEIGHT   * gar['pk_contribution'] +
    PD_WEIGHT   * gar['penalties_drawn'] +
    PT_WEIGHT   * gar['penalties_taken']
)
```

### Step 4: Convert GAR to WAR

Use the Pythagorean expectation relationship between goals and wins:

```python
# NHL Pythagorean exponent ≈ 2.15 (empirically derived)
# At league-average scoring (≈3.0 GF, 3.0 GA per game):
# dW/dG = Pythagorean derivative at league average

PYTH_EXP = 2.15
LEAGUE_AVG_GF = 3.0  # goals per game
GOALS_PER_WAR = 6.0  # empirically ~6 goals = 1 win in NHL

player_war = player_gar / GOALS_PER_WAR
```

See `war-components.md` for the full derivation of `goals_per_war` and comparison to Evolving Hockey's published conversion.

### Step 5: Contract Surplus Value

```python
MARKET_RATE_PER_WAR = 1_400_000  # ~$1.4M per WAR (2025-26 market rate)

# Pull AAV from external source (CapFriendly / PuckPedia)
player_aav = external_salary_lookup(player_id)

# Project WAR over contract remaining
contract_years_remaining = 3  # from contract data
projected_war_total = player_war * contract_years_remaining

# Surplus value
market_value = projected_war_total * MARKET_RATE_PER_WAR
surplus_value = market_value - (player_aav * contract_years_remaining)
# Positive surplus = underpaid relative to production. Negative = overpaid.
```

**Important:** WAR is a current-season metric. Projecting it forward assumes constant production, which is wrong for aging players. Apply an aging curve adjustment for players 32+:

```python
age_adjustment = {30: 0.95, 31: 0.90, 32: 0.83, 33: 0.75, 34: 0.65}
adjusted_war = player_war * age_adjustment.get(player_age, 1.0)
```

### Step 6: Player Card Output (JFresh-Style)

A JFresh-style player card shows the component breakdown on a radar chart. Six axes: EV Offense, EV Defense, PP, PK, Penalties Drawn, Penalties Taken. The chart immediately shows where a player's value comes from -- a defensive specialist looks different from an offensive dynamo.

```python
import matplotlib.pyplot as plt
import numpy as np

components_normalized = {  # normalize to percentile rank across league
    'EV Offense': percentile_rank(player_gar['ev_offense']),
    'EV Defense': percentile_rank(player_gar['ev_defense']),
    'PP': percentile_rank(player_gar['pp_contribution']),
    'PK': percentile_rank(player_gar['pk_contribution']),
    'Pen Drawn': percentile_rank(player_gar['penalties_drawn']),
    'Pen Taken': percentile_rank(player_gar['penalties_taken'])
}
# Radar chart: axes are percentile 0-100, 50 = league average
```

See `visualization` skill for full chart template.

## Season Resolution

- October through December: current calendar year is the season start (2026-27 season)
- January through September: previous calendar year is the season start (2025-26 season)
- "This season" = season currently in progress or most recently completed
- WAR/GAR require a minimum of 200-300 minutes of ice time for stable estimates (roughly 20-25 games)
- NHL regular season: October to April. Playoffs excluded from standard WAR calculation.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_game_detail` per game | 10 | Game metadata, odds, and goalie starts per game |
| Full NHL regular season | ~13,120 | 1,312 games x 10 credits per game |
| `get_player_stats` | 5 | Per player biographical lookup |
| Free alternative (Natural Stat Trick) | 0 | Recommended for historical volume |

**Practical recommendation:** Use the free NHL/Natural Stat Trick data sources for historical RAPM building. Reserve PuckAPI credits for game-level data (results, odds) not available freely.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll use raw +/- instead of RAPM" | Raw +/- is entirely driven by teammates and opponents; a bad player on a good team looks great | Use RAPM; the whole point is to isolate individual contribution |
| "One season of data is enough for stable RAPM" | 1-season RAPM has high variance for any player under 1,000 minutes; estimates oscillate year-to-year | Use 3 seasons minimum; report confidence intervals |
| "I don't need the ridge penalty -- OLS works fine" | Without regularization, players with few shifts get extreme coefficients; the matrix is near-singular | Always use Ridge; select alpha via cross-validation or published benchmarks |
| "Use raw goals as the RAPM target" | Goals are too sparse per shift; extreme variance drowns signal | Use xG per 60 as the target; map to goals via xG-to-goals calibration |
| "WAR is additive with teammates" | WAR is not a linear decomposition of team wins; two 4-WAR players don't guarantee 8 wins of value together | WAR estimates individual marginal contribution; team synergies are separate |
| "Contract surplus is straightforward at age 35" | Aging curve means past WAR is a poor predictor of future WAR for players 32+ | Apply aging curve adjustment; note the uncertainty explicitly |
| "Goalies should have WAR too" | RAPM was designed for skaters; goalie performance is better captured by GSAA | For goalies, use GSAA; see `goalie-analysis` |

## Output Format

The WAR/GAR model produces:

1. **Component table**: per player, per season: `ev_offense_gar`, `ev_defense_gar`, `pp_gar`, `pk_gar`, `penalties_drawn_gar`, `penalties_taken_gar`, `total_gar`, `war`.
2. **League percentile ranks**: each component ranked 0-100 across all qualifying players (200+ minutes).
3. **Contract surplus table**: `player_name`, `aav`, `war_current_season`, `projected_war_contract`, `market_value`, `surplus_value`, `contract_years_remaining`.
4. **Player card data**: dictionary of component percentiles for radar chart rendering in `visualization` skill.
5. **Validation check**: team-level sum of player WARs should correlate with actual standings points (r > 0.70 is acceptable; r > 0.80 is strong).

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| WAR computed, want contract surplus analysis | Use WAR * market rate vs AAV | Stay in this skill (Step 5) |
| Component breakdown ready, want radar chart | Render JFresh-style player card | `visualization` |
| Want to use WAR as a model feature for game prediction | Treat WAR as a team-level sum feature (sum of skater WARs) | `feature-engineering` |
| Need to evaluate goalie value separately | Goalies use GSAA, not WAR | `goalie-analysis` |
| Want to compare players for trade analysis | Use surplus value + component breakdown | `player-scouting` |
| RAPM estimates look noisy | Check sample size per player; increase regularization or add seasons | `walk-forward-validation` for stability check |
