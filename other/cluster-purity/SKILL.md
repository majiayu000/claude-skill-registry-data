---
name: cluster-purity
description: "Detect skills that may belong to a different cluster based on description, trigger, and script patterns. Trigger: /cluster-purity"
trigger: /cluster-purity
---
# /cluster-purity

Skills can drift into the wrong cluster. This skill analyzes each skill's description and script patterns against cluster definitions.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Security-pattern skills in the quality cluster
- Data-access skills in the operations cluster
- Cluster boundary violations
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: per skill, extract keywords and compare to expected cluster keywords

### Step 3

Report boundary candidates

### Step 4

Write `cluster-purity-report.md`

## Usage

```
/cluster-purity           # interactive
/cluster-purity <dir>     # scan project
/cluster-purity -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).