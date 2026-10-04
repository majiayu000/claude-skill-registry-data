---
name: timermeet-github-publisher
description: Publish TimerMeet changes to GitHub using the existing authenticated gh CLI account. Use when preparing commits, creating a GitHub repository, pushing to main, or tagging/releases for this project. Never store tokens in the repo, and detect whether only the timermeet folder or the wider monorepo should be published.
---

# TimerMeet GitHub Publisher

## Overview

Publish `TimerMeet` safely with `git` and `gh`. Treat repository scope as the first decision, because this project currently lives inside a larger Git root.

## Workflow

1. Run `gh auth status` and confirm the active GitHub account is the intended one.
2. Run `git rev-parse --show-toplevel`.
3. If the Git root is wider than `monitoreos/timermeet`, stop and decide between:
- committing inside the existing monorepo
- publishing only the `timermeet` folder as a standalone repository
4. Review `git status --short` and `git diff --stat` before staging.
5. Stage only the intended files.
6. Use a clear, non-interactive commit message.
7. Push only after the repo scope is explicit.
8. Read `references/github-commands.md` for exact commands.

## Guardrails

- Never write or echo the GitHub token into a file in this repo.
- Prefer existing CLI authentication over embedded credentials.
- Prefer non-interactive commands.
- Do not push sibling projects by accident from the `www` monorepo root.

## References

- Read `references/github-commands.md` for the safe command sequences.
