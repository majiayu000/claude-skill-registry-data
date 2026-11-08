---
name: build
description: 'Builds a new feature, module or component test-first, with code review. Use when the user wants something new built or implemented ("build X", "implement Y", "add feature"). Not for bug fixes (use debug) or bringing code up to criteria (use polish).'
argument-hint: <task description>
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(git status *), Bash(mkdir *), Bash(date *), Bash(printenv MZ_DEV_PIPE_AUTO_APPROVE *), Bash(mv *), Bash(printf *), Bash(${CLAUDE_PLUGIN_ROOT}/shared/journal-artifact.sh *), Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch, WebSearch
---

# Autonomous Development Pipeline (TDD)

## Overview

Orchestrates a full test-driven development lifecycle — research, plan, write failing tests (RED), implement to pass them (GREEN), review, refactor, and verify — using specialized sub-agents. Takes a task description and produces reviewed, tested, green code with explicit user approval at the plan gate.

The pipeline enforces red-green-refactor: tests are written and verified failing **before** any implementation code is allowed. Coders make tests pass without modifying them; refactor happens only after the green bar is restored.

## When to Use

Creating a new feature, module or component that spans multiple files and benefits from a plan, review and test loop.

### When NOT to use

- Fixing a known bug — use `debug`.
- Making existing code meet quality criteria — use `polish`.
- Read-only analysis or impact mapping — use `audit` (or `audit depth:deep` for blast-radius-driven impact analysis).
- One-line edits or trivial tweaks — just edit directly.

## Input

- `$ARGUMENTS` — The task description. If empty, ask the user what they want built.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands. Document any skill-specific overrides or restrictions below this line.

- **Default**: `global`.
- Scope constrains **edits only**; researchers and verification commands may read the full project.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **MAX_REVIEW_ITERATIONS**: 3 | **MAX_RED_ITERATIONS**: 2 | **MAX_GREEN_ITERATIONS**: 3 | **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase                                  | Reference                             | Loop?               |
| --- | -------------------------------------- | ------------------------------------- | ------------------- |
| 0   | Setup                                  | inline below                          | —                   |
| 1   | Research                               | `phases/research_and_planning.md`     | —                   |
| 2   | Planning + User Approval               | `phases/research_and_planning.md`     | plan review (max 3) |
| 3   | Test Writing (RED)                     | `phases/testing.md`                   | —                   |
| 4   | Test Review (2 parallel reviewers)     | `phases/testing.md`                   | max 3               |
| 5   | Verify RED                             | `phases/testing.md`                   | max 2               |
| 6   | Implementation (GREEN, parallel waves) | `phases/implementation_and_review.md` | —                   |
| 7   | Code Review                            | `phases/implementation_and_review.md` | max 3               |
| 8   | Lint, Format, and Verify GREEN         | `phases/implementation_and_review.md` | —                   |
| 9   | Final Code Review                      | `phases/finalization.md`              | max 2               |
| 10  | Refactor (Optimization)                | `phases/finalization.md`              | max 2               |
| 11  | Completeness Check                     | `phases/finalization.md`              | restart-from-phase  |

### Phase 0: Setup

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

Derive task name as `<YYYY_MM_DD>_build_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary (max 20 chars) of the description; on same-day collision append `_v2`, `_v3`.

**Resume check** (before creating the task directory): follow `<PLUGIN_ROOT>/shared/resume-protocol.md`, "On entry". A `complete`, `completed` or `aborted_by_user` file starts a `_vN`. A `pending`, `running`, `blocked` or `failed` file gets the resume gate. When the run is unattended or nobody can answer, report the path, `Status` and `what_remains`, and stop.

**Fresh-task setup**: run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"`. Write `state.md` per the v2 schema in `<PLUGIN_ROOT>/shared/state-schema.md` — first line must be `schema_version: 2`, followed by `Status`, `Phase`, `PhaseName`, `Started`, `Iteration`, `FilesWritten`, and the progress-ledger keys `phase_complete: false` and `what_remains: []` (`last_verified` is omitted until the first gate passes). Use TaskCreate for per-phase tracking. Run `printenv MZ_DEV_PIPE_AUTO_APPROVE` once and record `unattended: true` or `unattended: false` in `state.md`.

Then dispatch `pipeline-tooling-detector` to detect the project's test command, lint command, and formatter. Pass `project_root: <PROJECT_ROOT>` and `output_path: <PROJECT_ROOT>/.mz/task/<task_name>/tooling.md`. If it returns `DONE_WITH_CONCERNS` with the test or lint command set to "none detected", note `tooling: not_detected` in `state.md` and proceed. If it returns `BLOCKED` (it couldn't write `tooling.md`), record the reason in `state.md` and proceed the same way. Tooling gaps are non-fatal at setup time.

### Phase 1: Research

Gather codebase context, assess feasibility, compare 2-3 approaches in parallel. See `phases/research_and_planning.md` → Phase 1. Set `Phase: research_complete`.

### Phase 2: Planning

Generate detailed plan, run plan-review loop, get user approval. See `phases/research_and_planning.md` → Phase 2.

#### 2.3 User approval gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

See `<PLUGIN_ROOT>/shared/approval-gate.md` for the canonical two-surface pattern, the `MZ_DEV_PIPE_AUTO_APPROVE` unattended-mode bypass, and the cost-preview format used below.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/plan.md` with the Read tool. Capture the full plan body (work units, test strategy, risks, verification criteria) into context. The plan must already have passed automated review before this gate fires.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: plan gate]`; `Status` stays `running`.

**Compute the cost preview** before emitting the Surface 1 message:

- Count `N` from the plan: `N = 1 (test-writer) + 2 (test-reviewers) + W (parallel coder waves from plan.md work units) + 1 (code-reviewer) + 1 (final-reviewer) + 1 (optimizer) + 1 (completeness-checker)` where `W` is the number of work units in `plan.md`.
- Default per-agent budget: ~20k tokens (mixed Sonnet + Opus). For a typical 5-work-unit plan, `N ≈ 12`, total ≈ 240k tokens.
- Use the formula in `<PLUGIN_ROOT>/shared/approval-gate.md` to convert to a dollar estimate at the active price.

**Surface 1 — emit the plan message.** Output the plan verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/plan.md` — do not substitute a path, summary, or placeholder. Structure:

```
## Plan ready for review — build

<verbatim contents of plan.md>

---
**Approve** → proceed to Phase 3 (Test Writing — TDD/RED)  ·  **Reject** → task marked aborted, no files written  ·  reply with feedback to revise

Approve cost (estimated): <N> agents × ~20k tokens ≈ ~$<Y.YY> on mixed Sonnet+Opus
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the plan in the question body:

- question: `The plan above is ready for review. Approve to proceed, or Reject to abort — reply with feedback to revise.`
- header: `Plan`
- options: **Approve** — proceed to Phase 3 (Test Writing — TDD/RED) · **Reject** — abort, no files written

**Response handling**:

- **Approve** → add `- plan approved: .mz/task/<task_name>/plan.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: plan_approved`, and proceed to Phase 3.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → spawn `pipeline-planner` with feedback, overwrite `plan.md`. Do not re-run plan review — user's word is final. Return to Surface 1, re-read `<PROJECT_ROOT>/.mz/task/<task_name>/plan.md`, and re-emit the entire plan message from scratch — never diff-only, never summary-only. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 3 without explicit approval.
- **Unattended** (`unattended: true` in `state.md`) → `<PLUGIN_ROOT>/shared/approval-gate.md`, "Unattended mode": emit Surface 1, skip Surface 2, continue as on Approve, and log the gate in chat, under `## Auto-approvals`, in the journal and in the final report.
- **No answer** → set `Status: blocked`, keep `awaiting approval: plan gate`, stop. A missing answer is never approval.

### Phase 3: Test Writing (RED)

Create tests **before any implementation** with `pipeline-test-writer` (model: opus). Tests assert the correct behavior the plan requires; since no production code exists yet, they will fail. See `phases/testing.md` → Phase 3.

### Phase 4: Test Review

Spawn TWO review agents in parallel (model: sonnet, since this pass reads only test code and Phase 7 reviews production code on opus): the unified `pipeline-test-reviewer` (covers gaps + quality in one pass) and `pipeline-code-reviewer` (test-code craftsmanship). The reviewers verify the tests cover every work unit from the plan and that they would catch real regressions. See `phases/testing.md` → Phase 4. Set `Phase: test_review_passed`.

### Phase 5: Verify RED

Run the new tests and confirm they FAIL (or error with `not implemented` / missing-symbol errors). A test that passes against zero implementation is broken — it would not catch a regression. Re-dispatch `pipeline-test-writer` with the unexpectedly-passing test names if any pass. See `phases/testing.md` → Phase 5. Set `Phase: red_verified`.

### Phase 6: Implementation (GREEN)

Parse work units into execution waves and dispatch parallel `pipeline-coder` agents (model: opus). Each coder is told the relevant failing tests and instructed to make them pass **without modifying any test file**. After each wave, update state with `current_wave: N`, per-coder STATUS, and cumulative files modified — required for safe resumption if context compacts. See `phases/implementation_and_review.md` → Phase 6. Set `Phase: implementation_complete`.

### Phase 7: Code Review

Review with `pipeline-code-reviewer` (model: opus), iterate fixes up to 3 times. See `phases/implementation_and_review.md` → Phase 7. Set `Phase: code_review_passed`.

### Phase 8: Lint, Format, and Verify GREEN

Detect tooling, run linters/formatters, then run the **full test suite** including the Phase 3 tests. All target tests must now pass; no pre-existing tests may regress. See `phases/implementation_and_review.md` → Phase 8. Set `Phase: tests_passing`.

### Phase 9: Final Code Review

Last validation pass over all code with `pipeline-code-reviewer`. See `phases/finalization.md` → Phase 9. Set `Phase: final_review_passed`.

### Phase 10: Refactor (Optimization)

Clean up dead code, debug artifacts, unused imports — the refactor leg of red-green-refactor. Tests must remain green; no behavior change. Re-verify then review. See `phases/finalization.md` → Phase 10. Set `Phase: optimized`.

### Phase 11: Completeness Check

Final gate: `pipeline-completeness-checker` (model: opus) decides if the task is done. See `phases/finalization.md` → Phase 11. Max 2 iterations.

## Common Rationalizations

| Rationalization                                 | Rebuttal                                                                                                    |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| "plan is fine without review"                   | "plan review catches integration gaps that become 3 review cycles downstream"                               |
| "tests can wait until after first ship"         | "missing tests on Day 1 become 'why is this flaky?' in Week 2"                                              |
| "one big commit is easier"                      | "atomic commits are the only way to bisect a regression cheaply"                                            |
| "I'll write code first, tests are easier after" | "tests written after the code mirror the implementation; tests written first describe the behavior"         |
| "skip the RED check, of course they fail"       | "tests that pass against missing code are silently broken — Phase 5 catches mock-only or import-only tests" |

## Red Flags

- You dispatched coders without user approval of the plan.
- Plan review was skipped or truncated to save time.
- A coder agent was dispatched before tests were written and verified RED.
- A coder modified or deleted a test to make it pass.
- Phase 5 was skipped on the assumption that tests "must" fail without implementation.

## Verification

Output the final state block: task dir path, all phases marked complete, review iteration counts, file list, and tests-passing status. If any phase is incomplete, print the blocker explicitly.

## Error Handling

An agent returns nothing usable → `<PLUGIN_ROOT>/shared/retry-policy.md`: re-dispatch once with a clarified prompt, and don't retry API errors or usage limits. No test framework → ask how to proceed. No linter → note in summary, don't block. Always save state before spawning agents.

## State Management

After each phase, update `state.md` with current phase, iteration counts, files modified, and escalation notes. Allows resumption if interrupted.

Maintain the progress ledger on every phase transition: set `phase_complete: false` on entering a phase and `true` only once its artifacts are written and its gates pass; refresh `what_remains` (outstanding work as plain strings) — it must be `[]` when `Status: complete`. Stamp `last_verified` whenever a lint/test/review gate passes clean. Reading a `schema_version: 1` or unversioned `state.md` upgrades it in place: add the ledger keys, set `schema_version: 2`, and log the upgrade. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`.
