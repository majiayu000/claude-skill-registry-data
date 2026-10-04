---
name: kelly-portfolio-health
description: Busabase-backed App-in-Skill dashboard for a revenue-based-financing (RBF) fund or private-credit book of many small SME contracts. Use when the user invokes $kelly-portfolio-health or /kelly-portfolio-health, wants to check portfolio health, AUM, repayment progress, concentration risk, or a watchlist of contracts with declining revenue. Human actions (flag a contract for review, clear a flag, leave a note) write directly onto the contract's own Busabase record — this skill never moves money or changes contract terms. Generic and brand-free — not tied to any specific company or fund.
metadata:
  category: rbf
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-portfolio-health
    resources:
      - contracts
      - settings
    risk: local-write

---

# RBF Portfolio Health Dashboard

## Overview

Kelly Portfolio Health is a Busabase Cloud App-in-Skill. Its canonical
product surface is the AirApp in Busabase, not a separate local-data
product. The same Hono source supports an explicitly requested local preview
with OAuth connection bootstrap. It gives a fund/credit-desk operator a
read-mostly dashboard over a revenue-share / private-credit book: many small
SME (small/medium enterprise) contracts, each an advance repaid as a share
of the SME's future revenue up to a cap. The app aggregates the book into a
top-line health summary, a repayment-progress-vs-time-elapsed view, an
industry/city concentration breakdown, and a watchlist of contracts with a
recent revenue decline. The only human action is lightweight: flag a
contract for review, clear a flag, or leave a note — everything else is a
read view.

This is deliberately **generic and brand-free**: no real company, fund, or
SME name appears anywhere in the code, config, or seed data.

This is a direct-manipulation dashboard, not a review-then-approve queue:
there is no AI-authored draft to approve and no separate execute/decisions
step. Totals, repayment lag, concentration, and the watchlist are computed
by a documented, deterministic function
(`content/kelly-portfolio-health-app/app/js/portfolio-model.js`, ported from the retired
`content/kelly-portfolio-health-app/server/insights.ts`); the human flags/clears/annotates a contract
directly in the UI, writing straight onto the contract's own Busabase record
— the same way `kelly-llm-gateway`'s rollout promote/rollback/hold and
`kelly-lead-funnel`'s kanban stage moves work.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-portfolio-health-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's artifact and product
contracts, stop before the unavailable Busabase operation, and report the
exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Portfolio health overview"></td>
    <td width="50%"><img src="assets/screenshots/concentration.webp" alt="Portfolio concentration"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Total AUM, total collected, weighted-average repayment progress, at-risk count, category allocation, and the contracts most lagging behind their expected repayment pace.</td>
    <td><strong>Concentration</strong><br>Industry/category and city concentration by funding amount and contract count.</td>
  </tr>
  <tr>
    <td colspan="2"><img src="assets/screenshots/watchlist.webp" alt="Portfolio watchlist" width="50%"></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Watchlist</strong><br>Contracts whose most recent month's revenue dropped materially below their trailing average, with a revenue sparkline and a flag-for-review / clear-flag / note action.</td>
  </tr>
</table>

## Boundary

- Read-mostly aggregation and human review flags only. NEVER contact any
  external system, brokerage, payment processor, or SME directly. NEVER move
  money, disburse funds, or change contract terms. There is no transaction
  path in this skill by design.
- The AirApp reads and writes its own Busabase Bases only; it never calls a
  live portfolio-servicing API. There is no execution/merge step beyond the
  direct write itself — a human still applies the decision in the real
  system of record.
- Contracts are never created by the AirApp; they enter Busabase through an
  external portfolio-sync process, the same way `kelly-llm-gateway`'s routes
  and `kelly-lead-funnel`'s leads enter through an upstream process the app
  doesn't control. The AirApp only ever updates an existing contract's
  `flagged`/`note`/`decision-updated-at` fields.
- Generic, brand-neutral tool: never hardcode or reference a specific real
  company, fund, or SME name in code, templates, or docs.
- Treat contract-level revenue and repayment data as sensitive. Never commit
  a local credential file or Busabase secrets.

## Busabase Resources

Two Bases under one application Folder (`kelly-portfolio-health`), declared
in `content/kelly-portfolio-health-app/app/js/config.js` and the generated template sidecars under `content/`:

- `contracts`: one row per RBF/private-credit contract — funding terms
  (`funding-amount`, `cap-multiple`, `cap-amount`), `cumulative-repayment`, a
  6-month `monthly-revenue` series (JSON array), `status`, and the human
  review `flagged`/`note`/`decision-updated-at` fields written directly onto
  the same row. Totals, repayment lag, concentration, and the
  revenue-decline watchlist are never stored — they are pure/derived from
  these rows and recomputed on every read.
- `settings`: sanitized config (fund name, base currency, risk-policy
  thresholds), one row keyed by `kind`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/portfolio-schema.md` for
exact field shapes.

## Portfolio Health Model

`content/kelly-portfolio-health-app/app/js/portfolio-model.js` (`computeInsights`) is ported verbatim from
the retired `content/kelly-portfolio-health-app/server/insights.ts`:

- **Repayment lag** — per contract, `expected_pct` (months elapsed / term)
  vs. `actual_pct` (collected / cap); `lag_pp = expected_pct - actual_pct`,
  with a `severity` of `ok | watch | high` driven by
  `risk_policy.lag_watch_pp` / `lag_high_pp` (defaults 15 / 25 percentage
  points).
- **Concentration** — funding-amount concentration by category and by city,
  as a percentage of active-contract AUM.
- **Watchlist** — a contract qualifies when its most recent month's revenue
  is at least `risk_policy.revenue_decline_pct` (default 10%) below the
  average of its prior months (minimum 4 months of history).
- **At-risk count** — any contract with a non-`ok` lag severity, or
  `status: delinquent`.

No randomness, no ML — the same snapshot always produces the same insights.

## Direct Contract Decision

The human action writes straight onto the contract's own Busabase record
through `busabase-sdk`, exactly like `kelly-llm-gateway`'s rollout writes —
there is no approval queue and no separate decisions bucket:

- **Flag for review** / **Clear flag**: toggles `flagged` (`"true"`/`"false"`).
- **Save note**: sets `note` (free text).

Both stamp `decision-updated-at` with the current time. From a standalone
local preview the write merges immediately (trusted operator); from the
deployed AirApp it creates a pending ChangeRequest for the trusted process
to merge, per the AirApp boundary in `$busabase-app-creator`.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock portfolio (~52
  contracts across 8 categories and 10 cities) with computed insights, for
  documentation and screenshots. It never reads or writes Busabase and never
  claims a real connection; demo flag/note actions only update the
  in-memory snapshot already rendered in the browser tab.
- `?demo=overview`, `?demo=concentration`, `?demo=watchlist` select named
  demo scenes/routes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

UI language: support English and Chinese chrome with `Auto` default.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-portfolio-health-app dev` only when local preview/debugging is explicitly
requested.

## Views

- `#/overview`: total AUM, total collected, weighted-average repayment
  progress, at-risk count, category allocation donut, and the contracts most
  lagging their expected repayment pace.
- `#/contracts`: sortable table (business, category, city, funding amount,
  actual progress, lag, status).
- `#/contracts/<id>`: per-contract detail — funding/cap/collected, expected
  vs. actual progress, a revenue sparkline, and the flag/note action.
- `#/concentration`: funding-amount concentration by category and city.
- `#/watchlist`: contracts with a recent revenue decline, each with a
  sparkline and a flag-for-review / clear-flag action.
- `#/settings`: sanitized configuration summary — data provider, fund name,
  base currency, and risk-policy thresholds. Never expose secret values.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-portfolio-health-app/` project and
  `pnpm --dir content/kelly-portfolio-health-app dev` remains supported;
- all persistent config, state, and domain data use `busabase-sdk` and the
  declared resource map — no local JSON, browser storage, or provider
  choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Contracts, Concentration, Watchlist, and Help & Settings render
  on desktop and phone widths;
- `pnpm --dir content/kelly-portfolio-health-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never contact an external system, move money, or change
contract terms from the AirApp.
