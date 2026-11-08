---
name: combine
description: 'Consolidates existing local research, task artifacts and prior reports into one unified report. Use when the user says "combine our findings" or "pull together everything we found so far". Not for new research from scratch (use deep-research).'
argument-hint: '[output:<path>] [sources:<glob>] [scope:branch|global|working] [sections:<csv>] <task — what to synthesize>'
allowed-tools: Agent, Bash(git rev-parse *), Bash(git log *), Bash(git status *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(mkdir *), Bash(date *), Read, Write, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch, WebSearch
---

# Local Source Combination Pipeline

## Overview

You orchestrate a local-first synthesis that harvests prior pipeline output — `.mz/research/`, `.mz/task/*/`, `.mz/reports/`, `.mz/reviews/`, codebase files, and git history — and folds it into a unified report with task-adaptive sections (or user-supplied sections). Counterpart to `/deep-research`: that skill is web-first and starts from zero; this one assumes prior output exists and only consults the web to fill residual gaps, in one bounded wave.

## When to Use

Synthesizing knowledge that already lives on disk (prior research, task artifacts, reports, reviews, codebase files, git history) into one unified report.

### When NOT to use

- Zero prior local research exists — use `/deep-research` instead.
- The user wants to understand how code works — use `/explain` instead.
- The user wants to verify a hypothesis or run exploratory tests — use `/debug certainty:low`. If the user then wants to synthesize prior investigation output, `/combine` is the right follow-up.
- The user needs a fixed-template compliance report — use a dedicated audit skill.

## Input

- `$ARGUMENTS` — the task text plus any optional parameters: `output:<path>`, `sources:<glob>`, `scope:branch|global|working`, `sections:<csv>`. Remainder after parameter extraction is the task description.
- Example: `/combine sections:Context,Findings,Risks synthesize our findings on the auth refactor`.
- If empty or ambiguous, ask via AskUserQuestion. Never guess.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands. Document any skill-specific overrides or restrictions below this line.

- The `scope:` parameter narrows **only the codebase lens file-list**, not the `.mz/` source harvest — prior research, reports, and task artifacts are always eligible regardless of scope.
- **Default** (no `scope:`): codebase lens derived from task-text file-name hints by searching for and listing matching files.

## Output Parameter

Extract `output:<path>` from `$ARGUMENTS` if present — overrides the default report path.

**Default**: `<PROJECT_ROOT>/.mz/reports/<YYYY_MM_DD>_combine_<slug>.md`. On collision append `_v2`, `_v3`.

## Sections Parameter

Extract `sections:<comma-separated list>` from `$ARGUMENTS` if present. If provided, the report's top-level sections are taken **verbatim from the list, in the order given**. If absent, sections are derived from the task text — see `phases/synthesis.md §Phase 5`. Meta-sections (Timeline, Conflicts, Gaps, Sources, Methodology) are always appended regardless of branch.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.

Bounds: `MAX_LENSES = 6`, `MAX_GAP_FILL_WAVES = 1`, `MIN_TASK_QUERY_TOKENS = 5`.
Paths/freshness: `TASK_DIR = <PROJECT_ROOT>/.mz/task/`, `REPORT_DIR = <PROJECT_ROOT>/.mz/reports/`, `RESEARCH_DIR = <PROJECT_ROOT>/.mz/research/`, `TASK_ARTIFACT_STALE_DAYS = 30`, `REPORT_STALE_DAYS = 60`, `RESEARCH_STALE_DAYS = 90`.

Plugin root: `PLUGIN_ROOT = ${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase                                   | Reference                                                      | Loop? |
| --- | --------------------------------------- | -------------------------------------------------------------- | ----- |
| 0   | Setup                                   | inline below                                                   | —     |
| 1   | Source Inventory and Lens Decomposition | `phases/inventory.md`                                          | —     |
| 1.5 | Decomposition Approval Gate             | inline stub + body in `phases/inventory.md §Phase 1.5 Gate`    | yes   |
| 2   | Parallel Lens Dispatch                  | `phases/lens_dispatch.md`                                      | —     |
| 3   | Cross-Reference Synthesis               | `phases/synthesis.md`                                          | —     |
| 4   | Web Gap-Fill (conditional)              | `phases/lens_dispatch.md §Phase 4: Web Gap-Fill (conditional)` | —     |
| 5   | Task-Adaptive Report Generation         | `phases/synthesis.md`                                          | —     |

## Red Flags

- Inline `.mz/` reads from the orchestrator — only filenames and mtimes are allowed inline; file bodies belong in lens agents.
- More than `MAX_LENSES` lenses dispatched in a single wave.
- Fixed-template report produced when `sections:` was not explicitly supplied by the user.

## Verification

Before completing, output a visible block showing: task slug, lenses dispatched, gap-fill y/n, residual gaps count, absolute report path. Confirm the report file exists on disk.

## Phase 0: Setup

- **0.1 Resolve PROJECT_ROOT** — run the command in Constants, before any `cd` or worktree switch, and use its output for every `.mz/` path below.
- **0.2 Parse arguments** — extract `output:`, `sources:`, `scope:`, and `sections:` from `$ARGUMENTS` (case-insensitive); remove each matched parameter from the argument text — the remainder is the task description.
- **0.3 Vague-task check** — count whitespace-separated tokens in the task text; if fewer than `MIN_TASK_QUERY_TOKENS`, or the task contains a banned token (`everything`, `whatever`), fire AskUserQuestion with a focusing prompt before proceeding. Never guess intent.
- **0.4 Derive task name** — format `<YYYY_MM_DD>_combine_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary of the task text (max 20 chars); on same-day collision append `_v2`, `_v3`.
- **0.5 Create task directory and state** — `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>/"` and write `state.md` with fields, in order: `schema_version: 2` (first line), Status, Phase, Started, `phase_complete: false`, `what_remains: []`, Task, Output, Lenses, Sections (source: `task-derived` | `user-supplied`).
- **0.6 Create task tracking** — use TaskCreate for each pipeline phase.
- **0.7 Transition** — read `phases/inventory.md` and proceed to Phase 1.

## Phase 1.5: Decomposition Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/inventory.md` with the Read tool. Capture the full file contents (source inventory summary with bucket counts, stale-excluded count, unavailable buckets, and the proposed lens decomposition listing 3–6 lenses with names and file counts) into context. See `phases/inventory.md §Phase 1.5 Gate` for the inventory.md content schema.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: decomposition gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/inventory.md` — do not substitute a path, summary, or placeholder:

```
## Inventory ready for review — combine

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/inventory.md>

---
**Approve** → proceed to Phase 2 (parallel lens dispatch)  ·  **Reject** → abort synthesis, task marked aborted  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the inventory in the question body:

- question: `The inventory and decomposition above is ready for review.`
- header: `Inventory`
- options: **Approve** — proceed to Phase 2 (parallel lens dispatch) · **Reject** — abort synthesis, task marked aborted

**Response handling**:

- **Approve** → add `- decomposition approved: .mz/task/<task_name>/inventory.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: decomposition_approved`, and proceed to Phase 2 (`phases/lens_dispatch.md`).
- **Reject** → update `state.md` to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → incorporate, re-run Phase 1.2/1.3 as needed, overwrite `inventory.md`, return to this gate, re-read `inventory.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. This is a loop — repeat until the user explicitly approves. Never proceed without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: decomposition gate`, stop. A missing answer is never approval.

## Error Handling

Vague task → ask before Phase 1. Empty `.mz/` → offer codebase-only mode or abort; never silently degrade to `/deep-research`. Lens `BLOCKED` → escalate with no auto-retry. Lens `NEEDS_CONTEXT` → single re-dispatch, then escalate. `MAX_GAP_FILL_WAVES` exhausted → report unresolved gaps. Report collision → append `_v2`, `_v3`.

## State Management

After each phase, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with: current Phase, lenses dispatched / returned, residual gap count, gap-fill status, output path, and `sections_source` (`task-derived` | `user-supplied`).

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
