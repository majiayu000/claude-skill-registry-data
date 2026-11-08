---
name: github-review-pr
description: 'Reviews a GitHub pull request by URL or owner/repo#number and writes a findings report with a verdict. Use when the user says "review this PR", pastes a PR link or asks if a change is safe to merge. Not for local branches (use review-branch).'
argument-hint: <PR URL or owner/repo#number>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(gh pr view *), Bash(gh auth status *), Bash(git worktree list *), Bash(git worktree remove *), Read, Write, AskUserQuestion
---

# Review PR

## Overview

Dispatch the `github-pr-reviewer` agent to perform a thorough review of a GitHub pull request in a temporary PR worktree that the agent creates and removes. Produces a report under `.mz/reviews/` with severity-labeled findings and a verdict.

## When to Use

Reviewing a GitHub pull request, given by URL or `owner/repo#number`, and writing a findings report with a verdict.

### When NOT to use

- The changes live on a local branch, not a GitHub PR — use `review-branch`.
- The user wants to triage many PRs at once — use `github-scan-prs`.
- The PR reference is ambiguous or missing — ask for a URL or `owner/repo#number`.

## Arguments

`$ARGUMENTS` should be a GitHub PR reference:

- Full URL: `https://github.com/owner/repo/pull/123`
- Short form: `owner/repo#123`

If no argument is provided, ask the user for a PR URL.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| Phase | Goal                              | Details      |
| ----- | --------------------------------- | ------------ |
| 0     | Setup                             | Inline below |
| 1     | Dispatch github-pr-reviewer agent | Inline below |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. If the PR reference is empty or malformed, escalate via AskUserQuestion — never guess, never fabricate a PR URL.
1. Normalize the reference to `<owner>_<repo>_<pr_number>` form.
1. `task_name` = `<YYYY_MM_DD>_github_review_pr_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is `<owner>_<repo>_<pr_number>` truncated to 20 chars, snake_case; on same-day collision append `_v2`, `_v3`.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/`.
1. Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `PR: <reference>`, `Owner: <owner>`, `Repo: <repo>`, `Number: <pr_number>`.
1. Emit a visible setup block: `task_name`, PR reference, report dir (`.mz/reviews/`).

### 1. Dispatch

1. Validate via `gh pr view` that the normalized PR reference is accessible. On failure, escalate via AskUserQuestion.
1. Launch the `github-pr-reviewer` agent with the PR reference, `task_name: <task_name>` and `project_root: <PROJECT_ROOT>` as the prompt.
1. After the agent returns, whatever its status, run `git worktree list` and remove any leftover `.claude/worktrees/pr-<pr_number>-*` entry with `git worktree remove --force <path>`. The agent removes its own worktree, but a turn limit or crash can stop it first.
1. Parse the agent's final message for the `STATUS:` line:
   - `STATUS: DONE` or `STATUS: DONE_WITH_CONCERNS` → update `state.md` to `Status: complete`, `Phase: 1`. On `DONE_WITH_CONCERNS`, also log the concerns block into `state.md`.
   - `STATUS: NEEDS_CONTEXT` → re-dispatch **once** with the requested context; on a second `NEEDS_CONTEXT`, escalate via AskUserQuestion.
   - `STATUS: BLOCKED` → escalate via AskUserQuestion with the blocker reason. Never auto-retry on `BLOCKED`.
1. On any terminal success, display the absolute report path.

## Red Flags

- The PR argument is missing or malformed and you are guessing a URL instead of asking.
- You dispatched `github-pr-reviewer` without first validating PR accessibility via `gh pr view`.
- The agent returned `STATUS: BLOCKED` or `NEEDS_CONTEXT` and you retried more than once instead of escalating.
- The agent's final message had no `STATUS:` line and you proceeded anyway.

## Verification

Output the report path (`.mz/reviews/<YYYY_MM_DD>_github_review_pr_<owner>_<repo>_<pr_number><_vN>.md`), confirm the file exists, and print the `VERDICT:` line plus the count of `Critical:` findings.

## Error Handling

- **Empty / malformed PR argument** → escalate via AskUserQuestion; never guess, never fabricate a PR URL.
- **`gh` unavailable for Phase 0 validation** → before escalating, try `mcp__*github*` MCP tools if exposed. Only escalate via AskUserQuestion after both `gh` and MCP fail, and ask the user to authenticate `gh` or connect a GitHub MCP server.
- **Missing tooling** (`git worktree` unavailable, `Agent` tool absent) → escalate via AskUserQuestion with the exact missing command.
- An agent returns nothing usable (report file missing, empty, or no `VERDICT:` line) → `<PLUGIN_ROOT>/shared/retry-policy.md`: re-dispatch once with a clarified prompt, and don't retry API errors or usage limits.
- Never guess — on any ambiguity (inaccessible PR, 404, merge conflict in worktree, missing base ref) escalate via AskUserQuestion rather than proceed silently.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase` and `Started`. This skill runs setup, one dispatch and its report in a single turn with no approval gate, so it leaves out `phase_complete` and `what_remains`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed or a step fails, in the form `- (review|failure) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. On reading an older file, put `schema_version: 2` on line 1 and `Status` on line 2, add no other keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
