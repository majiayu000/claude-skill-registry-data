---
name: tool-call-fidelity-checker
description: "Check tool/function definitions for hallucination-prone schemas. Trigger: /tool-fidelity"
trigger: /tool-fidelity
---
# /tool-fidelity

LLM function calling requires precise tool definitions. This skill finds ambiguous schemas that cause models to call APIs wrong.

## What this is for

- Missing parameter descriptions (model guesses format)
- Ambiguous types (string without enum for fixed options)
- Excessive optional parameters (model fills hallucinated defaults)
- TOCTOU parameters (model can't know current state)
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/tool-fidelity -help` or `/tool-fidelity -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/tool-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each tool definition:

- **Safe**: well-defined, all parameters described
- **Risky**: ambiguous parameters, missing descriptions
- **Dangerous**: hallucination-prone definitions

### Step 5 - Write report

File `tool-fidelity-report.md` in current working directory:

1. **Summary** - tools by classification.
2. **Tool table** - dangerous first. Per tool: file, line, tool name, parameter count, missing descriptions, ambiguous types, TOCTOU risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight dangerous tool definitions.

## Usage

```
/tool-fidelity               # interactive
/tool-fidelity <dir>         # scan project
/tool-fidelity -help
```


