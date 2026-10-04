---
name: code-simplifier
description: Use this skill after completing code changes to review for reuse, quality, and efficiency. Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality.
---

# Code Simplifier

After completing code changes, review your work for opportunities to simplify and improve.

## What to Check

### Reuse

- Are there existing utilities, helpers, or patterns in the codebase that do the same thing?
- Did you duplicate logic that already exists elsewhere?
- Can any new helpers be consolidated with existing ones?

### Quality

- Is the code consistent with surrounding patterns and conventions?
- Are variable/function names clear and descriptive?
- Is control flow straightforward? Flatten nested conditionals with guard clauses and early returns.
- Are there unnecessary abstractions or over-engineering?
- Is error handling appropriate — not too much, not too little?

### Efficiency

- Are there redundant operations (duplicate API calls, repeated computations, unnecessary loops)?
- Could any logic be simplified with built-in language features or standard library tools?
- Are imports clean and minimal?

## Process

1. Review all files you modified in this session
2. For each file, check against the criteria above
3. Fix any issues found — do not just flag them
4. Keep changes minimal and focused: only simplify, do not add features or refactor beyond what's needed

## Scope

- Focus on code you wrote or modified in this session
- Do not refactor unrelated code
- Preserve all existing functionality — simplification must not change behavior
