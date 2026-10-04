---
name: kelly-deal-scorer
description: Busabase App-in-Skill review queue that scores candidate SME financing deals (revenue-based/RBF-style credit) with a deterministic, fully auditable rule-based rubric — never an LLM or API call. Use when the user invokes $kelly-deal-scorer or /kelly-deal-scorer, wants to review a deal-underwriting queue, score financing candidates, compute a composite score breakdown, see a suggested revenue-share rate range, or record approve/send-back/reject decisions for a private-credit or RBF-style lending pipeline.
metadata:
  category: rbf
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-deal-scorer
    resources:
      - candidates
      - settings
    risk: sandbox

---

# Deal Scoring Desk

## Overview

Use this skill as a Busabase-backed review-queue desk for a generic SME
financing deal desk (private-credit / revenue-based-financing style). It
holds a mock queue of candidate businesses (name, category, city, monthly
revenue history, requested principal, red flags) and computes a deterministic
composite score (0-100) per candidate with a full, hand-recomputable
breakdown: each sub-factor's raw score, weight, and contribution, plus a
suggested revenue-share rate range. This is a generic, brand-free tool — it
does not reference any specific real company, lender, or fund.

**The scoring rubric is plain arithmetic in `content/kelly-deal-scorer-app/app/js/scorer-model.js`, not
an LLM or API call.** Every number the app shows can be recomputed with a
calculator from the candidate's raw fields and the rubric weights in the
`settings` Base.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, ensure the mock queue exists (run the seed script below if the
`candidates` Base is empty) and give the user the clickable AirApp URL (or
the local preview URL when local preview is explicitly requested). Use
chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or
similar.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Deal Scoring Desk overview"></td>
    <td width="50%"><img src="assets/screenshots/candidate-detail.webp" alt="Deal Scoring Desk candidate detail"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Queue-level summary header — score distribution, counts needing review vs. high-confidence — plus the candidate list.</td>
    <td><strong>Candidate detail</strong><br>Revenue history, red flags, requested principal, and the decision row (approve for term sheet / send back for more data / reject).</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/score-breakdown.webp" alt="Deal Scoring Desk score breakdown"></td>
    <td width="50%"></td>
  </tr>
  <tr>
    <td><strong>Score breakdown</strong><br>Per-factor raw score, weight, and contribution with an arithmetic trace for every sub-factor, plus the suggested revenue-share rate range.</td>
    <td></td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-deal-scorer-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Review-only. The skill scores a candidate queue and records human
  decisions in Busabase; it never wires money, signs a term sheet, or
  contacts a business.
- NEVER treat the composite score as legal or financial advice, and never
  auto-approve: a human decision (`approve_term_sheet` / `send_back_for_data`
  / `reject`) is always required before `scripts/execute_decisions.mjs` marks
  a candidate `done`.
- The AirApp reads and writes its own two Busabase Bases only.
- Treat candidate financials as sensitive review data; the composite score
  and every intermediate number are always recomputed client-side from the
  candidate's raw fields, never fabricated.

## Busabase Resources

Two Bases under one application Folder (`kelly-deal-scorer`), declared in
`content/kelly-deal-scorer-app/app/js/config.js` and the generated template sidecars under `content/`:

- `candidates`: one row per candidate business — raw underwriting fields
  (category, city, requested principal, monthly revenue history, red flags)
  plus the reviewer's decision (`decision-action`/`decision-comment`/
  `decided-at`) and workflow `status`, all written directly onto the same
  row. The composite score breakdown is never stored — it is recomputed
  client-side from the raw fields on every read.
- `settings`: up to two rows, keyed by `record-id`/`kind`: `config`
  (base currency + an optional rubric override for the fund's underwriting
  policy) and `run` (the current queue's batch id + generated-at).

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/scoring-schema.md` for
exact field shapes.

## First Run And Onboarding

On invocation, check the `candidates` Base. If it's empty, run the trusted
seed script to generate the fixed mock queue:

```bash
node skills/kelly-deal-scorer/scripts/generate_batch.mjs --apply
```

There are no credentials to collect beyond Busabase itself — onboarding is
just confirming the rubric weights and category risk tiers in the `settings`
Base's `config` row match the fund's underwriting policy (defaults apply if
omitted).

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-deal-scorer-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: queue-level summary — score distribution (high-confidence /
  needs review / low-confidence), workflow counts, and the candidate list.
- `#/candidates` and `#/candidates/<id>`: the full queue, filterable by
  status; detail shows revenue history, red flags, requested principal,
  score breakdown, suggested revenue-share range, and the decision row.
  Decisions write directly onto the candidate record through `busabase-sdk`.
- `#/settings`: sanitized rubric summary (weights, thresholds), active data
  provider, and onboarding state.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock queue (8 candidates
  across F&B/Retail/Fitness/Education) for documentation and screenshots.
  Demo mode never reads or writes Busabase.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

UI language: English and Chinese chrome with `Auto` default.

## Workflow

1. `node scripts/generate_batch.mjs --apply` (dry run without `--apply`)
   writes the fixed 8-candidate mock queue to the `candidates` Base
   (resetting every candidate's decision fields to `needs_review`) and
   refreshes the `settings` Base's `run` row — run it once at setup, and
   again any time the demo queue needs resetting.
2. Open the app. **Overview** shows the score distribution and workflow
   counts; **Candidates** lists every candidate, filterable by status.
3. For each candidate, open the detail view, review the revenue history
   chart, red flags, and the full score breakdown (every sub-factor's raw
   score/weight/contribution with an arithmetic trace), then record
   `Approve for term sheet` / `Send back for more data` / `Reject` with an
   optional note — written straight onto the candidate record.
4. `node scripts/execute_decisions.mjs --apply` (dry run without `--apply`)
   re-reads Busabase and marks every `approved` candidate `done`, preparing
   the local term-sheet-draft artifact at the suggested revenue-share rate.
   It performs no external side effect — no wiring, no signing, no
   contacting the business.

Read `references/scoring-schema.md` before editing the app, scripts, or
`content/kelly-deal-scorer-app/app/js/scorer-model.js`.

## The Rubric (not a model)

`content/kelly-deal-scorer-app/app/js/scorer-model.js` documents and implements the entire scoring
rubric: five weighted 0-100 sub-factors (revenue stability, growth trend,
category risk tier, principal-to-revenue ratio, track record & scale), each
with a human-readable arithmetic trace in `detail`. `computeScore()` is a
pure function — same inputs always produce the same composite score and
suggested revenue-share range, so a human reviewer can check every number
with a calculator. It backs the trusted seed script
(`scripts/generate_batch.mjs`), the live Busabase read path
(`content/kelly-deal-scorer-app/app/js/providers/busabase-provider.js`), and the offline `?demo=`
scenario (`content/kelly-deal-scorer-app/app/js/providers/demo-provider.js`), so all three always
agree on scoring.

## Safety

- Deterministic scoring only: never call an LLM or external API to produce a
  candidate's score — `content/kelly-deal-scorer-app/app/js/scorer-model.js` is plain arithmetic so
  every number is auditable.
- Never auto-execute a decision the human has not made.
- Do not invent candidates outside the fixed seed set; if the user wants a
  different queue, add to `content/kelly-deal-scorer-app/app/js/scorer-model.js`'s `CANDIDATE_SEEDS`
  and re-run the seed script.

## Useful Commands

```bash
node skills/kelly-deal-scorer/scripts/generate_batch.mjs --apply
node skills/kelly-deal-scorer/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-deal-scorer/content/kelly-deal-scorer-app dev
```
