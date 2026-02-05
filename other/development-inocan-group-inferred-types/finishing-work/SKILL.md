---
name: finishing-work
description: Use when completing work on a task or feature. Prompts for code review before finishing. ALWAYS invoke this skill before saying work is done.
---

# Finishing Work

## CRITICAL: Always Ask About Code Review

Before finishing ANY work, you MUST ask the user:

> "Would you like me to request a code review before finishing? (Yes/No)"

Use the AskUserQuestion tool with options:

- **Yes** - Invoke `coderabbit-request` skill, then triage and fix any issues
- **No** - Skip review and proceed to finish

**Do NOT skip this prompt.** Even for small changes, the user decides.

## If User Says Yes: Code Review Workflow

Invoke `coderabbit-request` to start the review pipeline:

```
coderabbit-request
        ↓ (outputs JSON)
coderabbit-triage
        ↓ (outputs task plan)
coderabbit-fix (parallel or sequential)
```
