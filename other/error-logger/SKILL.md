---
name: error-logger
description: "Logs errors to the lessons registry with structured cause-prevention format when any command, build, test, or deployment fails. Triggers when a command returns a non-zero exit code, when a build fails, when tests fail, or when any unexpected error occurs."
---

# Error Logger

## Goal

Capture every error in a structured format so it is never repeated, and the orchestrator can understand what went wrong and why.

## Instructions

### Step 1: Capture Error Details

When an error occurs, immediately gather:
- The exact error message (last 5-10 lines of output)
- What command or action triggered it
- The current working directory and file context
- Whether this error has been seen before (check `.agent/knowledge/lessons.md`)

### Step 2: Check for Duplicates

Search `.agent/knowledge/lessons.md` for similar errors:
- Same error message?
- Same root cause?
- Same context?

If a matching entry exists:
- If the fix still works → apply the known fix, note "Known issue, applied existing fix"
- If the fix no longer works → update the entry with the new fix

### Step 3: Classify Severity

| Severity | Criteria |
|----------|----------|
| **Low** | Cosmetic issue, warning, or non-blocking error. Work can continue. |
| **Medium** | Blocking error but fixable. A command failed and needs a different approach. |
| **High** | Major failure. Build broken, tests failing, data at risk. |
| **Critical** | Security vulnerability, data loss risk, or production-affecting issue. |

### Step 4: Log the Entry

Append to `.agent/knowledge/lessons.md`:

```
[YYYY-MM-DD] SEVERITY: [level]
  ERROR: [exact error message — keep it concise but complete]
  CONTEXT: [what was being attempted when this happened]
  CAUSE: [root cause — WHY it failed, not just WHAT failed]
  FIX: [what resolved the immediate issue]
  PREVENT: [rule or check to avoid this in the future]
```

### Step 5: Explain to the Orchestrator

Use this format:
> **What went wrong**: [plain English, one sentence]
> **Why it happened**: [root cause, plain English]
> **What I did to fix it**: [the fix]
> **What I changed to prevent it**: [the new prevention rule]

### Step 6: Consider Rule Creation

If the prevention rule is significant (applies broadly, not just to this one case):
- Propose creating a formal rule via the rule-generator skill
- Example: "This error happens whenever we install packages in this project. Should I create a rule that always uses the --legacy-peer-deps flag?"

## Constraints

- Never delete or modify existing lessons — only append or update the FIX/PREVENT fields
- Always log BEFORE attempting a fix (so we have a record even if the fix fails)
- If the cause is unclear, write "CAUSE: Under investigation" and update later
- Keep entries concise — the lessons file will grow over time
