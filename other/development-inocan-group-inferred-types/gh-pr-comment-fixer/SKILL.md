---
name: gh-pr-comment-fixer
description: "Fix GitHub PR review comments using the gh CLI: fetch review threads, implement requested changes, run the full test suite, commit and push fixes, then resolve the review threads. Use when asked to address PR comments or review feedback on the current branch."
---

# Gh Pr Comment Fixer

## Overview

Use the gh CLI to retrieve PR review comments for the current branch, apply fixes, verify with
the full test suite, and resolve the review threads after pushing.

## Workflow

1. Identify the PR for the current branch.
   - Prefer `gh pr view --json number,headRefName` and confirm it matches the branch.

2. Retrieve review threads and comments.
   - Use `gh pr view --json reviewThreads` and `gh pr view --json comments`.
   - Summarize the requested changes and note any questions or ambiguities.

3. Evaluate each comment.
   - Decide if it is reasonable, needs clarification, or should be declined.
   - If clarification is needed, ask before changing code.

4. Implement fixes.
   - Make minimal, targeted edits.
   - Add or update tests if the change warrants it.
   - Keep commit scope aligned with a single comment or logical group.

5. Run the full test suite.
   - Use the repo standard test command unless instructed otherwise.
   - Report failures and decide whether to continue or request input.

6. Commit and push fixes.
   - Use a conventional commit message.
   - Mention which comments were addressed.

7. Resolve review threads.
   - Use `gh pr review --comment` for replies and `gh api` or `gh pr review` to resolve threads.
   - Resolve only after the fix is pushed.

## Notes

- Prefer `gh pr view` and `gh pr diff` over manual web browsing.
- If no PR exists for the current branch, ask the user to open one or provide a PR number.
