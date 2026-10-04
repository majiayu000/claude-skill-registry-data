---
name: full-refactor-cycle
description: Identify debt, fix it, verify quality improved
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# Full Refactor Cycle

Chain: quality-debt → refactor (appropriate type) → feature-test → quality-coverage → feature-review

## Process

1. Assess technical debt: identify worst areas
2. Propose refactoring plan: what to change, in what order
3. Get user approval
4. Execute refactoring
5. Run tests, verify nothing broke
6. Measure coverage improvement
7. Self-review the changes