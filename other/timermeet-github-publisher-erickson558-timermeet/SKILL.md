---
name: timermeet-github-publisher
description: Publish TimerMeet changes to GitHub (erickson558/timermeet, public) using the existing authenticated gh CLI account. Use when preparing commits, pushing to main, or tagging/releases for this project. Never store tokens in the repo.
---

# TimerMeet GitHub Publisher

## Overview

Publish TimerMeet safely with `git` and `gh`, using the `erickson558` GitHub account that is already authenticated on this machine and already owns the `timermeet` repository (public, Apache-2.0, default branch `main`).

## Workflow

1. Run `gh auth status` and confirm `erickson558` is the **active** account (this machine may have more than one `gh` account logged in -- check the `Active account: true` line, don't assume).
2. Run `git rev-parse --show-toplevel` and confirm it matches this repo's root -- unlike the historical EasyPHP `www` monorepo the legacy docs describe, this repository root already *is* the TimerMeet project root, so there is no "publish only a subfolder" decision to make anymore.
3. Review `git status --short` and `git diff --stat` before staging anything.
4. Stage only the intended files by name (never `git add -A`/`git add .` blindly) -- see `references/github-commands.md` for the exact do/don't list.
5. Use a clear, non-interactive, conventional commit message.
6. Push only after the diff has been reviewed.
7. Read `references/github-commands.md` for the exact command sequences (commit/tag/push/release).

## Guardrails

- Never write or echo the GitHub token into a file in this repo.
- Prefer the existing CLI authentication over any embedded credentials.
- Prefer non-interactive commands (no `git rebase -i`, no editor-opening commands).
- Never force-push `main`.
- Double-check `data/meetings.json`/`data/settings.json` (real personal data) are not staged -- they're gitignored, but verify with `git status` rather than trusting that blindly after any `.gitignore` edit.

## References

- `references/github-commands.md` -- exact command sequences for commit, tag, push, and GitHub Releases (including attaching `TimerMeet.exe`).
