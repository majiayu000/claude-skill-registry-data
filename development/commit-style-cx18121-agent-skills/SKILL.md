---
name: commit-style
description: Mandatory when writing, amending, squashing, or proposing a commit subject or pull request title.
---

# Commit style

Inspect the actual change before naming it.

Use `<type>(<scope>): <summary>`. The scope is optional and names a stable lowercase subsystem. Omit it for broad changes.

Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`.

Write a lowercase imperative summary with no ending period. Describe the outcome, not the files.

Commit bodies are opt-in. Write one only when the user explicitly requests it. Otherwise use the subject alone.

Use the same format for pull request titles.

Explicit instructions and documented repository requirements override this default.
