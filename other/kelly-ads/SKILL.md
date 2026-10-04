---
name: kelly-ads
description: Ad-campaign command desk (投放指挥台, Busabase App-in-Skill) for a cross-border e-commerce seller running Amazon Ads, Meta (FB/IG), TikTok Ads, and Google Ads. Use when the user invokes $kelly-ads or /kelly-ads, or asks about 投放, ad campaigns, ad spend, ACOS, ROAS, Amazon Ads, TikTok ads, Meta ads, Google Ads, search terms, negative keywords, bid adjustment, budget pacing, CPC spikes, rejected ads, ad anomaly detection, 广告优化, or reviewing agent-proposed adjustment cards (negative keyword, bid down/up, pause target, budget shift, creative refresh).
metadata:
  category: ecommerce
  tags:
    - risk:gated-write
    - industry:ecommerce
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-ads
    resources:
      - platforms
      - campaigns
      - anomalies
      - adjustments
      - sync-log
      - settings
    risk: gated-write

---

# Kelly Ads

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Ads overview"></td>
    <td width="50%"><img src="assets/screenshots/campaigns.webp" alt="Kelly Ads campaigns"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Cross-platform ads board: blended ROAS/ACOS vs target, per-platform cards, spend vs revenue bars, and worst offenders.</td>
    <td><strong>Campaigns</strong><br>Campaign table with budget pace, spend, ROAS, and color-coded ACOS vs target across Amazon, Meta, TikTok, and Google.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/adjustments.webp" alt="Kelly Ads adjustment queue"></td>
    <td width="50%"><img src="assets/screenshots/alerts.webp" alt="Kelly Ads anomaly alerts"></td>
  </tr>
  <tr>
    <td><strong>Adjustment queue</strong><br>Agent-proposed bid, budget, and negative-keyword changes with evidence and expected impact, gated on approval.</td>
    <td><strong>Alerts</strong><br>Deterministic anomaly feed: ACOS breaches, budget burnouts, zero-conversion spend, CPC spikes, rejected ads.</td>
  </tr>
</table>

## Overview

Use this skill as Kelly's ad-campaign command desk. It aggregates spend and
performance from Amazon Ads, Meta (FB/IG), TikTok Ads, and Google Ads into
one Busabase-backed App-in-Skill board (spend, impressions, clicks,
conversions, revenue, ROAS, ACOS per campaign), detects anomalies
deterministically (ACOS above target for N days, budget exhausted before day
end, high-spend zero-conversion search terms/creatives, sudden CPC spikes,
paused/rejected campaigns), and turns them into agent-proposed adjustment
cards with evidence and expected impact. The human approves; the agent
executes approved adjustments outside the app via the platform APIs. Report
ingestion (real ad-platform report pulls) and anomaly checks are genuine
external/trusted operations a browser cannot perform:
`scripts/ingest_reports.mjs` is the single write-path for performance data,
`scripts/run_checks.mjs` runs the anomaly rules and drafts adjustment cards,
and `scripts/execute_decisions.mjs` plans the concrete operation for an
approved card (and performs no external side effect itself). The AirApp
itself only reads Busabase and writes review decisions.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, ingest fresh reports and run checks when due, and give the user
the clickable AirApp URL (or the local preview URL when local preview is
explicitly requested). Use chat-only mode only when the user says "纯聊天",
"chat only", "不要打开 UI", or similar; then present numbered adjustment cards
(`Adjustment #1`) and take verdicts in chat.

**The AirApp itself never calls an Amazon/Meta/TikTok/Google Ads API.** It
reads and writes Busabase records only. All platform-report ingestion is
genuinely trusted-process-only: `scripts/ingest_reports.mjs` is the only
place performance data enters the system.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-ads-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Boundary

- Report ingestion is read-only against the platforms: the agent pulls platform reports (API pulls, report exports, or pasted CSVs) outside the app and feeds them to `scripts/ingest_reports.mjs`. Nothing in this skill mutates a platform on its own.
- The AirApp reads and writes Busabase records only. It must not call platform APIs, change bids, budgets, keywords, or creatives, or touch any network beyond Busabase.
- Every bid/budget/keyword/creative mutation is approval-required and executed by the agent outside the app, only after the matching adjustment card is `approved`. `scripts/execute_decisions.mjs` is a dry-run planner, never an executor — it writes only an `execution-status: "planned"` marker onto the adjustment record and never flips its workflow `status`.
- After the agent performs the real mutation outside the app with the user's own credentials, it marks the adjustment `done` and records the real `execution` result directly on the adjustment record — the only write step in this workflow that is not scripted, because the actual platform mutation itself must never be automated.
- Ad account credentials live only in local env files the agent's own tooling uses to pull reports; never store tokens in Busabase or paste them into chat.
- Never commit report exports, raw platform responses, or `.env` files.

## Busabase Resources

Six Bases under one application Folder (`kelly-ads`), declared in
`content/kelly-ads-app/app/js/config.js` and the generated template sidecars under `content/`:

- `platforms`: connected ad-platform roster (Amazon Ads, Meta, TikTok Ads, Google Ads) — display-safe account id, status, currency, last sync. Rollups (spend/revenue/ROAS/ACOS/campaign count) are derived client-side from `campaigns`, never stored.
- `campaigns`: one row per campaign — budget, status, ACOS target, and the daily spend/impressions/clicks/conversions/revenue series plus the search-term/audience/creative/asset-group targets (both JSON-encoded).
- `anomalies`: the deterministic anomaly feed (`acos_breach`/`budget_exhausted`/`zero_conversion_spend`/`cpc_spike`/`rejected`) with evidence, severity, state, and a link to the adjustment card when one exists.
- `adjustments`: the review queue — agent-proposed adjustment cards (`negative_keyword`/`bid_down`/`bid_up`/`pause_target`/`budget_shift`/`creative_refresh`) with reason, evidence, current/proposed value, expected impact, and the human verdict.
- `sync-log`: append-only feed of ingest runs, anomaly checks, and execution plans.
- `settings`: one row (`record-id: "config"`) with ACOS/ROAS targets (default plus per-platform/per-product overrides), anomaly thresholds, currency rates, and CSV column mappings.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ads-schema.md` for exact
field shapes. Derived values — `totals_7d`, `trend`, per-platform rollups,
and every top-level metric — are recomputed client-side from the stored
campaign rows on every read, so the board is always fresh regardless of when
a browser session loads it relative to the last ingest/check run.

## First Run And Onboarding

On invocation, check the `platforms` and `campaigns` Bases. If both are
empty, guide setup before ingesting real data: ask, turn by turn, which
platforms are live and their display-safe account ids (Amazon
entity/profile, Meta `act_…`, TikTok advertiser id, Google customer id),
ACOS/ROAS targets (default plus per-platform or per-product overrides), and
anomaly thresholds (breach days, zero-conversion spend floor, CPC spike %,
budget pace). Ask for non-secret details only; the agent's own tooling holds
platform tokens, never Busabase or chat. Write the settings row and platform
roster with an initial ingest:

```bash
node skills/kelly-ads/scripts/ingest_reports.mjs payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-ads-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: ads command desk. Human-attention panel (adjustments to approve, critical anomalies, budget at risk today), KPI cards (spend MTD vs last month, blended ROAS, blended ACOS vs target, conversions), per-platform mini-cards with badges, a 14-day spend-vs-revenue daily bar chart (inline SVG, no chart library), a worst-offenders list (highest-spend zero-conversion targets), data freshness per platform, and recent sync activity.
- `#/campaigns` and `#/campaigns/<id>`: campaign table with name, platform badge, product/SKU, status (active/paused/rejected), daily budget + % spent today, spend 7d, ROAS, ACOS vs target (color-coded), and trend arrow. Detail shows the daily spend/ROAS series (inline SVG), the search terms/audiences/creatives table with per-row metrics, linked anomalies, and adjustment history.
- `#/alerts`: anomaly feed with severity badge, type badge (acos_breach/budget_exhausted/zero_conversion_spend/cpc_spike/rejected), campaign + platform, one-line evidence, age, state (open/actioned/dismissed/resolved), and a link to the adjustment card when one exists.
- `#/adjustments` and `#/adjustments/<id>`: the review queue with workflow states `needs_review`, `changes_requested`, `approved`, `done`, `blocked`. Each card shows a stable ref (`Adjustment #1`), type badge (negative_keyword/bid_down/bid_up/pause_target/budget_shift/creative_refresh), target, current → proposed value, reason with evidence, expected impact, an editable `Review note`, and decision buttons (approve / request changes / block / save note) that write the verdict directly onto the adjustment record through `busabase-sdk`.
- `#/settings`: sanitized config summary. Platform roster with display-safe account ids, ACOS/ROAS targets, anomaly thresholds, currency, and onboarding state. Never exposes secret values.

Demo mode:

- `?demo=1` opens a deterministic mock command desk for documentation and screenshots.
- `?demo=overview`, `?demo=campaigns`, `?demo=alerts`, and `?demo=adjustments` select named mock scenes (persona: "Nimbus Home", a home/kitchen gadget seller).
- `lang=en` or `lang=zh` forces UI chrome language; with `lang=zh` the demo reasons, evidence, impact estimates, and summaries are meaningfully localized for Chinese screenshots (campaign names may keep English product names).
- Demo mode never reads or writes Busabase. Decision buttons still work but act on in-memory state only and show a demo notice.

UI language: support English and Chinese chrome with `Auto` default. Keep
campaign names, search terms, SKUs, and platform data in their original
language.

## Sync Workflow

Data collection is agent-driven on invocation — there is no cron and the app
never fetches anything itself.

1. Detect mode. Default to AirApp-first.
2. Check the `platforms`/`campaigns` Bases. If both are empty, enter onboarding.
3. When the user asks for fresh numbers (or the board is stale), gather report data per platform outside the app: pull via the platform reporting APIs with the configured credentials, download report exports, or accept a CSV the user pasted/dropped.
4. Feed everything through the single write path:
   - `node scripts/ingest_reports.mjs payload.json --apply` — normalized JSON performance payload (shape documented in the script header and `references/ads-schema.md`).
   - `node scripts/ingest_reports.mjs --csv report.csv --platform amazon [--campaign <id>] --apply` — raw platform CSV export, columns mapped via the Settings row's `csv_mappings.<platform>`; the built-in parser handles quoted fields with embedded commas.
   - The script validates, converts currencies via the Settings row's `currency_rates`, merges the daily series by campaign+date (idempotent re-ingest), updates platform `last_sync_at`, and appends a sync-log entry.
5. Without `--apply` every script is a dry run that only prints what would change.
6. Run `node scripts/run_checks.mjs --apply` to refresh anomalies and draft skeleton adjustment cards for new critical anomalies.
7. Give the user the AirApp URL and report what needs a decision.

## Check Workflow

1. After ingest, run `node scripts/run_checks.mjs --apply`. It reads thresholds from the Settings row and detects, deterministically:
   - `acos_breach`: campaign ACOS above target for N consecutive spend days (`acos_breach_days`).
   - `budget_exhausted`: daily budget spent to `budget_exhausted_pct` before day end.
   - `zero_conversion_spend`: an enabled target at or above `zero_conversion_spend_floor` in 14-day spend with 0 conversions.
   - `cpc_spike`: latest-day CPC at least `cpc_spike_pct` above the trailing mean.
   - `rejected`: campaign or creative rejected by the platform.
2. Anomalies are upserted with stable ids: re-detection refreshes evidence, cleared conditions auto-resolve, `dismissed` stays dismissed. Re-running without data changes is idempotent.
3. New critical anomalies without a linked card get a skeleton adjustment card (`needs_review`). Enrich each skeleton before asking for approval: re-ingest with better evidence, write the concrete `current_value` → `proposed_value`, and a numeric `expected_impact` via a direct Busabase field edit.

## Adjustment Workflow

1. The user reviews adjustment cards in `#/adjustments` (or by `Adjustment #N` in chat) and gives verdicts: approve, request changes (with a note), or block — written directly onto the adjustment record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. `request_changes` leaves the card `changes_requested` with the reviewer's note on the record; revise the card (new evidence, resized proposal), then set it back to `needs_review`.
3. For approved cards, run `node scripts/execute_decisions.mjs --apply` to write a concrete planned operation onto each card (`add_negative_keyword` with term + campaign id, `set_bid` current → new, `pause_target`, `shift_budget` from → to, `refresh_creative`) as `execution-status: "planned"` — no external side effects, and the card's workflow `status` stays `approved`.
4. Re-read decisions immediately before executing. Execute the approved operation outside the app via the platform APIs with the user's credentials, then write `status: "done"` and the real `execution` result directly onto the adjustment record (via `busabase-sdk`, the agent's own trusted write — not a script), and append a sync-log entry.
5. If a target is missing (no account id, no term text, no destination campaign), block and ask for configuration instead of guessing.

## Safety Defaults

- Treat every bid change, budget change, keyword/negative change, pause/enable, and creative swap as approval-required; anything spending money is never automatic.
- Prefer read-only reporting scopes for tokens where the platform offers them.
- Redact tokens and token-like strings in logs, reports, and UI state; Busabase never stores platform credentials.
- Keep stable ids (`campaign_id`, `target_id`, `anomaly_id`, `adjustment_id`, `ref`) so repeated ingests, checks, and executions are idempotent.
- If report numbers look inconsistent (spend without impressions, revenue with zero conversions), surface a warning and ask; do not invent corrections.

## Useful Commands

```bash
node skills/kelly-ads/scripts/ingest_reports.mjs payload.json --apply
node skills/kelly-ads/scripts/ingest_reports.mjs --csv report.csv --platform amazon --apply
node skills/kelly-ads/scripts/run_checks.mjs --apply
node skills/kelly-ads/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-ads/content/kelly-ads-app dev
```

In normal use, invoke `/kelly-ads`, let the skill ingest and check what's
due, and open the AirApp.
