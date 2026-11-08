---
name: outreach-brief
description: 'Captures an outreach brief (offer, targets) and researches the local business climate. Use when the user wants to scope outreach ("draft an outreach brief", "prep outreach", "research local market"). Not for finding companies (use outreach-research).'
argument-hint: '[<seed description of the outreach>]'
allowed-tools: Agent, AskUserQuestion, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(printf *), Bash(rm *), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Outreach Brief + Local-Climate Research

## Overview

You are an orchestrator that prepares the front of an outreach campaign in two steps. First you run an iterative clarification loop to capture a complete outreach **brief** — what the user sells, who they target, where, and how — never guessing a value, asking until every required dimension is clear. Then you research the **local business climate** for each target industry in each target region (economic trends, regulatory shifts, industry deals, sector pain points) and synthesize a climate dossier. You produce two artifacts — `brief.json`/`brief.md` and `climate.json`/`climate.md` — then stop. Downstream skills consume them via a `brief:` argument.

## When to Use

Scopes an outreach effort before discovery: pins down the offer and target profile and grounds later proposals in local market conditions, not only per-company facts.

### When NOT to use

- The user wants to discover companies or build a lead list now — use `outreach-research` (optionally seeded with this skill's `brief:`).
- The user wants to deepen one company card or draft letters — use `outreach-enrich-company`.
- The user wants per-company news or timing signals — that lives in the enrichment agents, not here.

## Input

- `$ARGUMENTS` — optional free-text seed describing the outreach (offer, audience, geography). Treated as a starting point the intake loop gap-fills; it never substitutes for the loop. If empty, start the loop from scratch.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **RECENCY_MONTHS**: 12 — climate signals must fall within this window.
- **MAX_CLIMATE_COMBOS**: 20 — hard cap on industry × region combos researched; any excess is truncated in priority order and disclosed.
- **MAX_AGENTS_PER_WAVE**: 6 — concurrency cap per research wave; the kept combos are covered in sequential waves.
- **REQUIRED_BRIEF_DIMS**: `offering`, `icp`, `geography`, `goal_channels_voice` — the loop will not finish until all four are complete and unambiguous.

## Directory Structure

Two separate directories:

- **State** — `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`, the source of truth across phases; never rely on conversation memory.
- **Outreach data** — `<PROJECT_ROOT>/.mz/outreach/<run_name>/` (called `<RUN_DIR>` in phase files) holds `brief.json`, `brief.md`, temp `_climate_sources/` and `_climate/` folders, and the permanent `climate.json` + `climate.md` dossier.

`task_name` and `run_name` both follow `<YYYY_MM_DD>_outreach_brief_<slug>` (leading-date convention, underscores).

## Core Process

### Phase Overview

| #   | Phase                 | Agent(s)                                              | Details                      |
| --- | --------------------- | ----------------------------------------------------- | ---------------------------- |
| 0   | Setup                 | —                                                     | Inline below                 |
| 1   | Intake (clarify loop) | — (orchestrator, AskUserQuestion)                     | `phases/intake.md`           |
| 1.5 | Brief approval        | — (orchestrator, AskUserQuestion)                     | Inline below                 |
| 2   | Climate research      | N × `outreach-climate-source-finder` + `…-researcher` | `phases/climate_research.md` |

Read the relevant phase file when you reach that phase. Do not read both phase files upfront.

### Phase 1.5: Brief Approval

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Why the gate matters**: Phase 2 dispatches two parallel agent waves per industry × region combo; each dispatch costs tokens and time. Approval here is the cost cap — the user confirms the brief is right before the expensive climate research runs.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/outreach/<run_name>/brief.md` with the Read tool and capture its full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: brief gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the brief verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/outreach/<run_name>/brief.md` — do not substitute a path, summary, or placeholder. Structure:

```
## Brief ready for review — outreach-brief

<verbatim contents of <PROJECT_ROOT>/.mz/outreach/<run_name>/brief.md>

---
**Approve** → proceed to Phase 2 (local-climate research)  ·  **Reject** → abort the task, no research will run  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the brief in the question body, it lives in the plan message above:

- question: `The brief above is ready for review.`
- header: `Brief`
- options: **Approve** — proceed to Phase 2 (local-climate research) · **Reject** — abort the task, no research will run

**Response handling**:

- **Approve** → add `- brief approved: .mz/outreach/<run_name>/brief.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: brief_approved`, and proceed to Phase 2.
- **Reject** → update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` `Status` field to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → return to the Phase 1 intake loop, ask targeted follow-ups to resolve the feedback, overwrite `brief.json` and `brief.md`, then return to Surface 1, re-read `brief.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: brief gate`, stop. A missing answer is never approval.

## Red Flags

- You guessed a required brief field instead of asking the user for it.
- You launched climate research before the brief was approved.
- The climate dossier lives in chat instead of `.mz/outreach/<run_name>/`.
- Combos beyond the cap were dropped silently instead of disclosed in `## Decisions`.

## Verification

Before completing, output a visible block showing: run name, the absolute paths of `brief.md` and `climate.md`, the number of industry × region combos researched, and the per-combo signal counts. Confirm both artifact pairs exist on disk and the temp folders are gone.

______________________________________________________________________

## Phase 0: Setup

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

Parse the optional seed. Derive the name (same value for both dirs):

- `task_name` / `run_name` = `<YYYY_MM_DD>_outreach_brief_<slug>` where `<slug>` is a snake_case summary of the seed (max 20 chars; if no seed, use `untitled` and refine after intake). `<YYYY_MM_DD>` is today's date with underscores. On same-day collision append `_v2`, `_v3`.

```bash
mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"
mkdir -p "<PROJECT_ROOT>/.mz/outreach/<run_name>"
```

Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`:

```yaml
schema_version: 2
Status: running
Phase: 0
Started: <ISO timestamp>
phase_complete: false
what_remains: []
Seed: <seed or null>
RunName: <run_name>
```

After setup completes, read `phases/intake.md` and proceed to Phase 1.

______________________________________________________________________

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer. Record the brief-approval outcome and the researched combos in a `## Decisions` section of `state.md`.

## Resume Support

Before creating anything in Phase 0, check if `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` exists for the resolved `task_name`. If it does, read the `Phase` field and resume from the next incomplete phase. All phases are idempotent — re-running overwrites output files.

## Error Handling

- A research agent fails or returns empty: append an `Errors:` bullet in `state.md` and continue with available combos.
- All agents in a wave fail (zero results): stop and report the failure; do not synthesize an empty dossier as if complete.
- The user declines to specify a required brief sub-field: record it as `unspecified — user declined` and move on; never loop forever on a refused value.
- Never fabricate brief content or climate signals — incomplete is better than false.
