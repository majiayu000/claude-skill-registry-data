---
name: documentation-sync
description: Update documentation when implementation behavior, configuration, interfaces, or workflows change. Use after any user-visible or developer-facing behavior change.
---

# Documentation Sync

1. Identify which docs describe the changed behavior: README, usage guides, API references, examples, configuration, migration notes, or troubleshooting.
2. Compare each relevant statement with the actual implementation and tests.
3. Update only the documentation affected by the change. Keep unrelated docs untouched.
4. Prefer executable or testable examples. Verify commands, paths, flags, defaults, and version assumptions.
5. Remove stale instructions that would lead a user to an invalid state.
6. Add migration or compatibility notes for breaking behavior.
7. Check cross-links and generated documentation workflows.

Do not document planned behavior as shipped. Do not copy secrets, private endpoints, or machine-specific paths into public docs. If there is no meaningful documentation impact, state that you checked and why no edit was needed.
