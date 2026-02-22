---
name: esper:review
description: Code review on branch or PR diffs. Analyzes code quality — bugs, security, style, complexity — and offers to batch issues into /esper:fix plans.
---

You are reviewing code for quality before it ships.

The user's initial prompt (if any): $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Determine the current branch:
```bash
git branch --show-current
```

Determine the base branch (usually `main`). If the current branch IS main, tell the user: "You're on main — switch to a feature branch first or provide a PR number." and stop.

## Step 2: Gather diff

If `$ARGUMENTS` contains a PR number (e.g. `123` or `#123`):
```bash
gh pr diff <number>
```

Otherwise, get the branch diff against main:
```bash
git diff main...HEAD
```

If the diff is empty, tell the user: "No changes to review — the branch is up to date with main." and stop.

If the diff is very large (more than ~2000 lines), summarize by file first, then focus the detailed review on the most critical files.

## Step 3: Read context

Read `.esper/CONSTITUTION.md` for project principles.

Run `esperkit plan list --dir active --format json`. If there's an active plan, read the plan file for intent context — what the code is supposed to do and what the acceptance criteria are.

Run `esperkit config get current_phase` and read `.esper/phases/<current_phase>.md` for phase goals.

## Step 4: Review

Analyze the diff for issues across these categories:

**Bugs & Logic Errors**
- Incorrect conditions, off-by-one errors, null/undefined handling
- Race conditions, missing awaits, unhandled promises
- Logic that doesn't match the stated intent from the plan

**Security**
- Command injection, path traversal, XSS, SQL injection
- Hardcoded secrets or credentials
- Missing input validation at system boundaries

**Code Style & Consistency**
- Deviations from patterns established in the existing codebase
- Naming inconsistencies
- Violations of project principles from the constitution

**Edge Cases & Error Handling**
- Missing error handling for I/O operations
- Unhandled edge cases (empty inputs, missing files, network failures)
- Silent failures that should be loud (per constitution principle #5)

**Complexity & Dead Code**
- Unnecessary abstractions or over-engineering
- Dead code, unused imports, commented-out code
- Code that could be simplified

## Step 5: Report

Print a structured review report:

```
## Code Review: <branch name>

### Critical
- [file:line] <description of critical issue>

### Warnings
- [file:line] <description of warning>

### Notes
- [file:line] <suggestion or observation>

### Summary
<overall assessment — is this ready to ship?>
```

If no issues are found, print: "No issues found — this branch looks ready to ship. Run `/esper:ship` when ready."

## Step 6: Offer fixes

If actionable issues were found (critical or warnings), use `AskUserQuestion`:

"Found [N] actionable issues. Want to create `/esper:fix` plans for any of them?"

Options:
- **Yes — batch all into one fix plan**: creates a single `/esper:fix` covering all issues
- **Yes — one fix per issue**: creates a separate `/esper:fix` for each actionable issue
- **No — I'll handle them manually**: skip fix creation

If the user wants fixes, invoke `/esper:fix` for each selected issue with a pre-filled description including the file, line, and issue details.
