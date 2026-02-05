---
name: create-plan
description: Create an implementation plan from issue analysis or feature concept
allowed-tools: Read, Grep, Glob, Write
---

# Create Implementation Plan

Generate a detailed implementation plan based on existing analysis or concept documents.

## Instructions

1. **Detect Current Context**
   - Check current git branch to determine workflow folder
   - Branch `feature/42-something` → look for `workflows/issue-42-*/`
   - Branch `feature/my-feature` → look for `workflows/feature-my-feature/`

2. **Find Source Document**
   - Look for `analysis.md` (from /analyze-issue) or `concept.md` (for features)
   - If not found, ask user to run `/analyze-issue` first or provide context

3. **Read Project Guidelines**
   - Review CODING_GUIDELINES.md for implementation standards
   - Review TESTING_GUIDELINES.md for test requirements
   - Review COMMIT_GUIDELINES.md for commit structure

4. **Create Implementation Plan**
   - Write `plan.md` in the same workflow folder
   - Break down into specific, actionable tasks
   - Include file paths and specific changes
   - Add test plan based on TESTING_GUIDELINES.md

## Plan Template

Write to `workflows/<folder>/plan.md`:

```markdown
# Implementation Plan: <branch-name>

## Source
- Issue: #<number> (<link>)
- Analysis: `workflows/<folder>/analysis.md`

## Overview
<Brief summary of what will be implemented>

## Prerequisites
- [ ] Feature branch created: `feature/<name>`
- [ ] Analysis reviewed and understood
- [ ] No blocking questions remain

## Implementation Tasks

### Task 1: <Name>
**Files**: `path/to/file.go`

**Changes**:
- [ ] <Specific change 1>
- [ ] <Specific change 2>

**Details**:
<Any additional context or code snippets>

### Task 2: <Name>
**Files**: `path/to/file1.go`, `path/to/file2.go`

**Changes**:
- [ ] <Specific change>

**Depends on**: Task 1

### Task 3: Add Tests
**Files**: `test/cmd/<file>_test.go`

**Changes**:
- [ ] Add `Test<FunctionName>` - <what it tests>
- [ ] Add `Test<FunctionName>WithError` - <error case>

**Test Requirements** (per TESTING_GUIDELINES.md):
- One test case per function
- Structured comments with Steps
- Use testutil helpers, not os.Chdir

## Test Plan

### Unit Tests
| Test Name | Purpose | File |
|-----------|---------|------|
| `TestXxx` | <purpose> | `test/...` |

### Integration Tests
| Test Name | Scenario | File |
|-----------|----------|------|
| `TestXxxCommand` | <scenario> | `test/cmd/...` |

## Documentation Updates
- [ ] `docs/<command>.1.md` - <changes needed>
- [ ] `docs/gitflow-config.5.md` - <if config changes>
- [ ] Command help text updates

## Checkpoints

After each checkpoint, verify:
1. `go build ./...` succeeds
2. `go test ./...` passes
3. Changes work as expected

| Checkpoint | After Task | Verification |
|------------|------------|--------------|
| 1 | Task 1 | <what should work> |
| 2 | Task 2 | <what should work> |
| 3 | Task 3 | All tests pass |

## Commit Strategy

Following COMMIT_GUIDELINES.md, plan these commits:
1. `<type>(<scope>): <description>` - <what's included>
2. `test(<scope>): <description>` - test additions
3. `docs(<scope>): <description>` - documentation updates

## Estimated Scope
- Files to modify: <count>
- New files: <count>
- Tests to add: <count>
```

5. **Validate Plan**
   - Ensure all affected files from analysis are covered
   - Verify test plan aligns with TESTING_GUIDELINES.md
   - Check documentation requirements

6. **Report Completion**
   - Show path to created plan
   - Suggest next step: `/validate-tests` to verify test approach, then start implementing
