---
name: code-review
description: Review code files for quality, patterns, and best practices. Auto-detects TypeScript or Python and applies the appropriate checklist. Produces findings with severity levels.
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

## Prime Directive

**"Find problems the author cannot see."**

Review code with fresh eyes. Check for correctness, patterns, security, and maintainability. Be specific in findings - cite exact lines and provide actionable recommendations.

## Arguments

Accepts file paths, directory paths, or PR references. Auto-detects file type.

## Process

### Step 1: Read Files

Read all files to be reviewed. If a directory is provided, glob for relevant source files (.ts, .tsx, .py).

### Step 2: Detect Language

For each file, detect the language:
- `.ts`, `.tsx` -> TypeScript / React (use frontend checklist)
- `.py` -> Python / FastAPI (use backend checklist)
- Mixed -> apply both checklists to respective files

### Step 3: Load Appropriate Checklist

Load the checklist from references:
- `references/frontend-checklist.md` for TypeScript/React files
- `references/backend-checklist.md` for Python/FastAPI files

### Step 4: Review Each File

For each file, systematically check every item on the appropriate checklist. Note findings with:
- **Severity**: Critical / Major / Minor
- **Location**: File path and line number (or line range)
- **Finding**: What the issue is
- **Recommendation**: How to fix it

### Step 5: Produce Output

Output the review in the following format:

```markdown
# Code Review

## Files Reviewed
- `path/to/file1.ts` (TypeScript)
- `path/to/file2.py` (Python)

## Critical Findings
1. **[CRITICAL]** `file.py:42` - <finding>
   **Recommendation:** <how to fix>

## Major Findings
1. **[MAJOR]** `file.ts:15-20` - <finding>
   **Recommendation:** <how to fix>

## Minor Findings
1. **[MINOR]** `file.py:88` - <finding>
   **Recommendation:** <how to fix>

## Positives
1. Good use of async/await in all route handlers
2. Proper error boundaries around data fetching components
3. Consistent naming conventions throughout

## Summary
- Critical: N findings
- Major: N findings
- Minor: N findings
- Verdict: APPROVE / APPROVE_WITH_CHANGES / REQUEST_CHANGES
```

## Severity Definitions

- **Critical**: Security vulnerability, data corruption risk, production crash. Must fix before merge.
- **Major**: Bug, performance issue, missing error handling, pattern violation. Should fix before merge.
- **Minor**: Style issue, naming inconsistency, missing documentation. Can fix in follow-up.

## Reference Files

- `references/frontend-checklist.md` - React 19 / TypeScript / Next.js 15 review checklist
- `references/backend-checklist.md` - FastAPI / Python review checklist
