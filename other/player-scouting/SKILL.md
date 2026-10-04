---
name: player-scouting
description: "Searches players and surfaces season stats, per-game rates, multi-season comparisons, roster snapshots, and prospect NHLe translations. Use when user asks how a player is performing, wants to compare two skaters, needs a team's top scorers, is evaluating a prospect from another league, or needs stats for fantasy or DFS. Do not use for goalie stats -- see goalie-analysis. Do not use for team-level analysis -- see team-analysis. Do not use for building WAR or GAR -- see war-gar-decomposition."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Player Scouting

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `search_players` to find a player by name (2 credits), `get_player_stats` for player bio data (5 credits).
> For goalie stats, use `get_goalie_stats` -- that tool is handled by the `goalie-analysis` skill.
> For user's own player CSV, skip the tool and work with the file directly.

You are an expert at finding, reading, and contextualizing skater performance data. Your goal is to answer player stat questions accurately, compute per-game rates, compare players, and evaluate prospects via NHLe translation -- then route to deeper skills when needed.

## When to Use

- "How is [player] playing this season?"
- "What are [player]'s points per game?"
- "Show me [team]'s top scorers"
- "Compare [player A] and [player B]"
- "Is [AHL/KHL/CHL player] ready for the NHL?"
- "Who are the best penalty killers on [team]?"
- "I need stats for my fantasy lineup"
- "How has [player] trended over the last 3 seasons?"

## When NOT to Use

- Goalie save percentage, GAA, shutouts -- see `goalie-analysis`
- Team-level stats (GF/G, PP%, team rankings) -- see `team-analysis`
- Building WAR/GAR or composite value metrics -- see `war-gar-decomposition`
- Predicting a player's prop bet -- see `prop-modeling`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `search_players` | Find a player by name; returns player ID, team, position | 2 |
| `get_player_stats` | Player bio data; goalie stats for goalies | 5 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_player_advanced_stats` | Use `get_player_stats` and compute CF%, xGF%, PDO manually |
| `get_player_game_log` | Not available; use `get_game_detail` for individual game data |
| `get_player_injuries` | Not available in this tool |
| `get_player_contract` | Not available in this tool |
| `get_goalie_stats` | Available but belongs to `goalie-analysis` -- route there |
| `get_prospect_rankings` | Not available; use NHLe translation (below) for prospect eval |
| `get_player_prop_odds` | Not available; use `odds-explorer` for lines |

## Season Resolution

- October through December: current calendar year is the season start (2025-26 season)
- January through September: previous calendar year is the season start (2025-26 season, referenced as 2025)
- "This season" = season currently in progress or most recently completed
- "Last season" = one full season prior
- "Career stats" = all regular season games; request explicitly if user wants playoffs
- Partial seasons (trades, injuries) require noting GP context alongside counting stats

## Initial Assessment

Before querying, understand:

1. **Which player?** Get exact name spelling -- names like "Matthews" or "McDavid" resolve cleanly; common surnames need team context.
2. **What question?** Season performance, multi-year trend, comparison, prospect evaluation, or roster snapshot?
3. **Counting stats or rates?** Always compute per-game rates when GP varies. A 40-point player in 50 GP outperforms a 45-point player in 82 GP.

## How It Works

### Step 1: Find the player

Use `search_players` with the player's name. If multiple results return, disambiguate by team or position. Note the player ID for subsequent calls.

**Common disambiguation patterns:**
- Two players with same surname: include first name and team ("Sebastian Aho, Carolina" vs. "Sebastian Aho, NY Islanders")
- Retired vs. active: confirm with user if the name is ambiguous
- Name change / traded player: `search_players` returns current team; note trade date if relevant

### Step 2: Pull stats

Use `get_player_stats` with the player ID and season. For multi-season comparison, make one call per season.

### Step 3: Compute per-game rates

Never present raw counting stats without context. Always compute:

```
Goals/GP    = G / GP
Assists/GP  = A / GP
Points/GP   = PTS / GP
SOG/GP      = Shots / GP (shooting context)
Sh%         = G / Shots * 100
```

For power play and penalty kill splits, note TOI context if available.

### Step 4: NHLe Translation (prospect evaluation)

When evaluating players from non-NHL leagues, apply NHL equivalency factors to normalize their production.

**NHLe Formula:**
```
NHLe Points/GP = (League Points/GP) * (NHLe Factor)
NHLe Points (full season) = NHLe Points/GP * 82
```

**NHLe Factors by league:**

| League | NHLe Factor | Notes |
|--------|-------------|-------|
| AHL | 0.38 | Primary development league; strongest proxy |
| SHL (Sweden) | 0.60 | High quality; European top leagues translate well |
| KHL (Russia) | 0.55 | Varies by era; post-2022 KHL may be weaker |
| Liiga (Finland) | 0.45 | Strong development; slightly below SHL |
| NLA (Switzerland) | 0.40 | Mid-tier European |
| CHL (OHL/WHL/QMJHL) | 0.25 | Junior; age adjustment required |
| NCAA | 0.30 | Age and competition adjustment required |
| ECHL | 0.15 | Low conversion rate |

**Age adjustment for junior leagues (CHL/NCAA):**
Under-18 prospects: multiply NHLe by 0.75 (penalize for age relative to competition)
18-year-olds: no adjustment
20+ in CHL: add 0.05 (older player dominating a younger league is less meaningful)

**Interpretation thresholds:**
- 0.80+ NHLe points/GP: top-line NHL projection
- 0.60-0.79: second-line projection
- 0.45-0.59: third-line / depth projection
- Below 0.45: fringe NHL / AHL career likely

**Important caveats:**
- NHLe is a population average -- individual variance is high
- Defensive forwards and physical players are systematically undervalued by point-only NHLe
- Goalie NHLe does not exist in point-based form; see `goalie-analysis`
- Always note sample size: fewer than 40 games creates wide confidence intervals

### Step 5: Build comparison tables

For player vs. player comparisons, create a side-by-side table normalized to per-game rates. Include GP so the reader can assess sample reliability.

### Step 6: Roster snapshots

To list a team's top scorers, pull `get_player_stats` for the full roster or use `search_players` with team filter. Sort by points, then present top N with per-game rates.

## Data Source

**PuckAPI (default):** Use `puckapi-tool` endpoints above.

**Your own data:** If user provides a player stats CSV:
1. Verify required columns: `player_name`, `team`, `gp`, `goals`, `assists`, `points`, `season`
2. Compute per-game rates if not already present
3. Flag players with fewer than 20 GP -- small sample, caveat results
4. Note: credits are not consumed when working with user's own data

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Player search | 2 | Name to ID resolution |
| Single player bio/stats | 5 | Per player |
| Three-season comparison | 17 | 1 search (2cr) + 3 stat pulls (5cr each) |
| Roster snapshot (full team) | ~125 | 25 players x 5 credits; use selectively |
| Two-player comparison | 14 | 2 searches (2cr each) + 2 stat pulls (5cr each) |

**Cost note:** Roster-wide pulls get expensive fast. If the user wants "top scorers," ask how many before pulling all 23 players.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "He has 30 goals -- that's great" | Context missing: 30 goals in 50 GP is exceptional; 30 in 82 is average | Always present goals/GP alongside raw totals |
| "The AHL player has great numbers, he's ready" | AHL stats without NHLe translation are not NHL projections | Apply NHLe factor (0.38) before drawing conclusions |
| "Points are the only thing that matters" | Defensive forwards, physicality, and PK contribution are real and point-invisible | Note role context and ice time when known |
| "I'll pull the full roster to find the top scorer" | 25+ API calls for a question that might need 5 | Ask the user how many players they want, or pull a targeted subset |
| "Same points total = same player quality" | Different positions, roles, and team contexts produce the same totals differently | Normalize by position and note TOI/role when available |
| "NHLe works the same for all positions" | Defensemen systematically score fewer points; NHLe undervalues them | Note position when applying NHLe; adjust threshold expectations for D |

## Output Format

### Single player season stats
```
[Player Name] -- [Position] | [Team] | [Season]
GP: [N] | G: [N] | A: [N] | PTS: [N]
Per game: [G/GP] G/GP | [A/GP] A/GP | [PTS/GP] PTS/GP
Shooting: [Sh%]% on [SOG/GP] shots/GP
[Power play split if available]
```

### Multi-season trend
```
[Player Name] -- Season-by-Season
Season | Team | GP | G | A | PTS | PTS/GP
2022-23 | ...
2023-24 | ...
2024-25 | ...
Trend: [improving / declining / stable -- one-sentence note]
```

### Player comparison table
```
              [Player A]    [Player B]
Team          [Team]        [Team]
Position      [Pos]         [Pos]
GP            [N]           [N]
Goals         [N]           [N]
Assists       [N]           [N]
Points        [N]           [N]
PTS/GP        [N]           [N]
Sh%           [N]%          [N]%
```

### Prospect NHLe card
```
[Player Name] -- [League] | [Team] | [Season]
Raw: [GP] GP | [PTS] PTS | [PTS/GP] PTS/GP
NHLe factor: [X] ([League])
NHLe projection: [NHLe PTS/GP] PTS/GP | [NHLe PTS] pts over 82 games
Projection tier: [Top line / 2nd line / 3rd line / Depth]
Sample note: [flag if < 40 GP]
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Found a strong player, want goalie on the same team | Check goalie stats separately | `goalie-analysis` |
| Want to build a player scoring model | Encode per-game rates as features | `feature-engineering` |
| Prospect NHLe looks ready, want team context | Check where they'd fit on the roster | `team-analysis` |
| Player stats for prop bet modeling | Model player outcomes vs. posted props | `prop-modeling` |
| Want WAR or composite player value | Run full value decomposition | `war-gar-decomposition` |
| Found a player, want to preview a game they're in | Full game context with odds | `game-preview` |
