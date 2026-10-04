---
name: kelly-lead-funnel
description: Busabase-backed App-in-Skill control panel / kanban board for a BD or sourcing team triaging merchant and business financing leads for a lender or investment fund. Use when the user invokes $kelly-lead-funnel or /kelly-lead-funnel, wants to review the deal sourcing pipeline, funnel, lead board, or asks to move a lead's stage, reject a lead, add a note, score a lead, or see funnel conversion rates. Deterministic rule-based lead scoring only — never an LLM call — and never sends outreach, signs term sheets, or moves money.
metadata:
  category: rbf
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-lead-funnel
    resources:
      - leads
      - settings
    risk: local-write

---

# Deal Sourcing Funnel

## Overview

Kelly Lead Funnel is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. It gives a BD/sourcing team a kanban board plus a
per-lead detail panel to triage merchant/business financing leads (merchant
cash advance, revenue-based financing, or similar) for any lender or
investment fund: move a lead's stage, reject with a reason, and leave notes —
all direct, immediate writes to Busabase.

This is a control-panel/kanban App-in-Skill, not a review-then-approve queue:
there is no AI-authored draft to approve and no separate execute/decisions
step. The score and suggested next action are computed by a documented
rule-based function (`content/kelly-lead-funnel-app/app/js/lead-funnel-model.js`, ported from the
retired `lib/scoring.ts`); the human sourcing-team operator makes every
stage/reject/note decision directly in the kanban UI, the same way
`kelly-crm`'s kanban stage moves work.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only mode
only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-lead-funnel-app/` artifact.
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
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Deal Sourcing Funnel overview"></td>
    <td width="50%"><img src="assets/screenshots/kanban.webp" alt="Deal Sourcing Funnel kanban board"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Funnel summary header with per-stage counts, conversion rates, and rejection rate.</td>
    <td><strong>Kanban board</strong><br>Leads across New → Data-Verified → Scored → Term-Sheet-Ready → Rejected, with a score chip per card.</td>
  </tr>
  <tr>
    <td colspan="2"><img src="assets/screenshots/lead-detail.webp" alt="Deal Sourcing Funnel lead detail"></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Lead detail</strong><br>Score breakdown by factor, suggested next action, notes, stage-move actions, and reject-with-reason.</td>
  </tr>
</table>

## Boundary

- Deterministic, rule-based lead-quality score only
  (`content/kelly-lead-funnel-app/app/js/lead-funnel-model.js`). NEVER call an LLM to score, rank, or
  auto-reject a lead.
- The AirApp reads and writes its own Busabase Bases only; it never sends
  outreach, emails, signs term sheets, disburses funds, or touches any
  external system. There is no trusted execute/handoff script — the direct
  kanban writes (stage move, reject, note) are the full extent of what
  happens.
- Generic, brand-neutral tool: never hardcode or reference a specific real
  company, lender, or fund name in code, templates, or docs.
- Treat lead financial data as sensitive. Never commit real lead data, a
  local credential file, or Busabase secrets.

## Busabase Resources

Two Bases under one application Folder (`kelly-lead-funnel`), declared in
`content/kelly-lead-funnel-app/app/js/config.js` and the generated template sidecars under `content/`:

- `leads`: one row per merchant/business lead — brand name, category, city,
  store count, est. monthly revenue, lead source, data verifiability, funnel
  `stage`, `rejection-reason`, `notes` (JSON array), and `stage-history`
  (JSON array). `score`/`score_breakdown`/`suggested_action` are never
  stored — they are pure/derived from these fields plus the fund's
  `scoring_criteria` and recomputed on every read, so a criteria change is
  reflected immediately with no staleness to manage. Stage moves,
  rejections, and notes are written directly onto the lead's own record by
  the human sourcing-team operator in the kanban board.
- `settings`: sanitized fund profile and scoring-criteria config (no
  secrets), one row keyed by `kind`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/lead-schema.md` for exact
field shapes.

## Scoring

`content/kelly-lead-funnel-app/app/js/lead-funnel-model.js` (`scoreLead`) computes a deterministic
0-100 score from four weighted, explainable factors — chain-size fit (30),
revenue-scale fit (30), category risk (25), and data verifiability (15) —
against the fund's `scoring_criteria` (ideal store-count band, ideal
monthly-revenue band, category risk tiers). `suggestNextAction` maps the
score and stage to a deterministic next step. Every point on the 0-100 scale
is explained by a `score_breakdown` row (factor, weight, contribution,
rationale) so the UI can show a transparent breakdown, never a bare number.

## Direct Kanban Actions

All human actions write straight onto the lead's own Busabase record through
`busabase-sdk`, exactly like `kelly-crm`'s kanban stage moves — there is no
approval queue and no separate decisions bucket:

- **Move stage**: advance a lead through New → Data-Verified → Scored →
  Term-Sheet-Ready. Appends a `stage-history` entry.
- **Reject**: move a lead to `rejected`. Always requires a `reason`, which is
  stored on the lead and also recorded in `stage-history`.
- **Add note**: append a timestamped note to the lead.

From a standalone local preview the write merges immediately (trusted
operator); from the deployed AirApp it creates a pending ChangeRequest for
the trusted process to merge, per the AirApp boundary in
`$busabase-app-creator`.

## Demo Mode

- `?demo=1` or `?demo=board` opens a deterministic, fully offline mock
  pipeline (21 leads across all 5 stages, ported verbatim from the retired
  `lib/mock-leads.ts`) for documentation and screenshots.
- `?demo=lead` opens the first lead's detail pane; `?demo=settings` opens
  Help & Settings.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase and never claims a real
  connection; demo actions (move/reject/note) are read-only and raise an
  error if attempted.

UI language: English and Chinese chrome with `Auto` default.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-lead-funnel-app dev` only when local preview/debugging is explicitly
requested.

## Views

- `#/board`: funnel summary header + kanban across all 5 stages.
- `#/board/<stage>`: single-stage filtered list (used by the human-attention
  shortcuts for New / Scored / Rejected).
- `#/leads/<id>`: score breakdown, suggested next action, notes, stage-move
  buttons, reject-with-reason.
- `#/settings`: sanitized fund profile and scoring-criteria summary.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-lead-funnel-app/` project and
  `pnpm --dir content/kelly-lead-funnel-app dev` remains supported;
- all persistent config, state, and domain data use `busabase-sdk` and the
  declared resource map — no local JSON, browser storage, or provider
  choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Board, lead detail, and Help & Settings render on desktop and phone widths;
- `pnpm --dir content/kelly-lead-funnel-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never send outreach, sign a term sheet, or move money from
the AirApp.
