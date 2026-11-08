---
name: github-scan-prs
description: 'Triages open GitHub PRs across repos into a ranked report of what needs attention. Use when the user says "scan PRs", "check PRs", "what PRs need attention", "PR inbox" or "daily PR report". Not for reviewing one specific PR (use github-review-pr).'
argument-hint: '[owner/repo1, owner/repo2, ...]'
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(gh repo view *), Bash(gh auth status *), Read, Write, AskUserQuestion
---

# Scan PRs

## Overview

Dispatch the `github-pr-scanner` agent to find pull requests that need the user's attention across multiple GitHub repositories, fan out per-PR haiku scorers for every PR, and produce a prioritized triage report. Deep code reviews are not part of this skill — for a thorough review on any single PR in the report, the user runs `/github-review-pr <url>` separately.

## When to Use

Triage of pull requests across one or more GitHub repositories into a prioritized list of what needs the user's attention; it scores PRs and does not review their code.

### When NOT to use

- The user already has a single PR in mind — use `github-review-pr` directly.
- The user wants to review their own local branch — use `review-branch`.
- No repositories are given and the current directory is not a git repo with a GitHub remote.

## Arguments

`$ARGUMENTS` should be a list of GitHub repositories:

- One per line: `owner/repo`
- Comma-separated: `owner/repo1, owner/repo2`
- As URLs: `https://github.com/owner/repo`

If no argument is provided, detect the current repository from `gh repo view --json nameWithOwner -q .nameWithOwner` and use that.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS` — list of GitHub repositories. If empty, resolve current repo via `gh repo view --json nameWithOwner -q .nameWithOwner`; if that fails, escalate via AskUserQuestion. Never guess.
1. `task_name` = `<YYYY_MM_DD>_github_scan_prs_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a snake_case summary of the repo list (max 20 chars, e.g. `owner_repo` or `multi_repo`); on same-day collision append `_v2`, `_v3`.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/`.
1. Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `Repos: [<list>]`, `ScannedPRs: 0`, `ScoredPRs: 0`.
1. Emit a visible setup block: `task_name`, repo list, report dir (`.mz/reviews/`).

### 1. Dispatch

1. Launch the `github-pr-scanner` agent with the repository list and `project_root: <PROJECT_ROOT>` as the prompt.
1. The agent scans for PRs where the user is requested for review, mentioned, assigned, or has changes requested on their own PRs, then fans out one `github-pr-info-scorer` haiku agent per PR (in parallel waves of up to 6) to gather metadata, complexity signals, and unanswered-question state.
1. Every PR returned by the scan is scored into one of three tiers — Tier 1 (directly asked, unanswered), Tier 2 (review or action requested), or Tier 3 (informational) — and ranked within its tier by complexity and age.
1. After completion, display the path to the triage report at `.mz/reviews/<YYYY_MM_DD>_github_scan_prs_<repo_names><_vN>.md` (append `_v2`, `_v3` etc. if a report with the same base name already exists).

## Red Flags

- You produced a triage report without scoring every PR the fetcher returned (top-N truncation is a bug here).
- You dispatched the `github-pr-reviewer` agent from this skill — deep reviews belong to `/github-review-pr`, not the triage flow.
- You let a Tier 2 or Tier 3 item outrank a Tier 1 item in the report (tier boundaries are absolute; complexity only orders within a tier).

## Verification

Output the triage report path (`.mz/reviews/<YYYY_MM_DD>_github_scan_prs_<repo_names><_vN>.md`), confirm the file exists, and confirm Tier 1 items (if any) appear above Tier 2 and Tier 3 in the report. The report should end with a `How to Deep-Review` footer pointing users to `/github-review-pr <url>` for any single PR that warrants a thorough read.

## Error Handling

- **Empty args** with no detectable current repo → before escalating, try the fallback for `gh repo view`: `mcp__*github*` MCP tools if exposed. Only escalate via AskUserQuestion after both `gh` and MCP fail; never guess.
- **`gh` unavailable** (not installed, not authenticated, rate-limited) → delegate to the fallback chain before blocking. The `github-pr-scanner` agent has its own `GitHub Access Fallback` section that governs downstream calls. Only escalate via AskUserQuestion if the MCP tier also fails.
- **Missing tooling** (`Agent` tool absent) → escalate via AskUserQuestion with the exact missing command.
- **Empty scanner result** (zero PRs returned or no priority-ranked list) → check the scanner's `pr_data.md` / report for `ZERO RESULTS` disclosure tokens before trusting:
  - `ZERO RESULTS VERIFIED` (per-repo smoke test passed) → report "no PRs need attention" and exit cleanly.
  - `ZERO RESULTS UNVERIFIED` or `ZERO RESULTS GLOBAL` → do not treat as a clean inbox; surface the warning in the final output and prompt the user to verify the GitHub username and repo list via AskUserQuestion before a silent "all clear" masks a real misconfiguration.
  - An agent returns nothing usable (no `ZERO RESULTS` token with an empty list, or a malformed response) → `<PLUGIN_ROOT>/shared/retry-policy.md`: re-dispatch once with a clarified prompt, and don't retry API errors or usage limits.
- Never guess — on any ambiguity (unresolvable repo, invalid URL, missing auth) escalate via AskUserQuestion rather than proceed silently.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase` and `Started`. This skill runs setup, one dispatch and its report in a single turn with no approval gate, so it leaves out `phase_complete` and `what_remains`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed or a step fails, in the form `- (review|failure) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. On reading an older file, put `schema_version: 2` on line 1 and `Status` on line 2, add no other keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

After Phase 1 completes, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with:

- `Status:` `complete`, or `blocked` / `failed` when the scan could not finish. Concerns and blockers go under `## Notes`.
- `Phase:` `1`, or `no_prs_found` when the scanner reported `ZERO RESULTS VERIFIED` (`Status` stays `complete`)
- `ScannedPRs:` total PR count from the fetcher artifact
- `ScoredPRs:` count of PRs with valid `github-pr-info-scorer` artifacts (should equal ScannedPRs on a clean run)
- `ReportPath:` absolute path to the triage report

Never rely on conversation memory — the state file is the source of truth if the session is interrupted.
