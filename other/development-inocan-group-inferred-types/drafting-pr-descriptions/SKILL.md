---
name: drafting-pr-descriptions
description: Summarize code changes on the current git branch (including uncommitted changes) and draft a pull request description using a provided template. Use when the user wants a PR description based on git diffs, branch history, and local working tree changes.
---

# Pr Description Drafter

## Overview

Generate a PR description by inspecting the current branch, committed changes, and uncommitted diffs. Fill a fixed template and ask only for missing essentials like related issue or test details.

## Workflow

1. Identify repo and current branch.
2. Determine the base branch for comparison.
3. Collect committed and uncommitted change summaries.
4. Draft the PR description using the template.
5. Ask brief follow-up questions only when required fields are missing.

## Base Branch Selection

- Always ask which base branch to compare against.
- Prefer the remote base when available (e.g., `origin/main`) once the user specifies the branch name.

## Data Collection Commands

Use these commands to build the summary:
```
git rev-parse --show-toplevel
git branch --show-current
git status -sb
git log --oneline <base>..HEAD
git diff --stat <base>...HEAD
git diff --stat
git diff --stat --cached
```

## Drafting Rules

- Summarize committed changes from `<base>..HEAD`.
- Summarize uncommitted changes from working tree and index.
- Use concise bullet points and name the main areas/files.
- If a related issue is not provided, ask for it.
- If tests are not mentioned, ask what was run; if none, state "Not run (not requested)."
- For "What to review", highlight high-risk files or behaviors changed.

## PR Template

Use the exact template in `references/pr-template.md`.

## Output

Return only the completed PR description in the template, with no extra commentary. Format the output as Markdown that is ready to copy. When filling the template, omit the instructional blockquote lines starting with "> Please ..." from the output.
