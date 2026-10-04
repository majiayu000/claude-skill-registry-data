---
name: kelly-creators
description: Influencer/creator marketing command desk (Busabase App-in-Skill) — the agent sweeps and fit-scores creator candidates, drafts outreach and briefs, and gates content before it ships; the human reviews creator cards, approves outreach/briefs/contracts, and tracks campaign ROI. Use when the user invokes $kelly-creators or /kelly-creators, mentions influencer or creator marketing, creator discovery, fit scoring, outreach DMs, campaign briefs, UGC, sponsorship or partnership deals, content review / FTC disclosure gating, or campaign ROI, or wants to review/approve agent-drafted creator outreach before it is sent through other channels.
metadata:
  category: marketing
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-creators
    resources:
      - creators
      - settings
    risk: gated-write

---

# Kelly Creators

## Overview

Kelly Creators is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. Use this skill as Kelly's personal influencer/creator
marketing operator: it keeps a dashboard over creator candidates, outreach
drafts, campaign briefs, and ROI, plus a review queue of agent-drafted
outreach and pre-publication content gates. The skill sweeps candidates from
whatever Kelly feeds it — a niche, a brand brief, a competitor's creators, an
exported list — scores fit, drafts outreach and briefs, and executes
approved sends only through other channels (for example `instagram-outreach`
or `kelly-email`) after explicit approval.

An **item is a creator engagement**: `handle`, `platform`, `followers`, `engagement_rate`, `fit_score`, `niche`, `est_rate`, `proposed_action`, `suggested_reply`, and the standard `status`/decision fields. A second item type is a **quality gate** on a live creator's draft post.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present numbered creators (`#1`) and take verdicts in the conversation.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-creators-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Philosophy

This skill is an App-in-Skill: a Codex/agent skill paired with a small companion UI. The skill does the real work (external reads, reasoning, drafting, executing approved sends); the app is a quiet operator surface over Busabase that never performs an external side effect. See the App-in-Skill specification paper: <https://mr-kelly.github.io/research/app-in-skill-specification-for-pairing-agent-skills-with-a-local-companion-ui.pdf>.

The domain follows the four-phase influencer-marketing discipline — **Discover → Plan → Activate → Measure** — used both as the pipeline funnel and as a `phase` facet on every item, derived from `stage`. Human clicks are reserved for judgment, edits, exceptions, and irreversible or money/contract actions.

## Capabilities (Discover / Plan / Activate / Measure)

The agent covers sixteen sub-skills, grouped by phase. Each generated item is tagged with its phase so the desk always shows where the program stands.

- **Discover** — `audience-mapper` (who the brand's buyers are), `trend-spotter` (rising formats/sounds/topics), `influencer-discovery` (sweep candidate creators), `fit-scorer` (the objective C³ ACE match score).
- **Plan** — `competitor-tracker` (which creators competitors use), `campaign-planner` (goals, mix, timeline), `brief-generator` (creative brief per creator), `budget-optimizer` (allocate spend across the roster).
- **Activate** — `outreach-manager` (draft and track outreach DMs/emails), `content-reviewer` (the pre-publication SHIP/FIX/BLOCK quality gate), `contract-helper` (terms, usage rights, exclusivity), `content-amplifier` (whitelisting/boosting approved posts).
- **Measure** — `landing-optimizer` (post-click experience), `performance-analyzer` (reach/engagement/conversion), `roi-calculator` (spend → estimated value, CPM, ROI), `report-generator` (campaign wrap-ups).

### Fit score — C³ ACE

`fit_score` (0-100) is the objective matching score: **C**ontent × **C**ommunity × **C**redibility crossed with **A**udience × **C**ost × **E**ngagement. `fit_breakdown` carries the six sub-scores shown in creator detail. Prefer fit over raw follower count when ranking candidates.

### Content-reviewer quality gate

Before a live creator's post publishes, the agent runs a `content-reviewer` gate that outputs **SHIP / FIX / BLOCK** over `ftc_disclosure` (is `#ad` disclosed above the fold?) and `claim_authenticity` (are product claims supportable, no cure/medical overreach?), plus `brand_safety`. A `fix` or `block` verdict is surfaced in the outreach queue for a human decision. This gate is `item_type: "quality_gate"` with `gate_verdict` and `gate_checks`.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Creators overview"></td>
    <td width="50%"><img src="assets/screenshots/creators.webp" alt="Kelly Creators candidates"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Pipeline funnel across the four phases, budget allocation, total reach, and the top fit-scored candidates.</td>
    <td><strong>Creators</strong><br>Sortable candidate cards with C³ ACE fit scores, platform, niche, and audience size.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/outreach.webp" alt="Kelly Creators outreach queue"></td>
    <td width="50%"><img src="assets/screenshots/roi.webp" alt="Kelly Creators ROI board"></td>
  </tr>
  <tr>
    <td><strong>Outreach</strong><br>Needs-review approval queue with editable outreach drafts and the FTC/claim disclosure gate.</td>
    <td><strong>ROI</strong><br>Per-creator spend, estimated value, CPM, and return once a partnership goes live.</td>
  </tr>
</table>

## Boundary

- The skill may read sources Kelly provides, sweep and score creators, draft outreach/briefs/contracts, run content gates, and write to Busabase.
- The AirApp reads and writes Busabase only. It must never send DMs or emails, call platform APIs, post content, or perform any external side effect.
- Outbound outreach, briefs, and contracts are always approval-required. Sending is delegated to other skills (for example `instagram-outreach`, `tiktok-outreach`, `kelly-email`) and happens only after the user approves the specific item. `scripts/execute_decisions.mjs` only marks an approved engagement `done` after re-reading Busabase; it performs no sending itself.
- Treat money and contract terms (rates, usage rights, exclusivity) as sensitive and approval-required. Never expose secret values in the UI.

## First Run And Onboarding

On invocation, check the `kelly-creators-profile` settings row for
readiness. If it is absent, guide setup before doing real creator work.

Ask for non-secret setup details only: operator profile (name, role, company, timezone), brand(s) and positioning, target niches, program budget and base currency, outreach platforms and which skill handles each, style/tone for drafts, and risk keywords (money/contract). Never ask the user to paste secret values into chat. Busabase authentication is ambient inside the deployed AirApp.

## Busabase Resources

Two Bases under one application Folder (`kelly-creators`), declared in
`content/kelly-creators-app/app/js/config.js` and the generated template sidecars under `content/`:

- `creators`: every creator candidate/engagement plus every content-reviewer quality gate under review — `handle`, `platform`, `niche`, `followers`, `engagement_rate`, the C³ ACE `fit_score`/`fit_breakdown`, `stage`, workflow `status`, `proposed_action`, `est_rate`, `risk`, `channel`, `reason`, `audience_note`, editable `suggested_reply`, `est_value`, `spend`, the quality-gate fields (`gate_verdict`, `gate_checks`), and the human verdict fields `decision_note` / `decided_at`.
- `settings`: one row per `kind` — `kelly-creators-profile` (operator profile, brand(s), program budget/currency/niches, style tone, platforms) and `kelly-creators-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/creators-schema.md` for
exact field shapes. `phase`, `cpm`, and every rollup metric on the overview
are computed client-side from the `creators` Base on every read — they are
never stored.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-creators-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: command desk. Human-attention counts, the discovery → outreach → negotiating → live → measured funnel (tagged by phase), budget allocation, total reach, and top candidates by fit.
- `#/creators` and `#/creators/<creator_id>`: candidate cards with fit score, platform, niche, followers, engagement rate, and rate — sortable by fit / followers / engagement / cost. Detail shows the C³ ACE breakdown, the outreach draft (or the quality-gate checks), and the full engagement record.
- `#/outreach`: review queue over agent-drafted outreach and content gates in workflow states `needs_review`, `changes_requested`, `approved`, `done`, `blocked`. Each item shows a stable row ref (`#1`), fit score, phase/risk badges, an editable `suggested_reply` draft, a `Review note` textarea, and decision buttons Approve / Request changes / Block that write straight onto the Busabase record.
- `#/roi`: per-creator spend, estimated value, CPM, and ROI.
- `#/settings`: sanitized config summary. Operator profile, brand(s), program budget and target niches, configured platforms, data provider, and onboarding state. Never expose secret values.

Demo mode:

- `?demo=1` opens a deterministic mock program for documentation and screenshots.
- `?demo=overview`, `?demo=creators`, `?demo=outreach`, `?demo=roi`, and `?demo=detail` select named mock scenes; `detail` deep-links to a creator detail.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase. All handles are invented.

UI language: support English and Chinese chrome with `Auto` default. Keep creator names, handles, notes, and drafts in their original language.

## Review Workflow

Read `references/creators-schema.md` before editing the app or its domain logic.

A human verdict (`approve` / `request_changes` / `block` / `revise`) writes
the new `status` plus `decision_note` / `decided_at` directly onto the
creator record through `busabase-sdk`; `approve` with an edited draft also
updates `suggested_reply`. From a standalone local preview the write merges
immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge.

## Normal Workflow

1. Detect mode. Default to App UI.
2. **Discover/Plan:** when Kelly feeds a niche, brand brief, competitor, or candidate list: upsert creator engagements to Busabase by stable `creator_id`, compute the C³ ACE `fit_score` and `fit_breakdown`, set `stage`/`phase`, draft `suggested_reply` outreach or briefs with `status: "needs_review"`, add money/contract risk badges and `est_rate`. The overview's rollups recompute automatically on every read.
3. Give the user the AirApp URL (or local preview URL) to review the funnel, the candidate cards, and the outreach queue.
4. For an engagement moved to `changes_requested`, re-draft `suggested_reply` per the review comment and write it back to `needs_review`.
5. **Activate:** on "execute" / "send approved outreach": run `node scripts/execute_decisions.mjs --apply` to re-read approved engagements from Busabase and mark them `done`. Then perform the actual sends only through the corresponding skill with the approved, possibly user-edited draft, one item at a time. Run the `content-reviewer` gate on live drafts and surface FIX/BLOCK verdicts for approval.
6. **Measure:** as campaigns go live and complete, update `spend`, `est_value`, and move engagements to `measured`; summarize ROI in the `#/roi` view.
7. Never send anything for items without an explicit `approve` decision, and never re-send items already marked `done`.

## Safety Defaults

- Treat every outbound message, brief, contract, rate commitment, usage-rights term, and exclusivity clause as approval-required.
- Never publish or approve a live post that fails the `content-reviewer` gate (missing FTC disclosure or unsupportable claims) without a human decision.
- Store only the minimum creator content needed for review; keep raw scraped data and platform exports out of Busabase.
- Redact tokens and credential-like strings from logs, reports, and UI state; expose only boolean readiness for configured platforms.
- Keep stable ids (`creator_id`) and `ref` numbers so repeated updates and executions are idempotent.
