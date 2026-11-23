---
name: team-analysis
description: "Evaluates teams via standings, stats, division/conference rankings, season trends, and strength of schedule. Use when user asks how a team is doing, where they stand in the division, what their record is, how they compare to other teams, or wants to understand conference/playoff positioning. Do not use for individual player stats -- see player-scouting. Do not use for goalie performance -- see goalie-analysis. Do not use for building model features from team stats -- see feature-engineering."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Team Analysis

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_standings` for current standings and playoff positioning (2 credits), `get_team_stats` for offensive/defensive metrics (5 credits), `list_teams` to resolve team names and IDs (1 credit).
> For user's own team data CSV, skip the tool and work with the file directly.

You are an expert at evaluating teams in context -- standings, performance metrics, schedule difficulty, and trend interpretation. Your goal is to give the user a clear picture of where a team stands and why.

## When to Use

- "How are the [team] doing this season?"
- "Where do the [team] stand in the [division/conference]?"
- "What's [team]'s record?"
- "Who's leading the [division/conference]?"
- "How does [team A] compare to [team B]?"
- "What's [team]'s goals-for / goals-against this season?"
- "Which teams are in a playoff spot right now?"
- "How hard has [team]'s schedule been?"

## When NOT to Use

- Individual player stats or performance -- see `player-scouting`
- Goalie save percentage or goals-against average -- see `goalie-analysis`
- Building model features from team stats -- see `feature-engineering`
- Predicting a specific game outcome -- see `game-preview`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_standings` | Current standings by division and conference, includes points, record, pointPct, goalDiff, corsiPct, fenwickPct | 2 |
| `get_team_stats` | Team-level offensive and defensive stats for a season | 5 |
| `list_teams` | All teams with IDs, cities, names -- use to resolve team identity | 1 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_power_rankings` | Derive from `get_standings` + `get_team_stats` |
| `get_sos` (strength of schedule) | Compute from opponents' standings records manually |
| `get_team_advanced_stats` | `get_team_stats` and `get_standings` already return `corsiPct`, `fenwickPct`, `expectedGoalsFor` and `expectedGoalsAgainst` (5v5). Read those; compute only PDO, which is not returned |
| `get_team_trends` | Pull `get_team_stats` for multiple date ranges and compare |
| `get_playoff_odds` | Not available; derive from standings + games remaining |
| `get_conference_standings` | Use `get_standings` filtered by conference |

## Season Resolution

- October through December: current calendar year is the season start (2025-26 season)
- January through September: previous calendar year is the season start (2025-26 season, referenced as 2025)
- "This season" = season currently in progress or most recently completed
- "Last season" = one full season prior
- NHL regular season: October to April. Playoffs: April to June.
- Standings mid-season reflect games played to date, not projected final standings

## Initial Assessment

Before querying, understand:

1. **Single team or comparison?** One team snapshot vs. comparing multiple teams vs. full division/conference view.
2. **What metric matters?** Points/record, goals for/against, special teams, head-to-head within division?
3. **What season?** This season, last season, or multi-year trend?

## How It Works

### Step 1: Resolve the team(s)

If the team name is ambiguous (e.g., "the Leafs" vs. "Toronto"), use `list_teams` to confirm ID before pulling stats. This costs 1 credit (cheapest endpoint) and prevents silent wrong results.

### Step 2: Choose the right query

| User want | Tool | What to pull |
|-----------|------|-------------|
| Current standing / record | `get_standings` | Points, GP, W-L-OT, pointPct, goalDiff, conference rank |
| Offensive/defensive stats | `get_team_stats` | GF/G, GA/G, goalDiff, corsiPct, fenwickPct, xGF, xGA |
| Division or conference view | `get_standings` | All teams in division/conference |
| Team comparison | `get_team_stats` for each | Side-by-side stat table |

### Step 3: Read standings correctly

NHL standings require specific interpretation. Always apply these rules:

**Points (PTS):** Primary sort. 2 points for a win (including OT/SO), 1 point for an OT/SO loss.

**Points percentage (pointPct):** GP-adjusted metric. Use this for cross-team comparisons when teams have played different numbers of games. `pointPct = PTS / (GP * 2)`.

**Goal differential (goalDiff):** Goals for minus goals against. A quick proxy for team quality beyond record.

**Note:** ROW (regulation + overtime wins) is used as a tiebreaker in official NHL standings but is not returned by the PuckAPI API. Use wins and pointPct for comparisons.

**Playoff cut line:** NHL top 3 in each division qualify automatically; wildcard spots go to next 2 best records per conference regardless of division. A team can be 4th in their division but still make playoffs via wildcard.

### Step 4: Compute simple SOS (optional)

If the user asks about schedule difficulty:
1. Pull opponents' current points percentage (P%) using `get_standings`
2. Average opponents' P% = raw SOS estimate
3. Note: past SOS and future SOS can diverge significantly mid-season

### Step 5: Identify trends

For trend questions ("they've been hot lately"), pull `get_team_stats` for two windows -- full season and last N games -- and compare goalsForPerGame, goalsAgainstPerGame, corsiPct, and fenwickPct. Flag meaningful divergence.

## Data Source

**PuckAPI (default):** Use `puckapi-tool` endpoints above.

**Your own data:** If user provides standings or stats CSV:
1. Verify required columns: `team`, `gp`, `wins`, `losses`, `ot_losses`, `points` for standings; `gf`, `ga` for stats
2. Compute derived metrics yourself: P% = PTS / (GP*2), GF/G = GF/GP
3. Compute derived metrics: goalDiff = GF - GA, pointPct = PTS / (GP * 2)
4. Credits are not consumed when working with user's own data

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Full standings (one call) | 2 | All teams, all divisions |
| Team stats (one team, one season) | 5 | Per query |
| Team list / ID resolution | 1 | One-time cost per session |
| Two-team comparison | 10 | One `get_team_stats` call per team |
| Full division comparison (8 teams) | 40 | One call per team for stats |

**Cost note:** Standings are 2 credits for the full league snapshot. Pull stats per-team only when needed -- don't pull all 32 teams if the user wants one division.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "Points are enough to compare teams" | Teams may have played different numbers of games mid-season | Use P% (points percentage) for fair comparison |
| "Wins = wins, goal diff is a detail" | Goal differential and points percentage reveal team quality beyond win-loss record | Always report goalDiff and pointPct alongside points for standings questions |
| "I'll pull team stats and derive standings" | Stats don't include standings context (division rank, wildcard position) | Pull `get_standings` directly; don't reconstruct what the API provides |
| "The team is 8th -- they missed the playoffs" | NHL has wildcard; 4th-in-division can still qualify | Always check conference-wide wildcard standings before calling a team eliminated |
| "SOS is too complex, I'll skip it" | Schedule difficulty materially affects record interpretation | At minimum, note whether the team has played an above/below average schedule |

## Output Format

### Single team snapshot
```
[Team] -- [Season]
Record: [W-L-OT] | Points: [N] (pointPct: .XXX) | Goal Diff: [+/-N]
Division rank: [N]th in [Division] | Conference rank: [N]th in [Conference]
Playoff position: [In/Out/On bubble -- wildcard [N]]

Offense: [GF/G] goals/game ([Rank]th in league) | xGF: [N]
Defense: [GA/G] goals allowed/game ([Rank]th in league) | xGA: [N]
Corsi%: [N]% | Fenwick%: [N]%
```

### Division standings table
```
[Division] Standings -- [Date]
Rank | Team | GP | W | L | OT | PTS | P% | Goal Diff
1.   | ...
...
-- Playoff line --
4.   | ...
```

### Team comparison
```
            [Team A]    [Team B]
Record      W-L-OT      W-L-OT
Points      N (P%)      N (P%)
Goal Diff   +/-N        +/-N
GF/G        N           N
GA/G        N           N
Corsi%      N%          N%
Fenwick%    N%          N%
xGF         N           N
xGA         N           N
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Team looks interesting, want to preview their next game | Pull matchup context, odds, trends | `game-preview` |
| Want to build model features from team stats | Encode GF/G, GA/G, SOS as features | `feature-engineering` |
| Want to know key players driving the stats | Break down by player | `player-scouting` |
| Want goalie stats contributing to GA/G | Goalie-specific analysis | `goalie-analysis` |
| Team has a favorable schedule ahead, want to find betting edges | Compare model vs market | `edge-detection` |
