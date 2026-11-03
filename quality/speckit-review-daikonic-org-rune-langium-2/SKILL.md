---
name: speckit-review
description: Review completed implementation work and update task status.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/review.md
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## Overview

Perform structured code review of completed implementation work, validate against specifications, and update task status in tasks.md.

## Steps

### 1. Load Context

Run script to get feature paths and information:

```bash
cd "$(git rev-parse --show-toplevel)" && \
source .specify/scripts/bash/common.sh && \
get_feature_paths
```

This provides:
- `FEATURE_DIR` - Feature directory path
- `FEATURE_SPEC` - Specification file (spec.md)
- `IMPL_PLAN` - Implementation plan (plan.md)
- `TASKS` - Task list (tasks.md)

Load these files to understand:
- Feature requirements and acceptance criteria
- Implementation approach and design decisions
- Task breakdown and current status

### 2. Identify Review Target

**If user provided task ID** (e.g., "T001" in arguments):
- Review that specific task
- Focus review on changes related to that task

**If no task ID provided**:
- Review all pending tasks (marked with `[ ]` in tasks.md)
- Or review most recent code changes
- Ask user which tasks to review if unclear

### 3. Review Implementation

Conduct thorough review:

**A. Load Code Changes**
```bash
# Show recent changes
git diff main..HEAD

# Or show diff for specific files
git diff main..HEAD -- path/to/file
```

**B. Verify Against Specification**
- Check if implementation meets acceptance criteria in spec.md
- Verify design decisions from plan.md are followed
- Ensure behavior matches expected outcomes

**C. Check Code Quality**
- Look for bugs, edge cases, error handling
- Check code clarity and maintainability
- Verify proper testing coverage
- Check documentation completeness
- Flag placeholder/TODO/FIXME code within the implementation scope

**D. Run Tests** (if available)
```bash
# Run test suite based on project structure
npm test              # Node.js projects
pytest                # Python projects
cargo test            # Rust projects
go test ./...         # Go projects
./gradlew test        # Java/Kotlin projects
```

**E. Validate Against Quality Gates**
- Code follows project standards
- Tests exist and pass
- Edge cases handled
- Documentation adequate
- No obvious security issues
- No placeholder/TODO/FIXME code left in reviewed scope unless justified and tracked

### 4. Determine Review Outcome

Choose one of three outcomes:

**Approved - Implementation Ready**

Criteria:
- All acceptance criteria met
- All tests passing
- No blocking issues found
- Code quality acceptable
- Ready to merge

**Approved with Minor Notes**

Criteria:
- Core functionality works correctly
- Tests passing
- Minor improvements suggested (not blocking)
- Can be addressed in follow-up
- OK to merge with notes

**Needs Changes - Issues Must Be Fixed**

Criteria:
- Bugs or regressions found
- Tests failing or missing
- Acceptance criteria not met
- Security or critical issues
- Must fix before approval

### 5. Update Tasks (For Approved Work Only)

For approved work, mark completed tasks as done:

```bash
# Mark specific task as done
.specify/extensions/workflows/scripts/bash/mark-task-status.sh --task-id T001 --status done

# Mark multiple tasks
.specify/extensions/workflows/scripts/bash/mark-task-status.sh --task-id T002 --status done
.specify/extensions/workflows/scripts/bash/mark-task-status.sh --task-id T003 --status done
```

This updates tasks.md, changing:
- `[ ] T001: Task description` -> `[X] T001: Task description`

**For "Needs Changes" outcome**: Do NOT mark tasks as done. They remain pending until issues are fixed.

### 6. Generate Review Report

Create a comprehensive review report:

```markdown
# Review Report

**Feature**: [Feature name from branch/spec]
**Reviewer**: [Your agent identifier]
**Date**: [Current date]
**Status**: [Approved / Approved with Notes / Needs Changes]

## Summary

[Brief overview of what was reviewed and outcome]

## Implementation Review

### What Was Reviewed
- [List tasks or changes reviewed]

### Implementation Quality
- **Code Quality**: [Assessment]
- **Test Coverage**: [Assessment]
- **Documentation**: [Assessment]
- **Standards Compliance**: [Assessment]

## Test Results

[Output from running tests, if applicable]

**Tests Executed**: [Number]
**Tests Passing**: [Number]
**Tests Failing**: [Number]

## Findings

### What Worked Well
- [Positive aspect 1]
- [Positive aspect 2]
- [Positive aspect 3]

### Issues / Concerns (if any)

#### [Issue Title]
- **Severity**: [Critical / High / Medium / Low]
- **Description**: [What the issue is]
- **Impact**: [Why it matters]
- **Recommendation**: [How to fix]

[Repeat for each issue]

## Tasks Status

### Completed (Marked as Done)
- [X] T001: [Task description]
- [X] T002: [Task description]

### Remaining Pending
- [ ] T004: [Task description]
- [ ] T005: [Task description]

## Recommendations

[Suggestions for improvement or follow-up work]

## Next Steps

**For Approved**:
1. Tasks marked as complete in tasks.md
2. Ready to merge feature branch
3. Consider creating PR for team review

**For Approved with Notes**:
1. Tasks marked as complete in tasks.md
2. Can merge with documented follow-up items
3. Create follow-up tasks for minor improvements

**For Needs Changes**:
1. Fix listed issues
2. Run tests to verify fixes
3. Request re-review with `/speckit.workflows.review`
```

### 7. Output Summary

Display concise summary to user:

```
[Status Icon] Review Complete

Feature: [feature name]
Status: [Approved / Approved with Notes / Needs Changes]
Tasks Reviewed: [T001, T002, T003]
Tests: [X passing, Y failing]
Issues: [N found]

[Next steps based on status]
```

## Important Notes

1. **Be Thorough**: Don't rush the review - quality matters
2. **Be Constructive**: Frame feedback positively and helpfully
3. **Be Specific**: Cite exact locations for issues (file:line)
4. **Test First**: Always try to run tests before reviewing
5. **Check Specs**: Compare implementation to specification
6. **Document Everything**: Write findings for future reference
7. **Only Mark Done**: Only mark tasks complete when truly done

## Edge Cases

**No tasks.md exists**:
- Review can still proceed
- Document findings but skip task updates
- Recommend creating tasks.md for tracking

**No tests available**:
- Review code manually without automated tests
- Note lack of tests as a finding
- Recommend adding tests

**Multiple features in review**:
- Review current feature based on branch/directory
- Use FEATURE_DIR to scope the review

**Ambiguous review target**:
- Ask user to clarify which tasks to review
- Or review all pending tasks by default

## Context Information

Review context: $ARGUMENTS

Ensure all review feedback is actionable, specific, and constructive.