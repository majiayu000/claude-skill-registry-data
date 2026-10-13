---
name: refactoring
description: Safe, incremental code refactoring using Martin Fowler's refactoring catalog
triggers: [refactor, clean up code, improve structure, extract method, rename, restructure]
audience: engineer
---

# Refactoring

## Context
Refactoring means changing the internal structure of code without altering its observable behavior. This skill applies Fowler's refactoring catalog to make targeted, safe improvements. It works in monoliths, modular codebases, and microservices alike.

Use this skill when:
- Code is hard to understand or modify
- You're preparing code for a new feature
- You've identified a code smell (duplication, long method, feature envy, data clump, etc.)

## Instructions

1. **Identify the smell first.** Before touching anything, name the specific code smell:
   - Long Method → Extract Method / Extract Function
   - Duplicate Code → Extract Function or Pull Up Method
   - Large Class → Extract Class or Extract Superclass
   - Feature Envy → Move Method
   - Data Clump → Introduce Parameter Object
   - Primitive Obsession → Replace Primitive with Object
   - Divergent Change / Shotgun Surgery → Move to cohesive module
   - Comments explaining *what* → Rename to make intent obvious

2. **Confirm tests exist before refactoring.** If no tests cover the code being changed, pause and write characterization tests first. Never refactor untested code at scale.

3. **Make the smallest possible change.** One refactoring at a time. Do not combine a refactoring with a behavior change in the same commit.

4. **Run tests after each step.** The test suite must stay green throughout. If it goes red, revert and try a smaller step.

5. **Use the two-hat rule.** When refactoring, wear only the "restructuring" hat. When adding features, wear only the "feature" hat. Never mix them in the same change.

6. **Commit atomically.** Each refactoring step is a separate commit with a message like:
   ```
   refactor: extract UserNotifier from OrderService
   ```

7. **For large-scale restructuring in a monolith**, use the Parallel Change (expand/contract) pattern:
   - Add the new structure alongside the old
   - Migrate callers incrementally
   - Remove the old structure once fully migrated

## Principles
- Source: [Refactoring — Martin Fowler](https://refactoring.com)
- Key idea: *"Refactoring is a disciplined technique for restructuring existing code, altering its internal structure without changing its external behavior."*
- The catalog lists 60+ named refactorings — always prefer a named refactoring over an ad-hoc change for clarity and reviewability.

## Output Format
When applying this skill, the agent should:
- Name the smell detected
- Name the refactoring being applied
- Show a before/after diff
- Confirm existing tests still pass (or note if they need to be written first)
- Suggest the commit message
