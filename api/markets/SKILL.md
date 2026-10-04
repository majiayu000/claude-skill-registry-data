---
name: markets
description: |
  Markets orchestration — connects ESPN live schedules with Kalshi and Polymarket prediction markets. Unified dashboards, odds comparison, entity search, and bet evaluation across platforms.

  Use when: user wants to see prediction market odds alongside ESPN game schedules, compare odds across platforms, search for a team/player on Kalshi or Polymarket, check for arbitrage between ESPN odds and prediction markets, or evaluate a specific game's market value.
  Don't use when: user wants raw prediction market data without ESPN context — use polymarket or kalshi directly. For pure odds math (conversion, de-vigging, Kelly) — use betting. For live scores without market data — use the sport-specific skill.
license: MIT
metadata:
  author: machina-sports
  version: "0.2.0"
---

# Markets Orchestration

Bridges ESPN live schedules (NBA, NFL, MLB, NHL, WNBA, CFB, CBB) with Kalshi and Polymarket prediction markets. Before writing queries, consult `references/api-reference.md` for supported sport codes, command parameters, and price normalization formats.

## Quick Start

```bash
sports-skills markets get_todays_markets --sport=nba
sports-skills markets search_entity --query="Lakers" --sport=nba
sports-skills markets compare_odds --sport=nba --event_id=401234567
sports-skills markets get_sport_markets --sport=nfl
sports-skills markets get_sport_schedule --sport=nba
sports-skills markets normalize_price --price=0.65 --source=polymarket
sports-skills markets evaluate_market --sport=nba --event_id=401234567
```

Python SDK:
```python
from sports_skills import markets

markets.get_todays_markets(sport="nba")
markets.search_entity(query="Lakers", sport="nba")
markets.compare_odds(sport="nba", event_id="401234567")
markets.get_sport_markets(sport="nfl")
markets.get_sport_schedule(sport="nba", date="2025-02-26")
markets.normalize_price(price=0.65, source="polymarket")
markets.evaluate_market(sport="nba", event_id="401234567")
```

## CRITICAL: Before Any Query

CRITICAL: Before calling any orchestration command, verify:
- A `sport` code is provided for sport-aware commands (`get_todays_markets`, `compare_odds`, `get_sport_markets`, `evaluate_market`).
- Price sources are identified correctly before normalization: `espn` = American odds, `polymarket` = 0-1 probability, `kalshi` = 0-100 integer.

## Important Notes

- **Sport context is passed through.** `--sport=nba` maps automatically to the correct Polymarket sport code and Kalshi series ticker.
- **Both platforms use sport-aware search.** Polymarket uses `sport` → series_id; Kalshi uses `KXNBA`, `KXNFL`, etc.
- **Prices are normalized.** Everything is converted to implied probability for comparison.

## Workflows

### Today's NBA Dashboard

```bash
sports-skills markets get_todays_markets --sport=nba
```
Returns each game with ESPN info, DraftKings odds, matching Kalshi markets, and matching Polymarket markets.

### Find Arb on a Specific Game

1. Get the ESPN event ID: `get_sport_schedule --sport=nba`
2. Compare odds: `compare_odds --sport=nba --event_id=<id>`
3. If arbitrage detected, response includes allocation percentages and guaranteed ROI.

### Full Bet Evaluation

1. `evaluate_market --sport=nba --event_id=<id>`
2. Fetches ESPN odds and matching prediction market price
3. Pipes through `betting.evaluate_bet`: devig → edge → Kelly
4. Returns fair probability, edge, EV, Kelly fraction, and recommendation

## Examples

Example 1: Today's games with prediction market odds
User says: "What NBA games are on today and what are the prediction market odds?"
Actions:
1. Call `get_todays_markets(sport="nba")`
Result: Unified dashboard with each game's ESPN info and Kalshi/Polymarket prices

Example 2: Cross-platform team search
User says: "Find me Lakers markets on Kalshi and Polymarket"
Actions:
1. Call `search_entity(query="Lakers", sport="nba")`
Result: All Lakers markets across both exchanges with prices and volume

Example 3: Odds comparison for a specific game
User says: "Compare the odds for this Celtics game across ESPN and Polymarket"
Actions:
1. Get event_id from `get_sport_schedule(sport="nba")`
2. Call `compare_odds(sport="nba", event_id="<id>")`
Result: Normalized side-by-side comparison with automatic arbitrage check

Example 4: Full market evaluation
User says: "Is there edge on the Chiefs game?"
Actions:
1. Get event_id from `get_sport_schedule(sport="nfl")`
2. Call `evaluate_market(sport="nfl", event_id="<id>")`
Result: Fair probability, edge percentage, EV, Kelly fraction, and bet recommendation

Example 5: Browse all markets for a sport
User says: "Show me all NFL prediction markets"
Actions:
1. Call `get_sport_markets(sport="nfl")`
Result: All open NFL markets across Kalshi and Polymarket

Example 6: Price conversion
User says: "Convert a Polymarket price of 65 cents to American odds"
Actions:
1. Call `normalize_price(price=0.65, source="polymarket")`
Result: Common structure with implied probability (0.65), American odds (-185.7), and decimal (1.54)

## Commands that DO NOT exist — never call these

- ~~`get_odds`~~ — does not exist. Use `compare_odds` to see odds across sources.
- ~~`search_markets`~~ — does not exist on the markets module. Use `search_entity` instead.
- ~~`get_schedule`~~ — does not exist. Use `get_sport_schedule` instead.

If a command is not listed in `references/api-reference.md`, it does not exist.

## Troubleshooting

Error: No markets returned for a sport
Cause: Sport code may be missing or incorrect
Solution: Check `references/api-reference.md` for valid sport codes. Use the exact code (e.g., `nba`, `epl`, `laliga`)

Error: `compare_odds` returns no data for an event
Cause: The event_id is incorrect or the game has not been indexed yet
Solution: Call `get_sport_schedule(sport=...)` to retrieve the correct event_id first

Error: One source shows warnings in the response
Cause: Kalshi or Polymarket is temporarily unavailable
Solution: The module returns partial results — use what is available. Retry the unavailable source separately using the kalshi or polymarket skill directly

Error: `normalize_price` returns unexpected American odds value
Cause: Wrong `source` parameter — Kalshi uses 0-100 integers, Polymarket uses 0-1 decimals
Solution: Verify the source. Kalshi price of 65 requires `source="kalshi"`, Polymarket price of 0.65 requires `source="polymarket"`
