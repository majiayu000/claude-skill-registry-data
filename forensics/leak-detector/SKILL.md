---
name: leak-detector
description: "Leak detector: trace resource acquisition and release across code paths, LLM classifies each as clean/leaky/uncertain. Read-only. Trigger: /leak-scan"
trigger: /leak-scan
---
# /leak-scan

Production incidents caused by leaked resources: this skill finds them before deployment.

## What this is for

- DB connection pools exhausted, file handles left open
- HTTP connections not closed, temp files never cleaned up
- Event listeners not unregistered
- **Read-only skill.** No code modification, no automated fix.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/leak-scan -help` or `/leak-scan -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/resource-trace.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each resource in context:

- **Safe**: acquired and released in all paths (finally block, using, defer, RAII)
- **Potential leak**: acquired but release is conditional or missing in error paths
- **Confirmed leak**: acquired with no release path in any code branch
- **Intentional escape**: resource returned, stored, or passed to callback (factory, pool)

### Step 5 - Write report

File `leak-report.md` in current working directory:

1. **Summary** - total resources, clean, potential-leak, confirmed-leak.
2. **Leak table** - confirmed first. Per resource: file, line, type, classification, evidence, fix suggestion.
3. **Intentional escapes** in appendix.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight confirmed leaks.

## Usage

```
/leak-scan               # interactive
/leak-scan <dir>         # scan project
/leak-scan -help
```


