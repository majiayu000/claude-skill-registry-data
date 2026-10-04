---
name: commit
description: Create git commits in Conventional Commits format. Use whenever committing changes or writing a commit message.
---

Write every commit in **Conventional Commits** format: `<type>(scope): <description>`, then an optional body and footer.

## Steps

1. **Read the diff.** Run `git status` and `git diff --staged` (fall back to `git diff` when nothing is staged).
2. **Classify.** Choose the `type` (`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`), the `scope` (the affected area, omitted when the change is broad), and a `description` — one imperative-mood line under 72 characters. Each of the three must trace to a specific change in the diff. If the diff holds more than one unrelated change, commit them separately.
3. **Compose.** Assemble the subject line. Add a body — the _why_, and what a reader can't see from the diff — when the change isn't self-evident, and a footer (`Closes: <id>`, `Refs: <id>`) when an issue applies. Signal a breaking change with `!` (`feat(api)!: require verified email`), or a `BREAKING CHANGE:` footer when the break needs explaining.
4. **Commit.** Stage the intended files — if they contain secrets or credentials, stop and flag it instead. Run `git commit` and let hooks run; if one fails, fix the cause or report it.

Rewriting shared history or bypassing checks — `--force`, `reset --hard`, `--no-verify`, `git config` edits — happens only when the user explicitly asks.
