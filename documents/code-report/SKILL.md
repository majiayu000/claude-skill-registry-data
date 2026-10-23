---
name: code-report
description: 'Generates implementation reports from executed parallel plans. Use when documenting completed work, listing changed files, or recording test guidance.'
argument-hint: '[feature-name] [--dry-run]'
---

# Code Report Generator

Generate structured implementation reports documenting changes made during plan execution. This is an **optional Step 4** in the planning workflow, providing comprehensive documentation of what was implemented.

**Operational context:** After implement-plan, write docs/plans/[feature-name]/report.md with an overview, changed files, implemented features, and test guidance; report generation is optional.

## Workflow Integration

This skill is the optional final step of the planning workflow. It requires `parallel-plan.md` to exist.

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ shared-context  │ ──▶ │  parallel-plan  │ ──▶ │ implement-plan  │ ──▶ │   code-report   │
│  (Step 1)       │     │  (Step 2)       │     │   (Step 3)      │     │ (Step 4 - Opt)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
     Creates:                Creates:               Executes:               Creates:
     shared.md              parallel-plan.md      parallel-plan.md        report.md
```

**If parallel-plan.md doesn't exist**, this feature was not planned using the workflow. The report can still be generated but will have limited context.

## Arguments

**Target**: `$ARGUMENTS`

Parse arguments:

- **feature-name**: The name of the feature to report on (matches directory name in `docs/plans/`)
- **--dry-run**: Show what would be created without making changes

If no feature name provided, abort with usage instructions:

```
Usage: /code-report [feature-name] [--dry-run]

Examples:
  /code-report user-authentication
  /code-report payment-integration --dry-run
```

**Questions:** class `clarify` (prerequisite failure "proceed anyway?", changed-file list request): headless (no question tool or chat turn), print the error or the missing input and stop; write no report. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

---

## Phase 0: Prerequisites Check

### Step 1: Validate Prerequisites

Extract the feature name from `$ARGUMENTS` (first non-flag argument).

Run the prerequisites check script in Step 1, before reading planning documents:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/code-report/scripts/check-prerequisites.sh [feature-name]
```

If the script exits with error:

- Display the error message
- Note that the report can still be generated but with limited context
- Ask user if they want to proceed anyway

### Step 2: Verify Planning Documents

Confirm which files exist in `docs/plans/[feature-name]/`:

- `parallel-plan.md` (strongly recommended)
- `shared.md` (optional but helpful)
- Any other planning documents

---

## Phase 1: Gather Context

### Step 3: Read Planning Documents

If they exist, read in this order:

1. `docs/plans/[feature-name]/parallel-plan.md` - The implementation plan
2. `docs/plans/[feature-name]/shared.md` - Architecture context
3. Any other `.md` files in `docs/plans/[feature-name]/`

### Step 4: Identify Changed Files

Use one of these methods to identify what changed:

**Method 1: Git diff (if working in git repo)**

```bash
git diff --name-status HEAD
```

**Method 2: From parallel-plan.md**

Extract all files from:

- "Files to Create" sections
- "Files to Modify" sections

**Method 3: Ask user**

If neither method works, ask user to list the files that changed.

### Step 5: Read Changed Files

Read a representative sample of changed files to understand:

- What features were implemented
- How the implementation works
- Any notable patterns or approaches used

Don't read every file - focus on key files that demonstrate the changes.

---

## Phase 2: Generate Report

### Step 6: Check for Dry Run Mode

If `--dry-run` is present in `$ARGUMENTS`:

Display:

```markdown
# Dry Run: Code Report for [feature-name]

## Report Location

docs/plans/[feature-name]/report.md

## Report Structure

- Overview: 2-4 sentence summary
- Files Changed: List with descriptions
- New Features: Feature list with descriptions
- Additional Notes: Important information and concerns
- E2E Tests To Perform: Testing guidance for QA

## Context Available

- parallel-plan.md: [found/not found]
- shared.md: [found/not found]
- Git changes: [available/not available]

## Next Steps

Remove --dry-run flag to generate the report.
```

**STOP HERE** - do not write files.

### Step 7: Load Report Template

Read the report template:

```bash
cat ${CLAUDE_PLUGIN_ROOT}/skills/code-report/templates/report-structure.md
```

### Step 8: Generate Report Content

Create `docs/plans/[feature-name]/report.md` with the following sections:

#### Frontmatter

```yaml
---
title: [Feature Name] Implementation Report
date: [current date in mm/dd/yyyy format]
original-plan: docs/plans/[feature-name]/parallel-plan.md
---
```

#### Overview Section

Write 2-4 sentences providing:

- What was implemented
- High-level approach taken
- Key architectural decisions made

Keep it information-dense and focused on the "what" and "why".

#### Files Changed Section

List all files that were created or modified, grouped by type:

```markdown
## Files Changed

### Created

- `/path/to/new/file.ext`: Brief description of what this file does

### Modified

- `/path/to/existing/file.ext`: Brief description of changes made
```

#### New Features Section

List each feature with:

- **Short descriptive name**
- One-sentence description of the feature and how it works

Include all features, both new and changed.

```markdown
## New Features

**Feature Name**: Brief description of what it does and how it works.

**Another Feature**: Description with implementation approach.
```

#### Additional Notes Section

Include:

- Important implementation details
- Concerns or technical debt
- Dependencies added
- Configuration changes required
- Migration steps if needed
- Performance considerations

Be thorough but concise. Only include information that's important for someone maintaining this code.

#### E2E Tests Section

Provide specific testing guidance:

- What functionality to test
- How to test it (step-by-step)
- Expected results
- Edge cases to verify

Write this for QA so they know exactly what to test.

```markdown
## E2E Tests To Perform

### Test 1: [Test Name]

**Steps:**

1. Step one
2. Step two
3. Step three

**Expected Result:**
Describe what should happen

**Edge Cases:**

- Edge case to test
```

---

## Phase 3: Validation & Summary

### Step 9: Validate Report

Check that the report includes:

- [ ] Frontmatter with title, date, original-plan reference
- [ ] Overview section (2-4 sentences)
- [ ] Files Changed with all modified/created files listed
- [ ] New Features with descriptions
- [ ] Additional Notes (even if brief)
- [ ] E2E Tests with actionable test cases

### Step 10: Display Summary

Provide completion summary:

```markdown
# Code Report Generated

## Location

docs/plans/[feature-name]/report.md

## Report Contents

### Overview

[First sentence of overview]

### Statistics

- **Files Created**: [count]
- **Files Modified**: [count]
- **Features Documented**: [count]
- **Test Cases**: [count]

## What's Included

- Implementation overview
- Complete file change list
- Feature descriptions
- Additional notes and concerns
- End-to-end testing guidance

## Next Steps

1. Review the report: docs/plans/[feature-name]/report.md
2. Share with QA team for testing guidance
3. Use as reference for documentation updates
4. Commit alongside implementation changes
```

---

## Quality Standards

### Report Quality Checklist

The report must have:

- [ ] Clear, concise overview (2-4 sentences)
- [ ] All changed files listed with descriptions
- [ ] Features described with implementation approach
- [ ] Relevant additional notes (concerns, dependencies, migrations)
- [ ] Actionable E2E test guidance for QA
- [ ] Professional tone suitable for team documentation

### Content Quality Guidelines

**Overview**

- Information-dense, not fluffy
- Focus on what was done and why
- Mention key architectural decisions

**Files Changed**

- Group by created vs modified
- Brief but useful descriptions
- Use relative paths from project root

**New Features**

- Clear feature names
- One-sentence descriptions
- Include "how it works" context

**Additional Notes**

- Only include important information
- Be honest about concerns or technical debt
- Mention any required follow-up work

**E2E Tests**

- Specific, actionable test cases
- Step-by-step instructions
- Clear expected results
- Don't forget edge cases

---

## Important Notes

- **You are the documenter** - accurately capture what was implemented
- **Be concise but complete** - every section should add value
- **Write for the team** - QA will use the tests, future devs will reference the notes
- **Link to the plan** - frontmatter should reference the original parallel-plan.md
- **Current date** - use the actual current date in mm/dd/yyyy format
