---
name: github_KM
description: "Use when the task centers on GitHub repositories, issues, pull requests, Actions runs, or `gh` CLI workflows. Trigger on requests to inspect or update issues and PRs, check CI status or logs, query repository metadata, or take a GitHub issue through branch, fix, test, commit, and push. Supersedes `gh-issue-fix-flow`. Do not use for generic local git work that does not involve GitHub."
---
# GitHub Skill

Use the `gh` CLI to interact with GitHub. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## Pull Requests

Check CI status on a PR:
```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:
```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:
```bash
gh run view <run-id> --repo owner/repo
```

View logs for failed steps only:
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## API for Advanced Queries

The `gh api` command is useful for accessing data not available through other subcommands.

Get PR with specific fields:
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON Output

Most commands support `--json` for structured output.  You can use `--jq` to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## Issue Fix Workflow

This skill now owns the issue-fix lane that previously lived in `gh-issue-fix-flow`.

End-to-end flow for resolving a GitHub issue through fix, validation, and push.

### 1. Intake and issue context

1. Use `gh issue view <id> --repo <owner/repo> --comments` to get full issue context.
2. If the repo is unclear, run `gh repo view --json nameWithOwner` to confirm.
3. Capture reproduction steps, expected behavior, and any maintainer notes.

### 2. Locate the code path

1. Use `rg -n` to locate likely files and entry points.
2. Read the relevant code paths with context.
3. Follow repo-specific conventions (AGENTS/CLAUDE instructions).

### 3. Implement the fix

1. Edit the minimal set of files.
2. Keep changes aligned with existing architecture and style.
3. Add tests when behavior changes and test coverage is practical.

### 4. Build and test

1. Use XcodeBuildMCP for required builds/tests:
   - Set defaults once: `mcp__XcodeBuildMCP__session-set-defaults`.
   - Build: `mcp__XcodeBuildMCP__build_macos` or `mcp__XcodeBuildMCP__build_sim`.
   - Tests: prefer targeted schemes (e.g., `mcp__XcodeBuildMCP__test_sim`).
2. If macOS tests fail due to deployment target mismatches, run the equivalent iOS simulator tests.
3. Report warnings or failures; do not hide them.

### 5. Commit and push

1. Check for unrelated changes with `git status --short`.
2. Stage only the fix (exclude unrelated files).
3. Commit with a closing message: `Fix … (closes #<issue>)`.
4. Push with `git push`.

### 6. Report back

1. Summarize what changed and where.
2. Provide test results (including failures).
3. Note any follow-ups or blocked items.
