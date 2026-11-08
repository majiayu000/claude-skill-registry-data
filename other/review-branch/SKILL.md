---
name: review-branch
description: 'Reviews every change on the current git branch against its base and writes a findings report. Use when the user says "review my branch", "what did I change" or "check this before I push". Not for a pushed GitHub PR (use github-review-pr).'
argument-hint: '[base-branch (default: main)]'
allowed-tools: Agent, Bash(git rev-parse *), Bash(git branch --show-current *), Bash(mkdir *), Bash(date *), Read, Write, Glob, Grep, AskUserQuestion
---

# Review Current Branch

## Overview

Launch the `branch-reviewer` agent to perform a comprehensive review of all changes on the current git branch against a base branch (default `main`). Produces a report under `.mz/reviews/`.

The agent runs a two-wave analysis: Wave A is a 6-lens parallel fan-out (bugs, security, architecture, performance, maintainability, over-engineering) with full repo context; Wave B is a 3-researcher blinded adversarial pass (production reliability, security adversary, ops/SRE) dispatched as its own wave of typed `pipeline-researcher` agents with only the raw diff. Wave B is always-on — there is no opt-out — and surfaces "Blind Spots" that Wave A missed because of confirmation bias. Wave B's blinded prompts are shared with `audit depth:deep` via `<PLUGIN_ROOT>/shared/blinded_lenses.md` (single source of truth, no duplication).

## When to Use

Reviewing every change on the current git branch against a base branch and writing a findings report.

### When NOT to use

- You want to review a GitHub PR — use `github-review-pr` instead.
- The current branch is `main` or `master` — nothing to diff.
- The user wants a scoped review of a single file — read and review it directly.

## Arguments

- `$ARGUMENTS[0]` (optional) — Base branch to diff against. Defaults to `main`.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. `task_name` = `<YYYY_MM_DD>_review_branch_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is the current branch name (snake_case, max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/`.
1. Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `BaseBranch: <base>`, `Branch: <current>`.
1. Emit a visible setup block: `task_name`, base branch, current branch, report dir.

### 1. Validate branch state

Verify the current branch is not `main` or `master`:

```bash
git branch --show-current
```

If on main/master, inform the user there is nothing to review and set `state.md` to `Status: complete` with `Phase: nothing_to_review`.

### 2. Launch the branch-reviewer agent

Dispatch `Agent(branch-reviewer)` with the following prompt and wait for its report:

```
Review the current branch against <base-branch>.
code_root: <output of `git rev-parse --show-toplevel`>
artifact_root: <PROJECT_ROOT>
base_branch: <base-branch>
task_name: <task_name>
Analyze all changes file-by-file for bugs, architecture issues, codebase consistency, missing functionality, and test coverage.
Run the always-on blind audit (Wave B) per Phase 3.6: dispatch the 3 blinded adversarial researchers as their own wave after Phase 3.5 returns, reading the prompts from <PLUGIN_ROOT>/shared/blinded_lenses.md, and cross-reference per Phase 3.7. The Blind Spots section is mandatory whenever wave_b_completed >= 1.
Use researcher agents for domain research if the implementation topic is complex.
Save the report to <PROJECT_ROOT>/.mz/reviews/ using the naming convention: <YYYY_MM_DD>_review_branch_<branch_name><_vN>.md (append _v2, _v3 etc. if a report with the same base name already exists).
```

Update `state.md` to `Phase: 2` before dispatch. When the agent returns, check that the report file exists on disk and isn't empty, then set `Phase: 3` and `Status: complete`.

### 3. Report to user

Once the agent completes:

- Show the path to the generated report file
- Print a brief summary of the verdict and key findings (critical bugs, missing tests, etc.)
- If the agent found critical issues, highlight them explicitly

## Red Flags

- You reviewed diff output without checking out or reading the branch's actual file contents.
- You skipped running (or at least reading) the tests that the branch changed.
- The report references files or symbols that do not exist on the branch.

## Verification

Output the report path (`.mz/reviews/<YYYY_MM_DD>_review_branch_<branch><_vN>.md`), confirm the file exists, and print the verdict line plus the top critical findings.

## Error Handling

- **Empty / invalid base-branch argument** → escalate via AskUserQuestion; never guess.
- **Missing tooling** (`git`, `gh`) → detect before dispatch; if absent, escalate via AskUserQuestion with the exact missing command.
- An agent returns nothing usable (report file missing or empty) → `<PLUGIN_ROOT>/shared/retry-policy.md`: re-dispatch once with a clarified prompt, and don't retry API errors or usage limits.
- Never guess — on any ambiguity (unknown base branch, detached HEAD, no diff) escalate via AskUserQuestion rather than proceed silently.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase` and `Started`. This skill runs setup, one dispatch and its report in a single turn with no approval gate, so it leaves out `phase_complete` and `what_remains`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed or a step fails, in the form `- (review|failure) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. On reading an older file, put `schema_version: 2` on line 1 and `Status` on line 2, add no other keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
