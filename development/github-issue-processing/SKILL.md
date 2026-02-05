---
name: github-issue-processing
description: Extract actionable information from GitHub issues including requirements, acceptance criteria, and technical constraints. Use when analyzing GitHub issues or preparing them for workflow execution.
---

# GitHub Issue Processing

This skill provides patterns for extracting and structuring information from GitHub issues.

## Information Extraction Pattern

When processing a GitHub issue, extract:

### 1. Core Requirements

```markdown
## Requirements
- Primary objective
- User stories or use cases
- Expected behavior
```

### 2. Technical Details

```markdown
## Technical Context
- Affected components/modules
- Current behavior vs. desired behavior
- Stack traces or error messages (if applicable)
- Environment details
```

### 3. Acceptance Criteria

```markdown
## Acceptance Criteria
- [ ] Criterion 1: Specific, testable condition
- [ ] Criterion 2: Specific, testable condition
- [ ] Criterion 3: Specific, testable condition
```

### 4. Constraints

```markdown
## Constraints
- Performance requirements
- Backward compatibility needs
- Security considerations
- Dependencies on other issues/PRs
```

## Labels Interpretation

Common GitHub labels and their implications:

- **bug**: Fix existing functionality, requires root cause analysis
- **enhancement**: Add new functionality, may need design review
- **documentation**: Update docs, ensure accuracy and completeness
- **breaking-change**: Impacts existing API, needs migration guide
- **help-wanted**: Good for community contribution, provide clear guidance
- **priority: high**: Address urgently, may need expedited review

## Issue Linking

Extract and track related issues:

```markdown
## Related Issues
- Blocks: #123, #456
- Blocked by: #789
- Related to: #321
- Duplicate of: (if applicable)
```

## Converting to PRP

Transform issue analysis into PRP format:

1. **Prompt**: Use issue title and description
2. **Response**: Include analysis and proposed approach
3. **Plan**: Break down into actionable steps with dependencies

## Integration Points

Works with:
- `context-engineering-github-issue-analyzer` agent
- `context-engineering-prp-generator` agent for issue → PRP conversion
- `/initial-github-issue` command
