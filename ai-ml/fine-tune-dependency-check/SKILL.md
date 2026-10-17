---
name: fine-tune-dependency-check
description: "Find fine-tuned model references and check base model deprecation status. Trigger: /finetune-deps"
trigger: /finetune-deps
---
# /finetune-deps

Fine-tuned models depend on their base model. When the base is deprecated, the fine-tune silently breaks.

## What this is for

- Fine-tune references with deprecated base models
- Missing version pinning on HuggingFace models
- Fine-tune IDs that may have expired
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/finetune-deps -help` or `/finetune-deps -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/finetune-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each fine-tune reference:

- **Current**: base model still supported
- **Expiring-soon**: within 3 months of EOL
- **Deprecated**: past EOL, will fail
- **Unknown**: model not in reference data, verify manually

### Step 5 - Write report

File `finetune-dependency-report.md` in current working directory:

1. **Summary** - references by classification.
2. **Reference table** - deprecated first. Per reference: file, line, base model, fine-tune name, deprecation date, alternative, risk.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight deprecated and expiring fine-tunes.

## Usage

```
/finetune-deps               # interactive
/finetune-deps <dir>         # scan project
/finetune-deps -help
```


