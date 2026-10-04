---
name: kelly-llm-gateway
description: Busabase-backed App-in-Skill dashboard for a shared LLM gateway's cost and model governance — daily spend trend, cost breakdown by service/model, a canary-rollout status board, and a deterministic cost/error anomaly list. Use when the user invokes $kelly-llm-gateway or /kelly-llm-gateway, or wants to review LLM gateway spend, model routing, canary rollouts, rollback readiness, or cost/error anomalies for services routed through one shared gateway to multiple LLM providers/models. Human actions (promote/rollback/hold a rollout, acknowledge an anomaly) write directly onto the route's own Busabase record — this skill never changes a real routing config.
metadata:
  category: platform
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-llm-gateway
    resources:
      - routes
      - services
      - models
      - settings
    risk: sandbox

---

# LLM Gateway Cost & Governance Desk

## Overview

Kelly LLM Gateway is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. It gives a platform team an operator dashboard over a
shared LLM gateway: several consuming services (e.g. Support Bot, Search
Ranking, Content Summarizer, Internal Copilot) routed through one gateway to
a mix of internal and external models. It aggregates per-service/per-model
call volume, cost, and error rate: an Overview (spend trend, rollout/anomaly
summaries), a Cost Breakdown table, a Canary Rollout status board, and an
Anomaly list.

This is deliberately **generic and brand-free**: no real company, product, or
model name appears anywhere in the code, config, or seed data — only role-based
service names ("Support Bot") and generic provider/model labels ("Provider A /
Model Large", "Internal Model v2").

This is a direct-manipulation operator dashboard, not a review-then-approve
queue: there is no AI-authored draft to approve and no separate execute/
decisions step. Anomalies are computed by a documented, deterministic
rule-based function (`content/kelly-llm-gateway-app/app/js/gateway-model.js`, ported from the retired
`content/kelly-llm-gateway-app/server/anomalies.ts`); the human platform operator makes every promote/
rollback/hold and acknowledgement decision directly in the UI, writing
straight onto the route's own Busabase record — the same way `kelly-lead-funnel`'s
kanban stage moves work.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only mode
only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-llm-gateway-app/` artifact.
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
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Gateway overview"></td>
    <td width="50%"><img src="assets/screenshots/cost-breakdown.webp" alt="Gateway cost breakdown"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Total daily spend trend, a canary-rollout summary, and a top anomalies preview.</td>
    <td><strong>Cost Breakdown</strong><br>Sortable service × model table: calls, cost, error rate, canary %, status.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/rollouts.webp" alt="Gateway rollouts"></td>
    <td width="50%"><img src="assets/screenshots/anomalies.webp" alt="Gateway anomalies"></td>
  </tr>
  <tr>
    <td><strong>Rollouts</strong><br>Canary-rollout status board with rollback readiness and promote/rollback/hold actions.</td>
    <td><strong>Anomalies</strong><br>Deterministic cost/error spikes vs each route's own rolling baseline, with acknowledgement.</td>
  </tr>
</table>

## Boundary

- Deterministic, rule-based anomaly detection only
  (`content/kelly-llm-gateway-app/app/js/gateway-model.js`). NEVER call an LLM to detect, rank, or
  auto-resolve an anomaly.
- The AirApp reads and writes its own Busabase Bases only; it never calls a
  live gateway API or touches a real routing config. There is no execution/
  merge step beyond the direct write itself — a human still applies the
  decision in the real system of record.
- Routes/services/models are never created by the AirApp; they enter
  Busabase through an external process (a future gateway usage-API adapter),
  the same way `kelly-lead-funnel`'s leads enter through an upstream sourcing
  process the app doesn't control. The AirApp only ever updates an existing
  route's rollout status or anomaly-ack fields.
- Generic, brand-neutral tool: never hardcode or reference a specific real
  company, gateway, or model name in code, templates, or docs.
- Treat cost/usage data as sensitive. Never commit a local credential file or
  Busabase secrets.

## Busabase Resources

Four Bases under one application Folder (`kelly-llm-gateway`), declared in
`content/kelly-llm-gateway-app/app/js/config.js` and the generated template sidecars under `content/`:

- `routes`: one row per service→model route — canary `status`, `canary-pct`,
  `rollback-ready`, a human decision `note`, a 14-day `daily` usage series
  (JSON array of `{date, calls, cost, errors}`), and per-anomaly-kind
  acknowledgement state (`cost-spike-ack`/`error-spike-ack`, JSON or empty).
  Today's totals and each route's own rolling cost/error baseline are never
  stored — they are pure/derived from `daily` and recomputed on every read.
- `services`: one row per consuming service routed through the gateway.
- `models`: one row per backing model/provider behind the gateway.
- `settings`: sanitized config (base currency, anomaly thresholds, non-secret
  gateway region/base URL/credential-env-var name), one row keyed by `kind`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/gateway-schema.md` for
exact field shapes.

## Anomaly Detection

`content/kelly-llm-gateway-app/app/js/gateway-model.js` (`computeAnomalies`) flags a cost spike and/or
an error spike per route by comparing today's `cost`/`error_rate` against
that route's own rolling baseline (mean of the preceding days in `daily`,
excluding today). Default thresholds: `cost_spike_threshold_pct: 50`,
`error_spike_threshold_pct: 100` (i.e. cost ≥1.5x baseline, or error rate
≥2x baseline), each overridable via the `settings` Base. Severity is `high`
at 2x the threshold, otherwise `watch`. No randomness, no ML — the same
snapshot always produces the same anomalies.

## Direct Rollout & Anomaly Actions

All human actions write straight onto the route's own Busabase record
through `busabase-sdk`, exactly like `kelly-lead-funnel`'s kanban stage
moves — there is no approval queue and no separate decisions bucket:

- **Promote**: sets `status: stable`, `canary-pct: 100`, `rollback-ready:
  false`.
- **Rollback**: sets `status: rollback`, `rollback-ready: false`.
- **Hold**: sets `status: hold` only.
- **Acknowledge an anomaly**: writes `{note, acknowledged_at}` onto the
  route's `cost-spike-ack` or `error-spike-ack` field, whichever the
  anomaly's `kind` refers to.

From a standalone local preview the write merges immediately (trusted
operator); from the deployed AirApp it creates a pending ChangeRequest for
the trusted process to merge, per the AirApp boundary in
`$busabase-app-creator`.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock gateway (4 services, 5
  models, 8 service/model routes, 14 days of history) with computed spend
  trend, rollout status, and anomalies for documentation and screenshots.
- `?demo=spend`, `?demo=rollouts`, and `?demo=anomalies` select named mock
  scenes (their initial route).
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase and never claims a real
  connection; demo rollout/ack actions only update the in-memory snapshot
  already rendered in the browser tab, never Busabase.

UI language: support English and Chinese chrome with `Auto` default.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-llm-gateway-app dev` only when local preview/debugging is explicitly
requested.

## Views

- `#/overview`: total daily spend trend (14 days), a canary-rollout summary,
  and a top anomalies preview.
- `#/spend`: sortable service × model cost-breakdown table (calls, cost, error
  rate, canary %, status).
- `#/rollouts`: canary rollout status board — canary %, rollback readiness,
  and `promote to 100%` / `rollback` / `hold` actions with a note.
- `#/anomalies`: cost/error anomalies vs each route's own rolling baseline,
  with acknowledgement.
- `#/settings`: sanitized setup summary — data provider, config path, gateway
  region/base URL, credential env var name, and onboarding state. Never
  expose secret values.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-llm-gateway-app/` project and
  `pnpm --dir content/kelly-llm-gateway-app dev` remains supported;
- all persistent config, state, and domain data use `busabase-sdk` and the
  declared resource map — no local JSON, browser storage, or provider
  choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Cost Breakdown, Rollouts, Anomalies, and Help & Settings render
  on desktop and phone widths;
- `pnpm --dir content/kelly-llm-gateway-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never call a live gateway API or change a real routing
config from the AirApp.
