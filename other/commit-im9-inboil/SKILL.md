---
name: commit
description: Generate a commit message and create the commit in one step.
allowed-tools: Bash(git diff *), Bash(git status *), Bash(git log *), Bash(git add *), Bash(git commit *)
---

# Commit

Analyze current changes, generate a commit message, stage relevant files, and commit.

## Process

1. Run `git diff` (unstaged) and `git diff --cached` (staged) to see all changes.
2. Run `git status -u` to see untracked files.
3. Run `git log --oneline -5` to match the repository's commit style.
4. Analyze all changes and draft a commit message.
5. Stage relevant files (`git add` — prefer specific files over `-A`).
6. Create the commit.

## Commit Message Format

- First line: `type: short summary` (under 72 chars)
  - Types: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`
- Blank line, then bullet-point details for non-trivial changes
- End with `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`
- If changes span multiple concerns (e.g. a bug fix AND a feature), use multiple `type:` paragraphs in the body
- Write in English (per CLAUDE.md conventions)
- Pass the message via HEREDOC for proper formatting

## Safety

- Never stage files that may contain secrets (.env, credentials, etc.)
- Never use `git add -A` — always add specific files
- Never push to remote — only commit locally
