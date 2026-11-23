---
name: playoff-simulation
description: "Monte Carlo playoff and season simulator for NHL. Use when user asks about playoff odds, championship probability, making the playoffs, division race odds, season simulation, bracket simulation, or how likely a team is to win the Stanley Cup. Do not use for single game prediction -- see model-building or game-preview. Do not use for team stats without simulation -- see team-analysis. Do not use for player-level analysis -- see player-scouting."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Playoff Simulation

> **Default data tool:** PuckAPI (`puckapi-tool`) for current standings and remaining schedule.
> Use `get_standings` (2 credits) and `get_games` (5 credits) for remaining schedule.
> Elo ratings as input: use `elo-engineering` to build, or bring your own rating system.
> For your own data (CSV of standings + ratings), skip the tool and work with the file directly.

You are an expert in Monte Carlo season and playoff simulation. Your goal is to take any team rating system, simulate thousands of futures, and produce probability distributions for every meaningful outcome: playoff berths, division titles, championship odds, and draft position. PuckCast runs 10,000 iterations nightly; the methodology here produces the same class of output.

## When to Use

- User asks what the playoff odds are for a specific team
- User wants to know championship probabilities across the league
- User asks who is likely to win the division
- User wants to simulate the rest of the season
- User asks for bracket simulation after the playoff field is set
- User wants to see how ratings translate to probability distributions

## When NOT to Use

- Single game win probability -- see `model-building` or `game-preview`
- Team evaluation without simulation context -- see `team-analysis`
- Player-level analysis or valuation -- see `player-scouting`
- Running Elo ratings from scratch -- see `elo-engineering` first, then bring ratings here

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_standings` | Current standings, points, record | 2 |
| `get_games` | Remaining schedule for all teams | 5 |
| `get_team_stats` | Goal data for Pythagorean ratings | 5 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `simulate_season` | Implement Monte Carlo loop in Python |
| `get_playoff_odds` | Compute from simulation output |
| `get_championship_probability` | Output of simulation, not a direct endpoint |

## Initial Assessment

Before simulating, establish:
1. Which sport and current date? (determines remaining games and tiebreaker rules)
2. What rating system to use? (Elo from `elo-engineering`, Pythagorean, or custom)
3. How many iterations? (10,000 minimum for stable output, 100,000 for publication)
4. What playoff format applies? (see sport-specific configs below)

## Data Source

**PuckAPI (default):** Pull current standings with `get_standings`, remaining schedule with `get_games` filtered to future dates.

**Your own data:** Required inputs:
1. Ratings table: `team`, `rating` (Elo or equivalent), `home_rating_boost` (optional)
2. Remaining schedule: `home_team`, `away_team`, `game_date`
3. Current standings: `team`, `points`, `gp`, `wins`, `losses` (sport-specific columns)

Flag missing data -- do not silently drop teams from the simulation.

## How It Works

### Step 1: Build the Rating System

If the user doesn't have ratings, recommend `elo-engineering` first. If they have a custom rating system, verify it produces win probabilities.

Win probability from Elo difference:
```python
def win_prob(rating_a, rating_b, home_advantage=0):
    # home_advantage in Elo points (NHL default: 35)
    return 1 / (1 + 10 ** ((rating_b - rating_a - home_advantage) / 400))
```

For Pythagorean ratings (alternative to Elo):
```python
def pythagorean_win_pct(goals_for, goals_against, exponent):
    # Exponent: NHL=2.15 (see elo-engineering parameter-reference for other sports)
    return goals_for ** exponent / (goals_for ** exponent + goals_against ** exponent)
```

### Step 2: Single Game Simulation

One Bernoulli trial per game, weighted by win probability.

```python
import numpy as np

def simulate_game(home_team, away_team, ratings, home_adv):
    p_home = win_prob(ratings[home_team], ratings[away_team], home_adv)
    home_wins = np.random.random() < p_home
    return home_team if home_wins else away_team
```

For NHL specifically: account for regulation/OT/SO. NHL awards 2 points for a win, 1 point each for OT losses.
```python
def simulate_nhl_game(home_team, away_team, ratings, home_adv=35):
    p_home_reg = win_prob(ratings[home_team], ratings[away_team], home_adv)
    # ~23% of NHL games go to OT; roughly 50/50 after that
    p_ot = 0.23
    if np.random.random() < p_ot:
        # OT: each team gets 1 point, winner gets 2nd
        ot_winner = home_team if np.random.random() < 0.5 else away_team
        return home_team, away_team, ot_winner  # (loser still gets 1 pt)
    else:
        winner = home_team if np.random.random() < p_home_reg else away_team
        return winner, None, winner  # no OT
```

### Step 3: Season Simulation Loop

```python
def simulate_season(teams, ratings, remaining_games, current_standings,
                    n_iterations=10000, sport='NHL'):

    results = {team: {
        'made_playoffs': 0, 'won_division': 0,
        'won_conference': 0, 'won_championship': 0,
        'draft_top5': 0
    } for team in teams}

    for i in range(n_iterations):
        # Copy current standings
        simulated_points = current_standings.copy()

        # Simulate remaining games
        for _, game in remaining_games.iterrows():
            winner = simulate_game(game['home'], game['away'], ratings, home_adv)
            simulated_points[winner] += 2  # sport-specific points

        # Determine playoff qualifiers
        playoff_teams = determine_playoffs(simulated_points, sport=sport)

        # Simulate playoff bracket
        champion = simulate_playoffs(playoff_teams, ratings, sport=sport)

        # Record outcomes
        for team in playoff_teams:
            results[team]['made_playoffs'] += 1
        results[champion]['won_championship'] += 1

    # Convert to probabilities
    for team in results:
        for key in results[team]:
            results[team][key] /= n_iterations

    return results
```

### Step 4: Playoff Bracket Simulation

#### NHL: Best-of-7 Series

```python
def simulate_series_nhl(team_a, team_b, ratings, home_team_a=True):
    wins_a, wins_b = 0, 0
    game = 1
    # Standard home/away format: 2-2-1-1-1
    home_games_a = [True, True, False, False, True, False, True]

    while wins_a < 4 and wins_b < 4:
        home_adv = 35 if home_games_a[game-1] else -35
        winner = simulate_game(team_a, team_b, ratings, home_adv)
        if winner == team_a:
            wins_a += 1
        else:
            wins_b += 1
        game += 1

    return team_a if wins_a == 4 else team_b
```

### Step 5: Determine Playoff Qualifiers

NHL tiebreakers matter when simulated points are tied:

Sort by points, then ROW (regulation + OT wins, excludes shootout wins), then head-to-head record, then goal differential. Wild card format: top 3 from each division + 2 wild cards per conference.

```python
def determine_playoffs(simulated_standings):
    return nhl_playoff_format(simulated_standings)
```

### Step 6: Convergence Check

Run 1,000 iterations first. Check that top-team probabilities stabilize (< 1% change per additional 1,000 iterations). If not, run more.

```python
def check_convergence(results_1k, results_10k, threshold=0.01):
    for team in results_1k:
        diff = abs(results_1k[team]['made_playoffs'] - results_10k[team]['made_playoffs'])
        if diff > threshold:
            return False
    return True
```

10,000 iterations: stable for most probabilities. 100,000 iterations: required for probabilities below 5% (low-probability events need more samples to be reliable).

## NHL Config

| Config | Value |
|--------|-------|
| Season length | 82 games |
| Playoff format | Best-of-7, 4 rounds |
| Home advantage (Elo pts) | 35 |
| Home field games | 2-2-1-1-1 |
| Season carryover | 0.88 |
| Pythagorean exponent | 2.15 |
| Points system | 2 for win, 1 for OT loss |

## Season/Date Logic

- NHL: October through April (regular season), April through June (playoffs)
- "Remaining games" = all games on the schedule with `game_date > today`
- If playoffs have already started, simulate only remaining rounds, not the regular season

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "1,000 iterations is enough" | A team at 5% championship odds has high variance at 1,000 iterations; the estimate can swing 2-3% just from sampling noise | Run 10,000 minimum; 100,000 for low-probability events |
| "Win probability is just current win%" | Win% doesn't account for strength of schedule or remaining schedule difficulty | Use Elo or Pythagorean ratings, not raw win% |
| "Home advantage doesn't matter in playoffs" | NHL home advantage is ~35 Elo points. Over a 7-game series with 2-2-1-1-1 format, home ice advantage compounds meaningfully. | Use the 35-point HFA in all playoff games; give it to the higher seed. |
| "Tiebreakers don't matter -- they're rare" | At the boundary of playoff spots, tiebreakers fire on 5-15% of simulated seasons | Implement ROW tiebreaker for NHL -- it affects the playoff probability bands meaningfully |
| "More iterations is always better" | Beyond 100,000, runtime cost exceeds precision gain | 100,000 is ceiling; 10,000 is floor; match to stakes and compute budget |
| "One rating system is sufficient" | A single Elo variant misses different signals (recent form vs cumulative quality) | Run simulations with 2-3 rating variants; report the range as uncertainty bounds |

## Output Format

Team-level probability table:

```
Team               | Playoff% | Div Title% | Conf%  | Cup%
-------------------|----------|------------|--------|------
Boston Bruins      | 94%      | 52%        | 28%    | 14%
Toronto Maple Leafs| 87%      | 31%        | 18%    | 8%
Tampa Bay Lightning| 79%      | 16%        | 12%    | 6%
Florida Panthers   | 71%      | 11%        | 9%     | 4%
...
Buffalo Sabres     | 23%      | 2%         | 1%     | 0.4%
```

For eliminated teams, include draft lottery position probability:

```
Team               | Top-5 Pick% | Top-10 Pick%
-------------------|-----------:|------------:
San Jose Sharks    | 48%         | 91%
Anaheim Ducks      | 41%         | 87%
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Simulation complete, want charts | Probability path charts over the season | `visualization` |
| Ratings feel off, want to improve | Build better Elo system | `elo-engineering` |
| Want to bet on futures using these odds | Compare simulation to market futures | `odds-explorer` |
| Want to backtest simulation accuracy | Test prior-season simulations vs outcomes | `backtesting` |
| Want to preview a specific playoff matchup | Single-series matchup analysis | `game-preview` |
