---
name: prompt-drift-tracker
description: "Track prompt changes across git history and flag drift that affects output quality or safety. Trigger: /prompt-drift"
trigger: /prompt-drift
---
# /prompt-drift

Prompts change subtly over commits. Each change can silently alter model behavior. This skill tracks prompt changes and flags semantic drift.

## What this is for

- Prompt output format constraints removed
- Safety instructions weakened or removed
- Prompt length changes that affect model behavior
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/prompt-drift -help` or `/prompt-drift -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir` and `-GitRange` (default: last 20 commits). Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/prompt-drift-scan.ps1" -ProjectDir "<path>" -GitRange 20
```

### Step 4 - Classification

For each drift:

- **Benign**: cosmetic or clarification changes
- **Monitor**: minor change, verify outputs
- **Significant**: output behavior likely changed
- **Critical**: safety posture weakened or output constraint removed

### Step 5 - Write report

File `prompt-drift-report.md` in current working directory:

1. **Summary** - drifts by severity.
2. **Drift table** - critical first. Per drift: file, commit, date, changed sections, before/after snippet, severity.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight critical and significant drifts.

## Usage

```
/prompt-drift               # interactive
/prompt-drift <dir>         # scan project
/prompt-drift -help
```


