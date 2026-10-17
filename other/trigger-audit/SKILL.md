---
name: trigger-audit
description: "Check trigger uniqueness, naming convention, and README documentation. Trigger: /trigger-audit"
trigger: /trigger-audit
---
# /trigger-audit

Every skill has a `/trigger`. This skill checks they're unique, follow convention (kebab-case), and are listed in README.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Duplicate triggers across skills
- Triggers that don't match kebab-case convention
- Triggers missing from README.md
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: extract triggers from SKILL.md, compare to README table

### Step 3

Report duplicates, convention violations, omissions

### Step 4

Write `trigger-audit-report.md`

## Usage

```
/trigger-audit            # interactive
/trigger-audit <dir>      # scan project
/trigger-audit -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).