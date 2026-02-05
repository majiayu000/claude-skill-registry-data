---
name: planning-refactors
description: Uses ast-grep to find patterns and analyze code for refactoring. Use when planning refactors, finding deprecated API usage, migrating code, or analyzing code quality before changes. For simple code search, use searching-code instead.
---

# Planning Refactors

Uses ast-grep to analyze code patterns and plan refactoring workflows. This skill focuses on systematic code changes, migrations, and quality analysis with human-in-loop validation.

## Quick Start

```bash
# Find deprecated API usage
ast-grep -p 'oldApi.$METHOD($$$)' --lang ts

# Find class components for hooks migration
ast-grep -p 'class $NAME extends Component' --lang tsx

# Find all direct state mutations
ast-grep -p 'this.state.$PROP = $VALUE' --lang ts
```

## When to Use This Skill

- Planning systematic refactors or migrations
- Finding deprecated API usage across codebase
- Analyzing code quality patterns before changes
- Understanding codebase structure for refactoring
- Creating migration strategies
- **NOT for**: Simple code searches (use searching-code instead)

## Refactoring Workflow

1. Find all pattern occurrences with ast-grep
2. Review matches for context
3. Identify edge cases
4. Plan replacement strategy
5. Execute changes with Edit tool
6. Verify with tests

## Common Refactoring Patterns

### Deprecated API Migration

```bash
# Find old API usage
ast-grep -p 'oldApi.$METHOD($$$)' --lang ts

# Find import statements
ast-grep -p 'import { $$$, oldApi, $$$ } from "$MODULE"' --lang ts

# Find all variations
ast-grep -p 'oldApi.$$$' --lang ts
```

### Class to Hooks Migration

```bash
# Find class components
ast-grep -p 'class $NAME extends Component { $$$ }' --lang tsx
ast-grep -p 'class $NAME extends React.Component { $$$ }' --lang tsx

# Find lifecycle methods
ast-grep -p 'componentDidMount() { $$$ }' --lang tsx
ast-grep -p 'componentWillUnmount() { $$$ }' --lang tsx

# Find state usage
ast-grep -p 'this.state.$PROP' --lang tsx
ast-grep -p 'this.setState($$$)' --lang tsx
```

### Code Quality Analysis

```bash
# Find console.log statements
ast-grep -p 'console.log($$$)' --lang ts

# Find empty catch blocks
ast-grep -p 'catch ($E) {}' --lang ts

# Find TODO comments
ast-grep -p '// TODO: $$$' --lang ts

# Find any statements
ast-grep -p 'any' --lang ts
```

## Reference Documentation

For detailed refactoring and analysis patterns:
- [REFACTORING.md](REFACTORING.md) - Deprecated APIs, migrations, systematic changes
- [ANALYSIS.md](ANALYSIS.md) - Code review patterns, quality checks, codebase structure

## Integration Workflow

```bash
# 1. Find pattern
ast-grep -p '<pattern>' --json > matches.json

# 2. Analyze matches
jq 'group_by(.file) | map({file: .[0].file, count: length})' matches.json

# 3. Read each unique file
jq -r '[.[].file] | unique[]' matches.json | while read file; do
    # Read file with Read tool
done

# 4. Execute refactor
# Use Edit tool for each file
```

## Risk Assessment

**Low Risk** (safe to automate):
- Renaming variables/functions in isolated scope
- Updating import statements
- Formatting changes

**Medium Risk** (review each change):
- API migrations with similar signatures
- Adding/removing function parameters
- Restructuring object properties

**High Risk** (requires careful analysis):
- Changing control flow logic
- Modifying error handling
- Altering async/await patterns
- Changes affecting multiple modules
