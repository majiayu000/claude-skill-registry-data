---
name: odds-explorer
description: "Multi-book odds comparison, best price identification, vig calculation, line shopping, and line movement analysis for NHL. Use when user asks about current odds, best line, which book has the best price, how lines have moved, sharp money, steam moves, or sportsbook comparison. Do not use for devigging or implied probability math -- see odds-analysis. Do not use for comparing model output vs market -- see edge-detection. Do not use for game results -- see game-lookup."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Odds Explorer

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_odds` for current multi-book odds (10 credits per game).
> Use `get_line_movement` for opening-to-closing line history (25 credits per game).
> For historical odds in a backtest, see `backtesting` -- costs 10 credits per game.

You are an expert in sports betting markets. Your goal is to help users find the best available price, understand what vig they're paying, and read line movement for market signals.

## When to Use

- Finding the best moneyline, spread, or total price across books for a specific game
- Calculating vig and understanding what you're giving up
- Identifying which book consistently has the best price on a team or market type
- Tracking how a line moved from open to current, and what that signals
- Explaining American odds to a new user

## When NOT to Use

- Devigging odds to get true implied probabilities -- see `odds-analysis`
- Comparing model probability vs market price to find edge -- see `edge-detection`
- Looking up final scores or game results -- see `game-lookup`
- Historical odds for backtesting -- see `backtesting`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_odds` | Current odds across all books for one game | 10 |
| `get_line_movement` | Full opening-to-closing line history for one game | 25 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_live_odds` | Use `get_odds` with today's date -- data reflects current available lines |
| `get_historical_lines` | Use `backtesting` skill with `get_odds` for past dates |
| `get_best_book` | Derive from `get_odds` output by comparing all returned books |
| `get_public_betting_percentage` | Not available -- infer from line movement direction using `get_line_movement` |
| `get_closing_line` | Use `get_line_movement` -- closing line is the final entry in the movement log |

## Season Resolution

- October through December: current calendar year is the season start (2026-27 season)
- January through September: previous calendar year is the season start (2025-26 season)
- NHL regular season: October to April. Playoffs: April to June.
- "Tonight's games" = games with today's date

## Sportsbook Abbreviations

| Abbreviation | Book |
|-------------|------|
| DK | DraftKings |
| FD | FanDuel |
| MGM | BetMGM |
| ESPN | ESPN BET |
| CZAR | Caesars |
| PINN | Pinnacle |
| BET365 | Bet365 |
| HARD | Hard Rock Bet |
| BARSTOOL | Barstool / Penn |
| POINTS | PointsBet |

## Initial Assessment

Before starting, understand:
1. Which game or slate? (One game, all games tonight, a specific team)
2. Which market? (Moneyline, puck line, total, or all three)
3. Is line movement needed, or just current best price? (10cr vs 25cr decision)

## How It Works

**Step 1: Confirm game identity**

If the user asks about a team or matchup without a specific game ID, call `get_schedule` (2 credits) to get the game ID first. This prevents pulling odds for the wrong game.

**Step 2: Pull current odds**

Call `get_odds` for the target game(s). Returns odds from all available books.

**Step 3: Find the best price**

For each market type (ML, spread, total):
- Identify the best price for each side independently
- A bettor on the home team should look at home ML across all books
- Best price = highest moneyline number for favorites (less negative), highest for underdogs (more positive)

**Step 4: Calculate vig**

Vig = the juice the book charges. Formula for a two-sided market:

```
Implied prob home = 1 / (1 + 10^(home_ml / 100))  [if favorite, negative ml]
Implied prob away = 1 / (1 + 10^(-away_ml / 100)) [if underdog, positive ml]
Vig = (implied_home + implied_away - 1) x 100%
```

Standard vig is ~4.5% on moneylines. Reduced-juice books (Pinnacle) run ~2-2.5%. Show the vig so users know what they're paying.

**Step 5: Line movement (if requested)**

Call `get_line_movement`. Parse the movement log:
- Opening line vs. current line
- Direction: did the line move toward or away from the favorite?
- Magnitude: moves of 1.5+ points on spreads, or 10+ cents on MLs, are significant
- Reverse line movement: line moves against majority of public bets = sharp money indicator
- Steam move: sudden, fast movement across multiple books within minutes = coordinated sharp action

**Step 6: Present findings**

Lead with the actionable insight (best price, significant movement), then show the full table. Do not bury the lede in a table with no interpretation.

## Reading American Odds (Teach This)

When a user appears unfamiliar with American odds format:

- **Negative odds** (-150): bet $150 to win $100. The team is favored.
- **Positive odds** (+130): bet $100 to win $130. The team is the underdog.
- **Even money** (+100 or -100): equal risk and reward.
- **Converting to implied probability:** -150 = 60% chance. +130 = 43.5% chance.
- The two sides of a market add up to more than 100% -- that's the vig.

## Data Source

**PuckAPI (default):** Use `get_odds` and `get_line_movement`. Data covers major US sportsbooks.

**Your own odds data:** If user provides a CSV of odds:
1. Verify columns: `game_id`, `book`, `market` (ML/spread/total), `home_odds`, `away_odds`, `timestamp`
2. Check timestamp format -- line movement analysis requires chronological ordering
3. Credits are not consumed when using own data

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Odds snapshot (one game) | 10 | All books, all markets |
| Line movement (one game) | 25 | Full open-to-close history |
| Odds for full tonight's slate | 10 x N games | 15-game NHL night = 150 credits |
| Line movement for full slate | 25 x N games | Use selectively; most expensive call |
| Schedule lookup (game ID) | 2 | Do this first if no game ID |

**Credit guidance:** For a single-game best-price lookup, total cost is 10-12 credits. For a sharp-money analysis with movement, 35 credits. Do not pull line movement on entire slates without user awareness of the cost.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "All books have similar prices, doesn't matter" | 1-3% ROI difference is the margin between profitable and losing | Show the spread; let the user decide it doesn't matter |
| "Line moved toward favorites, so bet favorites" | Line movement direction alone is not a signal -- volume matters | Show magnitude and speed; flag if it looks like sharp vs public |
| "Pinnacle is always best" | Pinnacle has the sharpest lines but often limited US availability and no bonuses | Include it as a reference line; note availability caveat |
| "The vig is small, ignore it" | Paying 4.8% vig vs 2.5% costs $2,300 per $100k wagered | Always show vig; it compounds over a season |

## Output Format

**Best price output:**
```
[Away Team] @ [Home Team] -- [Date]

Moneyline Best Prices:
  [Away Team]: +XXX @ [BOOK] | Range: +XXX (BOOK) to +XXX (BOOK)
  [Home Team]: -XXX @ [BOOK] | Range: -XXX (BOOK) to -XXX (BOOK)
  Market vig: X.X% (avg across books)

Puck Line (±1.5):
  [Away Team] +1.5: -XXX @ [BOOK]
  [Home Team] -1.5: +XXX @ [BOOK]

Total (O/U X.5):
  Over: -XXX @ [BOOK]
  Under: -XXX @ [BOOK]
```

**Line movement output:**
```
Line Movement -- [Away] @ [Home]

Moneyline:
  Open:    [Away] +XXX / [Home] -XXX  ([Time])
  Current: [Away] +XXX / [Home] -XXX  ([Time])
  Move:    [Away] moved X cents [toward/away from] favorite

Notable moves:
  [Time]: Sharp move -- [description of fast multi-book movement]

Signal: [Sharp money on Home / Public on Away / No clear signal]
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Best price identified | Convert to true probability, remove vig | `odds-analysis` |
| Have a model probability | Compare model vs market to find edge | `edge-detection` |
| Want full game context before betting | Game preview with team and goalie data | `game-preview` |
| Sharp movement on a game | Research why -- check injury reports and team context | `game-lookup` |
| Want to track bets placed | Log with best price taken | `bet-tracker` |
