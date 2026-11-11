---
name: evidence-based-analysis
description: "Use when analysing code, explaining how something works, writing or updating documentation, reviewing a change, debugging, tracing a CI or CD pipeline, or making any claim about the codebase. Also use when asked whether something is used, called, or dead code."
---

# Evidence Based Analysis

## Overview

You must verify every claim with concrete evidence from the codebase before stating it as fact. Never infer behavior without proof.

## When to use
- Any statement about what the code does, calls, or produces
- Documentation, explanations, reviews, debugging ([`debug`](../debug/SKILL.md) requires it)
- Pipeline or build analysis
- Claims about test results or command output

## Instructions

### Core Rules

1. **No assumptions** - If you cannot find direct evidence (grep match, file content, explicit reference), do not state it as fact
2. **Show your work** - When making claims, cite the file and line number
3. **Distinguish facts from inferences** - If you must infer, explicitly say "I infer..." or "This appears to..." and explain why
4. **Verify references** - When you see something defined (function, script, variable), verify it's actually used before claiming it's part of the workflow
5. **Trace the full path** - For CI/CD pipelines, trace job → script → reference chain completely
6. **Verify before documenting** - When updating documentation or source-of-truth files based on a claim about command output, test results, or runtime behavior, run the command yourself to confirm before writing it as fact. Never take stated results at face value when you can verify them directly

### Verification Checklist

Before documenting any behavior:

- [ ] Did I find the definition? (where it's declared)
- [ ] Did I find the usage? (where it's called/referenced)
- [ ] Did I verify the connection? (the caller actually invokes it)
- [ ] Can I cite file:line for each claim?

### Language Rules

### DO say:
- "In `file.yml:42`, the job `build` calls..."
- "I found the script `.tag_deployment_branch` defined at line 27, but I cannot find any job that references it"
- "Based on lines 10-15 of `config.yml`, this appears to..."
- "I could not find evidence of X in the codebase"

### DO NOT say:
- "The pipeline automatically creates tags" (without showing which job does it)
- "This script is used for..." (without showing where it's called)
- "The system does X" (without citing evidence)
- "All tests pass" (without running the tests yourself to confirm)

### When Uncertain

1. State what you found
2. State what you could not find
3. Ask the user if they have additional context
4. Never fill gaps with assumptions

### Documentation Tasks

When writing documentation:
1. Draft the content
2. For each claim, mentally check: "Can I cite where I found this?"
3. If no citation possible, either find evidence or remove/qualify the statement
4. Flag uncertain sections with "⚠️ Needs verification:" prefix

## Example

**Bad (hallucination risk):**
"Git tags are automatically created on production release"

**Good (evidence-based):**
"I found `.tag_deployment_branch` script in `ci.deploy.scripts.yml:27-34` that creates git tags, but I cannot find any job in the pipeline that calls this script. The tagging functionality appears to be unused."
