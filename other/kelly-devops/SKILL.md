---
name: kelly-devops
description: Product-fleet ops desk (Busabase App-in-Skill) for uptime/service health, SSL certificate expiry, domain renewal, API key rotation, cloud spend anomalies, and a review queue of agent-proposed action cards. Use when the user invokes $kelly-devops or /kelly-devops, or asks about uptime, service health checks, SSL certificate expiry, domain renewal, domain expiry, API key rotation, token rotation reminders, cloud spend anomaly, billing spikes, ops desk, incident review, or reviewing agent-proposed action cards (renew domain, rotate key, investigate spend, restart service, acknowledge incident).
metadata:
  category: platform
  tags:
    - risk:gated-write
    - surface:busabase
    - surface:sendgrid
  busabase:
    template: true
    folderSlug: kelly-devops
    resources:
      - services
      - expiries
      - spend-providers
      - spend-products
      - actions
      - events
      - settings
    risk: gated-write

---

# Kelly DevOps

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly DevOps overview"></td>
    <td width="50%"><img src="assets/screenshots/actions.webp" alt="Kelly DevOps action queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Fleet health desk with service, certificate, domain, and spend summaries plus a recent events feed.</td>
    <td><strong>Action queue</strong><br>Agent-proposed renew/rotate/investigate action cards with evidence and approval controls.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/expiries.webp" alt="Kelly DevOps expiry ledger"></td>
    <td width="50%"><img src="assets/screenshots/services.webp" alt="Kelly DevOps services"></td>
  </tr>
  <tr>
    <td><strong>Expiry ledger</strong><br>Domains, SSL certificates, key rotations, and plan renewals in one table with color-coded days-left.</td>
    <td><strong>Services</strong><br>Monitored endpoints with uptime, latency sparklines, TLS certificate status, and check history.</td>
  </tr>
</table>

## Overview

Use this skill as Kelly's product-fleet operations desk. It watches the
health and expiry surface of a multi-product SaaS portfolio — service
uptime, SSL certificate expiry, domain registration expiry, API key/token
rotation reminders, and cloud spend anomalies — in one Busabase-backed
App-in-Skill dashboard, plus a review queue of agent-proposed action cards.
Real network probes (HTTP/TLS, RDAP, cloud billing) are genuine external
operations a browser cannot perform: `scripts/check_services.mjs` probes
service health and TLS certificates, `scripts/sync_domains.mjs` checks
domain expiry via RDAP, `scripts/ingest_spend.mjs` is the single write-path
for billing data, and `scripts/execute_decisions.mjs` prints the plan for
approved action cards (and, only after the agent performs the real action
manually, marks it done). The AirApp itself only reads Busabase and writes
review decisions.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, run whatever checks are due and give the user the clickable
AirApp URL (or the local preview URL when local preview is explicitly
requested). Use chat-only mode only when the user says "纯聊天", "chat only",
"不要打开 UI", or similar; then present numbered action cards (`Action #1`)
and take verdicts in chat.

**The AirApp itself never probes a URL, checks WHOIS/RDAP, or touches a
cloud billing API.** It reads and writes Busabase records only. All three
external-check directions are genuinely trusted-process-only:
`scripts/check_services.mjs` and `scripts/sync_domains.mjs` are the only
places that make an outbound network probe, and `scripts/ingest_spend.mjs`
is the only place billing data enters the system.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-devops-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Boundary

- Checks are read-only network probes of Kelly's own endpoints and domains: HTTP GET for status/latency, a TLS handshake for certificate expiry, and public RDAP lookups for domain expiry. Nothing else is contacted.
- The AirApp reads and writes Busabase records only. It must not probe endpoints, call registrars or cloud APIs, renew anything, rotate anything, or restart anything.
- Renewals, key rotations, service restarts, and spend remediation are approval-required and executed by the agent outside the app, only after the matching action card is `approved`. `scripts/execute_decisions.mjs` never performs these operations itself — it only prints the plan, and its only write path (`--complete`) marks a card `done` after the agent reports the real action succeeded.
- Never store registrar, cloud, or provider credentials in Busabase. Secrets live only in local env files referenced by name from the roster JSON files the check scripts take as input.
- Never commit roster/payload JSON files, env files, or raw provider billing responses.

## Busabase Resources

Seven Bases under one application Folder (`kelly-devops`), declared in
`content/kelly-devops-app/app/js/config.js` and the generated template sidecars under `content/`:

- `services`: monitored endpoints — roster (name, product, url) and the latest HTTP/TLS check result (status, latency, uptime, SSL issuer/expiry, history, warnings) in the same row.
- `expiries`: one ledger row per domain, API key rotation, or plan renewal (registrar/auto-renew for domains, rotation policy detail for keys). SSL certificate expiry rows are derived client-side from `services`, never stored twice.
- `spend-providers`: per cloud/billing provider month-to-date vs last-month spend.
- `spend-products`: per-product spend allocation for the same billing period.
- `actions`: the review queue — agent-proposed action cards (`renew_domain`/`rotate_key`/`investigate_spend`/`restart_service`/`ack_incident`) with reason, evidence, plan, target, and the human verdict.
- `events`: append-only feed of check runs, incidents, expiry warnings, spend anomalies, and action decisions.
- `settings`: one row (`record-id: "config"`) with expiry-warning/critical days, degraded-latency threshold, and spend-anomaly percentage.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ops-schema.md` for exact
field shapes. Derived values — SSL cert expiry, `days_left` for every
expiry row, spend `delta_pct`/`anomaly`/`share_pct`, and every metric — are
recomputed client-side from the stored rows on every read, so the ledger is
always fresh regardless of when a browser session loads it relative to the
last check run.

## First Run And Onboarding

On invocation, check the `services` and `expiries` Bases. If both are empty,
guide setup before running real checks: ask, turn by turn, products in the
portfolio, monitored endpoints (name/URL/product), domains (registrar,
auto-renew flag), API keys under rotation policy (name, env var,
rotate-every-days, last rotation), billing sources (provider plus the agent's
own credential handling), and thresholds (expiry warning days, degraded
latency, spend anomaly %). Ask for non-secret details only; secrets go into
local env files, never chat. Write the answers into a roster JSON file (see
`references/ops-schema.md`) and register everything with:

```bash
node skills/kelly-devops/scripts/check_services.mjs roster.json --apply
node skills/kelly-devops/scripts/sync_domains.mjs roster.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-devops-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: ops command desk. Human-attention panel (actions needing decision, items expiring within 14 days, services down), fleet summary cards (services up/total, certs ok/expiring, domains ok/expiring, month-to-date spend vs last month), recent events feed, and check freshness per check type.
- `#/services` and `#/services/<id>`: monitored endpoints with name, product, URL, status (up/degraded/down), latency, 7-day uptime, and cert days-left. Detail shows recent check history with an inline SVG latency sparkline, certificate summary (issuer, expiry), response metadata, and warnings.
- `#/expiries` and `#/expiries/<id>`: one expiry ledger across types (domain, ssl_cert, api_key_rotation, plan_renewal) with item, product, type badge, expiry date, color-coded days-left (<7 red, <30 amber), auto-renew flag, and linked action. Detail shows renewal guidance.
- `#/spend`: per-provider cards (MTD, last month, delta %, anomaly flag) and a per-product allocation table. Anomaly cards link to their action card.
- `#/actions` and `#/actions/<id>`: the review queue with workflow states `needs_review`, `changes_requested`, `approved`, `done`, `blocked`. Each card shows a stable ref (`Action #1`), type, reason, evidence, concrete plan, editable review note, and decision buttons (approve / request changes / block / save note) that write the verdict directly onto the action record through `busabase-sdk`.
- `#/settings`: sanitized config summary. Monitored services/domains/key-rotation rosters derived from the same live Busabase rows, thresholds, and onboarding state. Never exposes secret values.

Demo mode:

- `?demo=overview`, `?demo=services`, `?demo=expiries`, `?demo=spend`, and `?demo=actions` select named deterministic mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase. Decision buttons still work but act on in-memory state only and show a demo notice.

UI language: support English and Chinese chrome with `Auto` default. Keep
service names, URLs, domain names, and provider names in their original
form.

## Check Workflow

1. Detect mode. Default to AirApp-first.
2. Check the `services`/`expiries` Bases. If both are empty, enter onboarding.
3. Run checks on a sensible cadence (or when the user asks):
   - `node scripts/check_services.mjs [roster.json] --apply` — HTTP status/latency per endpoint plus TLS certificate expiry via `node:tls`; re-checks every service already registered in Busabase and registers any new ones from `roster.json`. Also upserts key-rotation due dates into the expiry ledger. Run every visit or every few hours.
   - `node scripts/sync_domains.mjs [roster.json] --apply` — domain expiry via RDAP (`https://rdap.org/domain/<name>`); per-domain failures degrade gracefully. Run daily or on demand.
   - `node scripts/ingest_spend.mjs payload.json --apply` — the single write-path for billing data. The agent gathers the payload from cloud billing tools/exports (for example the aws-billing/google-cloud-billing skills), then this script validates, merges, and flags anomalies (MTD above the configured % of last month) and proposes `investigate_spend` action cards.
4. Every script is a dry run by default; pass `--apply` to actually write to Busabase.
5. Give the user the AirApp URL and report what needs a decision.
6. Trust the agent-proposed action cards created by the check scripts (renew_domain, rotate_key, investigate_spend, restart_service, ack_incident); each carries reason, evidence, and a concrete plan.

## Actions Workflow

1. The user reviews action cards in `#/actions` (or by ref in chat) and gives verdicts: approve, request changes (with a note), or block — written directly onto the action record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. For approved cards, run `node scripts/execute_decisions.mjs` to print the plan (`renew_domain` → registrar + domain, `rotate_key` → env var name, `investigate_spend` → provider, `restart_service` → service id, `ack_incident` → event id). This performs no external side effects and no Busabase writes.
3. Execute the approved operation outside the app with the user's own tools. Then run `node scripts/execute_decisions.mjs --complete <action_id> --note "what was done"` to mark the card `done` and append an event — the only write path this script has, and it only runs when explicitly asked.
4. If a target is missing (no registrar, no env var name), block and ask for configuration instead of guessing.

## Safety Defaults

- Treat domain renewals, key rotation, service restarts, DNS changes, billing changes, and anything spending money as approval-required.
- Prefer read-only credentials for billing sources when possible.
- Redact tokens and token-like strings in logs, reports, and UI state; the roster JSON files carry only env-var *names*, never values.
- Keep stable ids (`service_id`, `expiry_id`, `action_id`, `ref`) so repeated checks and executions are idempotent.
- If a check result looks inconsistent (e.g. cert days-left disagrees with RDAP), surface a warning and ask; do not invent corrections.

## Useful Commands

```bash
node skills/kelly-devops/scripts/check_services.mjs roster.json --apply
node skills/kelly-devops/scripts/sync_domains.mjs roster.json --apply
node skills/kelly-devops/scripts/ingest_spend.mjs payload.json --apply
node skills/kelly-devops/scripts/execute_decisions.mjs
node skills/kelly-devops/scripts/execute_decisions.mjs --complete <action_id> --note "..."
pnpm --dir skills/kelly-devops/content/kelly-devops-app dev
```

In normal use, invoke `/kelly-devops`, let the skill run the checks that are
due, and open the AirApp.
