---
name: code-commenter
description: Add detailed comments explaining WHY code works, its context, edge cases, and performance implications. Use when user mentions "add comments", "document", "explain code", "improve readability", or "maintainability". Supports C++, Python, Java, JavaScript, Go, Rust, SQL.
---

# Code Commenter

Add high-quality comments that explain WHY code works, not just WHAT it does.

## Core Principles

### 1. Explain WHY, not WHAT
Explain reasoning and business context, not just what the code does.

```cpp
// Bad: Increment counter
counter++;

// Good: Track failed connection attempts for exponential backoff
counter++;
```

### 2. Document Non-Obvious Decisions
Explain performance trade-offs, algorithm choices, constraints.

```cpp
// Use bloom filter for memory efficiency: 10x memory savings, false positives acceptable
// for duplicate detection. Hash set would be more accurate but needs 10x more RAM.
```

### 3. Highlight Edge Cases and Gotchas

```go
// IMPORTANT: Don't call from within a transaction - opens its own tx, causing deadlock
// NOTE: This mutex must be held when accessing sharedCache (race condition otherwise)
```

### 4. Document Assumptions

```java
// ASSUMES: Input already sanitized, max 1000 chars
// CONSTRAINT: Parser doesn't handle nested parens beyond depth 3
```

## Comment Types

**File/Module Level**: Purpose, dependencies, constraints
**Function/Method**: Purpose, parameters, side effects, performance notes
**Inline**: Explain specific lines when non-obvious
**Section**: Break long functions into logical sections
**TODO/FIXME**: Track technical debt

See [EXAMPLES.md](EXAMPLES.md) for detailed examples of each type.

## Language-Specific Guidelines

**C/C++**: Doxygen style, explain memory/thread safety
**Python**: Docstrings (PEP 257), type hints, examples
**Java**: JavaDoc, thread safety, exceptions  
**JavaScript/React**: Props, state, performance notes
**Go**: Exported symbols, concurrency, context
**Rust**: Doc comments, ownership, lifetimes
**SQL**: Join logic, performance, business rules

For detailed examples, see [LANGUAGE_GUIDE.md](LANGUAGE_GUIDE.md).

## What NOT to Comment

**Don't state the obvious**: `x = 5;` doesn't need a comment saying "set x to 5"
**Don't comment bad code - refactor it**: Make code self-documenting with good names
**Don't maintain outdated comments**: Delete rather than keep misleading comments

## Output Format

1. Preserve original code structure (don't reformat unless requested)
2. Add comments naturally where they make logical sense
3. Match existing comment style in the codebase
4. After commenting, provide brief summary of what was documented

Example:
```
I've added comments to explain:
- Algorithm complexity and trade-offs
- Edge case handling for empty inputs  
- Memory management strategy
- Non-obvious performance optimizations
```

## Best Practices

✅ **DO:**
- Explain WHY and provide context
- Document assumptions, constraints, edge cases
- Use clear, concise language
- Keep comments close to relevant code
- Update comments when code changes

❌ **DON'T:**
- State the obvious
- Comment bad code instead of fixing it
- Write novels - be concise
- Leave outdated comments
- Comment out code (use version control)
