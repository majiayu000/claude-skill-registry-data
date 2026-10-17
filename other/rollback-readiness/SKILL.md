---
name: rollback-readiness
description: "Rollback readiness: check each deployable change against rollback criteria, LLM estimates cost and risk of undoing it. Read-only. Trigger: /rollback"
trigger: /rollback
---
# /rollback

Every deployment is a bet until you know you can undo it. This skill checks rollback readiness.

## What this is for

- DB migration without down migration
- API change breaking backward compatibility
- Feature flag with no removal plan
- **Read-only skill.** No code changes, no automated rollback.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/rollback -help` or `/rollback -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/rollback-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read each change:

- Is there a rollback mechanism? (down migration, compat layer, flag inversion)
- What is the blast radius? (single service vs coordinated rollback)
- Is the rollback safe? (data loss risk, downtime required)

### Step 5 - Write report

File `rollback-readiness-report.md` in current working directory:

1. **Summary** - changes found, safe rollbacks, risky, no rollback path.
2. **Change table** - sorted by risk. Per change: kind, element, has rollback, mechanism, blast radius, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight changes with no rollback path.

## Usage

```
/rollback               # interactive
/rollback <dir>         # scan project
/rollback -help
```


