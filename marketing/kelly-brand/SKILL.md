---
name: kelly-brand
description: "Brand-narrative single source of truth (Busabase App-in-Skill) built on the TALE discipline — Trace / Architect / Land / Evaluate. The agent drafts positioning, the message house of value pillars, the story bank, evidence-backed proof points, and vocabulary/tone guardrails; the human curates which drafts become the CANONICAL narrative; a drift monitor flags off-brand usage across channels. Use when the user invokes $kelly-brand or /kelly-brand, mentions brand narrative, brand messaging, positioning, message house, value pillars, story bank, proof points, tone/vocabulary guardrails, narrative quality (NQS), brand drift, or wants a single source of truth for what the brand says."
metadata:
  category: marketing
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-brand
    resources:
      - items
      - drift-alerts
      - settings
    risk: local-write

---

# Kelly Brand

## Overview

Kelly Brand is a Busabase Cloud App-in-Skill. Its canonical product surface
is the AirApp in Busabase, not a separate local-data product. The same Hono
source supports an explicitly requested local preview with OAuth connection
bootstrap. Use this skill as the operator for a brand's **narrative single
source of truth**: it keeps a dashboard over the whole message house —
positioning, value pillars, the story bank, evidence-backed proof points,
and vocabulary/tone guardrails — plus a drift monitor that flags off-brand
usage across channels. The agent drafts; the human curates which drafts are
**adopted as the canonical narrative**; the skill records those adoptions
and can export the canonical narrative for downstream use.

Everything is organized by Aaron's **TALE** discipline — **Trace → Architect → Land → Evaluate** — and every narrative asset carries the TALE `phase` and the `sub_skill` that produced it.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present numbered assets (`#1`, `#2`) and take verdicts in the conversation.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-brand-app/` artifact.
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
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Brand message house"></td>
    <td width="50%"><img src="assets/screenshots/drift.webp" alt="Kelly Brand drift alerts"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>The message house — positioning, value pillars, overall NQS, and the drift-alert count.</td>
    <td><strong>Drift</strong><br>Cross-channel off-brand alerts — offending usage versus the canonical guardrail.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/narrative.webp" alt="Kelly Brand narrative"></td>
    <td width="50%"><img src="assets/screenshots/stories.webp" alt="Kelly Brand story bank"></td>
  </tr>
  <tr>
    <td><strong>Narrative</strong><br>Message pillars and vocabulary guardrails, canonical versus draft.</td>
    <td><strong>Story bank</strong><br>Customer stories and evidence-backed proof points.</td>
  </tr>
</table>

## The TALE Framework

The 4 phases are both an item facet (`phase`) and the shape of the work. The 16 sub-skills below are the capability taxonomy — each drafted asset names the sub-skill that produced it in `sub_skill`.

### Trace — map the ground truth
- **narrative-baseline-mapper** — capture the brand's current story as it actually reads today (origin story, status quo).
- **category-narrative-mapper** — map how the category talks so the brand can stand apart from it.
- **audience-belief-mapper** — surface what the audience already believes, needs, and objects to.
- **positioning-truth-tracer** — trace the defensible truths the positioning can stand on.

### Architect — design the message system
- **strategic-narrative-designer** — write the core **positioning statement** (the roof of the house).
- **message-system-architect** — build the **value pillars** that hold the positioning up.
- **brand-language-codifier** — codify the **vocabulary** (say-this/not-that) and **guardrails** (banned/regulated language).
- **story-bank-builder** — assemble the **story bank** of reusable customer and brand stories.

### Land — make it usable across channels
- **narrative-cascade-planner** — plan how the narrative cascades to each channel.
- **pitch-narrative-builder** — shape the narrative into a pitch.
- **narrative-enablement-kit** — package the narrative so teams can actually use it.
- **proof-point-packager** — package **proof points** with their evidence (a named source and stat).

### Evaluate — test, monitor, gate
- **message-test-designer** — design tests for whether messages land.
- **narrative-resonance-monitor** — monitor how the narrative resonates.
- **narrative-drift-monitor** — flag off-brand / misaligned usage across channels (the Drift view).
- **narrative-quality-auditor ⛩** — the **gate**: score narrative quality (NQS 0–100) via the TALE framework and output **SHIP / FIX / BLOCK**. This gate is prominent on the overview and on every asset.

## Narrative Quality Score (NQS) gate

The `narrative-quality-auditor ⛩` scores each asset and writes its own `SHIP`/`FIX`/`BLOCK` judgment as the item's `nqs-gate` — this is the auditor's call, not a numeric formula, so it is stored as-is. The **overall** NQS shown on the overview is a pure aggregate computed client-side from every scored item (mean of `nqs-score`, `Math.round`) with a purely numeric gate:

- **SHIP** (score ≥ 80) — ready to adopt as canonical.
- **FIX** (55–79) — usable but flagged for a concrete revision.
- **BLOCK** (< 55, or a proof point missing its source) — must not be published or adopted until fixed.

A `BLOCK` verdict from the auditor should be mirrored by a `blocked` status on the item until resolved.

## First Run And Onboarding

On invocation, check the `kelly-brand-profile` settings row for readiness.
If it is absent, guide setup before doing real narrative work.

Ask for non-secret setup details only: brand profile (name, category, audience, mission), the positioning inputs (for whom / who need / our brand is / that / unlike / because), channels monitored for drift and how each is reached, tone/style and reading level, official URLs, and the risk policy (banned phrases, regulated claims). Never ask the user to paste secret values into chat. Busabase authentication is ambient inside the deployed AirApp.

## Busabase Resources

Three Bases under one application Folder (`kelly-brand`), declared in
`content/kelly-brand-app/app/js/config.js` and the generated template sidecars under `content/`:

- `items`: every narrative asset under review — positioning, message pillars, story bank, proof points, vocabulary, and guardrails — with `type`, TALE `phase`, `sub_skill`, editable `draft`, NQS (`nqs-score`/`nqs-gate`), evidence (`evidence-source`/`evidence-stat`/`evidence-url`, proof points only), `risk`, workflow `status`, and the human verdict fields `decision-note` / `decided-at`.
- `drift-alerts`: cross-channel off-brand usage the drift monitor flagged — offending usage vs. canonical guidance, severity, and the same verdict fields.
- `settings`: one row per `kind` — `kelly-brand-profile` (brand profile, style/tone, official URLs, risk policy, monitored channels) and `kelly-brand-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/brand-schema.md` for
exact field shapes. The **overall NQS** and every metric on the overview are
computed client-side from the `items`/`drift-alerts` Bases on every read —
they are never stored.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-brand-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview` — **the message house**. The canonical/draft positioning statement at the top, the value pillars, the overall Narrative Quality Score (NQS) with its gate, canonical vs needs-review counts, and the open drift-alert count.
- `#/narrative` — message pillars plus vocabulary/guardrails, canonical vs draft, each editable with its NQS and TALE phase. Adopt / Request changes / Block per asset.
- `#/stories` — the story bank and the proof points with their evidence (source + stat). A proof point missing evidence is blocked.
- `#/drift` — off-brand/misalignment alerts the drift monitor flagged, each showing the offending usage vs the canonical guardrail, with Approve fix / Dismiss.
- `#/settings` — sanitized config summary: brand profile, tone/reading level, banned/regulated language, official URLs, monitored channels, data provider, and onboarding state. Never expose secret values.

The left sidebar keeps the fixed **workflow filters** (`All`, `Needs Review`, `Canonical` (= approved), `Done`, `Blocked`) as primary nav alongside the views. "Canonical" is the UI label for the `approved` state.

Demo mode:

- `?demo=1` opens a deterministic mock brand (invented "Fernpath") for documentation and screenshots.
- `?demo=overview`, `?demo=narrative`, `?demo=stories`, `?demo=drift`, and `?demo=settings` select named scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

UI language: support English and Chinese chrome with `Auto` default. Keep the brand's own narrative content (positioning, pillars, stories) in its original language.

## Review Workflow

Read `references/brand-schema.md` before editing the app or its domain logic.

A human verdict (`approve` / `request_changes` / `block` / `revise` for a
narrative item; `resolve_drift` / `dismiss_drift` for a drift alert) writes
the new `status` plus `decision-note` / `decided-at` directly onto the
record through `busabase-sdk`. From a standalone local preview the write
merges immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge.

## Normal Workflow

1. Detect mode. Default to App UI.
2. When the user feeds material (positioning inputs, existing copy, channel exports): write narrative items to Busabase — draft/upsert by stable `item_id` across the six `type`s, tag each with its TALE `phase` and `sub_skill`, run the **narrative-quality-auditor** to set each item's `nqs-score`/`nqs-gate`, and run the **narrative-drift-monitor** over monitored channels to (re)populate `drift-alerts`. The overview's overall NQS and every count recompute automatically on every read.
3. Give the user the AirApp URL (or local preview URL) to review the message house, the story bank, and the drift alerts.
4. For an item moved to `changes_requested`, re-draft it per the review comment and write it back to `needs_review`.
5. On "adopt" / "promote approved narrative": run `node scripts/execute_decisions.mjs --apply` to re-read approved items from Busabase and mark them `done`. Then, only for those promoted assets, update the canonical narrative and — if asked — `export_narrative` to a markdown file.
6. Never adopt or export an asset without an explicit `approve` verdict, and never re-promote an item already `done`. Never let a `BLOCK`/blocked proof point (no named source) reach any channel.

## Safety Defaults

- Treat unverified claims, regulated claims (`organic`, `#1`, `guaranteed`, `certified`, `carbon-neutral`), and legal/compliance wording as approval-required. Every public number must cite a named source.
- A proof point without evidence is `blocked` by the NQS gate; do not adopt or publish it.
- Store only the narrative content needed for review; keep raw channel exports out of Busabase.
- Redact tokens and credential-like strings from logs, reports, and UI state; expose only boolean source-readiness for configured channels.
- Keep stable ids (`item_id`, `alert_id`) so repeated updates and executions are idempotent.
