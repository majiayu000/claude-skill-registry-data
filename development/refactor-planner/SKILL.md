---
name: refactor-planner
description: Use when asked to refactor, clean up, restructure or modernize code, split a large file or god class, remove duplication, migrate to a new pattern or library, or reduce technical debt without changing behavior.
---

# Refactor Planner

## Overview

Refactoring changes structure, never behavior. Lock behavior with tests first, move in small steps that each leave the code working, and keep every step reviewable and revertible.

## Method

1. **State the goal** in one sentence and why it pays off: "Split `orders.ts` (1,400 lines) so checkout and refunds can change independently."
2. **Map the code:** who calls the target (find usages), what it depends on, public contracts that must not change.
3. **Build the safety net.** Run existing tests. If the behavior being moved is not covered, add characterization tests that capture what it does today, including odd behavior.
4. **Plan small steps.** Each step is one known refactoring, keeps tests green, and is one commit:
   - Rename, extract function, extract module, move function, inline, introduce parameter object, replace conditional with polymorphism, extract interface at a boundary.
   - For migrations: add the new path beside the old one, move callers in batches, delete the old path last.
5. **Execute step by step:** change, run tests, commit. Never mix a refactor and a behavior change in one commit.
6. **Finish:** remove dead code, update docs, report.

## Output

Before changing code, deliver the plan:

```
Goal: <one sentence>
Safety net: <existing tests, tests to add>
Steps:
1. <refactoring> — <files> — risk: low/medium/high
2. ...
Out of scope: <tempting changes deliberately left out>
```

After executing: the list of commits and the test result after the last one.

## Smells and the refactoring that fixes them

| Smell | Refactoring |
|---|---|
| Long function doing several things | Extract function per responsibility |
| File or class with many unrelated reasons to change | Split by responsibility, move functions |
| Same logic in several places | Extract shared function; keep it where all callers can reach it |
| Long parameter lists | Introduce parameter object |
| `switch` on type repeated in many places | Polymorphism or a lookup table |
| Deep nesting | Guard clauses, early returns |
| Feature envy (code that mostly uses another module's data) | Move function to that module |

## Common mistakes

- Big-bang rewrite in one commit that nobody can review or revert.
- Refactoring without tests, then discovering behavior changed in production.
- "While I am here" behavior changes mixed into the refactor.
- Abstracting for imagined future needs; extract only what has two real callers.
- Renaming public APIs without a deprecation path for external users.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
