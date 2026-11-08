---
name: polish
description: 'Removes dead code, unused imports, nesting and AI comments, behavior unchanged, or gets code past tests and CI gates. Use when the user says "clean up", "strip AI comments" or "fix failing tests". Not for one bug (use debug) or speed (use optimize).'
argument-hint: '[scope:branch|global|working] <completion criteria — what must pass, what to clean up, what must work>'
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(git log *), Bash(mkdir *), Bash(date *), Bash(printf *), Bash(printenv MZ_DEV_PIPE_AUTO_APPROVE *), Bash(${CLAUDE_PLUGIN_ROOT}/shared/journal-artifact.sh *), Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch, WebSearch
---

# Code Polishing Pipeline

## Overview

Orchestrates iterative polish of existing code against specific completion criteria. Unlike `build` which builds from scratch, polish works with what's already there — running tests, diagnosing failures, fixing issues with review loops, and optimizing.

When a behavioral criterion is not yet covered by any test, polish writes the test first (TDD-style), verifies it fails against the current code, then fixes. This keeps every fix anchored to a regression-catching assertion.

Two criterion kinds need no failing check. A **cleanup** criterion ("clean up src/billing/, behavior unchanged") asks for dead code, unused imports, duplication and needless complexity to go from a scope. A **residue** criterion ("no AI leftovers in this branch") asks for AI signatures, pipeline markers and comments that restate the code to go. Phase 5 meets both by running `pipeline-optimizer` over the scope, split into parallel chunks when the scope is large, with a green test run and a review for each chunk.

## When to Use

Existing code that must meet specific criteria, such as failing tests, lint or other quality gates, an unfinished implementation, a behavior-preserving cleanup of a module, or a sweep for AI leftovers.

### When NOT to use

- Starting a new feature from scratch — use `build`.
- A single isolated bug with a reproducer — use `debug`.
- If the root cause of failures is known (e.g., a specific bug was identified) — use `debug` to fix the root cause first, then return to `polish` for quality criteria.
- Making code faster, smaller or cheaper — use `optimize`; cleanup here makes code tidier and measures nothing.
- Prose or markdown that reads as AI-written — use `naturalize` (mz-creative).
- Running the checks only, with no fixing — run the project's test and lint commands directly.

## Input

- `$ARGUMENTS` — The completion criteria. This can be:
  - "All tests in test_foo.py must pass"
  - "Pre-commit hooks must pass on all changed files"
  - "The WebSocket reconnection must handle timeout correctly"
  - "Fix all failing tests and clean up the implementation"
  - "Clean up src/billing/ — dead code, unused imports, nesting; behavior unchanged" (a cleanup criterion)
  - "No AI leftovers in this branch" (a residue criterion)
  - Any combination of pass/fail criteria and behavioral requirements

If empty, ask the user what needs to be polished.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands. Document any skill-specific overrides or restrictions below this line.

- **Default** (no `scope:`): all project files eligible for edits.
- `scope:` controls **which files agents may edit**. Tests and linters always run on the full project. Criteria determine **what to verify**; scope determines **where fixes may be applied**.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **MAX_FIX_ITERATIONS**: 5 — max code-test-review cycles before escalating
- **MAX_REVIEW_RETRIES**: 3 — max times a review can fail before escalating
- **CHUNK_THRESHOLD**: 12 — a cleanup or residue scope larger than this is split into chunks
- **MAX_OPTIMIZERS**: 6 — chunk cap, one `pipeline-optimizer` per chunk in one wave
- **MAX_CHUNK_RETRIES**: 3 — re-runs of a rejected chunk before escalating
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| Phase | Goal                   | Details                             |
| ----- | ---------------------- | ----------------------------------- |
| 0     | Setup                  | Inline below                        |
| 1     | Initial Assessment     | `phases/assess_and_fix.md`          |
| 1.5   | User Approval Gate     | Inline below                        |
| 2     | Quick Fixes            | `phases/assess_and_fix.md`          |
| 3     | Research (if needed)   | `phases/assess_and_fix.md`          |
| 4     | Fix-Test-Review Loop   | `phases/fix_review_and_finalize.md` |
| 5     | Optimization & cleanup | `phases/fix_review_and_finalize.md` |
| 6     | Final Verification     | `phases/fix_review_and_finalize.md` |

Read the relevant phase file when you reach that phase. Do not read both phase files upfront.

### Phase 0: Setup

1. **Project root** — resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. **Resolve scope** — if `scope:` extracted, resolve to a concrete file list; the task-dir step saves it. Otherwise all project files eligible.
1. **Parse criteria** — break input into a checklist of discrete, verifiable criteria (e.g. "all tests pass", "pre-commit clean", "no debug prints in src/"). Mark each one `check` (verified by a command), `cleanup` or `residue`; the last two carry a scope (glob, directory, git range or description) that Phase 1 resolves.
1. **Task name** — `<YYYY_MM_DD>_polish_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is snake_case of criteria (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. **Task dir & state** — **Resume check** (before creating the task directory): follow `<PLUGIN_ROOT>/shared/resume-protocol.md`, "On entry". A `complete`, `completed` or `aborted_by_user` file starts a `_vN`. A `pending`, `running`, `blocked` or `failed` file gets the resume gate. When the run is unattended or nobody can answer, report the path, `Status` and `what_remains`, and stop. For a fresh task, run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"` and write `state.md` per `<PLUGIN_ROOT>/shared/state-schema.md` — first line must be `schema_version: 2`, followed by required keys (`Status`, `Phase`, `Started`, `Iteration` (0), `FilesWritten`, `phase_complete: false`, `what_remains: []`) plus the parsed criteria checklist as a skill-specific key. Run `printenv MZ_DEV_PIPE_AUTO_APPROVE` once and record `unattended: true` or `unattended: false` in `state.md`. Save the resolved scope list, if any, to `<PROJECT_ROOT>/.mz/task/<task_name>/scope_files.txt`.
1. **Task tracking** — TaskCreate per pipeline phase. Then read `phases/assess_and_fix.md` and proceed to Phase 1.

### Phase 1.5: User Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

See `<PLUGIN_ROOT>/shared/approval-gate.md` for the canonical two-surface pattern, the `MZ_DEV_PIPE_AUTO_APPROVE` unattended-mode bypass, and the cost-preview format used below.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/assessment.md` with the Read tool and capture its full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: assessment gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the assessment verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/assessment.md` — do not substitute a path, status summary, line count, or `<failing criteria list>` / `<proposed quick-fix plan>` / `<estimated file count>` placeholders. Structure:

```
## Assessment ready for review — polish

<verbatim contents of assessment.md>

---
**Approve** → proceed to Phase 2 (Quick Fixes)  ·  **Reject** → mark task aborted, stop here  ·  reply with feedback to revise

Approve cost (estimated): <N> agents × ~20k tokens ≈ ~$<Y.YY> on mixed Sonnet+Opus
```

Compute `<N>` from `assessment.md` quick-fix count plus the maximum review-loop budget (`MAX_FIX_ITERATIONS × (1 fix + 1 test + 1 review)`), plus two agents per chunk (optimizer and reviewer) when there are cleanup or residue criteria. Use the `<PLUGIN_ROOT>/shared/approval-gate.md` formula to convert to a dollar estimate.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the assessment in the question body, it lives in the plan message above:

- question: `The assessment above is ready for review.`
- header: `Assessment`
- options: **Approve** — proceed to Phase 2 (Quick Fixes) · **Reject** — mark task aborted, stop here

**Response handling**:

- **Approve** → add `- assessment approved: .mz/task/<task_name>/assessment.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: assessment_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → incorporate, re-run Phase 1 if needed, overwrite `assessment.md`, return to this gate, re-read `assessment.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. Then re-present the selector. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **Unattended** (`unattended: true` in `state.md`) → `<PLUGIN_ROOT>/shared/approval-gate.md`, "Unattended mode": emit Surface 1, skip Surface 2, continue as on Approve, and log the gate in chat, under `## Auto-approvals`, in the journal and in the final report.
- **No answer** → set `Status: blocked`, keep `awaiting approval: assessment gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                      | Rebuttal                                                 |
| ------------------------------------ | -------------------------------------------------------- |
| "good enough, ship"                  | "polish is the last line of defense before users see it" |
| "edge cases are rare"                | "every bug report you've ever gotten is an edge case"    |
| "tests are green, refactor can wait" | "green-test refactor debt compounds"                     |
| "dead code is harmless, leave it"    | "dead code hides the live code and decays the context"   |

## Red Flags

- Edge cases were deferred to "next sprint" instead of handled now.
- Code was declared "good enough" without a final criteria sweep.
- Polish was equated with refactor — criteria drifted mid-loop.

## Verification

Output the final criteria checklist with every item checked, along with the test run status, lint status, and iteration count. Any unchecked item blocks completion.

## References

- `${CLAUDE_SKILL_DIR}/references/dead-code-detection-patterns.md`: per-language commands and false-positive notes for unused imports, unreachable branches, dead exports, orphan files and duplicated logic. Grep it for the pattern you need on a cleanup criterion; do not read it whole.

## Error Handling

- If a test framework isn't detected, ask the user how to run tests.
- If a criterion can't be verified programmatically, ask the user for a verification command.
- If research fails to identify root cause after 2 attempts, ask the user for context.
- Always save state before spawning agents.
- If a fix makes things worse (more criteria fail than before), revert the change immediately and try a different approach.

## State Management

After each phase/iteration, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with:

- Current phase and iteration count
- Criteria checklist (checked/unchecked)
- Files modified so far
- Any escalation notes

Track cumulative file changes across iterations so the optimizer knows the full scope.

For cleanup and residue criteria, also record the resolved file list (`cleanup_files.txt`), the chunk table, and `chunk_retries` per chunk.

Maintain the progress ledger on every phase transition: set `phase_complete: false` on entering a phase and `true` only once its artifacts are written and its gates pass; refresh `what_remains` (outstanding work as plain strings) — it must be `[]` when `Status: complete`. Stamp `last_verified` whenever a verification gate passes clean. Reading a `schema_version: 1` or unversioned `state.md` upgrades it in place: add the ledger keys, set `schema_version: 2`, and log the upgrade. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`.
