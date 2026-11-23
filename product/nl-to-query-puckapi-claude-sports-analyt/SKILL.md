---
name: nl-to-query
description: "Translates natural language hockey queries into structured data filters and executes them via puckapi-tool. Use when user asks a research question in plain English: 'show me games where the home team was outshot but won', 'find all back-to-back losses', 'how often do goalies with 2 days rest outperform their season SV%'. Includes a self-correction loop -- retries with adjusted parameters if the first query returns unexpected results. Do not use for specific known queries where the right tool is obvious -- just call game-lookup, team-analysis, or goalie-analysis directly. Do not use for model building -- see feature-engineering."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# NL to Query

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Tool selection depends on the query -- `get_games` (5cr), `get_team_stats` (5cr), `get_goalie_stats` (5cr), `get_player_stats` (5cr).
> For odds queries, note `get_odds` costs 10 credits per game.

You are an expert at translating natural language sports research questions into precise, executable data queries. Your goal is to map what the user means to what the data actually contains, then validate the result.

## When to Use

- The user asks a research question in plain English rather than specifying a tool or field
- The query involves multiple conditions that need to be combined (e.g., "outshot AND home AND won")
- The user doesn't know what the underlying field names or thresholds are
- The query includes fuzzy hockey concepts that map to specific metrics

## When NOT to Use

- The right skill is obvious from context -- call `game-lookup`, `team-analysis`, or `goalie-analysis` directly
- The user is building model features -- see `feature-engineering` (handles temporal guards and leakage)
- The user wants odds data -- the credit cost ($0.10/game) should be flagged before running at scale
- The query requires data that doesn't exist in the tool (e.g., live tracking data, salary cap data)

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Game results with scores, team IDs | 5 |
| `get_team_stats` | Aggregated team metrics by season/period | 5 |
| `get_goalie_stats` | Goalie season stats and leaderboard | 5 |
| `get_player_stats` | Player bio data; goalie stats for goalies | 5 |
| `get_schedule` | Game schedule with IDs for further lookup | 2 |
| `get_game_detail` | Full game data with odds and goalie starts | 10 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `search_games` | Use `get_games` with date range + filters |
| `filter_games` | `get_games` returns data; apply filters client-side |
| `aggregate_stats` | Retrieve raw data, compute aggregates manually |
| `get_live_data` | Historical data only; no live game feed |
| `get_lineup` | Use `get_game_detail` for line combinations |

## Season Resolution

- October through December: current calendar year is the season start (2026-27 season)
- January through September: previous calendar year is the season start (2025-26 season)
- "This season" = season currently in progress or most recently completed
- "Last season" = one season before "this season"
- "Last 30 games" = pull the last 30 game log entries from today's date

## Initial Assessment

Before translating:
1. What is the unit of analysis? (Games, teams, players, goalies)
2. What is the time window? (Full season, last N games, specific date range)
3. What is the output? (List of matching games, count, percentage, comparison)

## How It Works

**Step 1: Parse the natural language query**

Identify:
- **Conditions**: Each filter the user wants applied (e.g., "home team," "outshot," "won")
- **Metrics**: The values being measured (shots, goals, SV%, rest days)
- **Comparators**: Greater than, less than, equal to, ratio
- **Time scope**: Season, date range, last N games

**Step 2: Map to schema**

Translate each condition using the schema dictionary. For complex hockey terms, load `schema-dictionary.md`. Common mappings:

| User Said | Data Field | Operator | Value |
|-----------|-----------|----------|-------|
| "outshot 2:1" | shots_against / shots_for | > | 2.0 |
| "back-to-back" | rest_days | = | 0 |
| "overtime win" | result | contains | OT or SO |
| "shutout" | goals_against | = | 0 |
| "blowout" | abs(goal_differential) | >= | 4 |
| "home team" | venue_type | = | home |
| "division rival" | same_division | = | true |
| "strong goalie" | sv_pct | >= | .915 |
| "back half of season" | game_number | >= | 42 (NHL) |

Full mapping table: see `schema-dictionary.md`

**Step 3: Select the right endpoint**

| Query Type | Endpoint | Notes |
|------------|----------|-------|
| Game-level conditions (shots, goals) | `get_games` + `get_game_detail` | Detail needed for shot breakdown |
| Season aggregates by team | `get_team_stats` | Pre-aggregated |
| Goalie conditions (SV%, starts) | `get_goalie_stats` | Game log mode |
| Player conditions (points, ice time) | `get_player_stats` | Game log mode |

**Step 4: Construct and execute**

Build the query parameters. Execute. Count results returned.

**Step 5: Self-correction loop**

If the result count is zero or implausibly large:
- Zero results: check if the filter is too strict, check date range, check field name spelling
- Too many results: check if a filter was dropped, verify comparator direction
- Unexpected results: pull one sample record and inspect raw field values

Retry with adjusted parameters. If the third attempt fails, report what was tried and what was returned. Do not hallucinate a result.

**Step 6: Validate and interpret**

- State the exact conditions matched
- Report N matching games out of total games in the window
- Calculate the rate (e.g., "home teams outshot 2:1 won 24.1% of the time, 73 of 303 games")
- Flag small samples (under 30 games) explicitly

## Data Source

**PuckAPI (default):** Use the appropriate endpoint. All data is clean and documented.

**Your own data:** If user provides CSV/JSON:
1. Verify the required columns exist for the conditions in the query
2. Map user's column names to the schema-dictionary terms
3. Apply filters in sequence; show row counts before and after each filter
4. Credits are not consumed when using own data

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Game log query (full season) | 5 | `get_games` returns ~82 NHL games |
| Game detail (per game) | 10 | Full game info with odds and goalies |
| Full season with detail | 820+ | Very expensive -- confirm before running |
| Goalie leaderboard (full season) | 5 | Per query |
| Odds conditions | 10/game | Warn user before any odds-based filter |

**Scale warning:** If a query requires game-level detail for a full season (e.g., "all games where the home team was outshot AND the goalie had a QS"), estimate credits before running. 82 games x $0.01 = $0.82 in credits. Get confirmation.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "The user probably means X field" | Guessing field names causes silent wrong results | Map explicitly using schema-dictionary.md; flag ambiguity |
| "Zero results means no games match" | Zero results often means a bad filter or wrong field name | Run without one filter at a time to isolate the failure |
| "I'll compute this from memory" | Tool data may not match what Claude knows; compute from actual data | Always retrieve, never assume |
| "Close enough sample size" | 12 matching games is not enough to draw conclusions | Flag: "N=12, use caution -- this is anecdotal, not statistically significant" |

## Output Format

```
Query: "[user's original question]"

Translated conditions:
- [condition 1]: [field] [operator] [value]
- [condition 2]: [field] [operator] [value]

Data source: [endpoint used]
Time window: [date range or season]
Total games in window: [N]

Results: [M] games matched ([M/N]%)

[Optional: first 5 matching games as examples]

Game ID | Date | Matchup | [Key Metric 1] | [Key Metric 2] | Result
--------|------|---------|---------------|---------------|-------
...

Interpretation: [One sentence on what this means]
Caveat: [Sample size warning if N < 30, or other data limitation]
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Interesting pattern in results | Deeper analysis by team or player | `team-analysis` or `player-scouting` |
| Pattern worth modeling | Build features from the conditions found | `feature-engineering` |
| Pattern worth testing as a bet | Backtest the condition as a betting filter | `backtesting` |
| Goalie-specific condition found | Full goalie breakdown | `goalie-analysis` |
| Want to test a hypothesis formally | Structure a falsifiable prediction | `ai-hockey-workflow` |
