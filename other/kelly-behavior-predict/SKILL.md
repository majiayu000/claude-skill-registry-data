---
name: kelly-behavior-predict
description: Busabase App-in-Skill dashboard over a fixed, deterministic mock user-behavior funnel dataset (browse → search → compare → booking attempt/abandon → complete) for a generic consumer booking product. Use when the user invokes $kelly-behavior-predict or /kelly-behavior-predict, wants to review funnel drop-off, per-segment predicted next actions, or backtest a rule-based "predicted next action" heuristic against a mock historical sample. Fully deterministic mock data and a hand-recomputable rule — never a real ML/LLM model, never a live system.
metadata:
  category: growth
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-behavior-predict
    resources:
      - sessions
      - segments
      - settings
    risk: sandbox

---

# Predictive Recommendation Analytics Desk

## Overview

Use this skill as a Busabase-backed analytics dashboard for a **generic,
brand-free** consumer booking/e-commerce product. It aggregates a fully
deterministic mock user-behavior sample — 100 sessions across 5 session
archetypes ("segments") — into a funnel drop-off view, a rule-based
"predicted next action" per segment, and a prediction-accuracy backtest.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, ensure the mock sample exists (run the seed script below if the
`sessions` Base is empty) and give the user the clickable AirApp URL (or the
local preview URL when local preview is explicitly requested). Use chat-only
mode only when the user says "chat only", "no UI", "纯聊天", "不要打开 UI", or
similar.

This is primarily a **dashboard** app type (read-mostly, no approval
lifecycle). It carries exactly one narrow human-review surface: marking a
segment's prediction rule "trusted" or "needs recalibration" with a note,
written directly onto that segment's own Busabase record. That review never
edits the rule, the dataset, or any live system — it is a review record only.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Analytics Desk overview"></td>
    <td width="50%"><img src="assets/screenshots/funnel.webp" alt="Analytics Desk segments"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Overall funnel drop-off (browse → search → compare → booking attempt → complete), total sessions, overall backtest accuracy, and how many segments still need a trust decision.</td>
    <td><strong>Segments</strong><br>Per-segment cards: session count, dominant predicted action, backtest accuracy/F1, and the current trusted / needs-recalibration badge.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/segment-detail.webp" alt="Analytics Desk segment detail"></td>
    <td width="50%"></td>
  </tr>
  <tr>
    <td><strong>Segment detail</strong><br>Segment funnel, predicted-action distribution, sample sessions (predicted vs. mock actual), the matched/unmatched rule triggers that drove the prediction, and the trusted / needs-recalibration review panel.</td>
    <td></td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-behavior-predict-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Fully mock, fully deterministic. There is no real user data, no live
  product integration, and no real ML/LLM call anywhere in this skill —
  every "predicted next action" comes from a fixed if/else rule in
  `content/kelly-behavior-predict-app/app/js/behavior-model.js` (`evaluateRules()`/`predictNextAction()`).
- The AirApp reads and writes its own three Busabase Bases only.
- The one human action (mark trusted / needs recalibration + note) writes
  the `segments` Base's own row for that segment only. It never changes the
  rule, regenerates the sample, or triggers any other system.
- Do not name any real company, brand, or product. Keep the product profile
  generic ("Example Booking Co.", overridable via the `settings` Base).

## Busabase Resources

Three Bases under one application Folder (`kelly-behavior-predict`), declared
in `content/kelly-behavior-predict-app/app/js/config.js` and the generated template sidecars under `content/`:

- `sessions`: the fixed mock sample — 100 rows across 5 segments (raw
  behavior features, the funnel stage reached, and the seeded mock
  "actual" next action used only to make the backtest non-trivial).
  `predicted_action`/rule triggers are never stored — they are recomputed
  client-side from the raw features on every read.
- `segments`: one row per segment (5 rows) — the human review verdict
  (`decision-status`/`decision-note`/`decided-at`) on that segment's
  prediction rule, written directly onto the segment's own record.
- `settings`: one row (`kind = "config"`) holding the sanitized product
  profile (name, vertical, target precision) and the dataset seed.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes.

## First Run And Onboarding

On invocation, check the `sessions` Base. If it's empty, run the trusted seed
script to generate the fixed mock sample:

```bash
node skills/kelly-behavior-predict/scripts/generate_batch.mjs --apply
```

There are no credentials to collect — this skill never calls an external
system, so onboarding is just the optional product-profile labels below
(defaults apply if omitted).

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-behavior-predict-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: overall funnel drop-off, total sessions, overall backtest
  accuracy, and how many segments still need a trust decision.
- `#/segments`: per-segment cards (funnel size, dominant predicted action,
  backtest accuracy/F1, decision badge).
- `#/segments/<id>`: segment detail — funnel, predicted-action distribution,
  sample sessions (predicted vs. actual), rule triggers, and the decision
  panel (mark trusted / needs recalibration + note). Decisions write
  directly onto the segment record through `busabase-sdk`.
- `#/backtest`: prediction-accuracy backtest — overall and per-segment
  precision/recall/F1 tables.
- `#/settings`: sanitized config summary — data provider, product profile,
  target-precision note, and dataset seed.

## Demo Mode

- `?demo=1` regenerates the same fixed mock sample in the browser (never
  reads or writes Busabase) at the Overview — there is no live data source
  to demo *against*, so demo mode is always the same deterministic sample
  the seed script writes.
- `?demo=segments`, `?demo=backtest`, and `?demo=detail` select a starting
  route for screenshots/docs (segments grid, backtest view, or the
  `price_sensitive_browser` detail pane).
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

## Workflow

1. `node scripts/generate_batch.mjs --apply` (dry run without `--apply`)
   writes the fixed 100-session mock sample to the `sessions` Base and
   ensures a `segments` row exists for every segment (never resetting an
   existing decision) — run it once at setup, and again to refresh the
   `settings` product-profile row.
2. Open the app. **Overview** shows the overall funnel and backtest accuracy;
   **Segments** lists every segment with its dominant predicted action and
   current trust badge.
3. For each segment, open the detail view, review the funnel, the
   predicted-action distribution, the sample sessions (predicted vs. mock
   actual), and the exact rule triggers, then record `Mark trusted` or
   `Needs recalibration` with a note — written straight onto the segment
   record.

Read `references/ui-schema.md` before editing the app, scripts, or
`content/kelly-behavior-predict-app/app/js/behavior-model.js`.

## The Rule (not a model)

`content/kelly-behavior-predict-app/app/js/behavior-model.js` documents and implements the entire
prediction rule: a short, ordered list of if/else triggers over four mock
session signals (`cart_abandon_count`, `price_check_count`,
`days_since_last_visit`, `session_length`) plus `reached_stage`. The first
matching trigger determines `predicted_action`; the segment detail view
shows every trigger and whether it matched, so "why this prediction" is
always inspectable. The same module's `computeBacktest()` computes a
standard precision/recall/F1 confusion-matrix summary comparing
`predicted_action` against a seeded mock `actual_action` per session — this
is what the Backtest view renders, at both the overall and per-segment level.

## Safety

- Deterministic mock rule and sample only — never present them as a real
  ML/LLM prediction to the user; keep `content/kelly-behavior-predict-app/app/js/behavior-model.js` the
  single source of truth for every prediction shown.
- Do not invent real user data or a real ML/LLM call.
- The decision panel is a review record only — it must never regenerate the
  sample, edit the rule, or reach any external system.

## Useful Commands

```bash
node skills/kelly-behavior-predict/scripts/generate_batch.mjs --apply
pnpm --dir skills/kelly-behavior-predict/content/kelly-behavior-predict-app dev
```
## Execution reports

Re-read the active provider's decisions immediately before any approved execution. Record each concrete operation, target, status, timestamp, and error in the provider-backed execution report; keep app actions local-only.
