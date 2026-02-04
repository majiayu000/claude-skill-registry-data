---
name: football
description: European football matches — upcoming games, results, and highlights for briefings.
homepage: https://www.football-data.org/
metadata: {"clawdis":{"emoji":"⚽","requires":{"bins":["node","curl"]},"env":["FOOTBALL_DATA_API_KEY"]}}
---

# Football Skill ⚽

Track European football matches — upcoming games, live scores, and results.

## Quick Start

```bash
# Upcoming matches (next 7 days)
{baseDir}/scripts/football.js upcoming

# Today's matches
{baseDir}/scripts/football.js today

# Specific league
{baseDir}/scripts/football.js upcoming --league bundesliga
{baseDir}/scripts/football.js upcoming --league premier-league
{baseDir}/scripts/football.js upcoming --league champions-league

# Interesting matches only (top teams, derbies)
{baseDir}/scripts/football.js highlights

# Results from recent matches
{baseDir}/scripts/football.js results
```

## Supported Leagues

| League | Code | API |
|--------|------|-----|
| Bundesliga | `bundesliga`, `bl1` | OpenLigaDB (free) |
| 2. Bundesliga | `bundesliga2`, `bl2` | OpenLigaDB (free) |
| DFB Pokal | `dfb` | OpenLigaDB (free) |
| Premier League | `premier-league`, `pl` | football-data.org |
| La Liga | `la-liga`, `pd` | football-data.org |
| Serie A | `serie-a`, `sa` | football-data.org |
| Ligue 1 | `ligue-1`, `fl1` | football-data.org |
| Champions League | `champions-league`, `cl` | football-data.org |
| Europa League | `europa-league`, `el` | football-data.org |

## Morning Briefing Integration

For daily briefings, use:
```bash
{baseDir}/scripts/football.js briefing
```

Returns a compact summary of:
- Today's interesting matches
- Yesterday's notable results  
- Upcoming highlights this week

## API Keys

**OpenLigaDB** (German leagues): No key required! ✅

**football-data.org** (other leagues): Free tier available
1. Register at https://www.football-data.org/client/register
2. Set `FOOTBALL_DATA_API_KEY` environment variable

## "Interesting" Match Criteria

The `highlights` command filters for:
- Top teams playing (Bayern, Dortmund, Real, Barça, etc.)
- Derby matches
- Champions League knockout games
- Title deciders (late season, close standings)

## Output Formats

```bash
# JSON (default)
{baseDir}/scripts/football.js today

# Human-readable
{baseDir}/scripts/football.js today --human

# Compact (for briefings)
{baseDir}/scripts/football.js briefing --compact
```
