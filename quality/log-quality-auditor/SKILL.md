---
name: log-quality-auditor
description: "Log quality auditor: inventory every log statement, check for structure, correlation IDs, levels, PII risk, then LLM judges operational quality. Read-only. Trigger: /log-audit"
trigger: /log-audit
---
# /log-audit

Logs that are not machine-parseable are not logs - they are noise. This skill audits log quality across your codebase.

## What this is for

- Free-text messages instead of structured fields
- Missing correlation IDs, inconsistent levels
- PII in log output, silent error paths
- **Read-only skill.** No log changes, no code modification.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/log-audit -help` or `/log-audit -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/log-harvest.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read log statements in context:

- Is the message structured (template with fields) or free-text interpolation?
- Are correlation IDs consistently threaded through request chains?
- Are error logs actionable (include error object + context)?
- Is there PII risk in log output?

### Step 5 - Write report

File `log-quality-report.md` in current working directory:

1. **Summary** - overall score, proportion structured vs free-text, correlation ID coverage.
2. **Per-module analysis** - module, log count, structured %, correlation ID %, top issues.
3. **Recommendations** - add structured fields, standardize levels, add correlation IDs, remove PII.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight worst modules and quick wins.

## Usage

```
/log-audit               # interactive
/log-audit <dir>         # scan project
/log-audit -help
```


