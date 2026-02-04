---
name: coderabbit-review
description: Perform code review using CodeRabbit. Must use this skill if instructed to perform a CodeRabbit review.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# CodeRabbit Review
This skill provides instructions on how to use CodeRabbit CLI for code reviews, and how to handle the feedback received.

## Instructions
1. Check authentication status with `coderabbit auth status`. If not logged in, prompt the user to log in using `coderabbit auth login`.
2. Determine whether to review uncommitted or committed code changes based on the git status.
3. Run the appropriate CodeRabbit command without sandbox:
   - For uncommitted changes: `coderabbit --plain --type uncommitted`
   - For committed changes: `coderabbit --plain --type committed`
4. When receiving the message "Review Completed", it indicates the review process is finished.
5. If there are no review comments from CodeRabbit, inform the user that no issues were found.
6. If there are review comments, address the issues as follows:
   - If the comment points out clear bugs, coding standard violations, security issues, or performance improvements, make the necessary changes immediately.
   - If the comment is overly strict, involves trade-offs, or requires significant architectural changes, ask the user for a decision before making any changes.
7. Report back to the user with a summary of the comments received from CodeRabbit and the actions taken for each comment.

## Note
- CodeRabbit reviews can take 5+ minutes. Please wait.
- You should communicate to the user in Japanese.
