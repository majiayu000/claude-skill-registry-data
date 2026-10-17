---
name: error-propagation-mapper
description: "Error propagation mapper: trace every error from origin through handling blocks to surface, LLM classifies each path as monitored/silent/dangerous. Read-only. Trigger: /error-map"
trigger: /error-map
---
# /error-map

Errors flow through code like water through pipes. This skill maps every path to find silent data loss and crash risks.

## What this is for

- Errors swallowed in empty catch blocks
- Error context lost through wrapping without cause chaining
- Returned null defaults that callers treat as success
- **Read-only skill.** No code modification.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/error-map -help` or `/error-map -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/error-trace.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each error path:

- **Monitored**: error is logged and surfaced (HTTP error, alert)
- **Silent**: error is swallowed or returns default without notification
- **Dangerous**: error causes crash, data corruption, or info leak

### Step 5 - Write report

File `error-propagation-report.md` in current working directory:

1. **Summary** - error paths by classification.
2. **Path table** - dangerous first. Per path: origin, handler chain, action taken, context preserved, final destination.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight dangerous silent paths.

## Usage

```
/error-map               # interactive
/error-map <dir>         # scan project
/error-map -help
```


