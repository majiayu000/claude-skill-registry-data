---
name: status
description: Quick "where am I?" snapshot - branch, uncommitted work, last commit, what was in progress, what's next.
user-invocable: true
---

# Status Check

Fast context recovery. For when you come back mid-task and forgot where you left off.

## 1. Git State

Run in parallel:

```bash
git branch --show-current
```

```bash
git status --short
```

```bash
git log --oneline -5
```

```bash
git stash list
```

## 2. Last Session

Read the last entry from `docs/session-log.md` (the most recent `## ` heading block). Extract: task, status, files touched, notes for next agent.

## 3. Uncommitted Work Analysis

If there are uncommitted changes, categorize them:

- Which features/areas do the changed files belong to?
- Are they staged or unstaged?
- Any untracked files that look like new work?

## 4. Staleness Check

Check the last `## ` entry date in `docs/session-log.md`. If older than 48 hours, add to report:

```
STALE: Last session log is [X] days old. Context may be outdated.
```

## 5. Active Priorities

Quick read of `memory/project_current_priorities.md` for what should be in focus.

## Report Format

```
STATUS - [time]

BRANCH:    [name]
LAST:      [last commit message]
CHANGES:   [X] files modified, [X] untracked
            -> [1-line summary of what areas]
STASHES:   [count or "none"]

LAST SESSION: [task] - [status: completed/partial/blocked]
NEXT UP:      [priority from memory or session log]
```

Keep under 150 words. This is a glance, not a report.
