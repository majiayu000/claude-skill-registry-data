---
name: task-estimation
description: Provides task estimation before starting work. Use when planning new features, refactoring, bug fixes, or any non-trivial changes. Triggered by keywords like estimate, plan, complexity, tokens, approach.
---

# Task Estimation

Before starting any non-trivial task, ALWAYS provide an estimation.

## Template

```
Complexity: [Simple / Medium / Complex]
Est. tokens: [Low (~5K) / Medium (~15K) / High (~30K+)]
Files: [list files you expect to touch]
Approach: [1-2 sentences on your plan]
```

## Guidelines

- **Simple**: Single file change, straightforward logic
- **Medium**: 2-5 files, moderate complexity, some exploration needed
- **Complex**: 5+ files, architectural changes, significant exploration

If you are unsure of any estimate, ask for clarification before proceeding.

## Example

```
Complexity: Medium
Est. tokens: ~15K
Files: types.ts, parser.ts (new), server-functions.ts
Approach: Create parser module with categorization logic, integrate with existing instruction extractor.
```

## When to Apply

- Before implementing new features
- Before refactoring existing code
- Before fixing non-trivial bugs
- When the user asks "how would you approach this?"
- When exploring implementation options