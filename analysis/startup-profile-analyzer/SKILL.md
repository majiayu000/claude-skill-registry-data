---
name: startup-profile-analyzer
description: "Startup profile analyzer: trace the entire initialization chain, LLM judges each step as essential/lazy-loadable/suspicious. Read-only. Trigger: /startup"
trigger: /startup
---
# /startup

What happens when your service starts? This skill traces every init step and finds cold-start optimizations.

## What this is for

- Module-level imports that could be lazy-loaded
- Connection pools, cache warming, scheduler registration at boot
- Heavy dependencies loaded at startup but used only in one handler
- **Read-only skill.** No code modification.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/startup -help` or `/startup -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/startup-trace.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read each init step in context:

- Is this essential at startup or could it be lazy-loaded?
- What would break if deferred?
- Is this a side effect at import time (suspicious)?

### Step 5 - Write report

File `startup-report.md` in current working directory:

1. **Summary** - total init steps, deferrable count, estimated boot time reduction.
2. **Init chain** - sorted by phase. Per step: phase, description, classification, deferral recommendation.
3. **Suspicious findings** (side effects at import time).
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight top 3 deferral candidates.

## Usage

```
/startup               # interactive
/startup <dir>         # scan project
/startup -help
```


