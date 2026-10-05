---
name: commit
description: Create a conventional commit with a well-formed message. Use when ready to commit changes.
disable-model-invocation: true
---

# Commit Changes

1. Run `git diff --staged` to see what's staged
2. If nothing staged, run `git add -p` for interactive staging
3. Write a Conventional Commits message: `type(scope): description`
4. Include WHY in the body if the change is non-obvious
5. Run `git commit -m "..."` or open editor for long messages

Valid types: feat fix docs style refactor test chore perf ci

Arguments: $ARGUMENTS — optional scope or context hint
