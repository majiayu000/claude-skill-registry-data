---
name: expert
description: 'Critiques one proposal or plan from several expert angles and reports strengths, weaknesses and risks. Use when the user says "critique this idea", "strengths and weaknesses of" or "poke holes in my plan". Not for generating ideas (use brainstorm).'
argument-hint: <idea or proposal to review>
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(mkdir *), Bash(date *), Bash(test *), Read, Write, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

# Expert Consultation Pipeline

## Overview

You orchestrate a Delphi-style expert panel review. A curated panel of 5 lenses — selected from 16 available perspectives — critiques an idea over **3 fixed rounds**. Each round every panelist emits a structured 5-field view (strengths/weaknesses/risks/suggestions/confidence); a neutral round synthesizer consolidates the outputs; the next round's panelists receive the summary plus their own prior view and may alter their position. After round 3, a dedicated report writer produces a multi-sided analysis report.

## When to Use

A critical multi-lens analysis of one specific proposal, plan, architecture, business idea, or design decision.

### When NOT to use

- The user wants to generate ideas from scratch — use `brainstorm`.
- The user wants a single concrete decision or implementation — use `build`.
- The user wants verification of an existing codebase change — use `audit` or `review-branch`.
- The problem has one objectively correct answer knowable from docs — look it up instead of consulting a panel.

## Input

`$ARGUMENTS` — The idea, proposal, or plan to review. Supports inline modifiers:

- `scope:branch|global|working` — when set, `expert-researcher` scans the codebase first so experts can ground feedback in real code (default: pure idea analysis, no scan). See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the scope modes and their git commands
- `@doc:<path>` — existing requirement/brief/RFC document to ingest

If `$ARGUMENTS` is empty, ask the user via `AskUserQuestion`. Never guess.

## Constants

- **PANEL_SIZE**: 5
- **TOTAL_LENSES**: 16
- **ROUNDS**: 3 (fixed — no early stopping, no convergence check)
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **REPORT_DIR**: `<PROJECT_ROOT>/.mz/reports/`
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Available Lenses

Panel picks 5 from 16 lenses: `lens-engineer`, `lens-artist`, `lens-philosopher`, `lens-mathematician`, `lens-scientist`, `lens-economist`, `lens-storyteller`, `lens-futurist`, `lens-psychologist`, `lens-historian`, `lens-cto`, `lens-seo`, `lens-security`, `lens-product`, `lens-devops`, `lens-data`.
Use the brief to balance primary, adjacent, and productive-tension lenses. Behavior is injected by this skill (critique mode); the same lens agents serve `/brainstorm` in ideation mode.

## Core Process

### Phase Overview

| #   | Phase                              | File                                                      | Loop?                        |
| --- | ---------------------------------- | --------------------------------------------------------- | ---------------------------- |
| 0   | Setup                              | inline below                                              | —                            |
| 1   | Intake + Optional Research + Panel | `phases/intake_and_panel.md`                              | —                            |
| 1.5 | Panel Approval Gate                | Inline below (+ `phases/intake_and_panel.md` for details) | user-feedback sub-loop       |
| 2   | Round Loop                         | `phases/round_loop.md`                                    | fixed 3 rounds, no early-out |
| 3   | Final Report                       | `phases/final_report.md`                                  | —                            |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. Extract brief, `scope:`, `@doc:` refs.
1. If brief is empty → `AskUserQuestion`. Never guess.
1. `task_name` = `<YYYY_MM_DD>_expert_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"`.
1. Write `state.md` with `schema_version: 2`, `Status`, `Phase`, `Started`, `phase_complete: false`, `what_remains: []`, `Round: 0`, `FilesWritten: []`.
1. Emit a visible setup block: `task_name`, working dir, report dir, detected modifiers.

### Phase 1.5: Panel Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/panel.md` and capture the full contents (5 selected panelist lenses with one-line rationale per pick — primary, adjacent, productive-tension picks all justified) into context. See `phases/intake_and_panel.md` Step 1.4 for the panel.md content schema.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: panel gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/panel.md` as a normal markdown chat message. Emit the full verbatim contents — do not substitute a path, summary, or placeholder. Structure:

```
## Panel ready for review — expert

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/panel.md>

---
**Approve** → begin 3 rounds of expert critique  ·  **Reject** → cancel task, no rounds will run  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** After the plan message, call AskUserQuestion. The question must not re-embed the panel — it lives in the plan message above.

- question: `The panel above is ready for review.`
- header: `Panel`
- options: **Approve** — begin 3 rounds of expert critique · **Reject** — cancel task, no rounds will run

**Response handling**:

- **Approve** → add `- panel approved: .mz/task/<task_name>/panel.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: 1.5` and `PhaseName: panel_approved`, and proceed to Phase 2 (Round Loop).
- **Reject** → update `state.md` to `aborted_by_user` and stop. Do not run rounds.
- **Any other reply (feedback)** → apply swaps/changes, overwrite `panel.md`, return to Surface 1, re-read `panel.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: panel gate`, stop. A missing answer is never approval.

## Red Flags

- You skipped the panel-approval gate.
- You exited the round loop before 3 rounds completed.
- You serialized the 5 panelists instead of dispatching in one parallel message per round.
- You let a panelist write `round_<N>_summary.md` instead of dispatching `expert-round-synthesizer`.
- You wrote the final report inline instead of dispatching `expert-report-writer`.
- The final report has claims not attributed to a specific panelist + round.

## Verification

At the end of Phase 3, output a visible block:

```
Expert consultation finalized.
Task dir:   .mz/task/<task_name>/
Report:     .mz/reports/<YYYY_MM_DD>_expert_<slug>.md
Panel:      <5 agent names>
Rounds:     3/3
Files:
  - intake.md
  - research.md (if scope: set)
  - panel.md
  - iter_1_<agent>.md × 5, round_1_summary.md
  - iter_2_<agent>.md × 5, round_2_summary.md
  - iter_3_<agent>.md × 5, round_3_summary.md
  - final report at .mz/reports/
```

If any phase is incomplete, print the blocker explicitly. The verification block is mandatory.

## Error Handling

- Empty brief → `AskUserQuestion`; never guess.
- `@doc:` path does not exist → ask the user whether to proceed without it.
- Agent returns malformed output → retry once with clarified prompt; if still malformed, note the gap in state.md and continue (do not block the round on a single agent).
- Researcher fails when `scope:` set → escalate to user; offer to proceed without scan.
- Panel-approval gate rejected → mark state `aborted_by_user`; stop without writing a report.
- Update `state.md` before and after every agent dispatch.

## State Management

After each phase, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`:

- `Status:` `pending` | `running` | `blocked` | `complete` | `aborted_by_user` | `failed`
- `Phase:` `0` | `1` | `1.5` | `2` | `3`
- `Round:` `0..3` (Phase 2 only)
- `FilesWritten:` cumulative list

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Never rely on conversation memory for cross-phase state — context compaction destroys specific paths and decisions. The state file is the source of truth.
