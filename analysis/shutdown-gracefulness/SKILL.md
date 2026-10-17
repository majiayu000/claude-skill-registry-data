---
name: shutdown-gracefulness
description: "Shutdown gracefulness analyzer: check if shutdown hooks actually drain, flush, and complete in-flight work. Read-only. Trigger: /shutdown"
trigger: /shutdown
---
# /shutdown

A pod is killed. What happens to in-flight requests, open transactions, half-written files? This skill checks shutdown implementation detail.

## What this is for

- Signal handlers that call process.exit(0) immediately (drops in-flight)
- DB connection pools without drain in shutdown (queries interrupted)
- File writers without flush (data loss)
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/shutdown -help` or `/shutdown -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/shutdown-detail-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each shutdown path:

- **Safe**: complete drain before exit
- **Mostly-safe**: drains but has timeout gaps
- **Risky**: drops in-flight work
- **Dangerous**: data corruption on termination

### Step 5 - Write report

File `shutdown-grade-report.md` in current working directory:

1. **Summary** - shutdown paths by classification.
2. **Path table** - dangerous first. Per path: process, mechanism, grace timeout, drains requests, flushes buffers, releases connections, handles errors, grade.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight processes that would corrupt data if terminated.

## Usage

```
/shutdown               # interactive
/shutdown <dir>         # scan project
/shutdown -help
```


