---
name: kelly-disclosure-tracker
description: Cross-Entity Disclosure Tracker App-in-Skill — a Busabase review workspace that helps a compliance/IR team assemble and track a standardized disclosure package per financing vehicle (fund/SPV), across a generic onshore origination entity, an offshore fund-manager entity, and a listing/exchange venue. Use when the user invokes $kelly-disclosure-tracker or /kelly-disclosure-tracker, wants to review disclosure checklists, vehicle readiness, cross-entity reconciliation flags, or reviewer notes across multiple financing vehicles. Review workspace only — it never files anything or calls any external system.
metadata:
  category: rbf
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-disclosure-tracker
    resources:
      - vehicles
      - items
      - settings
    risk: sandbox

---

# Cross-Entity Disclosure Tracker

## Overview

Use this skill as a Busabase-backed review-workspace desk for a compliance/IR
team assembling a standardized disclosure package per financing vehicle (fund
or SPV). Each vehicle's package spans three generic entity roles:

- **Origination entity** — the onshore entity that originates/services the
  underlying assets.
- **Fund-manager entity** — the offshore entity that manages the vehicle.
- **Listing venue** — the exchange/listing venue where the vehicle's notes or
  units are listed.

This is a **generic, brand-free** tool: no real company, regulator, or exchange
is referenced anywhere in the skill, its data, or its UI. All vehicle and entity
names in seed data are synthetic placeholders ("SPV Alpha 12", "Onshore
Originator A", "Exchange One", and so on).

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, ensure the mock portfolio exists (run the seed script below if the
`vehicles` Base is empty) and give the user the clickable AirApp URL (or the
local preview URL when local preview is explicitly requested). Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

This is a **workspace/review-queue hybrid**: the human works through a
checklist per vehicle rather than approving a linear queue, but the underlying
mechanics (statuses, decisions, writing straight to Busabase) follow the same
App-in-Skill review model used elsewhere in this batch.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Disclosure Tracker overview"></td>
    <td width="50%"><img src="assets/screenshots/vehicle-detail.webp" alt="Disclosure Tracker vehicle detail"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Portfolio-level summary (ready / blocked / in-progress vehicles) plus the vehicle grid.</td>
    <td><strong>Vehicle detail</strong><br>Checklist grouped by role (origination / fund-manager / listing venue) with a decision panel: verified, needs source, or flag inconsistent, plus a reviewer note.</td>
  </tr>
  <tr>
    <td colspan="2"><img src="assets/screenshots/flagged.webp" alt="Disclosure Tracker flagged items"></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Flagged</strong><br>Cross-entity reconciliation mismatches (e.g. a figure that doesn't reconcile between the fund-manager's AUM statement and the listing venue's filing) and reviewer-flagged inconsistencies, in one list.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-disclosure-tracker-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Review workspace only. The skill reads and writes its own Busabase Bases;
  it never calls any external system, filing portal, or exchange API.
- NEVER file, submit, or transmit anything to a real regulator, fund
  administrator, or exchange. There is no filing path in this skill by design.
- The AirApp reads and writes its own three Busabase Bases only.
- Treat all vehicle/entity data as sensitive by convention, even though the
  bundled seed data is synthetic.

## Busabase Resources

Three Bases under one application Folder (`kelly-disclosure-tracker`),
declared in `content/kelly-disclosure-tracker-app/app/js/config.js` and the generated template sidecars under `content/`:

- `vehicles`: one row per financing vehicle (fund/SPV) — the origination
  entity, fund-manager entity, listing venue, base currency, and target close
  date. Per-vehicle checklist completeness/readiness is never stored — it is
  recomputed client-side from the `items` Base on every read.
- `items`: one row per standardized disclosure checklist item, scoped to a
  vehicle and one of the three entity roles. Carries the raw checklist
  fields, an optional cross-entity reconciliation record, the reviewer's
  decision (`decision-action`/`decision-comment`/`decided-at`/
  `override-reconciliation`), and — once `scripts/execute_decisions.mjs`
  runs — an execution marker, all written directly onto the same row. Status
  is never stored — it is recomputed client-side from decision +
  reconciliation on every read.
- `settings`: up to two rows, keyed by `record-id`/`kind`: `config`
  (reviewer name) and `run` (the current batch's batch id + generated-at).

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes.

## First Run And Onboarding

On invocation, check the `vehicles` Base. If it's empty, run the trusted seed
script to generate the fixed mock portfolio:

```bash
node skills/kelly-disclosure-tracker/scripts/generate_batch.mjs --apply
```

There are no credentials to collect beyond Busabase itself — onboarding is
just confirming the reviewer's display name in the `settings` Base's `config`
row (defaults to "Unassigned reviewer" if omitted).

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-disclosure-tracker-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/vehicles`: portfolio summary (ready / blocked / in-progress vehicles)
  plus the vehicle grid; `?filter=needs_review|changes_requested|blocked|ready`
  narrows the grid.
- `#/vehicles/<vehicle_id>`: checklist grouped by role, with per-vehicle
  metrics.
- `#/vehicles/<vehicle_id>/<item_id>`: item detail + decision panel (verified /
  needs source / flag inconsistent) with a reviewer note. Decisions write
  directly onto the item record through `busabase-sdk`.
- `#/flagged`: every item currently flagged, across all vehicles, with the
  reconciliation detail that triggered the flag.
- `#/settings`: sanitized setup summary — data provider, reviewer name,
  onboarding state.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock portfolio (9 vehicles,
  6 items each) for documentation and screenshots. Demo mode never reads or
  writes Busabase.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

UI language: support English and Chinese (zh-CN) chrome with `Auto` default.

## Workflow

1. `node scripts/generate_batch.mjs --apply` (dry run without `--apply`)
   writes the fixed 9-vehicle / 54-item mock portfolio to the `vehicles` and
   `items` Bases (resetting every item's decision fields to the standard
   pre-seeded mix) and refreshes the `settings` Base's `run` row — run it
   once at setup, and again any time the demo portfolio needs resetting.
2. Open the app. **Vehicles** shows the portfolio summary and the vehicle
   grid; **Flagged** lists every cross-entity reconciliation mismatch or
   reviewer-flagged inconsistency in one place.
3. For each vehicle, open its checklist grouped by role (origination /
   fund-manager / listing venue), select an item, and record `Verified` /
   `Needs source` / `Flag inconsistent` with an optional reviewer note —
   written straight onto the item record. A "Verified" decision on an item
   with an unresolved reconciliation mismatch is held at "Awaiting source"
   until the reviewer explicitly acknowledges the mismatch.
4. `node scripts/execute_decisions.mjs --apply` (dry run without `--apply`)
   re-reads Busabase and writes an execution marker (`execution-status`,
   `execution-detail`, `executed-at`) onto every item, reporting which are
   settled (verified/done or flagged/blocked) vs still awaiting a human
   decision. It performs no external side effect — no filing, no submission,
   no transmission to a regulator, fund administrator, or exchange.

Read `references/ui-schema.md` before editing the app, scripts, or
`content/kelly-disclosure-tracker-app/app/js/tracker-model.js`.

## The Domain Model (not a filing system)

`content/kelly-disclosure-tracker-app/app/js/tracker-model.js` documents and implements the entire domain
model: the fixed seed portfolio (`buildSeedData()`), the per-item decision ->
status mapping (`computeItemStatus()`, including the reconciliation-mismatch
guardrail), and the per-vehicle/portfolio rollups
(`computeVehicleMetrics()`/`computeReadiness()`/`computeBatchMetrics()`).
Every function is pure and deterministic — same inputs always produce the
same output — so a human reviewer can audit every status and count by hand.
It backs the trusted seed script (`scripts/generate_batch.mjs`), the live
Busabase read path (`content/kelly-disclosure-tracker-app/app/js/providers/busabase-provider.js`), and the
offline `?demo=` scenario (`content/kelly-disclosure-tracker-app/app/js/providers/demo-provider.js`), so all
three always agree on the portfolio and its statuses.

## Safety

- Review workspace only: never file, submit, or transmit anything to a real
  regulator, fund administrator, or exchange — there is no filing path in
  this skill by design.
- Do not invent reconciliation figures beyond the deterministic demo/seed
  data; real usage should have the skill populate the `vehicles`/`items`
  Bases from actual source documents before asking the human to review.
- Redact anything that looks like a real credential or account number in
  logs, reports, and UI state (none are expected in this skill's data
  model).
- Keep the seed portfolio minimal and use stable item ids so repeated seeds
  stay idempotent (the seed script upserts by `vehicle-id`/`item-id`, never
  duplicating rows).

## Useful Commands

```bash
node skills/kelly-disclosure-tracker/scripts/generate_batch.mjs --apply
node skills/kelly-disclosure-tracker/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-disclosure-tracker/content/kelly-disclosure-tracker-app dev
```
