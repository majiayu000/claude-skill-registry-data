---
name: skill-dedup
description: "Find functional overlap between skills via description similarity and script pattern matching. Trigger: /skill-dedup"
trigger: /skill-dedup
---
# /skill-dedup

Detects skills that do similar things: same trigger domain, overlapping description keywords, identical script patterns.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Skills with overlapping purpose across clusters
- Skills that could be merged or deprecated
- Semantic duplication despite different trigger names
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: pairwise description Jaccard + script pattern overlap

### Step 3

Report candidate pairs with overlap score

### Step 4

Write `skill-dedup-report.md`

## Usage

```
/skill-dedup             # interactive
/skill-dedup <dir>       # scan project
/skill-dedup -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).