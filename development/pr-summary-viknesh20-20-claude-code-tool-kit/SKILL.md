---
name: pr-summary
description: "Generates a well-structured pull request description from the current branch diff. Includes summary, changes list, test plan, and breaking changes. Use before opening a PR."
argument-hint: "[base branch, default: main]"
allowed-tools: Read, Bash(git *), Bash(gh *)
---

# Generate PR Summary

## Branch Context
!`git branch --show-current 2>/dev/null`
!`git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline 2>/dev/null`

## Diff Summary
!`git diff main...HEAD --stat 2>/dev/null || git diff master...HEAD --stat 2>/dev/null`

## Full Diff
!`git diff main...HEAD 2>/dev/null | head -800 || git diff master...HEAD 2>/dev/null | head -800`

---

## Instructions

### Step 1: Analyze All Commits
Read every commit message and the full diff. Understand:
- What feature, fix, or change was implemented
- Why it was needed (from commit messages and code context)
- What files were touched and what changed in each

### Step 2: Generate PR Description

Use this format:

```markdown
## Summary
<!-- 1-3 sentences explaining what this PR does and why -->

## Changes
<!-- Bulleted list of specific changes, grouped by area -->

### [Area 1]
- Change description

### [Area 2]
- Change description

## Test Plan
- [ ] Test case 1
- [ ] Test case 2
- [ ] Edge case verification

## Breaking Changes
<!-- List any breaking changes, or "None" -->

## Notes for Reviewers
<!-- Anything reviewers should pay special attention to -->
```

### Step 3: Determine PR Title
- Format: `type: concise description` (under 72 chars)
- Types: feat, fix, refactor, docs, test, chore, perf
- Example: `feat: add user authentication with JWT refresh tokens`

## Rules
- Read ALL commits, not just the latest
- Don't embellish — describe what actually changed
- Flag any TODOs or known issues honestly
- Include breaking changes prominently
