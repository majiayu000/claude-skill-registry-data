---
name: llm-call-observability-gap
description: "Find LLM API calls that lack observability - no logging, error handling, timeout, or cost tracking. Trigger: /llm-obs"
trigger: /llm-obs
---
# /llm-obs

Every LLM call is a risk. This skill finds calls that lack observability and judges which gaps matter.

## What this is for

- LLM API calls without error handling
- Calls without logging or audit trail
- Missing timeouts and cost tracking
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/llm-obs -help` or `/llm-obs -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/obs-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each call site:

- **Observed**: logging + error handling + timeout present
- **Partially-observed**: missing some observability
- **Blind**: no monitoring at all

### Step 5 - Write report

File `llm-observability-report.md` in current working directory:

1. **Summary** - call sites by observability level.
2. **Call site table** - blind first. Per site: file, line, provider, has error handling, has logging, has timeout, has cost tracking, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight blind call sites.

## Usage

```
/llm-obs               # interactive
/llm-obs <dir>         # scan project
/llm-obs -help
```


