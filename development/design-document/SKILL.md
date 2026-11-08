---
name: design-document
description: 'Writes a UI/UX design document with wireframes and a WCAG contrast report. Use when the user wants an interface designed as a spec ("design a UI for X", "create a design document", "design spec", "UX spec"). Not for building it in code (use build).'
allowed-tools: Agent(design-researcher), Agent(design-document-writer), Agent(ui-designer), Agent(ux-designer), Agent(art-designer), Agent(accessibility-specialist), Agent(design-critique-synthesizer), Agent(design-revision-writer), AskUserQuestion, Read, Write, Grep, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(printf *), Bash(test *), Bash(${CLAUDE_PLUGIN_ROOT}/shared/journal-artifact.sh *), WebSearch
---

# Design Document Pipeline

## Overview

Takes a UI/UX design brief and produces a comprehensive design document with ASCII wireframes, Mermaid diagrams, and a WCAG 2.2 AA contrast report. Refines the draft through four specialist critics in parallel (ui-designer, ux-designer, art-designer, accessibility-specialist) with a WCAG hard gate, for up to 5 iterations, until all critics approve and zero contrast violations remain. If the cap is reached with findings still open, the user can accept them as unresolved and move on to the approval gate.

## When to Use

A UI/UX design document or interface spec for a page, screen or flow of a software product. It produces a spec document, not an implementation.

### When NOT to use

- Implementing the design in code — use `build` (mz-dev-pipe).
- Reviewing an existing design doc — use `audit` or `review-branch`.
- Brainstorming directions without committing to a spec — use `brainstorm` (mz-creative).
- Print, brand, or industrial design — out of scope for this skill.

## Input

`$ARGUMENTS` — The design brief. Supports inline modifiers:

- `scope:branch|global|working` — codebase scope for design-researcher (default: `global`). See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the scope modes and their git commands
- `@image:<path>` — reference image path (acknowledged, not decoded)
- `@doc:<path>` — existing requirement/brief document to ingest

If empty, ask the user for a brief via `AskUserQuestion`. Never guess.

## Constants

- **MAX_DESIGN_ITERATIONS**: 5
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **DESIGN_DIR**: `<PROJECT_ROOT>/.mz/design/`
- **TASK_NAME_FORMAT**: `<YYYY_MM_DD>_design_<slug>`
- **WCAG_AA_NORMAL**: 4.5
- **WCAG_AA_LARGE**: 3.0
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase             | File                            | Loop?                           |
| --- | ----------------- | ------------------------------- | ------------------------------- |
| 0   | Setup             | inline below                    | —                               |
| 1   | Intake & Research | `phases/intake_and_research.md` | —                               |
| 2   | Initial Draft     | `phases/initial_draft.md`       | —                               |
| 3   | Critique Loop     | `phases/critique_loop.md`       | max `MAX_DESIGN_ITERATIONS` (5) |
| 4   | Finalization      | `phases/finalization.md`        | user-approval sub-loop          |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. Extract brief, `scope:`, `@image:` refs, `@doc:` refs.
1. If brief is empty → `AskUserQuestion` asking for the brief. Do not guess.
1. Derive task name as `<YYYY_MM_DD>_design_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary of the brief (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/` for `state.md` and `<PROJECT_ROOT>/.mz/design/<task_name>/` for the design artifacts.
1. Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with `schema_version: 2` as the first line, then `Status: running`, `Phase: 0`, `Started: <ISO>`, `phase_complete: false`, `what_remains: []`, `Iteration: 0`, `FilesWritten: []`.
1. Output a visible setup block showing: `task_name`, `DESIGN_DIR` path, detected modifiers.

### Phase 4: User Approval Gate

Read `<SKILL_DIR>/phases/finalization.md` and follow Steps 4.1-4.5. **This orchestrator** (not a subagent) presents the gate; it must not be delegated.

This skill has no unattended mode, so an unattended run stops `blocked` at the gate.

## Common Rationalizations

| Rationalization                                      | Rebuttal                                                                                                                                                                    |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "The first draft is fine, skip the critique loop"    | "Four parallel critics catch issues in one round that would surface as rework during implementation. The loop costs 5 agents per round and prevents 10+ downstream cycles." |
| "WCAG AA is overkill for internal tools"             | "Internal users include colleagues with visual impairments. AA is the legal floor, not a stretch goal. The hard gate is non-negotiable."                                    |
| "Mermaid diagrams and ASCII wireframes are busywork" | "Flow diagrams surface IA gaps invisible in prose. Wireframes make layout decisions concrete — without them, ui-designer has nothing to critique."                          |
| "I'll approve iteration 1 to save time"              | "The 5-iteration cap is a ceiling, not a target. Most drafts pass in 1–2 rounds. Approving an unreviewed draft defeats the purpose of the specialist critics."              |

## Red Flags

- You dispatched the writer before the researcher returned `STATUS: DONE`.
- You accepted `AGGREGATE: FAIL` and advanced without running the revision writer.
- You advanced past `MAX_DESIGN_ITERATIONS` without escalating to the user.
- You trusted the writer's self-reported WCAG numbers instead of the accessibility-specialist's re-validation.
- You presented the final doc without the Phase 4 user approval gate.
- You serialized the four critics instead of dispatching them in parallel (single message, four Agent calls).

## Verification

At the end of Phase 4, output:

```
Design document finalized.
Task dir:   <PROJECT_ROOT>/.mz/design/<task_name>/
Iterations: <N>/5
Aggregate:  <PASS | ACCEPTED_WITH_UNRESOLVED>
WCAG gate:  <PASS | FAIL>
Files:
  - design.md (<lines>)
  - wireframes.md (<lines>)
  - wcag-report.md (<lines> — <pair count> pairs)
  - final-summary.md
```

If any phase is incomplete, print the blocker explicitly. The verification block is mandatory — do not skip it.

## References

- `${CLAUDE_SKILL_DIR}/references/design-spec-template.md`: the 14-section skeleton every design document follows. Grep it for the section being drafted in Phase 2 or revised in Phase 3.
- `${CLAUDE_SKILL_DIR}/references/nielsen-heuristics.md`: Nielsen's 10 usability heuristics with probing questions. Grep it for the heuristic being applied, in the Phase 2 self-check and the Phase 3 UX critique.
- `${CLAUDE_SKILL_DIR}/references/wcag-contrast-thresholds.md`: WCAG 2.2 contrast thresholds, the luminance and ratio formulas, and the `wcag-report.md` table format. Grep it for the value needed when computing the Phase 2 report and re-validating it in Phase 3.

## Error Handling

- An agent returns nothing usable → `<PLUGIN_ROOT>/shared/retry-policy.md`.
- Brief is empty → ask the user; never guess.
- `@image:` path does not exist → note in `intake.md`, continue with placeholder.
- `@doc:` path does not exist → ask the user whether to proceed without it.
- WCAG hard gate fails at iteration 5 → escalate with options (accept as-is, provide guidance for one more round, abort).
- Critic emits malformed output → treat as FAIL, proceed to revision.
- Always update `state.md` before and after spawning agents.

## State Management

After each phase, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with:

- `Status:` `pending` | `running` | `blocked` | `complete` | `aborted_by_user` | `failed`
- `Phase:` `0` | `1` | `2` | `3` | `critique_passed` | `critique_accepted` | `4`
- `PhaseName:` short label (`setup`, `intake_and_research_complete`, etc.)
- `Iteration:` `0..MAX_DESIGN_ITERATIONS`
- `LastVerdict:` (Phase 3 only) the 6-line verdict block from `critique_<N>.md`
- `unresolved:` `<count>` of findings the user accepted at the iteration cap; absent or `0` when Phase 3 passed
- `FilesWritten:` cumulative list of paths

Never rely on conversation memory for cross-phase state — context compaction destroys specific paths and decisions. The state file is the source of truth.

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
