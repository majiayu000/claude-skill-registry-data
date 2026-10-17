---
name: aiwf-avoid-ai-pushes
description: Use before committing, pushing, or publishing AIWF and related project changes to verify intended scope, preserve user and local-only files, inspect ignored and tracked state, avoid broad staging, validate public prose, confirm remotes and branches, and report an exact release receipt.
---

# AIWF Avoid AI Pushes

## Core Rule

Publish only the files Shawn intended, from the verified repo and branch, after inspecting staged content and relevant validation. Ignore status is evidence, not permission to delete or untrack a file.

## Workflow

1. Verify the real git root, current branch, requested destination, and whether the user authorized commit, push, release, or only a review.
2. Inspect before staging:

```powershell
git status --short --branch --untracked-files=all
git diff --stat
git diff --check
git remote -v
```

3. For uncertain files, inspect both ignore and tracked state:

```powershell
git check-ignore -v --no-index <path>
git ls-files -- <path>
```

4. Stage explicit paths. Use broad staging only when Shawn explicitly confirms the whole worktree is in scope.
5. Inspect `git diff --cached --stat`, `git diff --cached --check`, and the staged patch before committing.
6. Run the narrow tests or validators required by the changed files.
7. Confirm branch and remote immediately before push, then report commit hash and pushed ref.

## Guardrails

- Do not assume `AGENTS.md`, plans, receipts, models, outputs, logs, caches, or local configuration are ignored or publishable. Check the live repo.
- Do not delete, untrack, force-add, or rewrite ignored/tracked state unless Shawn explicitly asks and the exact path is verified.
- Do not use destructive git commands or rewrite history as cleanup.
- Do not stage unrelated user changes.
- Keep secrets, credentials, private datasets, customer data, machine paths, generated archives, and local caches out of public commits.
- For README, release notes, UI copy, commit messages, and PR text, remove unsupported claims, fake metrics, placeholder text, and repetitive AI-style filler without rewriting quoted source material.
- Do not claim a push succeeded without the command result or remote receipt.

## Output

Report the repo, branch, remote, staged files, validation commands, commit hash, pushed ref, and anything intentionally left local. For review-only requests, report findings without staging or publishing.
