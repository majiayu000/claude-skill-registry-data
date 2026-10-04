---
name: puckapi-tool
description: "Default data source for PuckAPI Skills. Routes all MCP tool calls for NHL games, schedules, team standings, player stats, goalie performance, and betting odds. Use when any other skill needs data. Do not invoke directly -- other skills call this. Not for data analysis, modeling, or bet recommendations -- see hockey-analytics, model-building, or edge-detection instead."
metadata:
  version: 1.0.0
  author: PuckAPI
  user-invocable: false
---

# PuckAPI Tool

Every other skill delegates data retrieval here. This skill owns the 15 MCP tools, routes requests to the right endpoint, tracks credit cost, and handles the fallback when users bring their own data.

**Database coverage:** 6,882,653 plays | 23,495 games (2010-11 onward) | 107,058 odds records (2019-20 onward, sparse in the first year) | 4,898 players | 1,509 goalie-seasons | 1,803 skater-seasons | 21,994 games with derived goalie starts | 494 standings records | 34 franchises (32 active + 2 historical)

**Full parameter schemas:** See `endpoints.md` in this directory (Level 3 -- load on demand).

---

## When to Use Each Tool

| Task | Tool | Credits |
|------|------|---------|
| List all teams | `list_teams` | 1 |
| Upcoming schedule | `get_schedule` | 2 |
| Find a player by name | `search_players` | 2 |
| League or conference standings | `get_standings` | 2 |
| Games by date, team, or season | `get_games` | 5 |
| Player bio + stats by NHL player ID | `get_player_stats` | 5 |
| Single team stats + advanced metrics | `get_team_stats` | 5 |
| Goalie leaderboard | `get_goalie_stats` | 5 |
| Full game detail with odds + goalies | `get_game_detail` | 10 |
| Head-to-head history between two teams | `get_head_to_head` | 10 |
| Odds snapshot for a game | `get_odds` | 10 |
| Opening vs closing line movement | `get_line_movement` | 25 |

---

## Tool Selection Guide

Use this table when a request could match multiple tools.

| You Need | Use This | Not This |
|----------|----------|----------|
| "What games are on tonight?" | `get_schedule` | `get_games` (returns past games too) |
| "Show me BUF's last 10 games" | `get_games` with `team=BUF`, `limit=10` | `get_schedule` (future only) |
| "Full game info with odds" | `get_game_detail` | `get_games` + `get_odds` separately |
| "How have BUF and TOR fared against each other?" | `get_head_to_head` | `get_games` filtered manually |
| "Where does BUF rank in the Atlantic?" | `get_standings` with `division=Atlantic` | `get_team_stats` |
| "BUF's Corsi and xG numbers" | `get_team_stats` | `get_standings` (standings have basic metrics only) |
| "Find Connor McDavid's ID" | `search_players` with `query=McDavid` | `get_player_stats` (requires numeric ID) |
| "McDavid's bio and current stats" | `get_player_stats` with known ID | `search_players` |
| "Best save percentage goalies this season" | `get_goalie_stats` with `sort_by=save_pct` | `get_player_stats` |
| "What's the line on tonight's BUF game?" | `get_odds` with that game's ID | `get_line_movement` (movement, not snapshot) |
| "Did DraftKings move the line today?" | `get_line_movement` | `get_odds` |

---

## Credit Usage

| Tier | Endpoints | Credits |
|------|-----------|---------|
| Lightweight | `list_teams` | 1 |
| Standard | `get_schedule`, `search_players`, `get_standings` | 2 |
| Moderate | `get_games`, `get_player_stats`, `get_team_stats`, `get_goalie_stats` | 5 |
| Heavy | `get_game_detail`, `get_head_to_head`, `get_odds` | 10 |
| Expensive | `get_line_movement` | 25 |

**Bulk cost examples:**
| Operation | Credits | Notes |
|-----------|---------|-------|
| Full season odds backfill | ~12,300 | 10 credits x ~1,230 games |
| Full season game details | ~12,300 | 10 credits x ~1,230 games |
| Playoff odds (full bracket) | ~150-250 | Depends on rounds reached |

**Odds coverage caveat:** Odds data covers 2020-2026 NHL seasons. Calls to `get_odds` or `get_line_movement` for games before the 2019-20 season return empty odds arrays, not an error.

---

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_live_odds` | `get_odds` with today's game ID (snapshot_type omitted returns all) |
| `get_player_advanced_stats` | `get_player_stats`, then compute via `hockey-analytics` |
| `get_team_schedule` | `get_games` with `team=ABBREV` |
| `get_game_by_teams` | `get_head_to_head` or `get_games` with `team` filter |
| `get_playoff_bracket` | `get_games` with `game_type=playoff` |
| `get_historical_lineups` | Not available -- no lineup data in this dataset |
| `get_goalie_game_log` | Not available -- use `get_game_detail` for per-game goalie starts |
| `get_injuries` | Not available |
| `get_power_play_stats` | Not available as a standalone endpoint |
| `search_games` | Use `get_games` with filters |

---

## Season Resolution

Every skill that touches time-sensitive data must resolve season IDs before calling tools.

**Season ID format:** `YYYYYYYY` (eight digits, no separator). Example: 2025-26 season = `20252026`.

**Current date resolution rules:**
- October through December: current calendar year starts the season (Oct 2026 = season `20262027`)
- January through September: previous calendar year starts the season (Mar 2026 = season `20252026`)
- "This season" = season currently in progress or most recently completed
- "Last season" = one season before "this season"

**NHL calendar:**
- Regular season: early October to mid-April
- Playoffs: mid-April to mid-June
- Offseason: July to September
- Data coverage starts at `20102011` (2010-11 season). There is nothing before it; querying an earlier season returns empty, not an error

**How to resolve when user says "current season":**
1. Call `get_standings` with no `season` parameter -- the server resolves automatically
2. Or call `get_team_stats` with no `season` -- same auto-resolution
3. For `get_games`, pass `season=20252026` explicitly when targeting a specific season

---

## BYOD (Bring Your Own Data)

When a user provides their own CSV, JSON, or database instead of using PuckAPI:

1. **Verify required columns exist** before proceeding (see `endpoints.md` for column schemas)
2. **Check date format** -- ISO 8601 preferred (`YYYY-MM-DD`). Flag anything else.
3. **Flag missing data explicitly** -- do not silently drop rows or impute without noting it
4. **No credits consumed** when working with user-provided data
5. **Column name mapping** -- if user data uses different column names, map them to the PuckAPI schema before passing to analytics skills

**Common user-provided formats:**
| Format | Required Minimum Columns | Notes |
|--------|--------------------------|-------|
| Game results CSV | `game_date`, `home_team`, `away_team`, `home_score`, `away_score` | `game_id` helpful but not required |
| Odds CSV | `game_id` or (`game_date` + `home_team`), `bookmaker`, `ml_home`, `ml_away` | Snapshot type required for line movement analysis |
| Player stats CSV | `player_id` or `player_name`, `team`, `season`, stat columns | Prefer numeric ID over name for joins |

---

## How to Call These Tools

### Pattern: Find game ID then fetch detail

Most analytics workflows need a `game_id`. Get it from `get_games` or `get_schedule`, then pass to `get_game_detail`, `get_odds`, or `get_line_movement`.

```
Step 1: get_games(team="BUF", date_from="2026-01-01", date_to="2026-01-31")
        -> returns game list with IDs
Step 2: get_game_detail(game_id="2025020887")
        -> returns full game with odds and goalie starts
```

### Pattern: Player lookup by name then stats

`get_player_stats` requires a numeric NHL player ID. Always search first.

```
Step 1: search_players(query="McDavid", active=true)
        -> returns player list with IDs
Step 2: get_player_stats(player_id=8478402)
        -> returns bio + career stats
```

### Pattern: Standings with advanced metrics

`get_standings` includes Corsi, Fenwick, and xG columns. No need to call `get_team_stats` separately for a full league view.

```
get_standings(conference="Eastern", season="20252026")
-> returns all Eastern teams sorted by rank with advanced metrics
```

---

## Anti-patterns

| What Claude Might Do | Why It's Wrong | Do This Instead |
|---------------------|---------------|-----------------|
| Call `get_odds` for every game in a season | 10 credits x 1,230 games = 12,300 credits | Warn user before bulk odds pulls, ask for date range |
| Call `get_line_movement` when user just wants current odds | 25 credits wasted | Use `get_odds` with `snapshot_type=current` (10 credits) |
| Call `search_players` and then guess the ID | IDs must be exact | Use the actual `id` field from `search_players` results |
| Pass a team name like "Buffalo Sabres" to `team` parameter | Tool expects abbreviation | Always use 2-3 letter abbreviation (e.g. `BUF`) |
| Assume odds exist for pre-2020 games | Returns empty array, not an error | Check game season before calling odds endpoints |
| Call `get_game_detail` in a loop for many games | N x 10 credits per game | Use `get_games` (5 credits) for bulk data, `get_game_detail` only when you need odds/goalies for a specific game |

---

## What to Do Next

| What You Retrieved | Next Action | Skill |
|--------------------|-------------|-------|
| Game results for a season | Compute Elo ratings or features | `elo-engineering` or `feature-engineering` |
| Standings with Corsi/Fenwick | Analyze team performance trends | `team-analysis` |
| Odds for upcoming games | Find edge vs market | `edge-detection` |
| Line movement data | Detect sharp action signals | `odds-analysis` |
| Player/goalie stats | Scout performance vs league | `player-scouting` or `goalie-analysis` |
| Head-to-head history | Build game preview | `game-preview` |
| Full season game log | Run a backtest | `backtesting` |
| Raw game data, need features | Engineer model inputs | `feature-engineering` |
