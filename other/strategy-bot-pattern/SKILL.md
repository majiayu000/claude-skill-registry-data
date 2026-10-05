---
name: strategy-bot-pattern
description: Build automated strategy bots that make decisions against live data feeds in gamified challenge systems
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [strategy-bots, automated-trading, gamification, decision-agents]
    triggers:
      - "build automated bots"
      - "strategy bots"
      - "test trading strategies"
      - "automated decision agents"
      - "bot competition platform"
    related_skills: [pokemon-player, a betting-pipeline skill]
---
# Strategy Bot Pattern

Build automated decision-making bots that compete against live data feeds
in gamified challenge systems (e.g., $100→$10M bankroll challenge, trading
competitions, prediction markets).

## Architecture

```
strategies/
├── __init__.py        # Module init, exports
├── base.py            # BaseStrategy + StrategyDecision dataclass
├── engine.py          # Singleton engine, auto-loads bots from DB
├── data.py            # Data layer: fetch + normalize live data
├── display.py         # Dashboard formatting helpers
├── register_bots.py   # Registration script (DB + challenge.json)
├── run_bots.py        # Runner: register → fetch → decide → execute
└── bots/              # Individual strategy implementations
    ├── *_bot.py       # Each bot = one file, one class
    └── ...
```

### Base Strategy Contract

Every bot inherits from `BaseStrategy` and implements:

```python
class MyBot(BaseStrategy):
    @property
    def description(self) -> str:
        return "Human-readable strategy description"

    def decide(self, odds_data: Dict[str, List[Dict]], bankroll: float) -> List[StrategyDecision]:
        """Analyze live data and return bet decisions.
        
        Args:
            odds_data: {sport_name: [game_dicts]} — odds already normalized to American
            bankroll: Current bankroll
        Returns:
            List of StrategyDecision (empty = no bets this cycle)
        """
        ...
```

### StrategyDecision dataclass

```python
@dataclass
class StrategyDecision:
    sport: str
    game: str
    external_game_id: str
    pick: str
    selection: str
    odds: int            # American odds
    wager: float
    confidence: int      # 1-10
    reasoning: str       # Explain why (stored in DB)
    strategy_name: str
    bot_username: str
    timestamp: str
```

### Engine Singleton Pattern

Engine auto-loads bots from `challenge_participants` table on first use:

```python
from strategies.engine import get_engine
engine = get_engine()
engine.register_bot(MyBot(username="my_bot", display_name="My Bot", bankroll=100.0))
decisions = engine.run_all()       # Fetch live odds → call decide() on all bots
bets = engine.execute_decisions()  # Log to DB, update internal state
```

`_ensure_bots_loaded()` queries `SELECT user_id, display_name, current_units FROM challenge_participants WHERE user_id LIKE 'prefix_%'` and instantiates the correct bot class via a `BOT_CLASSES` mapping dict.

## Odds Format Handling

**The Odds API returns decimal odds**, not American. Convert before passing
to bot logic:

```python
def decimal_to_american(dec: float) -> Optional[int]:
    if dec >= 2.0:
        return int(round((dec - 1) * 100))
    else:
        return int(round(-100 / (dec - 1)))
```

| Decimal | American |
|---------|----------|
| 1.01    | -10000   |
| 1.25    | -400     |
| 1.44    | -227     |
| 2.0     | +100     |
| 2.7     | +170     |
| 3.0     | +200     |
| 5.0     | +400     |
| 10.0    | +900     |

Apply this conversion in the data layer so bot logic always sees American odds.

## Bankroll Tracking & Settlement

Each bot has a running bankroll. After every bet (win, loss, or push) the
bankroll is updated. This is the core settlement math.

### Payout Formula

For a wager at **American odds**:

| Odds | Profit | Payout (returned to bettor) |
|------|--------|----------------------------|
| **Positive** (+200) | `Wager × Odds / 100` | `Wager + Profit` |
| **Negative** (-150) | `Wager × 100 / \|Odds\|` | `Wager + Profit` |

### Settlement — One Function

```python
def settle_bet(wager: float, odds: int, won: bool, pushed: bool = False) -> float:
    \"\"\"Return net P/L for a single bet. Positive = profit, negative = loss.\"\"\"
    if pushed:
        return 0.0
    if not won:
        return -wager
    # Win — calculate profit
    if odds > 0:
        profit = wager * odds / 100
    else:
        profit = wager * 100 / abs(odds)
    return round(profit, 2)
```

### "Is the original stake returned?" — The Common Confusion

**Yes, it is.** The formula looks like it only tracks profit, but it's
algebraically identical to returning the stake. Here's why:

```
payout = wager + profit      ← full amount returned on a win
profit = payout - wager      ← what settle_bet() returns
bankroll += profit            ← the bankroll update

bankroll + profit = bankroll + (payout - wager) = (bankroll - wager) + payout
```

Both approaches produce the same final bankroll:

| Step | `bankroll += profit` (implicit) | `bankroll - wager + payout` (explicit) |
|------|--------------------------------|----------------------------------------|
| Start | $100.00 | $100.00 |
| Wager deducted | *(implicit)* | $100.00 − $32.50 = $67.50 |
| Win returned | $100.00 + $25.00 = **$125.00** | $67.50 + $57.50 = **$125.00** |

### Worked Examples

| Scenario | Wager | Odds | Outcome | `pl` | Bankroll update |
|----------|-------|------|---------|------|-----------------|
| Fave win | $32.50 | -130 | WIN | +$25.00 | $100 → $125 |
| Fave loss | $32.50 | -130 | LOSS | −$32.50 | $100 → $67.50 |
| Dog win | $20.00 | +200 | WIN | +$40.00 | $100 → $140 |
| Push | $20.00 | +200 | PUSH | $0.00 | $100 → $100 |

### Multi-Bet Sequencing

When a bot places multiple bets in the same cycle (e.g. 3 picks in
one week), settle them sequentially. Each bet's bankroll update feeds
the next bet's wager calibration:

```python
bankroll = 100.0
for bet in decisions:
    result, pl = settle_bet(bet.wager, bet.odds, ...)
    bankroll = round(bankroll + pl, 2)    # ← feeds next bet
    gap = max(0, weekly_target - bankroll)
    # Recalibrate remaining wagers if needed
```

Because `bankroll += profit` and `bankroll - wager + payout` are
algebraically identical, sequential settlement produces the same
bankroll as real sportsbook accounting.

### Pitfalls

- **Don't double-count the stake.** If you return `payout` (wager + profit)
  instead of `profit`, you must also **first deduct** the wager from
  bankroll. Using `bankroll += profit` avoids this entirely — the wager
  is implicitly handled by the formula.
- **Negative odds math.** For -110 odds, profit is `wager × 100/110`, NOT
  `wager × 110/100`. The sign matters.
- **Odds field format.** Some LLMs return odds as strings (`"-110"`).
  Always `float()` the value before arithmetic.
- **Cap at bankroll.** Never let `wager > bankroll` unless you allow
  margin/credit — but for the $100→$10M challenge, the bot busts if it
  over-wagers.
- **Pushes don't affect bankroll.** A push returns the full wager (net
  zero P/L). The bot's bankroll stays unchanged.

**See also:** `references/bankroll-tracking.md` — full algebraic proof,
multi-bet scenarios, and verification against real sportsbook math.

## Data Layer

`strategies/data.py` — fetch live odds from your own API, normalize:

```python
def normalize_odds(game: Dict) -> Dict:
    """Convert decimal ML odds to American in a game dict."""
    for field in ["home_ml", "away_ml"]:
        val = game.get(field)
        if val and 1.0 < float(val) < 100:
            game[field] = decimal_to_american(float(val))
    return game
```

## Registration

Bots must be registered in **two places** for full compatibility:

1. **`challenge_participants` SQLite table** — engine auto-loads from here
2. **`challenge.json`** — `WeeklyChallenge` class reads from here for the leaderboard

The registration script does both.

## API Endpoints

Add these to the FastAPI server:

| Endpoint | Returns |
|----------|---------|
| `GET /api/strategies` | All bot statuses + leaderboard | `week_reached` included |
| `GET /api/strategies/bets` | All bets placed by bots |
| `GET /api/strategies/run` | Trigger a manual run |
| `GET /api/strategies/leaderboard` | Just the sorted leaderboard |
| `GET /api/strategies/backtest` | Latest backtest results |
| `POST /api/strategies/backtest/run` | Run backtest + sync to DB + save history |
| `GET /api/strategies/backtest/history` | All past backtest runs (newest first) |

Import the engine lazily inside the endpoint functions to avoid startup
dependency issues.

## Cron Job

Schedule daily automated runs:

```yaml
schedule: "0 8 * * *"     # 8 AM daily
workdir: /path/to/project
command: cd /path && python -m strategies.run_bots
```

## Pitfalls

- **Port conflicts on restart** — always verify old PID is fully killed
  (`netstat -ano | grep :PORT`, `powershell Stop-Process -Id PID -Force`)
- **Decimal odds** — bots check `ml <= -400` but DB stores 1.44. Always
  convert in data layer before bot logic runs.
- **Engine singleton isolation** — `run_bots.py` creates its own engine.
  The API creates a separate one. Use auto-load from DB so both stay in sync.
- **DB connection lifecycle** — don't close the connection in a registration
  script if the engine will reuse it. Get the connection once, keep it.
- **Affiliates dedup** — without a UNIQUE constraint, INSERT OR IGNORE
  inserts duplicates. Add `CREATE UNIQUE INDEX` on the name column.
- **Mock user cleanup** — when replacing mock users with bots, delete old
  `challenge_participants` rows and old bets for those user IDs first.
- **Commit often** — per user preference: commit after every meaningful
  change so rollback is possible. Small focused commits > one big commit.
- **No max wager cap = guaranteed bust.** A bot with 90% win rate betting
  100% of bankroll busts on the first loss. Add `self.max_wager_pct = 0.15`
  to `BaseStrategy.__init__` and enforce in every `decide()` override.
  See `references/backtest-methodology.md#max-wager-cap-base-class-pattern`.
- **Threshold tuning is iterative.** Lower thresholds (e.g., -400→-200)
  increase bet frequency but also increase loss rate. Change one parameter
  per iteration, retest, measure delta. Some strategies (underdog-heavy,
  pure arbitrage with thin edge) are fundamentally wrong regardless of
  threshold tuning — replace them rather than keep tweaking.
- **`week_reached` must be in every layer.** Store it in the
  `challenge_participants` table (DB), load it in the engine
  (`bot.week_reached = r.get("week_reached", 1)`), expose it in the
  API (`"week_reached": getattr(self, "week_reached", 1)` in
  `get_status()`), render it in the frontend strategy table (Week column
  with deadline countdown in Days column). Missing at any layer means
  the strategy table shows stale data.
- **Strategy table columns are: # Bot Strategy W L Win% Bankroll ROI Week Deadline.**
  The Week column shows `Wk {bot.week_reached}` and Deadline shows
  `{7 - (week_reached % 7)}d`. Deadline highlights orange when ≤2 days.
- **Backtest history navigation.** The frontend stores past backtest runs
  (fetched from `/api/strategies/backtest/history`) in a `_btHistory`
  array with a `_btIdx` cursor. ◀ ▶ arrows call `prevBacktest()` /
  `nextBacktest()` which `applyBacktestRun()` maps into strategy table
  format and calls `renderStrategyTable()`. Call `loadBacktestHistory()`
  on page init and after every backtest run.

**See also:** `references/backtest-methodology.md` — 5-week backtest runner with probabilistic settlement against historical odds data.

## User Preferences

- Keep designs **simple and clean** — avoid over-engineering the UI
- Commit frequently with descriptive messages
- Production-grade thoroughness on data pipelines and schema
