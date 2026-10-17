---
name: dead-code-at-runtime
description: "Dead code at runtime detector: find feature flags, date gates, and env checks that make code unreachable in practice. Read-only. Trigger: /dead-runtime"
trigger: /dead-runtime
---
# /dead-runtime

Code that never executes is dead weight. This skill finds code that is reachable in theory but dead in practice.

## What this is for

- Feature flag branches that always take the same path
- Date-gated code past its expiration
- Env-specific code that never matches deployed environments
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/dead-runtime -help` or `/dead-runtime -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/runtime-dead-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each candidate:

- **Safe-to-remove**: condition permanently true/false, no active references
- **Requires-verification**: may still have dependents (check with team)
- **Keep**: condition still active or useful for debugging

### Step 5 - Write report

File `dead-runtime-report.md` in current working directory:

1. **Summary** - candidates by classification.
2. **Candidate table** - safe-to-remove first. Per candidate: file, line, condition, branch content, git blame age, has tests, classification.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight code that can be safely removed.

## Usage

```
/dead-runtime               # interactive
/dead-runtime <dir>         # scan project
/dead-runtime -help
```

