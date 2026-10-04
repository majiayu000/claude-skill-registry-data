---
name: robinhood
description: Use when reading or acting on the user's live Robinhood accounts via the mcp__robinhood__* MCP tools — account/portfolio lookups, equity and options positions, watchlists, scanners/screeners, and placing or reviewing orders. Read before any Robinhood tool call, especially the first one in a session.
---

## Overview

Robinhood connects as an MCP server (`mcp__robinhood__*`, ~50 tools, deferred — load via
`ToolSearch("select:mcp__robinhood__...")` before first use). This is a **live brokerage account**,
not a sandbox — `place_equity_order`/`place_option_order`/`exercise_option`/`cancel_*` are real,
irreversible-in-spirit actions. Always confirm with the user before submitting or canceling an order;
`review_equity_order`/`review_option_order` (dry-run risk/cost preview) is safe to call freely and
should be used before every place_* call.

Almost every tool response includes a `guide` field with binding formatting/behavior rules (masking
account numbers, which field is authoritative for buying power, sort order, etc.) — those rules live
in the tool response itself, not duplicated here, since they can change server-side. Follow them.

## Accounts (inventory as of 2026-08-18)

Two individual margin/limited-margin accounts, both option_level_3. Numbers are masked to the last
4 digits because this repo is public: `get_accounts` returns the full numbers, and the agentic one is
`ROBINHOOD_AGENTIC_ACCOUNT` in the root `.env`. Mask to `••••XXXX` in any user-facing text too, per
the `get_accounts` guide.

| Account | Number | Type | Nickname | Agentic (this agent can trade) | Default |
|---|---|---|---|---|---|
| A | ••••8556 | margin | — | No | Yes |
| B | ••••1659 | limited_margin | "Agentic" | **Yes** | No |

**Only account B (••••1659, "Agentic") is `agentic_allowed: true`** — that's the one this agent can
place/cancel orders in. Account A is visible (read) but not tradable by this agent; if the user wants
a trade in A, say it's not accessible to this agent, don't imply it needs enabling on Robinhood's side.

Snapshot at inventory time (**stale the moment markets move — always re-fetch before making decisions,
this is just orientation**):

- **Account A (••••8556)**: total value ~$53.88 (equity $6.27, options $37, cash $10.61). Positions:
  0.028 sh NVDA (fractional, avg $211.94). Options: an SPY call spread (long/short $26/$23 avg,
  exp 2026-08-28), a long SPCX call (avg $13, exp 2026-10-16), an NVDA call spread (long $47 / short
  $37, exp 2026-11-20), a CRGY call spread (long $50 / short $16, exp 2026-09-18).
- **Account B (••••1659, Agentic)**: total value ~$527.27 (equity $121.97, cash $405.30, $350 pending
  deposit). Positions: 3 sh UUUU (avg $14.17), 8 sh TGB (avg $8.86), 3 sh KOS (avg $2.57). No open
  options.

Re-run `get_portfolio` + `get_equity_positions` + `get_option_positions(nonzero=true)` per account
before quoting current numbers — don't trust this table for anything but "what generally exists."

## Watchlists

`get_watchlists` → 4 custom lists (all owner_type `custom`, writable):
- **Options watchlist** (`5f643fd5-a094-48a8-ad22-1a0d8a756617`) — single-leg option contracts, 14
  items at inventory time but `get_option_watchlist` returned empty on the last check; re-poll, don't
  trust the stale count. Use `get_option_watchlist`, not `get_watchlist_items`, for this one (the
  latter 400s on option strategy items).
- **Crypto to watch** (`63604e85-...`) — 6 items.
- **First list** (`ad481bfe-...`) — 16 items, general/unlabeled.
- **Sell Vol Plays** (`dad631c6-...`) — 8 items, described as "Aug 5 post-earnings IV-crush sell-vol
  candidates (SEDG CVS IRM CPRI PRGO SHAK DK HMC)" — a vol-selling watchlist the user already curated;
  a natural target basket for a "trading mode" IV-crush/mean-reversion sweep.

Use `get_watchlist_items(list_id)` for the non-options lists.

## Scanners (Legend screeners)

`get_scans` → 4 saved scans, notably two vol-relevant ones already built:
- **"Volatility Comparison"** (`2c7667c4-...`, Cortex-managed / read-only) — ATM IV(30d), HV(1M),
  IV rank, IV−HV delta, options volume, sorted by options volume desc. This is the fastest single call
  for "where's IV rich vs. realized right now" across the market.
- **"High options volume and IV"** (`ad2715de-...`, editable) — ATM IV(30d), options volume + relative
  options volume, sorted by IV desc. Good for unusual-activity-meets-elevated-IV screens.
- Two generic "Untitled Scan"/"Untitled Scan 2" (market-cap sorted, no vol columns) — not vol-specific,
  ignore for trading-mode work unless the user repurposes them.

Call `get_scanner_filter_specs` before constructing/editing any filter (`create_scan`,
`update_scan_filters`) — don't guess `filter_type_enum` values. Cortex-managed scans can be `run_scan`'d
but not modified; clone into a new scan via `create_scan` instead.

`run_scan` on a broad/unfiltered scan can exceed the tool-result token limit (seen live: 52,685/88,697
characters over the max) — the harness falls back to saving the output to a side file rather than
returning it. Prefer scans with tighter filters, or check for a results-limit param, before running a
scan you expect to return a large universe.

## Tool map (by task)

- **Account/portfolio**: `get_accounts`, `get_portfolio`, `get_limited_margin_upgrade_info`,
  `get_option_level_upgrade_info`.
- **Positions & history**: `get_equity_positions`, `get_option_positions`, `get_equity_tax_lots`,
  `get_pnl_trade_history`, `get_realized_pnl`, `get_equity_orders`, `get_option_orders`.
- **Quotes & chains**: `get_equity_quotes`, `get_equity_price_book`, `get_option_chains`,
  `get_option_quotes`, `get_option_instruments` (strike/type lookup from an option_id),
  `get_equity_historicals`, `get_option_historicals`, `get_index_quotes`/`get_index_historicals`.
- **Fundamentals/context**: `get_equity_fundamentals`, `get_financials`, `get_earnings_calendar`,
  `get_earnings_results`, `get_equity_technical_indicators`, `get_equity_tradability`.
- **Screeners**: `get_scans`, `run_scan`, `create_scan`, `update_scan_filters`, `update_scan_config`,
  `get_scanner_filter_specs`.
- **Watchlists**: `get_watchlists`, `get_watchlist_items`, `get_option_watchlist`,
  `create_watchlist`, `update_watchlist`, `add_to_watchlist`/`remove_from_watchlist`,
  `add_option_to_watchlist`/`remove_option_from_watchlist`, `follow_watchlist`/`unfollow_watchlist`,
  `get_popular_watchlists`.
- **Orders (live, act with care)**: `review_equity_order` → `place_equity_order` → `cancel_equity_order`;
  `review_option_order` → `place_option_order` → `cancel_option_order`; `exercise_option`,
  `cancel_option_exercise`.

## Working conventions

- Never default an `account_number` from `get_accounts` when a write tool requires one explicitly per
  its schema (`get_equity_positions`, `get_option_positions`, etc. say "must come from the user or be
  clearly implied") — ask or infer from context, don't silently pick account A vs. B.
- Buying-power questions always route through `get_portfolio`, never derive from `get_accounts`.
- Before any `place_option_order`/`place_equity_order`, call the matching `review_*_order` first and
  surface the cost/risk preview to the user; wait for explicit go-ahead before placing.
- Claude Code auto-mode classifier blocks `place_equity_order` / `place_option_order`. Do not retry
  the same tool after "Blocked by classifier" / "Permission denied by Claude Code auto mode classifier".
  Tell the user auto-mode cannot place live orders.
- This account's options are multi-leg (spreads) in account A — `get_option_watchlist` and
  `get_option_positions` only show single-leg detail per contract; a spread shows as two separate
  long/short legs sharing a `chain_id`+near-identical `opened_at`, not as one strategy object. Group by
  `chain_symbol` + `opened_at` proximity when presenting a "position" to the user.
- `get_equity_quotes`/`get_option_quotes`'s `symbols` param is a JSON array, not a comma-joined
  string — pass `["KOS","TGB"]`, never `"KOS,TGB"` (the latter 400s: "has type \"string\", want one of
  \"null, array\"").
- `place_option_order` rejects any top-level property outside its schema — e.g. `underlying_type`,
  `chain_symbol` — with "unexpected additional properties"; only pass the fields the schema defines.
  **Re-verified 2026-09-03 against a live 400**: multi-leg orders (2+ legs in one `place_option_order`
  call) are rejected for account B with `"Multi-leg options orders aren't supported in Robinhood
  agentic accounts yet."` — this is a Robinhood-side restriction on agentic accounts specifically, NOT
  gated by `option_level` (B is `option_level_3`, same as A). The tool's own schema/description doesn't
  surface this restriction — it only mentions option_level gating — so don't trust the schema text
  alone here; the 400 message is the ground truth. **A straddle/strangle is still achievable** by
  placing the call leg and the put leg as two independent single-leg orders (each reviewed and placed
  separately) — this gives the same economic position, just without atomic net-debit execution (one
  leg can fill without the other; check both fills before treating the position as fully on).
