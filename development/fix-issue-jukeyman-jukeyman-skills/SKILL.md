---
name: fix-issue
description: Debug and fix GitHub issues with root cause analysis
argument-hint: <issue-url-or-description>
---

# Fix Issue Workflow

1. Read the issue description and reproduction steps
2. Search codebase for related files: grep, glob, file reads
3. Identify root cause — not just symptoms
4. Write a failing test that reproduces the bug
5. Implement the fix (minimal change)
6. Verify the test passes
7. Run full test suite to catch regressions
8. Commit with: fix: [description] (closes #N)
