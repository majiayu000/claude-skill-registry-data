---
name: violation-scanner
description: Delegates coding standards violation scanning to a lightweight agent. Use when checking files for violations without loading full source files into context.
---

# Violation Scanner Skill

This skill delegates coding standards violation scanning to a specialized lightweight agent, keeping your context lean.

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **Post-implementation check**: Code was just written and needs standards verification
2. **Pre-refactor analysis**: You need to identify violations before refactoring
3. **File size/complexity check**: You need to verify files stay under 500 lines / 5 functions
4. **Standards compliance audit**: You need to scan multiple files for violations
5. **Hardcoded value detection**: You need to find hardcoded URLs, ports, credentials

## Why Use This Skill?

**Without this skill**: You would read full source files (100-500 lines each) to check for violations manually.

**With this skill**: The violation-scanner agent (haiku model) uses Grep patterns to find violations and returns a concise violation list.

**Context savings**: 80-95% reduction in violation-checking context usage.

## Invocation

When you need to check for violations, invoke the agent:

```
Task(subagent_type="violation-scanner", prompt="
Scan for coding standards violations.

Files to scan:
- src/services/user_service.py
- src/services/order_service.py
- src/utils/helpers.py
")
```

For directory scanning:

```
Task(subagent_type="violation-scanner", prompt="
Scan for coding standards violations.

Directory: src/services/
")
```

For specific standards focus:

```
Task(subagent_type="violation-scanner", prompt="
Scan for coding standards violations.

Files: src/api/endpoints.py
Focus on: hardcoded values, environment variable reads
")
```

## What violation-scanner Will Do

The agent will:

1. **Detect language**: Determine which standards apply based on file extensions
2. **Pattern scan**: Use Grep to find violations without reading full files
3. **Check limits**: Verify file size (<500 lines) and function count (<5)
4. **Categorize severity**: Critical vs Warning violations
5. **Return summary**: Concise violation list with file:line references

## Violations Detected

**Critical (must fix)**:
- Hardcoded secrets/credentials
- Global mutable state
- Environment reads in business logic
- File > 500 lines
- Functions > 5 per file

**Warning (should fix)**:
- Missing type hints
- Default argument values
- Console/print statements
- Hardcoded URLs/ports (non-secret)

## Expected Output

You will receive a structured summary like:

```
## Violation Scan Results

**Files Scanned**: 5
**Violations Found**: 8

### Critical Violations

| File | Line | Violation | Rule |
|------|------|-----------|------|
| src/services/auth.py | 45 | `os.getenv('SECRET')` | no env reads in functions |
| src/services/auth.py | 89 | Global: `CACHE = {}` | no global mutable state |

### Warnings

| File | Line | Violation | Rule |
|------|------|-----------|------|
| src/services/user.py | 12 | Default arg: `id=None` | no default arguments |
| src/utils/helpers.py | 8 | `print()` statement | use logging |

### File Size Violations

| File | Lines | Limit |
|------|-------|-------|
| src/services/order.py | 623 | 500 |

### Summary by Category

- Hardcoded values: 1
- Environment reads: 1
- Global state: 1
- File size: 1
```

## Example Usage

**Scenario**: Coder agent just finished implementing a new service.

**Without skill**: Read the 200-line service file, manually check each standards rule.

**With skill**:
```
Task(subagent_type="violation-scanner", prompt="
Scan for coding standards violations.
Files: src/services/new_service.py
")
```

**Result**: You get a violation list with exact line numbers in 20 lines of context.

## Do NOT Invoke When

- You're already reading the file for other reasons (check violations while reading)
- The file is very small (<50 lines) - just read it directly
- You only need to check one specific pattern (use Grep directly)
- The user has explicitly said to skip standards checks

## Consumers

This skill is particularly useful for:
- `coding-standards-checker` - Post-implementation verification
- `refactorer` - Identifying what needs to be fixed
- `coder` - Pre-commit validation
- `acceptance-qa` - Final quality gate
