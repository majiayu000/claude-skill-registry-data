---
name: gh-current-issue
description: Determine the GitHub issue number by parsing the current git branch name that starts with digits (e.g., 38-migrate...). Use when you need the issue number for comments, status updates, or automation.
---

# Get Current Issue Number

## Overview

Derive a GitHub issue number from the current branch name, assuming the branch begins with the issue number.

## Workflow

1. Read the current branch name and extract the leading issue number.
2. Return the issue number for later automation (comments, status updates).

## Quick Start

Run the script from any directory in the repo and show the full output:

```bash
.codex/skills/gh-current-issue/scripts/issue_from_branch.sh
```

## Notes

- Expected branch pattern: `^<digits>-.+` (e.g., `38-migrating-code-to-pwa`).
- If the branch does not start with digits, ask the user to confirm the issue number or rename the branch.
