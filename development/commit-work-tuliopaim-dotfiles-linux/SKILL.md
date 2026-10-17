---
name: commit-work
description: Use when asked to analyze completed work and create one or more git commits while excluding unrelated files, docs-only noise, and secrets.
---

# Commit Work

Create clean, intentional commits from the current working tree.

## Workflow

1. Inspect repository state before touching git history:
   - `git status --short`
   - `git diff --stat`
   - `git diff`
   - `git diff --staged`
   - `git log --oneline -10`
2. Extract ticket prefix from current branch name, if present:
   - Run `git branch --show-current` to get the branch name
   - Recognize both keyed tickets (e.g., `PROJ-123`, `FEAT-42`) and standalone numeric ticket IDs of any length (e.g., `1234567`)
   - Infer numeric tickets from branch context such as `feature/1234567-description`; do not mistake dates, versions, or unrelated numbers for tickets
   - If a ticket is identified, prefix all commit messages with `TICKET: description`; if ambiguous, ask before committing
   - If no ticket is present, fall back to conventional commits (step 8)
3. Identify the actual work done and group changes by intent.
4. Exclude unrelated files by default, especially:
   - incidental docs or notes unless requested or directly tied to the code change
   - editor/OS artifacts
   - generated noise that is not required for the change
   - unrelated local modifications
5. Refuse or stop if a change appears to include secrets, credentials, private keys, tokens, or unintended personal data.
6. Stage only files/hunks that belong to the current commit group.
7. Create one commit per coherent intent when multiple unrelated intents exist.
8. Commit message format:
   - **With ticket prefix** (from step 2): `TICKET: description` (e.g., `PROJ-123: add user login endpoint` or `1234567: add user login endpoint`)
   - **Without ticket prefix**: use conventional commits:
     - `feat(scope): summary`
     - `fix(scope): summary`
     - `refactor(scope): summary`
     - `test(scope): summary`
     - `chore(scope): summary`
9. After committing, report:
   - commit SHA(s) and message(s)
   - intentionally uncommitted files, if any
   - anything skipped due to uncertainty

## Rules

- Do not amend existing commits unless explicitly requested.
- Do not force push.
- Do not stage all changes blindly with `git add .` unless every changed file was inspected and belongs in the same commit.
- Prefer path-specific staging. Use hunk staging when only part of a file belongs.
- If the working tree contains unrelated changes and separation is unclear, ask before committing.
- If tests or checks are obvious and cheap, run them before committing; otherwise mention they were not run.
- Keep commit bodies short and only include them when they add useful context.
