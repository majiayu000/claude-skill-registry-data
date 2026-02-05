---
name: fetch-pr-review-comments
description: MUST use this skill when user asks to check/review PR comments, address reviewer feedback, fix review issues, or respond to code review. Fetches unresolved review comments from GitHub PR for the current branch.
---

# Fetch PR Review Comments

Fetches unresolved review comments from the GitHub pull request corresponding to the current branch.
You should use the bundled script to do this.

## Instructions

1. Run the script: `bash ~/.claude/skills/fetch-pr-review-comments/get_unresolved_review_comments.sh`
2. Report the fetched unresolved review comments in a clear format. Do not use table format.
3. **STOP HERE** - Do not proceed to fix or address the comments yet.
4. Wait for user to explicitly request fixes.

## Important Notes

- Requires `gh` CLI to be authenticated
- Only works when on a branch that has an associated pull request
- After reporting the comments, STOP and WAIT for user instructions. DO NOT:
  - Create todo lists for fixing the comments
  - Read or edit the mentioned files
  - Start implementing any fixes
