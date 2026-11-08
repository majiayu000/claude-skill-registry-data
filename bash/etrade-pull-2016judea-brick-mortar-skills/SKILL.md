---
name: etrade-pull
description: >-
  Pull a live E*TRADE account — positions, weights, cost basis, unrealized P&L, or
  full transaction history — via a bundled OAuth 1.0a client. Use whenever real
  account numbers are needed rather than a reconstruction, or when an auth handshake
  fails, 401s, or hangs. Owns everything about E*TRADE authentication, including the
  token that dies at midnight Eastern and the interactive prompt that hangs in a
  non-interactive shell.
---

# Pull live E*TRADE data

> **Setup.** The scripts sit beside this file. Run them from a working folder that
> holds your `.env` (E*TRADE consumer key/secret) and a `data/` directory; install
> deps with `pip install -r requirements.txt` where one is included. Part of a set:
> `etrade-pull`, `order-check`, `portfolio-review`, `realized-pnl`, `rebalance-plan`,
> `price-history`, `trade-journal`, `intrinsic-value`, `sec-financials`, `buffett-checklist`.

Scripts: `fetch_portfolio.py` → `data/portfolio.csv`; `fetch_transactions.py` →
`data/transactions.csv`; `etrade.py` is the client to import.

```bash
source .venv/bin/activate
ETRADE_ENV=prod python fetch_portfolio.py
ETRADE_ENV=prod python fetch_transactions.py --start 2023-01-01
```

Called from `portfolio-review`, which is the entry point for anything that
starts "what do they hold."

## Rules

- **`ETRADE_ENV=prod` on every single call.** Unset means sandbox, and the sandbox
  returns four canned accounts with **zero securities trades**, dated 2013. *It does
  not error and it does not look empty — it looks like a real account belonging to
  someone who never trades.* The OAuth URLs are hardcoded to prod either way, so a
  successful login proves nothing about which environment you're reading.

- **Never print or echo the contents of `.env` or `.tokens`.** They are the account.
  A traceback that includes the consumer secret has published it.

- **Re-pull rather than reuse a CSV from a previous session.** Prices move; weights
  computed off yesterday's file are wrong in a way nobody notices.

## The auth gotcha

OAuth 1.0a with an out-of-band verifier: there is no redirect, the user reads a
short code off E*TRADE's page and pastes it back.

**Tokens go inactive after ~2 hours idle and expire at midnight US Eastern, every
night.** `etrade.get()` catches the resulting 401 and re-runs the handshake once,
which is enough for a long-running script to cross the boundary.

**But the handshake needs a human, and `input()` hangs in a non-interactive shell** —
which is where an agent usually is. Split it across two invocations instead:

```bash
python auth_cli.py start            # prints the authorize URL — give it to the user
python auth_cli.py finish <code>    # exchange the code they paste back
```

If a pull hangs with no output, this is why. Kill it and use `auth_cli.py`.

## What the API will not give you

- **~3 years of transactions.** Older dates return error 2003. A complete archive
  needs statement CSV exports from the web UI.
- **A request with no date range silently returns only the last ~month.**
  `fetch_transactions.py` always sends an explicit window for this reason.
- Field shapes and the sandbox's exact limitations are documented in `SCHEMA.md`.

## Writing: orders can be placed, and the API's limits shape the design

`etrade.py` exposes `post()` / `put()`; the transmitter is `place_order.py`, owned
by `order-check`. Four tool facts:

- **⚠️ There is NO OCO / bracket / one-cancels-other field.** `priceType` covers
  MARKET / LIMIT / STOP / STOP_LIMIT / trailing / hidden; `orderTerm` covers
  GOOD_UNTIL_CANCEL / GOOD_FOR_DAY / GOOD_TILL_DATE / IMMEDIATE_OR_CANCEL /
  FILL_OR_KILL; the only linkage is `conditionType` (`CONTINGENT_GTE` /
  `CONTINGENT_LTE`) against **another symbol's** price. OCO is a Power-E*TRADE UI
  construct. *Any plan prescribing "an OCO bracket" describes something the API
  cannot do — say so rather than trying.*
- **A write is NEVER auto-retried on a 401.** `get()` re-auths and replays;
  `_send()` deliberately raises instead. Replaying an order body after a token
  refresh can transmit the same order twice, and a duplicate stop is a duplicate
  exit.
- **A preview creates no order**, so `POST /orders/preview` is a free, safe,
  end-to-end validation against the live account and returns the `previewId` that
  `place` requires. **Use preview as the integration test; never use the sandbox
  for orders** — it holds no positions, so nothing about a sell is exercised.
- **`clientOrderId` is capped at 20 alphanumeric characters.** Longer or
  punctuated ids fail with an error that reads like an auth problem.

Endpoints: `orders/preview`, `orders/place`, `orders/{id}/change/preview`,
`orders/{id}/change/place`, `orders/cancel` (a PUT taking `{"CancelOrderRequest":
{"orderId": N}}`).

## `/orders` is also the only SIMULTANEOUS price record you get

`Instrument[].averageExecutionPrice` on an `EXECUTED` order is a real fill, and
`executedTime` is stamped per leg. **When several legs execute in the same minute,
those fills are simultaneous prices for every name involved** — which is what makes
a "should I have bought the other one instead" comparison honest, with no
close-vs-intraday fudging. Nothing else in this API gives you that.

## ⚠️ A cash-identity reconciliation is NOT a fill price

If a fill hasn't posted yet, the tempting move is to solve for it: *proceeds +
prior cash − cost = the residual the broker reports.* **Don't.** Real instance:
that arithmetic produced `~$380.00` against an actual fill of **$377.955** — off
by $2.045/share — and it failed in the *flattering* direction, recording a sell as
better than the quote when it was worse.

Solving an identity for its one unknown silently absorbs every unmodelled term —
fees, unsettled credits — into precisely the number you wanted. **It cannot come
out inconsistent, so it never warns you.** Read the fill off `/orders`, or write
"unknown." Never off an identity, and never off the limit price: a limit fills at
or *better* than its limit.
