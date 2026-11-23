---
name: game-preview
description: "Complete pre-game analysis for a single NHL (or other sport) matchup: team records, goalie matchup, key stats, odds snapshot, model edge, and head-to-head history in one shareable report. Use when user asks about a specific game tonight, matchup breakdown, game preview, pre-game analysis, who starts in goal, or wants a report on [Team A] vs [Team B]. Do not use for full slate analysis -- see daily-card. Do not use for odds-only lookup -- see odds-explorer. Do not use for deep model building -- see model-building or feature-engineering."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Game Preview

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Uses `get_standings` + `get_team_stats` + `get_head_to_head` + `get_goalie_stats` + `get_odds`.
> Credit cost per preview: ~34 credits (2+5+10+5+10+2).
> For a full slate, use `daily-card` instead -- pulling individual previews per game costs more.

You are an expert sports analyst. Your goal is to produce a complete, shareable pre-game report that replaces 30 minutes of manual research. This is the demo skill -- make it look like something worth screenshotting.

## When to Use

- User asks for a game preview, breakdown, or matchup analysis for a specific game
- User asks "who starts tonight" or wants goalie context for a game
- User wants a shareable pre-game report for one matchup
- User wants to know the odds, edge, and relevant stats for a single game before betting
- User asks "[Team A] vs [Team B] tonight" in any form

## When NOT to Use

- Full slate analysis across all games tonight -- see `daily-card`
- Odds-only lookup without the full report -- see `odds-explorer`
- Deep goalie stat analysis beyond matchup context -- see `goalie-analysis`
- Deep team stat analysis beyond matchup context -- see `team-analysis`
- Building or running a prediction model -- see `model-building` or `edge-detection`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_standings` | Current records, division standings, points percentage | 2 |
| `get_team_stats` | 5v5 metrics, special teams, home/away splits | 5 |
| `get_head_to_head` | Season series + last 5-10 historical meetings | 10 |
| `get_goalie_stats` | Probable starter stats, SV%, GAA, recent form | 5 |
| `get_odds` | Moneyline, puck line, total across books | 10 |
| `get_schedule` | Confirm game time, rest days, back-to-back status | 2 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_game_preview` | Compose this manually from the 6 calls above |
| `get_starter` | Use `get_goalie_stats` + `get_game_detail`; note pregame starters require beat reporter sources |
| `get_live_odds` | Use `get_odds` with today's date |
| `get_injury_report` | Not available via API; direct user to team injury report feeds |
| `get_rest_days` | Derive from `get_schedule` using game dates |

## Season Resolution

- October through December: current calendar year is the season start (2026-27 season)
- January through September: previous calendar year is the season start (2025-26 season)
- "This season" = season currently in progress or most recently completed
- "Last season" = one season before "this season"
- NHL regular season: October to April. Playoffs: April to June.

## Initial Assessment

Before starting, understand:
1. Which two teams? Confirm spelling and current team names (relocations happen).
2. Does the user have a model? If yes, include the Model Edge section. If no, skip it.
3. What is the game date? Default to today unless specified.

## How It Works

Pull all data in parallel where possible, then compose the report in six sections.

### Step 1: Matchup Context

Call `get_standings` for both teams. Pull:
- Current record (W-L-OTL), points, points percentage
- Division rank and conference rank
- Recent form: last 10 games record (W-L-OTL in last 10 if available, else compute from game log)
- Rest status: derive from `get_schedule` -- days since last game, back-to-back flag

Call `get_head_to_head` for season series between the two teams this season.

### Step 2: Goalie Matchup

Call `get_goalie_stats` for both teams' likely starters.

Pull: GP, GS, W-L-OTL, SV%, GAA, SO, last 5 starts SV%.

If both goalies have faced each other: pull from `get_head_to_head` output.

Note: the API shows post-game confirmed starters only. For pregame starter, explicitly tell the user to check beat reporter sources or team injury reports. Do not guess or fabricate a starter.

Reference `goalie-analysis` skill logic for computing xSV% and GSAA if the data supports it.

### Step 3: Key Stats Comparison

Call `get_team_stats` for both teams. Pull and compare:

| Metric | Home Team | Away Team |
|--------|-----------|-----------|
| Corsi% | | |
| Fenwick% | | |
| Goals For per game | | |
| Goals Against per game | | |
| Expected Goals For | | |
| Expected Goals Against | | |
| Goal Differential | | |
| Points Percentage | | |

Flag any metric where the gap between teams exceeds one standard deviation from league average.

### Step 4: Odds Snapshot

Call `get_odds` (10 credits). Pull moneyline, puck line (-1.5/+1.5), and total (Over/Under) across all available books.

Show:
- Best available moneyline for each side (line shop)
- Consensus total (most common line)
- Implied probabilities (devigified from the consensus line)

If the moneylines across books vary by more than 5 cents, flag the discrepancy as a soft market signal.

### Step 5: Model Edge (conditional)

Only include if the user has provided model probabilities.

Compute EV against best available line using `edge-detection` skill logic:
```
ev = (model_prob * decimal_odds) - 1
```

Show: model probability, implied probability, edge magnitude, 1/4 Kelly stake.

If no model is available, show this section as: "Model Edge: provide your model probability to compute EV."

### Step 6: Head-to-Head History

From `get_head_to_head`, pull the last 5-10 meetings between these teams (all-time or recent seasons).

Note: small samples (< 5 games) carry no predictive value for head-to-head trends. State this explicitly rather than over-interpreting 2-3 games.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_standings` (both teams) | 2 | One query covers both |
| `get_team_stats` (both teams) | 5 | One query covers both |
| `get_head_to_head` | 10 | Season series + history |
| `get_goalie_stats` (both teams) | 5 | One query covers both |
| `get_odds` | 10 | Tied for most expensive with H2H |
| `get_schedule` (rest check) | 2 | Optional; skip if user knows dates |
| **Total per preview** | **~34** | Skip `get_odds` and `get_head_to_head` for 14-credit version |

## Data Source

**PuckAPI (default):** All six endpoints. Data is clean and joined.

**Your own data:** If user provides team/goalie stats as CSV:
1. Verify columns: team names, record fields (W, L, OTL), SV%, GAA, corsiPct, fenwickPct, goalsForPerGame, goalsAgainstPerGame
2. For odds: user must provide manually or use `get_odds`
3. Credits only consumed for the API calls made; own-data sections are free

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "The goalie starting tonight is X" | Pregame starters are not in the API | State the last confirmed starter and direct user to beat reporter for pregame confirmation |
| "Team A has won 4 of the last 5 H2H meetings" | 5 H2H games over 2+ seasons is noise, not a trend | Report the data, note the small sample, do not interpret as a meaningful edge |
| "The odds haven't moved so the sharp money is neutral" | Lack of line movement is not confirmation of neutrality | Report the current lines; absence of movement is absence of signal, not neutrality |
| "Skip the stats and just give the pick" | A pick without context is gambling, not analysis | Always include the data that supports or contradicts any directional conclusion |

## Output Format

```
## Game Preview: [Away Team] @ [Home Team]
[Date] | [Arena] | [Time]

---

### Matchup Context
[Away] Record: XX-XX-XX | Pts%: .XXX | Div Rank: X | Last 10: X-X-X
[Home] Record: XX-XX-XX | Pts%: .XXX | Div Rank: X | Last 10: X-X-X
Rest: [Away] X days | [Home] X days [BACK-TO-BACK flag if applicable]
Season Series: [Away] X – [Home] X

---

### Goalie Matchup
[Away] Likely Starter: [Name] | SV%: .XXX | GAA: X.XX | Last 5: .XXX
[Home] Likely Starter: [Name] | SV%: .XXX | GAA: X.XX | Last 5: .XXX
Note: Pregame starters unconfirmed -- check beat reporter sources.

---

### Key Stats Comparison
| Metric        | [Away] | [Home] |
|---------------|--------|--------|
| Corsi%        | XX.X%  | XX.X%  |
| Fenwick%      | XX.X%  | XX.X%  |
| GF/game       | X.XX   | X.XX   |
| GA/game       | X.XX   | X.XX   |
| xGF           | X.XX   | X.XX   |
| xGA           | X.XX   | X.XX   |
| Goal Diff     | +/-N   | +/-N   |

---

### Odds Snapshot
Moneyline: [Away] [+/-XXX] | [Home] [+/-XXX] (best available)
Puck Line: [Away] +1.5 [odds] | [Home] -1.5 [odds]
Total: O/U X.X [odds]
Implied (devigified): [Away] XX.X% | [Home] XX.X%

---

### Model Edge
[If model provided]
Model: [Away] XX.X% | [Home] XX.X%
Market: [Away] XX.X% | [Home] XX.X%
Edge: [Side] +X.X% EV | 1/4 Kelly: X.X% of bankroll
[If no model]
Provide your model probability to compute EV.

---

### Head-to-Head History (Last N meetings)
| Date | Winner | Score | Notes |
|------|--------|-------|-------|

---

Built with PuckAPI Skills
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Want to see the full slate tonight | Full card with edge rankings across all games | `daily-card` |
| Have a model and want to confirm EV | Compute edge, Kelly sizing, significance | `edge-detection` |
| Want to dig deeper on the goalie matchup | Leaderboard context, xSV%, workload flags | `goalie-analysis` |
| Want shareable visual output | Generate matchup card chart | `visualization` |
| Want to bet and track performance | Log this bet after placing | `bet-tracker` |
| Want deeper team metrics | Full 5v5, special teams, shot quality breakdown | `team-analysis` |
