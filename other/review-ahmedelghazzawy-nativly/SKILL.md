---
name: review
description: Review the current changes for bugs, security issues, design problems and missing tests before pushing, then fix what's found.
argument-hint: "[file or empty for the current branch diff]"
---

Review: $ARGUMENTS (if empty: uncommitted and untracked files plus unpushed commits, `git diff origin/main`).

1. Use the code-reviewer subagent on the change.
2. Verify each finding against the code; drop anything that doesn't hold up.
3. Report findings grouped 🔴 must fix (bugs, security, data loss) · 🟡 should fix (design,
   missing tests, types) · 🟢 nice (polish), each with file:line and why it matters.
4. Fix the 🔴 and 🟡 items, add tests for them, and re-run the checks. List 🟢 items for later.
