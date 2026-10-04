---
name: cli-gh-axi
description: 'Uses the gh-axi CLI for GitHub shell operations: issue, pull request, workflow run, release, repo, search, and API tasks. Prefer this over regular `gh` for GitHub reads and simple mutations when an agent needs compact, structured, suggestion-rich output. Triggers on: gh, GitHub CLI, github issue, github pr, pull request, workflow run, github release, gh api, repo inspection, list PRs, view issue, check workflow runs, inspect repo, GitHub shell operations.'
---

# gh-axi

Use `gh-axi` when you want GitHub CLI operations with agent-friendly output instead of the default human-oriented `gh` formatting.

## Why This CLI

`gh-axi` wraps `gh` and improves the shell experience for agents:

- compact structured output instead of verbose tables or prose
- contextual next-step suggestions after each command
- better default dashboard with repo, issue, and PR state on `gh-axi` with no args
- command coverage for issues, PRs, workflow runs, workflows, releases, repos, labels, search, and raw API access

Prefer `gh-axi` over plain `gh` for read-heavy GitHub tasks and straightforward mutations.

## Safe Invocation

Always disable the CLI's hook auto-install behavior when invoking it from this repo:

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi --help
```

Use the same prefix for every command unless you explicitly want it to modify global Claude/Codex hook config in your home directory.

Requirements:

- `gh` must be installed
- `gh auth login` must already be completed

## Core Workflow

Start with the dashboard or a small listing command, then drill into the specific object you need.

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr list --limit 5
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr view 46 --comments
```

Use the dashboard when you need quick repo context. Use the subcommands when you already know the domain you need.

## Repository Targeting

Most commands operate on the current repo by default. Override with `-R` or `--repo` when needed.

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi issue list -R owner/name
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi run list --repo owner/name
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi search issues "login bug" --repo owner/name
```

Prefer `-R owner/name` when you want the repo target to be visually prominent in the command.

## Issues

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi issue list --state open --limit 10
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi issue view 42 --comments
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi issue create --title "Fix login" --body "Steps to reproduce..."
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi issue comment 42 --body "Investigating now"
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi issue close 42 --reason completed
```

Useful filters for `issue list` include `--state`, `--label`, `--assignee`, `--author`, `--milestone`, `--sort`, and `--limit`.

## Pull Requests

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr list --state open --limit 10
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr view 46 --comments
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr diff 46
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr checks 46
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr review 46 --approve --body "Looks good"
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi pr merge 46 --method squash --delete-branch
```

Use `pr view`, `pr diff`, and `pr checks` as the normal triad for understanding a PR before taking action.

## Workflow Runs And Workflows

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi run list --status failure --limit 10
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi run view 123456 --log-failed
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi run rerun 123456 --failed
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi run cancel 123456
```

Use workflow-run commands for CI debugging. Reach for `run view --log-failed` before broader reruns when you need signal fast.

For workflow definitions:

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi workflow list
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi workflow view ci.yml
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi workflow run ci.yml
```

## Releases, Repos, And Labels

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi release list
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi release view v1.2.3

env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi repo view
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi repo list hashintel

env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi label list
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi label create bug --color ff0000
```

Use these when you need structured GitHub metadata without dropping to raw API calls.

## Search

Use `search` when you know the query shape but not the object number.

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi search issues "login bug" --repo hashintel/brunch --state open
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi search prs "router migration" --author lunelson --sort updated
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi search repos "cli tool" --language TypeScript --stars ">50"
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi search code "createRootRouteWithContext" --repo hashintel/brunch
```

This is especially useful when an agent would otherwise guess IDs or manually scan multiple lists.

## Raw API

Use `api` when the wrapped subcommands do not expose the endpoint or fields you need.

```bash
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi api repos/hashintel/brunch/pulls
env GH_AXI_DISABLE_HOOKS=1 npx -y gh-axi api repos/hashintel/brunch/actions/runs
```

Prefer higher-level subcommands first. Use `api` as an escape hatch, not the default.

## When To Prefer Graphite Or Plain gh

Prefer `cli-graphite` instead of `gh-axi` when the task is stack-aware PR management:

- creating or maintaining a Graphite stack
- submitting stacked PRs
- restacking or moving dependent branches

Prefer plain `gh` only when:

- you already need an exact `gh` invocation from existing docs or automation
- `gh-axi` does not expose a needed flag or subcommand shape
- you are debugging `gh` behavior itself

## Practical Guidance

- Start with `gh-axi` alone for the dashboard when you need quick repo state.
- Prefer `gh-axi` over `gh` for issue, PR, run, release, repo, and search reads.
- Use `--comments` on `view` commands when conversational context matters.
- Use `--limit` aggressively to keep output small and focused.
- Use `-R owner/name` whenever the repo target is not obvious from cwd.
- Always invoke with `GH_AXI_DISABLE_HOOKS=1` in ad hoc repo work unless you intentionally want global hook installation.
