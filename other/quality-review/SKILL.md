---
name: quality-review
description: Review code for quality issues including readability, maintainability, complexity, and adherence to best practices. Use for PR reviews, code audits, identifying technical debt, and ensuring code meets quality standards before merge.
---

# Code Quality Review

Evaluate code for readability, maintainability, and adherence to best practices.

## Review Focus Areas

### Readability
- Clear, descriptive names (variables, functions, classes)
- Appropriate function/method length (< 30 lines preferred)
- Logical code organization
- Consistent formatting and style
- Self-documenting code (minimal comments needed)

### Maintainability
- Single Responsibility Principle
- Low coupling between modules
- High cohesion within modules
- No duplicated code (DRY)
- Clear dependency relationships

### Complexity
- Cyclomatic complexity (< 10 per function)
- Nesting depth (< 4 levels)
- Number of parameters (< 5 per function)
- Class size (< 300 lines)
- File size (< 500 lines)

## Review Checklist

### Naming
- [ ] Variables describe their content
- [ ] Functions describe their action
- [ ] Boolean names are questions (is_valid, has_permission)
- [ ] No abbreviations except common ones (id, url, etc.)
- [ ] Consistent naming conventions throughout

### Structure
- [ ] Functions do one thing
- [ ] No deep nesting (extract to functions)
- [ ] Related code is grouped together
- [ ] Dependencies are explicit (no globals)
- [ ] Error handling is consistent

### Code Smells
- [ ] No magic numbers/strings (use constants)
- [ ] No commented-out code
- [ ] No dead code (unreachable paths)
- [ ] No overly clever code
- [ ] No premature optimization

## Issue Severity Levels

```
CRITICAL - Must fix before merge
- Security vulnerabilities
- Data corruption risks
- Breaking changes without migration

HIGH - Should fix before merge
- Logic errors
- Performance problems
- Missing error handling

MEDIUM - Fix soon after merge
- Code smells
- Minor maintainability issues
- Missing tests for edge cases

LOW - Consider fixing
- Style inconsistencies
- Minor naming improvements
- Documentation gaps
```

## Review Output Format

```markdown
## Code Review: [File/PR Name]

### Summary
[1-2 sentence overview of the change and overall quality]

### Critical Issues
- **[Location]**: [Issue description]
  - Impact: [What could go wrong]
  - Suggestion: [How to fix]

### Suggestions
- **[Location]**: [Improvement suggestion]
  - Rationale: [Why this matters]

### Positive Notes
- [What was done well]
```

## Common Patterns to Flag

### Complexity
```python
# Too complex - extract conditions
if user.is_active and user.has_permission('edit') and not user.is_banned and item.is_editable:
    ...

# Better
def can_edit(user, item):
    return (user.is_active
            and user.has_permission('edit')
            and not user.is_banned
            and item.is_editable)
```

### Magic Values
```python
# Bad
if status == 3:
    ...

# Good
STATUS_COMPLETED = 3
if status == STATUS_COMPLETED:
    ...
```

### Deep Nesting
```python
# Bad - deeply nested
def process(items):
    for item in items:
        if item.is_valid:
            if item.needs_processing:
                if item.has_data:
                    # actual logic buried here

# Good - early returns
def process(items):
    for item in items:
        if not item.is_valid:
            continue
        if not item.needs_processing:
            continue
        if not item.has_data:
            continue
        # actual logic at top level
```
