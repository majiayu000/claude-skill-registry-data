---
name: kelly-invest-webull
description: Busabase-backed, read-only App-in-Skill portfolio dashboard that aggregates Webull brokerage holdings (accounts, positions, cash/margin, market value, unrealized P/L, day change, buying power). Use when the user invokes $kelly-invest-webull or /kelly-invest-webull, wants to review their Webull portfolio, holdings, positions, accounts (cash/margin), asset allocation, market value, unrealized P/L, day change, cash, or buying power. Read-only aggregation only — it never places, modifies, or cancels orders and never moves money.
metadata:
  category: invest
  tags:
    - risk:read-only
    - surface:busabase
    - surface:webull
  busabase:
    template: true
    folderSlug: kelly-invest-webull
    resources:
      - accounts
      - positions
      - settings
    risk: read-only

---

# Kelly Invest (Webull)

## Overview

Kelly Invest (Webull) is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. Use this skill as Kelly's read-only Webull portfolio
operator: an Overview (totals, unrealized P/L, day change, cash, allocation
donut, top movers, insights), a sortable Positions table, an Accounts view
(cash and margin), and a per-symbol Position detail pane.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

This is a monitoring dashboard: there is no approval lifecycle and no
decisions workflow.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-invest-webull-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Invest overview"></td>
    <td width="50%"><img src="assets/screenshots/positions.webp" alt="Kelly Invest positions"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Portfolio command desk with market value, unrealized P/L, day change, cash, an allocation-by-asset-type donut, and top day movers.</td>
    <td><strong>Positions</strong><br>Sortable holdings table across symbol, asset type, quantity, average cost, last price, market value, unrealized P/L, and portfolio weight.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/accounts.webp" alt="Kelly Invest accounts"></td>
    <td width="50%"><img src="assets/screenshots/detail.webp" alt="Kelly Invest position detail"></td>
  </tr>
  <tr>
    <td><strong>Accounts</strong><br>Per-account view (cash and margin) with net liquidation, total cash, buying power, and the positions held in each account.</td>
    <td><strong>Position detail</strong><br>Single-symbol view with cost basis, market value, unrealized P/L and percentage, day change, weight, and holding account.</td>
  </tr>
</table>

## Boundary

- The skill may read Webull account/balance/position data, normalize it, and
  write Accounts/Positions/Settings rows into Busabase through the trusted
  `scripts/sync_webull.mjs` process only.
- The AirApp reads Busabase records only; it is entirely read-only and must
  NEVER place, modify, or cancel orders. NEVER move money, transfer,
  withdraw, or change account settings. There is no trading path in this
  skill by design (`readOnly: true`, no `writeProcedures`).
- Treat all holdings/account data as sensitive. Never commit Webull
  credentials, `config.local.json`, env files, or raw Webull responses.

## Busabase Resources

Three Bases under one application Folder (`kelly-invest-webull`), declared in
`content/kelly-invest-webull-app/app/js/config.js` and the generated template sidecars under `content/`:

- `accounts`: Webull cash and margin accounts (`account_id`, `account_type`,
  `display_name`, `currency`, `net_liquidation`, `total_cash`,
  `buying_power`).
- `positions`: holdings per account (`position_id` = `account_id:symbol`,
  `symbol`, `name`, `asset_type`, `account_id`, `quantity`, `avg_cost`,
  `last_price`, `market_value`, `cost_basis`, `unrealized_pnl`,
  `unrealized_pnl_pct`, `day_change`, `day_change_pct`, `currency`). Weights,
  totals, and allocation are computed at read time by
  `content/kelly-invest-webull-app/app/js/webull-model.js` (`assembleSnapshot`), never stored.
- `settings`: two rows — `config` (sanitized Webull region/base URL/account
  allowlist, base currency, target allocation, generated_at, warnings — no
  secrets) and `onboarding`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/portfolio-schema.md` for
exact field shapes. The AirApp never writes to any Base — only the trusted
sync script does.

## Data Provider — Real Webull Integration

The skill reads Webull; the app only ever reads the normalized Busabase
snapshot.

- `lib/data-provider/webull.ts`'s field-mapping and credential-resolution
  logic (`mapAccount`, `mapPosition`, `normalizeAssetType`,
  `resolveWebullCredentials`) was ported **verbatim** into
  `content/kelly-invest-webull-app/app/js/webull-model.js`, shared by both the browser (for
  `assembleSnapshot`/`computeInsights`) and the trusted sync script (for the
  Webull-specific mapping).
- `scripts/sync_webull.mjs` is the only process that writes to Busabase. It
  resolves Webull App Key / App Secret from env vars named in local config
  (`config.webull.app_key_env` / `app_secret_env`, defaults
  `KELLY_INVEST_WEBULL_APP_KEY` / `KELLY_INVEST_WEBULL_APP_SECRET`), fetches
  live account/balance/position data, and writes normalized rows via
  `bases.createChangeRequest` / `records.changeRequest` with its own
  `BUSABASE_BASE_URL` / `BUSABASE_API_KEY` / `BUSABASE_SPACE_ID` credentials
  (`autoMerge: true`).
- Webull has no first-party Node SDK — the official SDK is
  `webull-openapi-python-sdk` (Python), and Webull's wire-level
  signing/endpoint shape is not published outside that SDK (the retired
  `webull.ts` adapter itself never implemented raw HTTP calls, only the
  credential + mapping logic, for the same reason). `scripts/sync_webull.mjs`
  therefore shells out to `scripts/webull_bridge.py`, which calls the exact
  SDK methods documented in the original adapter's comments
  (`get_account_list()`, `get_account_balance(account_id)`,
  `get_account_positions(account_id)`). Confirm the Python SDK's exact
  import path against `https://developer.webull.com/apis/docs/sdk/` before
  first live use.
- For a credential-free dry run (e.g. CI, local testing), pass
  `--fixture <path/to/raw.json>` to `sync_webull.mjs` with a JSON payload
  shaped like `{ "accounts": [...], "positions": [...] }` using the raw
  Webull SDK field names documented in `webull-model.js`.
- Rate limit is ~10 requests / 30 seconds per App ID; batch and back off.

Run the sync from the skill root:

```bash
BUSABASE_BASE_URL=... BUSABASE_API_KEY=... BUSABASE_SPACE_ID=... \
  node scripts/sync_webull.mjs
```

## First Run And Onboarding

On invocation, check the `config` and `onboarding` Settings rows for
readiness. If absent, guide setup before syncing real holdings.

To connect Webull, the user needs a Webull OpenAPI **App Key** and **App
Secret** from Webull's OpenAPI Management/Portal (region id `us`; approval
typically takes 1-2 business days). A UAT test host exists at
`us-openapi-alb.uat.webullbroker.com`.

Ask for non-secret setup details only: region, base URL, base currency,
account allowlist, and which env var names hold the App Key / App Secret.
Never ask the user to paste secret values into chat. Secrets belong only in
local env files read by the trusted sync script, and config references them
by name (`app_key_env`, `app_secret_env`).

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock portfolio (~10
  positions across STOCK/ETF/CRYPTO in one cash and one margin account) with
  computed P/L for documentation and screenshots.
- `?demo=positions`, `?demo=accounts`, and `?demo=detail` select named mock
  scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase and never claims a real
  connection.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-invest-webull-app dev` only when local preview/debugging is explicitly
requested. UI language supports English and Chinese chrome with an `Auto`
default; the user is Chinese, keep symbols and provider values in their
original form.

## Views

- `#/overview`: total market value, total unrealized P/L (color + %), day
  change, cash, and allocation-by-asset-type donut plus top day movers and
  insights.
- `#/positions`: sortable table (symbol, name, qty, avg cost, last, market
  value, unrealized P/L %, weight).
- `#/accounts`: cash and margin accounts with net liquidation, cash, buying
  power.
- `#/accounts/<account_id>`: account summary and its filtered positions.
- `#/positions/<symbol>`: per-symbol detail pane.
- `#/settings`: sanitized setup summary — data provider, Webull region and
  base URL, credential-readiness booleans, and onboarding state. Never
  exposes secret values.

## Insights

Read-only, deterministic observations computed by `computeInsights` in
`content/kelly-invest-webull-app/app/js/webull-model.js` (ported verbatim from the retired
`content/kelly-invest-webull-app/server/insights.ts`): `single_position_concentration`,
`crypto_concentration`, `allocation_drift`, `cash_drag`, `negative_cash`,
`top_gainer`, `top_laggard`. Neutral facts/flags, never advice or actions —
no buy/sell/rebalance suggestions.

## File Contract

Read `references/portfolio-schema.md` before editing the app,
`content/kelly-invest-webull-app/app/js/config.js`, `content/kelly-invest-webull-app/app/js/webull-model.js`, or
`scripts/sync_webull.mjs`.

## Safety

- Read-only by design. Prefer read-only Webull scopes/credentials.
- Do not invent prices or fills. If a price or balance looks stale or
  missing, add a snapshot warning instead of guessing.
- Redact credential-like strings in logs, reports, and UI state.
- Keep syncs idempotent — `scripts/sync_webull.mjs` upserts by
  `account_id`/`position_id` so repeated runs never duplicate rows.
