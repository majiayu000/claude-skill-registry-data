---
name: kelly-launch
description: "Product-launch command desk (Busabase App-in-Skill) built on the RAMP discipline — Research / Assemble / Mobilize / Prove. The agent assembles the launch checklist and drafts launch assets, channel submissions (Product Hunt / Hacker News / directories), press pitches, and the launch-day runbook; the human approves the launch-readiness gate and steers launch day in a review UI. Use when the user invokes $kelly-launch or /kelly-launch, or mentions launching / shipping a product, a launch checklist or runbook, launch readiness, RAMP, Product Hunt / Show HN / press-kit / launch-email drafting, or wants to review and approve launch assets and channel submissions before they go public. This is launch OPERATIONS — the checklist, assets, submissions, and runbook — not a launch video (for a promo video use product-launch-video)."
metadata:
  category: marketing
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-launch
    resources:
      - items
      - channels
      - runbook
      - settings
    risk: gated-write

---

# Kelly Launch

## Overview

Kelly Launch is a Busabase Cloud App-in-Skill. Its canonical product surface
is the AirApp in Busabase, not a separate local-data product. The same Hono
source supports an explicitly requested local preview with OAuth connection
bootstrap. Use this skill as Kelly's product-launch command desk: it keeps a
dashboard over the launch checklist, launch assets, channel submissions,
press pitches, and the launch-day runbook, plus a review queue of
agent-drafted assets and submissions. The skill gathers launch context from
whatever Kelly feeds it — product docs, positioning notes, a target date —
assembles the RAMP checklist, drafts the assets and submissions, scores
launch readiness, and executes approved submissions/sends only through other
channels (for example `kelly-email` for press/launch email, or a channel
connector for Product Hunt) after explicit approval.

This is launch **operations**, not a launch video. For a promotional launch video, use `product-launch-video`; this desk drafts the checklist, copy, submissions, press pitches, and runbook that surround such a video.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present numbered items (`#8`) and take verdicts in the conversation.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-launch-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## The RAMP Discipline

kelly-launch implements the **RAMP** launch discipline — **Research / Assemble / Mobilize / Prove** — as its four item `phase`s and as the structure of the checklist. Every launch task or asset belongs to exactly one phase. The capability taxonomy the skill draws on within each phase:

- **Research** — decide what the launch is and who it's for: `positioning-mapper` (ICP + wedge + one-line positioning), `launch-tier-planner` (how big a launch this warrants), `launch-window-planner` (target date + timing around competitors/holidays), `early-access-designer` (waitlist / private beta / design partners).
- **Assemble** — build the assets: `message-house-builder` (headline + message pillars every asset inherits), `launch-asset-packager` (press kit, screenshots, demo, landing hero, changelog), `pricing-packaging-planner` (tiers + pricing page), `sales-enablement-kit` (support macros, launch FAQ, objection handling).
- **Mobilize** — put it in front of people: `launch-day-conductor` (the ordered launch-day runbook + on-call roster), `community-launch-runner` (Product Hunt submission, Show HN post, directory listings, waitlist email), `press-media-relations` (Tier-1 press pitches, embargo, briefings).
- **Prove** — measure and sustain: `launch-monitor` (channel status, funnel, support queue on launch day), `launch-feedback-synthesizer` (roll up reactions and objections), `launch-retro-analyzer` (what worked / what to change), `momentum-planner` (the follow-through after day one).

### Launch-readiness gate (RAMP → LQS → SHIP / FIX / BLOCK)

The `launch-readiness-auditor` ⛩ is the gate that decides whether the launch is go/no-go. It runs the RAMP framework across every item and produces a **Launch Quality Score (LQS, 0–100)** and a verdict:

- Each item carries a per-item readiness verdict: `SHIP` (ready), `FIX` (needs work but recoverable), or `BLOCK` (a hard blocker).
- **LQS** counts SHIP items full, FIX items half, BLOCK items zero, over all items.
- The overall verdict is `BLOCK` if any item is BLOCK, `FIX` if any blockers remain, else `SHIP`.

The readiness gate is the most prominent element of the Overview screen. The human approves the gate (steers which blockers must clear before launch) — this is the primary judgment call the desk reserves for a person.

## Philosophy

The App-in-Skill pattern pairs an agent skill with a small local companion UI: the skill does the real work (reads sources, drafts, scores, executes approved actions through other skills), while the app is a quiet operator surface for review and approval over local handoff files. See the spec paper: <https://mr-kelly.github.io/research/app-in-skill-specification-for-pairing-agent-skills-with-a-local-companion-ui.pdf>.

The boundary is the point: a launch is a burst of irreversible public actions, so the human's clicks are reserved for judgment (approve the gate, approve public submissions and press) while the agent absorbs the drafting and bookkeeping.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Launch overview"></td>
    <td width="50%"><img src="assets/screenshots/assets.webp" alt="Kelly Launch assets queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Launch countdown, the RAMP readiness gate with its LQS score, phase progress, and channel status.</td>
    <td><strong>Assets</strong><br>Approval queue for launch assets, Product Hunt / Hacker News submissions, and press pitches.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checklist.webp" alt="Kelly Launch checklist"></td>
    <td width="50%"><img src="assets/screenshots/launchday.webp" alt="Kelly Launch launch-day runbook"></td>
  </tr>
  <tr>
    <td><strong>Checklist</strong><br>Launch tasks grouped by RAMP phase — Research, Assemble, Mobilize, Prove.</td>
    <td><strong>Launch day</strong><br>An ordered launch-day runbook with war-room notes.</td>
  </tr>
</table>

## Boundary

- The skill may read sources Kelly provides, assemble the checklist, draft assets/submissions/pitches, score readiness, and write it all to Busabase.
- The AirApp reads and writes Busabase records only. It must never submit to Product Hunt / Hacker News, send press pitches or launch email, publish pages, call external APIs, or perform any other external side effect.
- Public submissions and press are always approval-required. Submitting/sending is delegated to other skills (for example `kelly-email` for press and launch email) and happens only after the user approves the specific item. `scripts/execute_decisions.mjs` only marks an approved item `done`; it performs no submission or sending itself.
- Treat launch copy, embargoed facts, and press lists as sensitive. Never commit real launch copy, tokens, press contacts, or Busabase credentials.

## Busabase Resources

Four Bases under one application Folder (`kelly-launch`), declared in
`content/kelly-launch-app/app/js/config.js` and the generated template sidecars under `content/`:

- `items`: the RAMP checklist/review queue — phase, title, owner, channel, readiness (SHIP/FIX/BLOCK), proposed action, workflow `status`, editable `draft`, reason, format, risk, and the human verdict fields `decision-note` / `decided-at`.
- `channels`: launch channels and their submission status.
- `runbook`: the ordered launch-day timeline.
- `settings`: one row per `kind` — `kelly-launch-profile` (product/launch profile, style tone, press lists, readiness policy, configured channels) and `kelly-launch-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/launch-schema.md` for
exact field shapes. The **RAMP readiness gate** (LQS + SHIP/FIX/BLOCK
verdict) and phase progress are computed client-side from the `items` Base
on every read — they are never stored.

## First Run And Onboarding

On invocation, check the `kelly-launch-profile` settings row for readiness.
If it is absent, guide setup before doing real launch work.

Ask for non-secret setup details only: product profile (name, tagline, homepage, category), launch target date and timezone, channels and which skill handles each submission, press list names, readiness policy (which channels are hard blockers, minimum ship ratio), style/tone for drafts, and which env var names hold channel/email tokens. Never ask the user to paste secret values into chat. Busabase authentication is ambient inside the deployed AirApp.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-launch-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: launch command desk. The launch-readiness gate (LQS + SHIP/FIX/BLOCK + blockers), a countdown to the target date, RAMP phase progress, channel-submission status, and the top assets awaiting review.
- `#/checklist`: the RAMP checklist — every launch task/asset grouped by phase (Research → Assemble → Mobilize → Prove), with status, per-item readiness, channel, and proposed action.
- `#/assets`: the approval queue over agent-drafted assets and submissions (press kit, PH submission, Show HN post, launch email, press pitch, changelog…). Each item shows a stable ref (`#8`), phase/readiness/risk badges, an editable `draft`, a `Review note`, and Approve / Request changes / Block decisions that write directly onto the item record.
- `#/launchday`: the launch-day runbook — an ordered timeline of actions (`T-60m … T+8h`) with owner and a war-room note per step.
- `#/settings`: sanitized config summary. Product/launch profile, readiness policy, press lists, configured channels, and onboarding state. Never expose secret values.

Sidebar workflow filters (All / Needs Review / Approved / Done / Blocked) remain the primary lens on the asset queue.

Demo mode:

- `?demo=1` (or `?demo=overview`) opens a deterministic mock launch for an invented product ("Trailhead") ~10 days out.
- `?demo=checklist`, `?demo=assets`, `?demo=launchday` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

UI language: support English and Chinese chrome with `Auto` default. Keep product names, launch copy, drafts, and runbook notes in their original language.

## Review Workflow

Read `references/launch-schema.md` before editing the app or its domain logic.

A human verdict (`approve` / `request_changes` / `block` / `revise`) writes
the new `status` plus `decision-note` / `decided-at` directly onto the item
record through `busabase-sdk`. From a standalone local preview the write
merges immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge.

## Normal Workflow

1. Detect mode. Default to App UI.
2. When Kelly feeds new material (product docs, positioning, a date): write RAMP items to Busabase with `phase`, per-item `readiness`, `proposed_action`, and an editable `draft` for assets/submissions. The readiness gate, phase progress, and channel status recompute automatically on every read.
3. Give Kelly the AirApp URL (or local preview URL) to review the checklist, the asset queue, and the launch-day runbook.
4. For an item moved to `changes_requested`, re-draft it per the review comment and write it back to `needs_review`.
5. On "execute" / "submit approved": run `node scripts/execute_decisions.mjs --apply` to re-read approved items from Busabase and mark them `done`, then perform the actual submissions/sends only through the corresponding skill (for example `$kelly-email` for a press pitch or launch email), one item at a time.
6. Never submit or send anything for an item without an explicit `approve` decision, and never re-submit an item already `done`. Do not let the launch go if the readiness gate is `BLOCK`.

## Safety Defaults

- Treat every public submission (Product Hunt, Hacker News, directories), press pitch, launch email, and pricing commitment as approval-required.
- Store only the minimum launch copy needed for review; keep raw source docs out of Busabase.
- Redact tokens and credential-like strings from logs, reports, and UI state; expose only boolean readiness for configured env vars.
- Keep stable ids (`item_id`, `ref`, `step_id`) so repeated updates and executions are idempotent.
