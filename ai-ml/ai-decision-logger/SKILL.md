---
name: ai-decision-logger
description: "Find model-based decision points and check if they are logged with sufficient context. Trigger: /ai-log"
trigger: /ai-log
---
# /ai-log

AI decisions must be auditable. This skill finds every model-based decision point and checks logging coverage.

## What this is for

- Model output used in conditionals without audit logging
- Classification results used for actions without context
- Approval/recommendation decisions missing human review path
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/ai-log -help` or `/ai-log -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/ai-decision-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each decision point:

- **Auditable**: full context logged + human review option
- **Partially-logged**: some context captured
- **Black-box**: no log, no audit trail

### Step 5 - Write report

File `ai-decision-report.md` in current working directory:

1. **Summary** - decisions by classification.
2. **Decision table** - black-box first. Per decision: file, line, decision type, has audit log, includes context, has human review, risk.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight black-box decisions.

## Usage

```
/ai-log                     # interactive
/ai-log <dir>               # scan project
/ai-log -help
```


