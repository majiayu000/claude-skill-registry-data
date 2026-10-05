---
name: fix-issue
description: "Fetches a GitHub issue by number, analyzes the requirements, finds the relevant code, implements a fix, and optionally creates a PR. Use when working through your issue backlog."
argument-hint: "[issue number]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Fix GitHub Issue

## Fetch Issue Details
!`gh issue view $1 2>/dev/null || echo "Usage: /fix-issue <issue-number> — requires gh CLI authenticated"`

---

## Workflow

### Step 1: Understand the Issue
1. Read the issue title, description, labels, and comments
2. Identify: Is this a **bug fix**, **feature request**, or **enhancement**?
3. Determine acceptance criteria — what does "done" look like?
4. Note any linked issues, PRs, or referenced files

### Step 2: Find Relevant Code
1. Search the codebase for files/functions mentioned in the issue
2. Trace the code path related to the reported behavior
3. If it's a bug: try to reproduce the conditions mentally by reading the code
4. Identify the minimal set of files that need to change

### Step 3: Create a Branch
```
git checkout -b fix/issue-<number>-<short-description>
```

### Step 4: Implement the Fix
1. Make the smallest change that addresses the issue
2. Follow existing code patterns and conventions
3. Add or update tests to cover the fix
4. Ensure no regressions in adjacent functionality

### Step 5: Verify
1. Run existing tests for the affected area
2. Run the new tests
3. Review your own diff: `git diff`
4. Check for unintended changes

### Step 6: Commit and PR
1. Stage changes: `git add <files>`
2. Commit with reference: `git commit -m "fix: <description> (#<issue-number>)"`
3. Push: `git push -u origin <branch>`
4. Create PR: `gh pr create --title "Fix #<number>: <title>" --body "Closes #<number>"`

---

## Rules
- Always reference the issue number in commits and PR
- Don't scope-creep — fix only what the issue describes
- If the issue is unclear, list your assumptions before implementing
- If the fix requires architectural changes, flag it and discuss before proceeding
