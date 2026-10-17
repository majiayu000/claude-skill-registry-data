---
name: commit
description: Use when committing changes, staging files, saving work, or making a git commit. Creates clean commits in the repository's own convention (conventional commits, area prefix, tracker ID, or plain) with secret scanning (GitLeaks).
license: MIT
allowed-tools: Read Bash(git:*) Bash(gitleaks:*) Bash(trufflehog:*)
model: sonnet
effort: high
compatibility: Requires git and a secret scanner (GitLeaks default; TruffleHog accepted); detects the repository's commit convention from tooling, history, and ecosystem
metadata:
  short-description: Clean commits in your repo's own convention.
---

You create git commits with short, readable messages that match the repository's existing convention.

Load an ecosystem guide **only** when `rules/convention-detection.md` reaches Tier 3 and the manifest matches it: `references/go.md`, `references/swift.md`, `references/python.md`, `references/systems.md`.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Convention detection | HIGH | `rules/convention-detection.md` |
| Message format | HIGH | `rules/message-format.md` |
| Commit type selection | HIGH | `rules/commit-type.md` |
| Issue references | MEDIUM | `rules/issue-references.md` |
| Change scope | MEDIUM | `rules/change-scope.md` |

## Pre-Commit Security Check

Scan staged changes for secrets before every commit, using the project's secret scanner. GitLeaks is the default; TruffleHog is accepted if the project already uses it.

1. Run the scanner over staged changes after staging, piping the staged diff into its stdin mode — GitLeaks: `git diff --cached | gitleaks stdin --redact --verbose`; TruffleHog: `git diff --cached | trufflehog stdin --results=verified,unknown --fail` (include `unknown` so credentials TruffleHog cannot verify online still block the commit, matching GitLeaks). Piping keeps `git` a plain command, so worktree-isolated sessions accept it; `gitleaks git` and `trufflehog git` pass `git` as an operand and are refused there.
2. If the scanner reports a leak, **STOP** — do not commit. Report the finding and ask the user to remove the secret (and rotate it if it was ever pushed).
3. If no secret scanner is installed (command not found), do not install one implicitly. When the project's pre-commit hook runs a scanner, commit and let the hook scan. Otherwise tell the user no scanner is available, suggest installing one (`brew install gitleaks` or equivalent), and ask before committing unscanned.

Never edit `.husky/`, `commitlint`, or other project tooling as part of a commit. If pre-commit hooks are missing, report that and point the user to the `setup` skill instead of configuring it yourself.

## Workflow

A commit request stages and commits only — it must never pull, stash, restore stashes, or rewrite project tooling.

1. Show current `git status` and analyse all changes
2. Detect the repository's commit convention (see `rules/convention-detection.md`)
3. Check conversation context for issue references (see `rules/issue-references.md`)
4. Assess scope of changes (see `rules/change-scope.md`)
5. Stage only the explicit, related paths for this change — never blanket-stage unrelated modifications
6. Choose the commit type or leading verb from branch context, not the staged diff alone (see `rules/commit-type.md`)
7. Run the Pre-Commit Security Check above
8. Create the commit with a message following `rules/message-format.md`

When the convention came from Tier 3 or Tier 4 of detection — an ecosystem default or the plain fallback rather than enforced tooling or clear history — state which convention was used and why, so a wrong guess is visible.
