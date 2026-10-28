---
name: commit-staged
description: Commit staged changes
---

Review the staged changes and understand the nature of it.
Commit staged changes with a message following the Conventional Commits format required by Release Please.

Message format: `<type>(<optional scope>): <short description>`

Types that trigger a version bump:
- `feat:` — new feature (minor bump)
- `fix:` — bug fix (patch bump)
- `feat!:` or `fix!:` or any type with `BREAKING CHANGE:` in footer — breaking change (major bump)

Types that do NOT trigger a version bump (use freely):
- `chore:` — maintenance, dependencies, tooling
- `ci:` — CI/CD changes
- `docs:` — documentation
- `refactor:` — code restructure without behaviour change
- `test:` — tests
- `style:` — formatting

Keep the description short and to the point. No need to iterate every detail from the change.
Do not add the line: "Co-Authored-By: Claude Sonnet 4.6"
