---
name: implement-code
description: 'Implement features, write code, and build functionality following best practices and language conventions. Use when the user asks to implement, code, build, create a function, add a feature, or write code.'
compatibility: Requires code read/write tools and terminal access
allowed-tools:
    - Bash(node:*, npm:*, npx:*, pnpm:*, yarn:*, python:*, pip:*, pytest:*, go:*, cargo:*, mvn:*, ./mvnw:*, gradle:*, ./gradlew:*, make:*, cmake:*, g++:*, gcc:*, clang:*)
    - Glob
    - Grep
    - Read
    - Write
    - mcp__context7
    - mcp__fetch
    - mcp__jetbrains
    - mcp__markitdown
    - mcp__serena
---

# Code Implementation Skill

Implement features and write code following best practices and
language conventions.

## Implementation Principles

### Core Rules

- Follow language conventions
- Avoid unnecessary comments; document only when naming cannot convey intent (`@DisplayName`, JSDoc, docstrings)
- Minimal changes: implement what is requested

### Language-Specific Guidelines

Load only when working in that stack:

- Java: `references/java-guidelines.md`
- Kotlin: `references/kotlin-guidelines.md`
- Python: `references/python-guidelines.md`
- JavaScript/TypeScript: `references/js-ts-guidelines.md`
- Go: `references/go-guidelines.md`
- C/C++: `references/cpp-guidelines.md`

## Implementation Process

1. Understand requirements: clarify scope, I/O contracts, existing patterns.
   Tools: `mcp__serena__get_symbols_overview`, `mcp__context7__get-library-docs`, `mcp__jetbrains__get_symbol_info`.
2. Plan: break into tasks, note dependencies, design interface first.
3. Write code:
    1. Skeleton (interfaces/signatures)
    2. Core logic
    3. Edge cases
    4. Error handling
4. Validate: run narrow, relevant checks (lint/typecheck/build) for the touched stack.

## Code Quality Guidelines

### Self-Documenting Code

```java
// BAD: Comment explains obvious code
// Increment counter by one
counter++;

// GOOD: Code is self-explanatory
userLoginAttempts++;
```

### When to Add Documentation

Use documentation annotations when:

- Method name cannot fully express behavior
- Complex algorithm needs explanation
- Public API requires usage examples
- Prefer doc comments (Javadoc/KDoc/JSDoc/reStructuredText/GoDoc) over inline line comments for reusable helpers.

```java
@DisplayName("Should retry up to 3 times with exponential backoff")
@Test
void retryWithExponentialBackoff() {
    // test implementation
}
```

```python
def calculate_compound_interest(principal, rate, time, n=12):
    """
    Calculate compound interest.

    Uses formula: A = P(1 + r/n)^(nt)

    Args:
        principal: Initial amount
        rate: Annual interest rate (decimal)
        time: Time in years
        n: Compounding frequency per year

    Returns:
        Final amount after compound interest
    """
    return principal * (1 + rate / n) ** (n * time)
```

### Error Handling

```typescript
function parseConfig(path: string): Config {
    const content = readFileSync(path, 'utf-8');
    if (!content.trim()) {
        throw new EmptyConfigError(path);
    }
    return JSON.parse(content);
}
```

## Output Format

```markdown
## Implementation Summary

### Files Changed

| File | Change Type | Description |
| ---- | ----------- | ----------- |
| path | Added | Description |

### Implementation Details

[Key design decisions and approach]

### Testing

[If tests are needed, use the `generate-tests` skill to add/extend coverage.]

### Usage

(example code)
```

## Edge Cases

- **Unclear requirements**: Ask 1-3 clarifying questions
- **Large features**: Break into smaller PRs
- **Legacy code**: Match existing style, suggest improvements separately
- **Performance-critical**: Document algorithmic complexity

## Tips

- MCP tools are optional; omit if unavailable or add others as needed
- Always run tests before completing implementation
- Check for existing similar implementations in the codebase
