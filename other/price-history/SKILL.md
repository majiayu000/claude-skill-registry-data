---
name: price-history
description: >-
  Get ~10 years of daily bars, trailing returns, distance off the period high, and
  month-by-month seasonality for any ticker — no API key required. Use when locating
  a name in its own cycle, checking whether a move is unusual for it, testing a
  seasonality claim against data instead of eyeballing a chart, or when a price
  series is needed and the usual free endpoints are blocked.
---

# Price history and seasonality

> **Setup.** The scripts sit beside this file. Run them from a working folder that
> holds your `.env` (E*TRADE consumer key/secret) and a `data/` directory; install
> deps with `pip install -r requirements.txt` where one is included. Part of a set:
> `etrade-pull`, `order-check`, `portfolio-review`, `realized-pnl`, `rebalance-plan`,
> `price-history`, `trade-journal`, `intrinsic-value`, `sec-financials`, `buffett-checklist`.

```bash
python price_history.py AAPL       # 10y windows + seasonality
python price_history.py SPY 5      # limit to 5 years
```

```python
from price_history import daily_bars, windows, seasonality
```

Reads Nasdaq's public quote endpoint, which needs only a browser User-Agent. It's
this endpoint and not a better-known one because **Yahoo's chart API began hard-429ing
in 2026 and Stooq put a JavaScript proof-of-work wall in front of theirs** — if you
reach for either out of habit, you'll get a wall, not data.

Nasdaq keys history by asset class, so `daily_bars` tries equities then ETFs. A
caller never has to know which a ticker is.

## Rules

- **Seasonality on 10 years is n=10 per month.** The script prints the sample size
  and a warning for this reason. *A 90% win rate on ten observations is four coin
  flips' worth of evidence.* Report `n` beside any monthly claim, or don't make the
  claim.

- **Never let seasonality drive a decision on its own.** It's a tiebreak on timing
  for a position already justified on other grounds. *Buying something because
  September is historically weak for it is data-mining with extra steps.*

- **A spread under ~2x is not a finding.** If one month means +1.2% and another
  +0.9%, there is no seasonal effect worth a sentence.

- **`off_high` is a location, not a signal.** "Down 10% from its period high" says
  where a name sits; it says nothing about whether that's an opportunity. Pair it
  with why the thesis is or isn't intact — see `portfolio-review`.

- **An empty response means blocked or a bad symbol, and the script raises.** Don't
  catch it and carry on with a partial series — a silently short series makes every
  trailing return wrong.
