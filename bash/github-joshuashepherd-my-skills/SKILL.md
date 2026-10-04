---
name: github
description: "Interact with GitHub using the `gh` CLI — PRs, issues, CI runs, code review, and API queries. Use when checking PR status, creating/commenting on issues, listing/filtering PRs, or viewing run logs."
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Agent
---

Use the `gh` CLI to interact with GitHub: $ARGUMENTS

Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

---

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

## Issues

List open issues:

```bash
gh issue list --repo owner/repo --state open
```

Create an issue:

```bash
gh issue create --repo owner/repo --title "Title" --body "Description"
```

## Code Review

Review a PR diff:

```bash
gh pr diff 55 --repo owner/repo
```

Comment on a PR:

```bash
gh pr comment 55 --repo owner/repo --body "Comment text"
```

## API for Advanced Queries

The `gh api` command is useful for accessing data not available through other subcommands.

Get PR with specific fields:

```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

Get PR review comments:

```bash
gh api repos/owner/repo/pulls/55/comments
```

## JSON Output

Most commands support `--json` for structured output. Use `--jq` to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```
