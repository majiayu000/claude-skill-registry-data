---
name: development-workflow-standards
description: Development process rules for this project including testing, branching, and commit standards. Use when implementing features, fixing bugs, or making any code changes.
---

# Development Workflow Standards

Refer to [development-workflow-standards.md](development-workflow-standards.md) for detailed rules.

## Key Rules

- **Testing with code changes**: Always update or add tests. Code without tests is incomplete.
- **TDD for bug fixes**: Write a failing test first, then implement the fix.
- **GitHub-Flow**: Always `git fetch origin` then branch from `origin/main`.
- **Conflict assessment**: Before PR, check conflicts with latest main. If severe, propose re-implementation.
- **Never merge PRs**: Merging is always the user's decision.
- **Verification**: Run `bun run test` and `bun run typecheck` before completing changes.
