---
name: token-budget-analyzer
description: "Analyze static code for token usage patterns, waste, and budget risks. Trigger: /token-budget"
trigger: /token-budget
---
# /token-budget

LLM costs are dominated by token consumption. This skill finds excessive token waste and missing budgets before deployment.

## What this is for

- Unnecessarily long system prompts
- Context larger than max_tokens (truncation risk)
- Repetitive instructions across messages
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/token-budget -help` or `/token-budget -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/token-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each call site:

- **Efficient**: appropriate sizing for the task
- **Wasteful**: could be optimized without quality loss
- **Critical**: context window exceeded, truncation guaranteed

### Step 5 - Write report

File `token-budget-report.md` in current working directory:

1. **Summary** - call sites by efficiency.
2. **Call site table** - critical first. Per site: file, line, estimated input tokens, estimated output tokens, max tokens, truncation risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight critical sites that will truncate or waste tokens.

## Usage

```
/token-budget               # interactive
/token-budget <dir>         # scan project
/token-budget -help
```


