---
name: pull-request-msg-with-gh
description: >
  Generate a PR_MESSAGE.md file from session context using GitHub CLI.
  Detects related issues via branch-keyword search, writes a structured
  PR description with commit subject, summary, test plan, and changelog.
  Validates with commitlint and markdownlint. Use when preparing a pull
  request on GitHub.
compatibility: >
  Requires GitHub CLI (gh) authenticated with the target repository.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Pull Request Message Generator

Generate a `PR_MESSAGE.md` file summarizing the current session's work.
Requires `gh` CLI authenticated with the target repository.

## Prerequisite check

```bash
gh --version 2>/dev/null && gh auth status 2>/dev/null
```

If `gh` is not installed, stop and report:

- Install from <https://cli.github.com>
- `gh` cannot be installed via npm
- After install, run `gh auth login` to authenticate

Do **not** proceed without a working, authenticated `gh` CLI.

## Workflow

1. **Analyze session context** — review changes made in the current
   session. Explore changed files with `git diff` and `git status` to
   understand the full scope of work, in addition to reviewing
   conversation history. Both sources inform the PR message.
2. **Detect issue number** — use the issue detection algorithm below.
   If the user indicates there is no associated issue, omit the
   `Closes #<issue-number>` footer entirely.
3. **Determine commit type** — based on the nature of changes (see
   `references/pr-message-format.md` for the list of types)
4. **Write PR_MESSAGE.md** — using the format in
   `references/pr-message-format.md`
5. **Add to .gitignore** — add `PR_MESSAGE.md` if not already present
6. **Validate** — run commitlint and markdownlint checks

## Issue number detection

The issue number MUST be determined by searching GitHub, NOT by
extracting numbers from branch names.

### Algorithm

```bash
# Step 1: Get branch name
BRANCH=$(git branch --show-current)

# Step 2: Extract keywords (strip leading numbers and hyphens)
# Example: "125-greenops-equivalencies" → "greenops equivalencies"
KEYWORDS=$(echo "$BRANCH" | sed 's/^[0-9]*-//' | tr '-' ' ')

# Step 3: Search GitHub issues
gh issue list --search "$KEYWORDS" --state all \
  --json number,title --limit 5
```

### Evaluation rules

1. **Exactly 1 result** with title containing most keywords → use it
2. **0 results** → ask the user for the issue number
3. **2+ results** → show options and ask the user to pick
4. **Ambiguous match** → ask the user to confirm

### Never extract issue numbers from

- Branch name digits (e.g., `125-` is NOT issue #125)
- Spec folder names (e.g., `specs/125-xyz/`)
- Worktree folder names

These are internal identifiers, not GitHub issue numbers.

## Critical rules

1. **No redundancy** — summary must add context beyond the commit subject
2. **No `## Commit Message` section** — the first line IS the commit
   message
3. **Never modify `.markdownlint.json`** — use CLI flags instead
4. **Trailing newline** — file must end with a single newline
5. **Ask when ambiguous** — if issue search returns 0, 2+, or unclear
   results, ask the user

## Validation

If the **commitlint** and **markdownlint** skills are available in the
current context, use them to validate PR_MESSAGE.md. Otherwise, run
directly:

```bash
# Validate commit message format
cat PR_MESSAGE.md | npx commitlint

# Validate markdown (MD041 disabled — first line is commit subject,
# not heading)
npx markdownlint --disable MD041 -- PR_MESSAGE.md
```

If neither the skills nor `npx` are available, fail hard:

- Install commitlint: `npm install -g @commitlint/cli
  @commitlint/config-conventional`
- Install markdownlint: `npm install -g markdownlint-cli`

Do **not** silently skip validation.

Fix any issues and re-validate before reporting success.
