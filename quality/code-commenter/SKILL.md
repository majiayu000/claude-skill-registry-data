---
name: code-commenter
description: Guides Codex in writing high-quality, language-agnostic code comments and documentation. Use when asked to comment code, document functions, or improve code readability by explaining technical intent and rationale.
---

# Code Commenting Guidelines

This skill provides a set of principles and patterns for writing code comments that are helpful, maintainable, and non-redundant.

## Core Principles

- **Explain the "Why", Not the "What":** Code should ideally be self-documenting regarding _what_ it is doing. Comments must focus on the _rationale_, _technical intent_, and _constraints_ that are not immediately obvious from the code itself.
- **Avoid Redundancy:** Never write comments that merely restate what the code clearly says. If the code is complex, prioritize refactoring for clarity over adding a descriptive comment.
- **Remove Obsolete Comments:** When modifying code, always update or remove associated comments. Stale comments are worse than no comments.
- **Documentation Blocks for Public APIs:** Use formal documentation blocks (e.g., JSDoc, Docstrings) for public methods, classes, and complex internal interfaces. Focus on parameters, return values, and side effects.
- **Use Inline Comments Sparingly:** Use inline comments only for non-obvious hacks, workarounds, or business logic that requires specific context.

## Commenting Patterns

### 1. Rationale Comments

Use these when a specific implementation choice was made for non-obvious reasons (e.g., performance, bug workaround).

```typescript
// BAD: Increment counter
counter++;

// GOOD: Use a manual increment here instead of the utility function
// to avoid the overhead of the recursive check in hot loops.
counter++;
```

### 2. Implementation Warnings

Alert other developers to non-obvious side effects or fragile logic.

```python
# GOOD: This function is not thread-safe because it shares a global state
# with the database connection pool. Ensure it's called within a lock.
def process_data():
    ...
```

### 3. API Documentation

Standardized blocks for interfaces.

```javascript
/**
 * Processes the incoming request and validates the signature.
 *
 * @param {Request} req - The raw HTTP request object.
 * @throws {InvalidSignatureError} If the HMAC signature check fails.
 * @returns {Promise<User>} The authenticated user object.
 */
async function authenticate(req) {
    ...
}
```

## Anti-Patterns to Avoid

- **The "Captain Obvious":** `i++; // Increment i`
- **The "History Log":** `// Modified by John on 2021-05-21 to fix bug X` (This belongs in Git history).
- **The "Zombie Code":** Commented-out code blocks. Delete them; they are preserved in Git.
- **The "Vague Directive":** `// Fix this later` (Always provide context or a ticket number).

## Workflow

1. **Analyze the code:** Identify non-obvious logic, business rules, or complex interfaces.
2. **Refactor first:** If a comment is needed to explain _what_ the code does, try to rename variables or extract methods first.
3. **Write the rationale:** If the _why_ is still unclear, add a concise comment.
4. **Choose the format:** Use inline comments for logic, and blocks for APIs.
5. **Review for redundancy:** Strip away any comments that add zero value to a senior developer reading the code.
