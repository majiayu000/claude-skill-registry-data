---
name: standup
description: >
  Generate daily standup reports from Copilot session history and git data.
  Scoped to the current git user; files accumulate multi-author contributions
  in `.standup/`. Auto-detects date range from existing files.
  Triggers: "standup", "/standup", "daily standup", "what did I work on",
  "yesterday's work".
metadata:
    version: 0.6.2
machina:
    machine: machine/standup-machine.json
    scenario: default
---

# Standup

> **⚠️ Machina rule.** Driven by `machine/standup-machine.json` via `machina-driving`. Machine is source of truth.

## States

`idle` → `detecting-dates` ([alg](references/date-algorithm.md)) → `collecting-data` ([script](references/script-usage.md)) → `composing-entries` → `cross-checking-git` ([git](references/git-cross-check.md), skip if `!isRepo`) → `checking-dedup` ([rules](references/merge-flow.md#dedup-rules)) → `writing-fresh`/`appending-author` → `next-date-or-complete` → `complete`. Terminal: `nothing-to-generate`. Error → `abort` ([details](references/error-handling.md)).

## Repo Scoping

Auto-detect repo from `git remote get-url origin`, author from `git config user.name`. No git repo → skip git ops, author = `$env:USERNAME`.

## Per-Date Merge

Collect data → compose entries (skip if no usable entries and no commits) → cross-check git → write fresh or dedup-append by key **(feature, branch, author)**. **Done** = commits or completion signal. **In Progress** = ongoing or no commits.

## Key Rules

- No empty sections, no truncated UUIDs, no raw git output
- Each entry: `Author: @<name>` + description + `Session: <uuid>`

## References

[dates](references/date-algorithm.md) · [script](references/script-usage.md) · [merge](references/merge-flow.md) · [data](references/data-rules.md) · [git](references/git-cross-check.md) · [errors](references/error-handling.md)
