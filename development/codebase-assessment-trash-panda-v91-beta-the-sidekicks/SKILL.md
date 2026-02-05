---
name: codebase-assessment
description: Use when starting open-ended tasks in unfamiliar codebases, before following existing patterns
---

# Codebase Assessment

Assess codebase maturity before implementing. Don't blindly follow patterns that may be outdated or inconsistent.

## Quick Assessment Checklist

1. **Check config files**: linter, formatter, type config present?
2. **Sample 2-3 similar files**: Are patterns consistent?
3. **Note project age signals**: Dependencies current? Patterns modern?

## State Classification

| State | Signals | Your Behavior |
|-------|---------|---------------|
| **Disciplined** | Consistent patterns, configs present, tests exist | Follow existing style strictly |
| **Transitional** | Mixed patterns, some structure | Ask: "I see X and Y patterns. Which to follow?" |
| **Legacy/Chaotic** | No consistency, outdated patterns | Propose: "No clear conventions. I suggest [X]. OK?" |
| **Greenfield** | New/empty project | Apply modern best practices |

## Verification Before Assuming

If codebase appears undisciplined, verify before assuming:

- Different patterns may serve different purposes (intentional)
- Migration might be in progress
- You might be looking at the wrong reference files

## What To Check

| Area | Check For |
|------|-----------|
| **Style** | ESLint/Prettier/Biome config, consistent formatting |
| **Types** | tsconfig.json strictness, type coverage |
| **Testing** | Test framework, coverage expectations, test file patterns |
| **Structure** | Folder conventions, naming patterns, module boundaries |
| **Dependencies** | Package age, maintenance status, duplicate functionality |

## Output Format

After assessment, state:

```
Codebase state: [Disciplined/Transitional/Legacy/Greenfield]
Key patterns to follow: [list 2-3]
Concerns noted: [any issues observed]
Proceeding with: [your approach]
```
