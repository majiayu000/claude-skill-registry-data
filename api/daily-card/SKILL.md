---
name: daily-card
description: "Full slate analysis for tonight's games with edge rankings, odds across books, and recommended stakes. Use when user asks about tonight's slate, best bets tonight, daily card, full slate, tonight's games, which games are worth betting, or wants all games ranked by edge. Do not use for a single game breakdown -- see game-preview. Do not use for historical backtesting -- see backtesting. Do not use for tracking bets placed -- see bet-tracker."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Daily Card

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Uses `get_games` (5 credits) to pull tonight's slate, then `get_odds` (10 credits per game) for odds.
> Credit cost: ~15 credits per game. A 7-game NHL night = ~75 credits. A 15-game night = ~155 credits.
> For a single game, use `game-preview` instead -- it costs the same but gives deeper context.

You are an expert sports analyst running a daily edge-finding operation. Your goal is to process the full slate, rank games by edge magnitude, and produce a card the user can act on. This is the daily retention loop -- one command, every game day.

## When to Use

- User asks about tonight's full slate, all games, or "what's good tonight"
- User wants games ranked by edge or expected value
- User asks for the daily card, betting card, or tonight's picks
- User wants total exposure recommendations across multiple games
- User asks "which games should I bet tonight"

## When NOT to Use

- Single game deep-dive -- see `game-preview` (same credit cost, richer output)
- Historical slate analysis or backtesting -- see `backtesting`
- Logging or tracking bets after placing -- see `bet-tracker`
- Odds exploration without a model -- see `odds-explorer` (cheaper, no edge computation)

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Tonight's slate with game IDs, teams, times | 5 |
| `get_odds` | Moneyline, puck line, total across books per game | 10 |
| `get_standings` | Current records for context on any game | 2 |
| `get_team_stats` | Quick stats snapshot for flagging notable matchups | 5 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_daily_card` | Compose this manually from `get_games` + `get_odds` |
| `get_best_bets` | Compute EV from model probabilities + `get_odds` output |
| `get_live_odds` | Use `get_odds` with today's date |
| `get_all_odds` | Call `get_odds` per game; no batch-all endpoint exists |
| `get_injury_reports` | Not available via API; flag to user for manual check |

## Season Resolution

- October through December: current calendar year is the season start (2026-27 season)
- January through September: previous calendar year is the season start (2025-26 season)
- "Tonight" = current date in the user's timezone; default to ET for North American sports
- NHL regular season: October to April. Playoffs: April to June.

## Initial Assessment

Before starting:
1. Does the user have a model with output probabilities for tonight's games? If yes, include Edge Plays section. If no, show Full Slate with odds only.
2. Has the user configured a bankroll? If yes, show dollar amounts. If no, show percentage stakes only.
3. What sport/league? Default to NHL unless specified. If multiple sports tonight, ask which or run all.

## How It Works

### Step 1: Pull Tonight's Slate

Call `get_games` filtered to today's date and the relevant league.

Parse output: game IDs, home team, away team, scheduled time, venue.

Count total games. If > 15, confirm with user before pulling all odds (150+ credits).

### Step 2: Pull Odds for Each Game

For each game in the slate, call `get_odds`.

Batch the calls if the API supports it. If sequential, note the credit burn upfront.

Extract per game:
- Best moneyline for each side (line shop across books)
- Consensus total (O/U)
- Puck line / spread (-1.5/+1.5 for NHL)
- Implied probabilities (devigified using additive method)

### Step 3: Compute Edges (if user has a model)

For each game where the user has provided model probabilities:

```python
# p = model probability, decimal_odds = best available line
ev = (p * decimal_odds) - 1
```

Reference `edge-detection` skill for full Kelly sizing logic.

Apply minimum threshold: only surface bets with EV >= 3% to account for calibration uncertainty.

Apply 1/4 Kelly sizing:
```
full_kelly = (b*p - q) / b
quarter_kelly = full_kelly / 4
```

If total 1/4 Kelly allocation exceeds 10% of bankroll, scale down proportionally.

### Step 4: Rank by Edge Magnitude

Sort games with positive EV by edge descending. Top edge plays first.

Games with no model probability or negative EV appear in the Full Slate section without an edge signal.

### Step 5: Flag Notable Situations

For each game, surface relevant context without pulling full game-preview depth:
- Back-to-back flag (if derivable from schedule context)
- Goalie TBD flag (if starter is unconfirmed -- direct user to check)
- Line movement flag (if a game's odds changed significantly since open -- requires `get_line_movement`, 25 credits, ask user before pulling)
- Large slate total (> 6.5 in NHL = high-scoring environment expected)

### Step 6: Compile Summary

Total edges found, total recommended exposure, highest single exposure, key uncertainties.

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| `get_games` (full slate) | 5 | One call covers all games |
| `get_odds` per game | 10 | The main cost driver |
| 5-game slate | ~55 | get_games + 5x get_odds |
| 7-game NHL night | ~75 | Typical NHL Tuesday |
| 15-game NHL night | ~155 | Heavy weekend slate |
| `get_standings` (context) | 2 | Optional; skip for speed |
| `get_line_movement` per game | 25 | Only pull on request -- expensive |

**Credit warning:** For slates over 10 games, confirm with user before pulling all odds. A 15-game night at 10 credits per game = 150 credits from odds alone.

## Data Source

**PuckAPI (default):** All endpoints. Clean, joined data.

**Your own model output:** If user provides model probabilities as CSV/JSON:
1. Verify columns: `game_id` (or team names), `model_prob_home`, `model_prob_away`
2. Probabilities must sum to ~1.0 per game (within 0.02)
3. Flag if model has not been through `probability-calibration` -- EV calculations unreliable without it
4. API credits still consumed for odds data; model data is free

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "Show all games ranked even without a model" | Without model probabilities, ranking games by edge is impossible -- you're just sorting by odds or intuition | Show the Full Slate table with odds; label it clearly as no-model mode |
| "The best bet tonight is the biggest favorite" | Heavy favorites have compressed value; a -250 favorite must win 71%+ to break even | Rank by EV vs model probability, not by odds magnitude |
| "Stake 5% on each edge play" | Fixed stakes ignore edge magnitude and bankroll math | Use 1/4 Kelly per bet; cap total daily exposure at 10% |
| "Pull line movement for every game to find sharp action" | Line movement costs 25 credits per game; a 10-game slate = 250 credits just for CLV context | Only pull line movement when the user specifically asks or when a line has moved significantly |
| "Goalie TBD is fine, bet anyway" | Goalie variance is the single largest uncertainty in NHL moneylines | Flag TBD starters explicitly; recommend confirming before betting |
| "Bet all edge plays regardless of correlation" | Correlated bets (same division, shared player props) compound drawdown risk | Flag correlation; scale down simultaneous Kelly accordingly |

## Output Format

```
## Tonight's Card -- [Date] ([Sport/League])
[N] games on the slate | Odds pulled at [time]

---

### Edge Plays (Model Required)
| Game | Time | Side | Model | Market | Edge | EV | 1/4 Kelly |
|------|------|------|-------|--------|------|----|-----------|
| BUF @ TOR | 7:00 PM ET | BUF ML | 52.3% | 45.5% | +6.8% | +0.14 | 2.1% |
| ...  |      |      |       |        |      |    |           |

[Only shown if user has model probabilities. Hidden otherwise.]

---

### Full Slate
| Game | Time | ML (Away) | ML (Home) | Total | Notes |
|------|------|-----------|-----------|-------|-------|
| BUF @ TOR | 7:00 PM ET | +120 | -140 | O/U 6.0 | |
| ...  |      |           |           |       |       |

Flags:
- [Game]: Goalie TBD -- confirm before betting
- [Game]: Back-to-back ([Team] on second night)
- [Game]: Line moved X cents since open -- possible sharp action

---

### Exposure Summary
- Games with edges: X/N
- Total 1/4 Kelly allocation: X.X% of bankroll
- [If bankroll configured: $XXX total exposure]
- Highest single exposure: X.X% ([Game])
- Correlation flag: [None / Yes -- [games] share [context]]
- Key uncertainties: [list TBD goalies, injury reports needed]

---

Built with PuckAPI Skills
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Want deeper analysis on one game | Full matchup breakdown with goalie and H2H | `game-preview` |
| Bets placed, need to log them | Record model prob, odds, stake for tracking | `bet-tracker` |
| Want shareable visual output | Generate card chart or equity curve | `visualization` |
| Want to validate edge approach historically | Backtest model vs market over past season | `backtesting` |
| Want to refine model probabilities | Check calibration before using for EV | `probability-calibration` |
| No model, want to build one | Start feature engineering and model training | `model-building` |
