---
name: kelly-revshare-simulator
description: Busabase-backed App-in-Skill control-panel/workspace for a deal analyst to model revenue-based-financing (RBF) deals for SME businesses (retail/F&B chain stores). Use when the user invokes $kelly-revshare-simulator or /kelly-revshare-simulator, wants to model a revenue-share or merchant-cash-advance deal, project cash flow and repayment, compute a Cash-Flow Payout Multiple, effective annualized merchant cost, or compare/underwrite multiple financing scenarios. Pure deterministic math, no external calls, no real trading/payment side effects. Scenario create/edit/delete and the underwriting decision are direct writes made by the analyst, not a review/approval queue.
metadata:
  category: rbf
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-revshare-simulator
    resources:
      - scenarios
      - settings
    risk: sandbox

---

# Revenue-Share Contract Simulator

## Overview

Kelly Revenue-Share Simulator is a Busabase Cloud App-in-Skill. Its canonical
product surface is the AirApp in Busabase, not a separate local-data
product. The same Hono source supports an explicitly requested local preview
with OAuth connection bootstrap. It is a control-panel/workspace for a deal
analyst modeling revenue-based-financing (RBF) deals: a funder advances a
principal to an SME business (e.g. a bubble tea, gym, or hotpot restaurant
chain) in exchange for a share of monthly revenue until a repayment cap
multiple is reached or the term ends. The analyst tunes inputs, sees the
projected cash flow and cumulative repayment, and records an underwriting
decision per named scenario — then saves several scenarios for side-by-side
comparison.

This is generic, brand-free tooling: business names in seed data are
placeholder archetypes (bubble tea chain, gym chain, hotpot restaurant), not
real companies.

This is a direct-manipulation control panel, not a review-then-approve
queue: creating, editing, or deleting a scenario, and recording the
underwriting decision, are all direct writes made straight through
`busabase-sdk` from the browser — the same way `kelly-lead-funnel`'s kanban
stage moves and `kelly-agent-builder`'s agent-config CRUD work. There is no
AI-authored draft to approve and no separate execute/decisions step; the
projected result (`cash_flow_payout_multiple`, `effective_annual_cost_pct`,
risk flags) is pure/derived from a scenario's saved inputs and recomputed on
every read (`content/kelly-revshare-simulator-app/app/js/simulator-model.js`, ported from the retired
`lib/simulate.ts`).

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-revshare-simulator-app/` artifact.
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
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Revenue-Share Simulator overview"></td>
    <td width="50%"><img src="assets/screenshots/scenario-detail.webp" alt="Revenue-Share Simulator scenario detail"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Portfolio-level summary across saved scenarios: average effective cost, flagged deals, and deals still needing an underwriting decision.</td>
    <td><strong>Scenario detail</strong><br>Cash-flow/cumulative-repayment chart, Cash-Flow Payout Multiple, effective annualized merchant cost, risk flags, and the decision panel.</td>
  </tr>
  <tr>
    <td colspan="2" width="100%"><img src="assets/screenshots/comparison.webp" alt="Revenue-Share Simulator comparison"></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Comparison</strong><br>Side-by-side table of selected scenarios' inputs, projected repayment, payout multiple, effective cost, and decisions.</td>
  </tr>
</table>

## Boundary

- Pure deterministic math over analyst-supplied inputs. The app never
  fetches live revenue, banking, or payment data, and never disburses,
  transfers, or moves money.
- The AirApp reads and writes its own Busabase Bases only; there is no
  execution/merge step beyond the direct write itself. Deleting a scenario
  always requires an explicit Busabase review step before it merges (the
  platform rejects `autoMerge` on record deletes) — on a standalone local
  preview the app completes that review+merge itself immediately since the
  local operator is the trusted actor; from a deployed AirApp the delete
  request stays pending for a human to review directly in Busabase.
- Risk flags are neutral, rule-based observations — never automated
  approve/reject decisions. A human always makes the underwriting call.
- Generic, brand-neutral tool: never hardcode or reference a specific real
  company or SME name in code, templates, or docs.

## Busabase Resources

Two Bases under one application Folder (`kelly-revshare-simulator`),
declared in `content/kelly-revshare-simulator-app/app/js/config.js` and the generated template sidecars under `content/`:

- `scenarios`: one row per saved deal scenario — the analyst's raw inputs
  (business type, average monthly revenue, revenue volatility, principal,
  initial and step-down revenue-share rates, repayment cap multiple, term)
  and the underwriting decision (`decision-action`, `decision-note`,
  `decided-at`). The projected cash-flow/repayment result (monthly
  projection, Cash-Flow Payout Multiple, effective annualized cost, risk
  flags) is never stored — it is pure/derived from these inputs and
  recomputed on every read.
- `settings`: sanitized config (base currency, underwriting policy
  thresholds), one row keyed by `kind`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes.

## Domain Model

Inputs per scenario (`content/kelly-revshare-simulator-app/app/js/simulator-model.js` `simulateScenario`,
ported verbatim from the retired `lib/simulate.ts`):

- `business_type`, `avg_monthly_revenue`, `revenue_volatility_pct`
- `principal` (proposed advance)
- `initial_share_rate_pct` (revenue share until breakeven)
- `step_down_share_rate_pct` (reduced share rate after principal is recovered)
- `repayment_cap_multiple` (e.g. 1.5x principal — the total obligation cap)
- `term_months`

Computed, always fresh, never stored:

- `monthly[]`: month-by-month revenue, share rate, payment, cumulative
  repayment, and breakeven/cap flags.
- `cash_flow_payout_multiple`: a P/E-like ratio — principal ("price") divided
  by the annualized repayment cash flow ("earnings"). Lower is faster payback
  for the funder.
- `effective_annual_cost_pct`: the annualized cost implied by paying back
  `total_repayment` over the months elapsed, expressed like an APR.
- `risk_flags[]`: `cap_not_reached`, `merchant_cost_too_high`,
  `high_revenue_volatility`, `thin_term_buffer` — deterministic, rule-based,
  never automated decisions.

No randomness, no ML — the same scenario input always produces the same
result. Read `references/ui-schema.md` before editing the app or
`content/kelly-revshare-simulator-app/app/js/simulator-model.js`.

## Direct Scenario Writes

There is no decisions/approval bucket. Every scenario action writes straight
through `busabase-sdk` from the browser (`content/kelly-revshare-simulator-app/app/js/providers/busabase-provider.js`):

- **Create** / **Update**: `bases.createChangeRequest` / `records.changeRequest`
  with the analyst's saved inputs.
- **Record underwriting decision**: `records.changeRequest` sets
  `decision-action`/`decision-note`/`decided-at` directly on the scenario's
  own record — `approve_underwriting`, `needs_revision`, `reject`, or
  cleared back to undecided.
- **Delete**: `records.changeRequest` with `operation: "delete"`. Busabase
  always requires an explicit review before a delete merges (`autoMerge` is
  rejected server-side for deletes, unlike create/update) — from a
  standalone local preview the app reviews and merges its own delete request
  immediately after submitting it (the trusted local operator approving
  their own action); from a deployed AirApp the request stays pending for a
  human to review directly in Busabase.

From a standalone local preview create/update/decision writes merge
immediately (trusted operator); from the deployed AirApp they create a
pending ChangeRequest for the trusted process to merge, per the AirApp
boundary in `$busabase-app-creator`.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock batch of four
  scenarios (bubble tea chain, gym chain, hotpot restaurant, one
  deliberately risky example that trips the risk flags) for documentation
  and screenshots. It never reads or writes Busabase and never claims a real
  connection; demo create/edit/delete/decision actions only update the
  in-memory snapshot already rendered in the browser tab.
- `?demo=scenarios` and `?demo=comparison` select named mock scenes;
  `?demo=detail` opens the first mock scenario's detail pane.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

UI language: support English and Chinese chrome with `Auto` default.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-revshare-simulator-app dev` only when local preview/debugging is explicitly
requested.

## Views

- `#/overview`: portfolio-level metrics and the list of scenarios still
  needing a decision.
- `#/scenarios`: filterable scenario list (`All`, `Undecided`, `Approved`,
  `Needs Revision`, `Rejected`).
- `#/scenarios/new`: new scenario input form.
- `#/scenarios/<id>`: cash-flow chart, computed metrics, risk flags, editable
  inputs, the underwriting decision panel, and delete.
- `#/comparison`: pick multiple saved scenarios for a side-by-side table.
- `#/settings`: sanitized config summary and underwriting policy thresholds.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-revshare-simulator-app/` project and
  `pnpm --dir content/kelly-revshare-simulator-app dev` remains supported;
- all persistent config, state, and domain data use `busabase-sdk` and the
  declared resource map — no local JSON, browser storage, or provider
  choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Scenarios, Comparison, and Help & Settings render on desktop and
  phone widths;
- `pnpm --dir content/kelly-revshare-simulator-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never fetch live revenue/banking/payment data or move
money from the AirApp.
