---
name: skill-lifecycle
description: "Report on skill age, last modified, git activity, and deprecation status across all clusters. Trigger: /skill-lifecycle"
trigger: /skill-lifecycle
---
# /skill-lifecycle

Tracks the health and freshness of every skill in the project.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Skills with no git activity in months (stale)
- Skills that have never been smoke-tested
- Skills that reference deprecated patterns
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: git log per skill directory + file stats

### Step 3

Report stalest skills by cluster

### Step 4

Write `skill-lifecycle-report.md`

## Usage

```
/skill-lifecycle           # interactive
/skill-lifecycle <dir>     # scan project
/skill-lifecycle -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).