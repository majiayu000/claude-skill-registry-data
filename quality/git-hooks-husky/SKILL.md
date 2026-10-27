---
name: git-hooks-husky
description: "Git hooks automation with Husky and lint-staged, pre-commit validation, and commit-msg linting."
---

# Git Hooks & Husky Protocol

1. Run lint-staged on pre-commit to only lint files modified in the commit.
2. Validate commit messages with commitlint on commit-msg hook.
3. Keep hooks fast (< 2 seconds) to avoid developer friction.
