---
name: kelly-agent-eval
description: Review board (Busabase App-in-Skill) that runs a fixed suite of mock test cases against a baseline vs candidate agent version and surfaces rubric-scored regressions before a release. Use when the user invokes $kelly-agent-eval or /kelly-agent-eval, wants to review agent-version regressions, compare baseline vs candidate quality, triage a release, or record a release approve/block decision. Deterministic mock rubric scores only — not a real LLM-judge call, and it never deploys anything.
metadata:
  category: platform
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-agent-eval
    resources:
      - cases
      - settings
    risk: sandbox

---

# Agent Eval & Regression Board

## Overview

Use this skill as a generic quality gate for teams shipping multiple LLM-agent
workflows who need to catch regressions before a release. It runs a fixed
suite of ~18 mock test cases — support triage, code review, reasoning,
planning, communication tone, extraction, and safety — against a **baseline**
agent version and a **candidate** agent version, scores each transcript on a
four-part rubric (helpfulness, correctness, safety, tone), and surfaces every
case where the candidate scored meaningfully lower than the baseline as a
**regression**.

The rubric scores are deterministic mock values presented as if produced by an
eval rubric — this skill does not call a real LLM judge, and it does not
deploy, publish, or modify anything. It only reads and writes its own two
Busabase Bases.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, generate the run if it's missing and give the user the clickable
AirApp URL (or the local preview URL when local preview is explicitly
requested). Use chat-only mode only when the user says "chat only", "no UI",
or similar.

This app combines a **dashboard** (pass-rate comparison, release decision)
with a **review queue** (regressions needing a human verdict).

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Agent Eval Board overview"></td>
    <td width="50%"><img src="assets/screenshots/regressions.webp" alt="Agent Eval Board regressions list"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Baseline vs candidate pass-rate comparison, case-count metrics, and the release approve/block panel.</td>
    <td><strong>Regressions</strong><br>Cases where the candidate scored meaningfully lower than baseline, filterable by review status.</td>
  </tr>
  <tr>
    <td colspan="2"><img src="assets/screenshots/case-detail.webp" alt="Agent Eval Board case detail"></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Case detail</strong><br>Rubric bar comparison (helpfulness/correctness/safety/tone) plus a side-by-side transcript diff and the mark-blocking / mark-acceptable review note.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-agent-eval-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Read/generate the fixed mock eval suite in Busabase only.
- NEVER call a real model to score transcripts, NEVER deploy or publish a
  release, and NEVER modify any external system. There is no deploy path in
  this skill by design.
- The AirApp reads and writes its own two Busabase Bases only.
- Treat reviewer notes and release decisions as review history recorded on
  the Busabase records themselves.

## Busabase Resources

Two Bases under one application Folder (`kelly-agent-eval`), declared in
`content/kelly-agent-eval-app/app/js/config.js` and the generated template sidecars under `content/`:

- `cases`: one row per fixed mock test case — baseline/candidate transcripts,
  the four rubric scores for each, and the reviewer's decision
  (`decision-action`/`decision-note`/`decided-at`) on the same row.
- `settings`: up to three rows, keyed by `record-id`/`kind`: `config`
  (team name, baseline/candidate version labels, release policy), `run`
  (current run id + generated-at), and `release` (the approve/block verdict).

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/eval-schema.md` for exact
field shapes. `overall`/`pass`/`regression`/`improvement`/`status` are never
stored — they are recomputed client-side from the raw rubric scores on every
read (`content/kelly-agent-eval-app/app/js/eval-model.js`), so the board is always fresh regardless of
when a browser session loads it.

## First Run And Onboarding

On invocation, check the `cases` Base. If it's empty, run the trusted seed
script to generate the fixed mock suite:

```bash
node skills/kelly-agent-eval/scripts/generate_eval_run.mjs --apply \
  --team "Agent Quality Team" --baseline "v2.4.0 (baseline)" --candidate "v2.5.0-rc1 (candidate)"
```

There are no credentials to collect — this skill never calls an external
system, so onboarding is just the team/version labels above (all optional;
defaults apply if omitted).

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-agent-eval-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: baseline vs candidate pass-rate comparison, case-count metrics
  (total, regressions, improvements, pending review), and the release
  `Approve release` / `Block release` panel with a required note.
- `#/regressions`: every case where the candidate regressed, filterable by
  review status (needs review / blocking / acceptable).
- `#/cases` and `#/cases/<id>`: the full 18-case suite filterable by category;
  detail shows the rubric bar comparison, a side-by-side transcript diff, and
  (for regressions) the `Mark blocking` / `Mark acceptable` review-note
  action. Decisions write directly onto the case record through
  `busabase-sdk`.
- `#/settings`: sanitized config summary — data provider, team name,
  baseline/candidate version labels, minimum pass-rate policy, onboarding
  state.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock run (18 cases across
  seven categories) for documentation and screenshots.
- `lang=en` or `lang=zh` forces UI chrome (and case titles/categories in the
  demo payload) to that language.
- Demo mode never reads or writes Busabase.

UI language: supports English and Chinese chrome with `Auto` default.

## Workflow

1. `node scripts/generate_eval_run.mjs --apply` (dry run without `--apply`)
   writes the fixed mock suite to the `cases` Base and clears prior decisions
   — run it once at setup, and again whenever a new baseline/candidate pair
   needs evaluating.
2. Open the app. **Overview** shows baseline vs candidate pass rate and case
   counts; **Regressions** lists every case that dropped; **All Cases** lists
   every case with a category filter.
3. For each regression, open the case detail, compare the rubric bars and the
   side-by-side transcript diff, and record `Mark blocking` or
   `Mark acceptable` with a note — written straight onto the case record.
4. Once every regression has a decision, record the overall
   `Approve release` / `Block release` verdict with a note — written to the
   `settings` Base's `release` row.
5. `node scripts/export_release_report.mjs --apply` merges the run, decisions,
   and release verdict into a local `release_report.json` handoff file (default
   `exports/release_report.json` at the skill root). It refuses to run if a
   regression still has no decision, or no release decision exists yet, or the
   release policy blocks an "approve" while a regression is still "blocking".

Read `references/eval-schema.md` before editing the app, scripts, or
`content/kelly-agent-eval-app/app/js/eval-model.js`.

## Safety

- Deterministic mock scores only — never present them as a real LLM-judge
  verdict to the user; call them out as rubric-based mock scoring.
- Refuse to export a release report while a regression has no decision.
- Do not invent scores outside the fixed suite; if the user wants a different
  case, add it to `content/kelly-agent-eval-app/app/js/eval-model.js`'s `RAW_CASES` and regenerate the
  run.

## Useful Commands

```bash
node skills/kelly-agent-eval/scripts/generate_eval_run.mjs --apply
node skills/kelly-agent-eval/scripts/export_release_report.mjs --apply
pnpm --dir skills/kelly-agent-eval/content/kelly-agent-eval-app dev
```
