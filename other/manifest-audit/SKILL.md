---
name: manifest-audit
description: "Verify project tracking docs, README.md, and actual filesystem are in sync. Trigger: /manifest-audit"
trigger: /manifest-audit
---
# /manifest-audit

The manifest (tracking.md) and README.md are manually maintained. This skill detects drift between declared and actual skills.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Skills on disk not in tracking.md or README
- Skills in tracking.md missing from disk
- Sprint count or skill count mismatches
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: compare filesystem skills vs tracking vs README

### Step 3

Report additions, deletions, count mismatches

### Step 4

Write `manifest-audit-report.md`

## Usage

```
/manifest-audit           # interactive
/manifest-audit <dir>     # scan project
/manifest-audit -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).