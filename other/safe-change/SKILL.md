---
name: safe-change
description: The protocol for changing anything that can move real money — order placement, closing, position sizing, the MT5 bridge, or the risk governor. Use before editing services/trading, services/risk, services/broker, or anything named close/open/partial/lot/sizing. Also use when the user asks to "just tweak" a trading value.
---

# Changing money-touching code

This app places real orders on a live MetaTrader 5 account. Work through this
in order. Do not skip to step 4.

## 1. Establish whether it is money-touching

It is, if it touches any of:

| Surface | Where |
|---|---|
| Open | `services/trading/open_trade.py`, `instant_entry.py`, `limit_order_signal.py` |
| Close | `services/trading/close_trade.py`, `partial_close.py` |
| Modify | `services/broker/repo.py` SL/TP writes, the strategy handlers |
| Sizing | `services/risk/governor.py`, `suggest_lot_size` |
| Bridge | `mt5_bridge.py`, `services/broker/ea_bridge.py` |

If yes, read `docs/system/rules/20-trading-safety.md` in full before
continuing, plus the affected domain's knowledge file —
`docs/system/domains/trading/`, `risk/`, `broker/` or `positions/` — for
constraints and gotchas specific to that surface.

## 2. Check whether the close path is involved

`close_trade`, `record_close`, `_make_close_trade_ctx`, `partial_close_trade`,
`_schedule_profit_sync` are **frozen**.

They may be renamed or relocated verbatim. They may not be reshaped — no
argument added, removed, reordered or defaulted, no branch restructured —
without owner sign-off **and** a demo-account session.

`tests/core/test_close_trade_characterization.py` must pass **unmodified**.
If your change requires editing it, stop: the change is out of scope, and
saying so is the correct outcome.

## 3. Decide if you can proceed at all

**Stop and tell the user** if the change:

- alters when, whether or how much an order is placed
- alters the closing sequence
- needs a real or demo broker connection to verify
- changes money arithmetic (rounding, epsilon, operation order)

Say plainly which part needs a demo session, do the rest, and leave that
piece. A user saying "yes, go ahead" to a plan is **not** sign-off for the
money-touching part of it.

## 4. If it is a value, it is probably config, not code

Before editing a constant, check whether it is already in
`EXPERT_PARAMS` (`backend/src/services/risk/expert_params.py`). If it is,
this is a settings change, not a code change. If it should be, use the
`add-tunable` skill.

## 5. Write the test first

- Fakes only. No test may place, close or modify a real or demo order.
- Bridges return canned dicts; order calls are sentinels that record.
- Watch the test fail before making it pass.
- State in the module docstring that nothing here reaches a broker.

## 6. Make the smallest change

No bundled tidy-ups. If the fix and a refactor ship together and something
breaks, you cannot tell which half did it.

## 7. Verify

```bash
python -m tools.checks all
```

Plus, explicitly, that the close-path characterization pack passes
unmodified:

```bash
pytest tests/core/test_close_trade_characterization.py -q
git diff --stat tests/core/test_close_trade_characterization.py   # must be empty
```

## 8. Say what you did

End the report with the standing line, and mean it:

> No real or demo MT5 order is placed, closed or modified by this work or
> its tests.

If you cannot say that truthfully, say what you did instead.

## Incidents these rules come from

- Telegram entries once bypassed the Max Risk per trade ceiling.
- A cache served the previous environment's risk settings for 10s after a
  demo/live switch.
- A follow-up signal opened a second independent trade on a paired node —
  two real orders for one signal.
- One slow health check triggered a real bridge restart, causing the
  disconnects it existed to prevent.

Each has a dated comment at the site. Read it before simplifying anything
nearby.
