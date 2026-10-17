---
name: mock-production-gap
description: "Mock-production gap detector: compare test mocks against real implementations, LLM judges dangerous divergences. Read-only. Trigger: /mock-gap"
trigger: /mock-gap
---
# /mock-gap

Tests pass with mocks; production breaks with real dependencies. This skill finds mock divergences before they ship.

## What this is for

- Mock return values missing fields that production code uses
- Mock error types that don't match real error types
- Mock function signatures that differ from real implementations
- **Read-only skill.** No test changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/mock-gap -help` or `/mock-gap -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/mock-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each mock divergence:

- **Dangerous**: divergent field is used in production code path (test doesn't test real behavior)
- **Noisy**: divergent field exists but isn't used by calling code
- **Benign**: mock intentionally simplified for unrelated tests
- **Outdated**: real API changed, mock not updated

### Step 5 - Write report

File `mock-gap-report.md` in current working directory:

1. **Summary** - divergences by severity.
2. **Divergence table** - dangerous first. Per divergence: test file, mocked module, divergent field, mock value, real value, severity, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight mocks that silently test wrong behavior.

## Usage

```
/mock-gap               # interactive
/mock-gap <dir>         # scan project
/mock-gap -help
```


