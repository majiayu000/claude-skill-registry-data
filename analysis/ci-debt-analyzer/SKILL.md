---
name: ci-debt-analyzer
description: "CI debt analyzer: read CI configuration (GitHub Actions, GitLab CI, Jenkins, CircleCI), measure pipeline health, then LLM judges what is costing the team most. Read-only. Trigger: /ci-debt"
trigger: /ci-debt
---
# /ci-debt

CI pipelines silently rot. This skill measures pipeline health and identifies the biggest time waste.

## What this is for

- Jobs that take 40 minutes because caching is missing
- Tests that always pass because they never run
- Matrix builds testing the same thing 8 times
- **Read-only skill.** No pipeline modification, no CI config changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/ci-debt -help` or `/ci-debt -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/ci-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read the CI config and scan results:

- Identify the #1 time waste per pipeline
- Is the matrix appropriate for the project's support policy?
- Are tests actually running? Check for empty test commands, always-green steps
- Is caching missing? Are jobs sequential when they could be parallel?

### Step 5 - Write report

File `ci-debt-report.md` in current working directory:

1. **Summary** - estimated CI time, #1 bottleneck, potential time savings.
2. **Per-job analysis** - job name, duration estimate, cache status, matrix efficiency, sequential blockers.
3. **Recommendations** - specific config changes with estimated time savings.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight biggest potential time savings.

## Usage

```
/ci-debt               # interactive
/ci-debt <dir>         # scan project
/ci-debt -help
```


