---
name: rebalance-plan
description: >-
  Turn a target allocation into a concrete order list — dollar and share deltas per
  name, a tax tag per row, and an optional schedule that stages the buys over N
  trading days. Use when someone has decided what they want to own and needs the
  actual orders, when trimming a concentrated position, when deploying cash, or when
  asked "what do I actually type into the broker". Produces a list; never an order.
---

# Plan a rebalance

> **Setup.** The scripts sit beside this file. Run them from a working folder that
> holds your `.env` (E*TRADE consumer key/secret) and a `data/` directory; install
> deps with `pip install -r requirements.txt` where one is included. Part of a set:
> `etrade-pull`, `order-check`, `portfolio-review`, `realized-pnl`, `rebalance-plan`,
> `price-history`, `trade-journal`, `intrinsic-value`, `sec-financials`, `buffett-checklist`.

```bash
cp targets.example.json targets.json     # then edit
python rebalance.py
python rebalance.py --dca 10 --start 2026-06-08
```

Needs `data/portfolio.csv` — see `etrade-pull`. Reached from
`portfolio-review` once the decision is already made; this skill executes a
decision, it doesn't reach one.

## How the weights are defined

Weights are fractions of **investable capital**:

```
(market value of positions) + cash_on_hand - cash_reserve
```

A reserve you intend to keep is excluded from the denominator rather than quietly
diluting every target. `0.15` means 15% — the script rejects a target set summing
over 100% rather than producing a plan that can't be executed.

A name set to `0.0` is a full exit. `sell_unlisted: true` also exits every held name
absent from `targets`.

## Rules

- **This prints an order list. It never places an order, and neither do you.** The
  person types the orders. *That gap is the last place a wrong premise can be caught
  before it costs money, and it's the reason nothing in this repo holds trading
  permissions.*

- **`targets.json` is gitignored — keep it that way.** It is a complete statement of
  what someone intends to own, which is as sensitive as the positions themselves.

- **The tax tag cannot see holding periods.** It reads unrealized P&L, so it knows
  "harvest loss" from "realizes gain" and nothing more. *It cannot tell short-term
  from long-term, and that distinction is often larger than the trade's edge.* Check
  the lot dates before acting on any row tagged `realizes gain`.

- **A name you don't hold needs a price in the config.** There's no market value to
  derive one from, so the shares column comes back empty and the script says which
  names it couldn't size. *It reports the gap rather than guessing, because a guessed
  price produces a share count that looks authoritative.*

- **Share counts are rounded; the dollar figures are the plan.** For high-priced
  names a DCA day may be one or two shares. Keep the dollar pace.

- **Re-pull positions immediately before generating a plan.** Deltas computed from a
  stale CSV are wrong by however much the market moved.

## Staging

`--dca N --start YYYY-MM-DD` splits the **buy** side evenly across N trading days,
skipping weekends and any date in the config's `holidays` list. Sells are untouched
— they're assumed to clear first and fund the buys. Add market holidays yourself;
the script has no calendar and will happily schedule a purchase on Juneteenth if you
don't list it.
