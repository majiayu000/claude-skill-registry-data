---
name: runtime-type-mismatch
description: "Runtime type mismatch detector: find every runtime type assumption, LLM judges which will fail in production. Read-only. Trigger: /type-mismatch"
trigger: /type-mismatch
---
# /type-mismatch

Types only exist until compile time. At runtime, `any`, casts, and untyped boundaries let anything through. This skill finds unvalidated runtime type assumptions.

## What this is for

- JSON.parse() result used without validation (crash on unexpected shape)
- API response accessed without schema check (missing field = undefined)
- Type assertions/casts that hide real type mismatches
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/type-mismatch -help` or `/type-mismatch -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/type-assumption-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each assumption:

- **Crash**: uncaught TypeError on null/undefined access
- **Data-loss**: wrong value used silently
- **Safe**: validated upstream or internal source

### Step 5 - Write report

File `type-mismatch-report.md` in current working directory:

1. **Summary** - assumptions by risk level.
2. **Assumption table** - crash risk first. Per assumption: file, line, kind, origin, has validation, risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight assumptions that will crash in production.

## Usage

```
/type-mismatch               # interactive
/type-mismatch <dir>         # scan project
/type-mismatch -help
```

