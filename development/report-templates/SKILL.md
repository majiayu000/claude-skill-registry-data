---
name: report-templates
description: Standard templates for debugging reports, reviews, and implementation plans
---

# Report Templates Skill

Use these templates for consistent documentation output.

## Debugging Report Template

**Output Location:** `{project}-implementation-plan/{NN}-debug-{issue-name}.md`

```markdown
# Debugging Report: [Brief Issue Description]

**Date**: [Current date]
**Status**: [In Progress | Root Cause Identified | Resolved]

## 1. Issue Summary
[Concise description of the problem]

## 2. Evidence Log
[Observed symptoms, error messages, logs]

## 3. Hypotheses
[Potential causes ranked by likelihood]

## 4. Test Results
[Results of investigation steps]

## 5. Root Cause Analysis
[Identified root cause with evidence]

## 6. Resolution
[Fix applied or recommended]

## 7. Lessons Learned
[Prevention strategies for future]
```

## Implementation Plan Template

**Output Location:** `{project}-implementation-plan/{NN}-{feature-name}.md`

```markdown
# Implementation Plan: [Feature Name]

## Overview
[Brief description of what will be implemented]

## Prerequisites
[Dependencies, setup requirements]

## Architecture Summary
[High-level design decisions]

## Implementation Steps
1. [Step with file changes]
2. [Step with file changes]
...

## Security Considerations
[Security implications and mitigations]

## Testing Strategy
[Unit, integration, e2e test approach]

## Deployment Notes
[Rollout considerations]
```

## Task Document Template

**Output Location:** `{project}-implementation-plan/{NN}-{task-name}.md`

```markdown
# Task: [Descriptive Title]

## Issue Description
[What needs to be done and why]

## Reference
[Link to parent document or issue]

## Scope of Changes
[Files and modules affected]

## Implementation Details
[Specific code changes required]

## Dependencies
[Other tasks this depends on]

## Testing Considerations
[Tests to write or update]
```

## Review Summary Template

**Output Location:** `{project}-implementation-plan/{NN}-review.md`

```markdown
# Task {NN}: [PR Title] - Review Summary

**PR:** #{PR_NUMBER}
**Branch:** `{BRANCH_NAME}`
**Date:** {current_date}

## Claude Review Summary

### Verdict: [Approve | Request Changes | Conditionally Approve]
Code Quality: X/10 | Test Coverage: X/10 | Documentation: X/10

### Strengths
- [Positive finding]
- [Positive finding]

## Critical Issues
[If any - must fix before merge]

## Medium Issues
[Should fix, lower priority]

## GitHub Review Summary
[Summary of existing GH comments]

## Validation Summary
| Issue | Severity | File | Status |
|-------|----------|------|--------|
| [Title] | CRITICAL | [file:line] | PENDING |
```

## Index File Template

**Output Location:** `{project}-implementation-plan/00-index.md`

```markdown
# Implementation Plan: [Project/Feature Name]

Generated from: `{source-document}`
Created: {date}

## Overview
[Brief summary of scope and approach]

## Task Sequence

| # | Task | Files Affected | Dependencies | Status |
|---|------|----------------|--------------|--------|
| 10 | [Task Name](./10-task-name.md) | file1.py | None | Pending |
| 11 | [Task Name](./11-task-name.md) | file2.py | Task 10 | Pending |

## Review Findings

| # | Document | Source | Key Findings |
|---|----------|--------|--------------|
| 10 | [Review](./10-review.md) | PR #14 | [Summary] |

## Dependency Graph
[ASCII diagram or description]

## Notes
[Additional context, risks, considerations]
```

## File Naming Convention

| Pattern | Use Case | Example |
|---------|----------|---------|
| `00-index.md` | Always the index file | `00-index.md` |
| `10-{name}.md` | First task group | `10-add-database-schema.md` |
| `{NN}-review.md` | Review of task NN | `10-review.md` |
| `{NN}-review-impl.md` | Implementation plan for fixes | `10-review-impl.md` |
| `{NN}-debug-{name}.md` | Debug report | `15-debug-memory-leak.md` |
