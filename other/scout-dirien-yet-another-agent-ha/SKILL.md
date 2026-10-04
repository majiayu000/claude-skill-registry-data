---
name: scout
description: >
  Scout Rule — identify the top 3 highest-impact improvement
  opportunities in files you're already touching. Analyzes entire file
  content, not just changed lines. Focuses on pre-existing code quality,
  not PR bugs. Use when preparing a PR, during code review, or after
  completing a feature.
compatibility: >
  Requires git. Works with any project that has a diff to analyze.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Scout Rule

> "Leave the code better than you found it."

Identify the **top 3 highest-impact, lowest-risk** improvement
opportunities in files touched by a diff. Reads entire file content,
not just changed lines. Focuses on pre-existing code quality — things
the next developer will thank you for fixing.

## Prerequisite check

```bash
git --version 2>/dev/null && git rev-parse --is-inside-work-tree 2>/dev/null
```

If `git` is not installed or the working directory is not a git
repository, stop and report the issue. Do **not** proceed.

## Detect changed files

Determine which files to analyze based on input.

### Default — working tree vs base branch

```bash
# Detect base branch
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \
  | sed 's@^refs/remotes/origin/@@' || echo "main")

# Combine committed + uncommitted + staged changes vs base
{ git diff --name-only ${BASE_BRANCH}...HEAD 2>/dev/null; \
  git diff --name-only; \
  git diff --name-only --cached; } | sort -u
```

If all sources return empty, report that there are no changed files
to analyze.

### Specific branch

If the user specifies a target branch to analyze, detect the base
branch the same way as the default mode, then diff:

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \
  | sed 's@^refs/remotes/origin/@@' || echo "main")
git diff --name-only ${BASE_BRANCH}...${BRANCH}
```

### Specific files

If given an explicit list of file paths rather than a branch name,
use those directly without running git diff.

## Scope

Read the **full content** of each changed file, not just diff hunks.
Look for improvements in the entire file.

**Do not:**

- Find bugs in PR changes (that's a code reviewer's job)
- Suggest architectural redesigns
- Flag style preferences not established in the codebase
- Propose changes requiring new dependencies

## Categories

### `dead-code`

Unused functions, variables, imports, or types. Commented-out code
blocks. Unreachable branches. Stale TODO/FIXME comments referencing
completed work.

### `naming`

Misleading names that don't match current behavior (code evolved,
name didn't). Inconsistent patterns within the same file (e.g.,
`getUserID` vs `fetchUserId`). Single-letter variables in
non-trivial scope (beyond simple loop counters). Abbreviations
that hurt readability when the full word is short.

### `magic-values`

Hardcoded numbers or strings that should be named constants.
Repeated literal values that represent the same concept.
Timeout/limit values embedded in logic without explanation.

### `deprecated-patterns`

Old APIs when newer alternatives exist in the same codebase.
Patterns that the project has moved away from (check other recent
files for the modern approach). Legacy error handling when the
project now uses a different convention.

### `simplification`

Overly complex logic that can be expressed more directly.
Unnecessary indirection (wrapper functions that add no value).
Redundant nil/error checks where the invariant is already
guaranteed. Nested conditionals that can be flattened with early
returns.

## Scoring

Score each opportunity on two dimensions (1-5 each):

- **Impact**: How much does fixing this help the next developer?
  - 5 = Prevents real confusion or bugs
  - 3 = Noticeable improvement to readability
  - 1 = Minor polish
- **Low-Risk**: How safe is this change?
  - 5 = Pure cleanup, zero behavior change possible
  - 3 = Safe but touches logic paths
  - 1 = Could change behavior if not careful

**Composite score** = Impact × Low-Risk. Return only the **top 3**.

## Output format

Present a summary table followed by per-suggestion details:

| # | File:Line | Category | Description | Effort | Score |
| - | --------- | -------- | ----------- | ------ | ----- |
| 1 | location | category | description | effort | I×R=S |
| 2 | location | category | description | effort | I×R=S |
| 3 | location | category | description | effort | I×R=S |

For each suggestion, include:

- **Category** and **Effort** (trivial / small / medium)
- **Why this matters** — one sentence explaining value to the next
  developer
- **Suggested change** — concrete code snippet or diff showing the
  improvement

If no improvement opportunities are found, report:

> No significant improvement opportunities found. The touched files
> are in good shape.

## Anti-patterns — do not suggest

- Refactoring entire files or modules
- Changing public API signatures
- Style preferences not established in the codebase
- Anything requiring new dependencies or architectural decisions
- Changes that would touch more than ~20 lines
- Issues a linter would catch
