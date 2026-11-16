---
name: kit-commit
description: Create git commits with messages that follow the repository's existing conventions, committing only the intended changes. Use when the user asks to commit, make a commit, or write a commit message for current changes. Do not use for pushing, opening pull or merge requests, rewriting history, or reviewing code.
---

# Commit

Commit only when the user asked for a commit. Never push, amend published commits, or rewrite history unless the user explicitly asks.

## 1. Inspect the changes

- Run `git status` and `git diff` (staged and unstaged). Read the changes; do not commit what you have not looked at.
- If the user named what to commit, commit only that. Otherwise determine whether the changes form one logical change. If they mix unrelated work, ask whether to split them or propose separate commits.
- Never stage secrets, credentials, `.env` files, large generated artifacts, or files that `.gitignore` should cover. Stop and tell the user if any are part of the changes.

## 2. Match the repository's message convention

- Read recent history (`git log --oneline -20` and one or two full messages) and follow what it uses: Conventional Commits (`type(scope): subject`), ticket prefixes, capitalization, tense, line length, and trailers such as `Signed-off-by`.
- Check for documented rules in `CONTRIBUTING.md`, commitlint configuration, or commit hooks.
- If there is no convention, write a concise imperative subject of at most 72 characters, a blank line, and a body explaining what changed and why. Skip the body for trivial changes.
- Describe the change accurately. Do not claim tests passed unless they ran.

## 3. Commit

- Stage the intended paths explicitly (`git add <paths>`), not everything by default.
- Respect hooks. If a pre-commit hook fails, fix the reported problem when it is within the change, or report it. Never bypass hooks with `--no-verify` unless the user asks.
- Do not change git configuration or author identity.

## 4. Report

Show the commit hash and subject, list what was committed, and mention anything intentionally left uncommitted.

## Examples

- Use: "Commit these changes." "Write a commit message for what I staged."
- Skip: "Push my branch." "Open a PR." "Squash the last three commits." (history rewrite needs explicit instructions)
