---
name: pr-review
description: Comprehensive pull request code review
argument-hint: <pr-number-or-branch>
---

# PR Review Protocol

1. Read the PR description and linked issue
2. Review diff file-by-file
3. Check for: security issues, performance problems, type safety,
   error handling, test coverage, accessibility, naming conventions
4. Flag any BANNED patterns (see CLAUDE.md design standards)
5. Rate: APPROVE / REQUEST_CHANGES / COMMENT
6. Provide specific, actionable feedback with line numbers
