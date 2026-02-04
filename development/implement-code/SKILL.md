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

- **Follow Conventions**: Use language-specific naming conventions
- **No Unnecessary Comments**: Code should be self-documenting
- **Document Only When Needed**: Use `@DisplayName`, JSDoc, or
  docstrings only when naming cannot convey intent
- **Minimal Changes**: Implement only what is requested
- **Test Coverage**: Write tests alongside implementation

### Naming Conventions by Language

#### Java/Kotlin

- Classes: `PascalCase`
- Methods/variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Packages: `lowercase.dot.separated`

#### Python

- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- Modules: `snake_case`

#### JavaScript/TypeScript

- Classes/Components: `PascalCase`
- Functions/variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE` or `camelCase`
- Files: `kebab-case` or `camelCase`

#### Go

- Exported: `PascalCase`
- Unexported: `camelCase`
- Packages: `lowercase`
- Acronyms: `URL`, `HTTP` (all caps)

#### C/C++

- Classes/structs: `PascalCase` or `snake_case`
- Functions: `snake_case` or `camelCase`
- Macros: `SCREAMING_SNAKE_CASE`
- Namespaces: `lowercase`

## Implementation Process

### 1. Understand Requirements

- Clarify the feature scope
- Identify input/output contracts
- Check existing patterns in codebase

Use MCP tools:

- `mcp__serena__get_symbols_overview` - Understand code structure
- `mcp__context7__get-library-docs` - Get library documentation
- `mcp__jetbrains__get_symbol_info` - Get existing implementations

### 2. Plan Implementation

- Break down into smaller tasks
- Identify dependencies
- Design the interface first

### 3. Write Code

```text
1. Create skeleton (interfaces, function signatures)
2. Implement core logic
3. Handle edge cases
4. Add error handling
5. Write tests
```

### 4. Validate

Run appropriate validation commands:

```bash
npm test
```

```bash
pytest
```

```bash
go test ./...
```

```bash
mvn test
```

```bash
gradle test
```

```bash
cargo test
```

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
| path | Added       | Description |

### Implementation Details

[Key design decisions and approach]

### Testing

[Tests added or suggested]

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
