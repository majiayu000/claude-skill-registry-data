---
name: git-workflow
description: Perform requested Git actions while preserving user work. Triggers on "commit", "提交".
---

# Git Workflow and Versioning

## When to use

- Perform requested Git actions while preserving user work.

**Not for:** implement for code; shipping for production rollout.

## Steps

1. Inspect status, staged changes, branches and operation state; determine the authorized action.

2. Prepare coherent changes and relevant checks; stage explicit paths and commit only when requested.

3. Resolve conflicts by tracing both intents and verifying each coherent unit; do not reset or abort destructively without authority.

4. Report local state; every push requires explicit confirmation after the verified result is prepared.

## Verify

- Content matches authorization and checks; user history is preserved and local work does not imply push.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/block-dangerous-git.sh](references/block-dangerous-git.sh) — PreToolUse hook blocking force pushes, `reset --hard`, `clean -f`, `branch -D`, etc.
- [references/block-dangerous-git-setup.md](references/block-dangerous-git-setup.md) — settings.json wiring (project + global) for the block-dangerous-git hook
- [references/pre-commit-setup.md](references/pre-commit-setup.md) — Husky + lint-staged + Prettier pre-commit hook setup
- [references/git-debugging.md](references/git-debugging.md) — bisect/log/diff/blame commands for tracing regressions
- [references/versioning.md](references/versioning.md) — semver definitions, tag commands, changelog format
