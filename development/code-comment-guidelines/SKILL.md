---
name: code-comment-guidelines
description: Code comment guidelines based on industry best practices. Use when reviewing code, writing new code, or when asked about comment quality. Applies to all languages but specializes in TypeScript/JavaScript. Enforces "JSDoc for public APIs only, no redundant comments" principle. Automatically suggests comment additions, removals, or refactoring alternatives.
allowed-tools: Read, Grep, Glob
---

# Code Comment Guidelines

Enforce industry best practices for code comments based on principles from Robert C. Martin (Clean Code), Martin Fowler (Refactoring), and other software engineering experts.

## Core Principle

**"JSDoc for public APIs only, no redundant comments"**

- Comments are a **last resort**, not a first choice
- Code should be **self-explanatory** through good naming and structure
- Comments explain **WHY**, never WHAT or HOW
- Prefer **refactoring** over commenting

## When to Use This Skill

Invoke this skill when:

1. **Code review**: Evaluating comment quality in pull requests
2. **Writing code**: Deciding whether to add a comment
3. **Refactoring**: Removing outdated or redundant comments
4. **Documentation**: Writing JSDoc for public APIs
5. **Quality checks**: Asked to "check comments" or "improve documentation"

## Decision Framework

Use this checklist to determine if a comment is needed:

### Step 1: Can you refactor instead?

```typescript
// ❌ Bad: Comment explains complex logic
// Calculate total with tax and discount
const total = price - price * discount + (price - price * discount) * taxRate;

// ✅ Good: Refactor to self-documenting code
const discountedPrice = price * (1 - discount);
const total = discountedPrice * (1 + taxRate);
```

**Action**: If logic is complex, extract to well-named functions/variables.

### Step 2: Is this a public API?

```typescript
// ✅ Required: Public exported function needs JSDoc
/**
 * Calculates tax-inclusive total price after discount
 * @param price - Base price in cents
 * @param discount - Discount rate (0-1)
 * @param taxRate - Tax rate (0-1)
 * @returns Final price in cents
 */
export function calculateTotal(price: number, discount: number, taxRate: number): number {
  const discountedPrice = price * (1 - discount);
  return discountedPrice * (1 + taxRate);
}
```

**Action**: All `export`ed functions, classes, and complex constants **require** JSDoc.

### Step 3: Is there a non-obvious technical reason?

```typescript
// ✅ Good: Explains performance optimization
// Convert to Map for O(1) lookup instead of O(n) array.find()
// Reduces search time from ~500ms to <1ms with 1000+ items
const postsMap = new Map(posts.map((p) => [p.id, p]));
```

**Action**: Comment **only** when explaining:

- Performance optimizations with measurements
- Library constraints or workarounds
- Hardware/browser compatibility issues
- Non-obvious algorithm choices

### Step 4: Does TypeScript already document this?

```typescript
// ❌ Redundant: Type already documents this
const user: User = fetchUser(); // Returns a User object

// ✅ Good: Type is sufficient
const user: User = fetchUser();
```

**Action**: Remove comments that duplicate type information.

## Automatic Actions

When analyzing code, automatically:

### 1. Flag Redundant Comments

```typescript
// ❌ Remove: Repeats what code says
counter++; // Increment counter
if (user === null) return null; // Return null if user is null
```

**Suggestion**: "Remove redundant comment. Code is self-explanatory."

### 2. Suggest Refactoring

```typescript
// ❌ Comment indicates refactoring opportunity
// Loop through users and check if email matches
for (let i = 0; i < users.length; i++) {
  if (users[i].email === email) return users[i];
}

// ✅ Suggest: Extract to function
function findUserByEmail(email: string): User | undefined {
  return users.find((u) => u.email === email);
}
```

**Suggestion**: "Extract to function `findUserByEmail()` instead of commenting."

### 3. Request JSDoc for Public APIs

```typescript
// ❌ Missing documentation
export function processPayment(amount: number, currency: string) {
  // implementation
}

// ✅ Suggest: Add JSDoc
/**
 * Process payment transaction
 * @param amount - Payment amount in smallest currency unit (e.g., cents)
 * @param currency - ISO 4217 currency code (e.g., "USD")
 * @throws {PaymentError} If payment gateway rejects transaction
 */
export function processPayment(amount: number, currency: string) {
  // implementation
}
```

**Suggestion**: "Add JSDoc documentation for exported function."

### 4. Improve Existing Comments

```typescript
// ❌ Low-quality comment
// TODO: fix this later

// ✅ Suggest improvement
// TODO(issue-#123): Implement exponential backoff for retry logic
```

**Suggestion**: "Make TODO specific with issue link and description."

## Language-Specific Guidance

### TypeScript/JavaScript

For TypeScript-specific patterns (React hooks, Server Components, type guards, etc.), refer to:

**See [typescript-specific.md](references/typescript-specific.md)** for:

- JSDoc requirements for public APIs
- React component documentation
- Server vs Client Components
- Type guard documentation
- useMemo/useCallback comment patterns

### General Programming

For language-agnostic principles with examples in multiple languages, refer to:

**See [examples.md](references/examples.md)** for:

- Redundant comment examples
- Function documentation patterns
- Performance optimization comments
- Business logic refactoring
- Complex algorithm documentation

## Expert Principles

For detailed rationale behind these guidelines, refer to:

**See [experts.md](references/experts.md)** for:

- Robert C. Martin (Uncle Bob) - "Comments are a failure"
- Martin Fowler - "Comment needs are code smells"
- Jeff Atwood - "Code = HOW, Comments = WHY"
- Steve McConnell - "Elevate abstraction level"
- Linus Torvalds - "Explain design decisions"
- John Carmack - "Small functions eliminate comments"

## Output Format

When reviewing code comments, provide:

1. **Overall Assessment**: Comment quality score (Good / Needs Improvement / Poor)
2. **Specific Issues**: List each problem with location
3. **Suggestions**: Concrete improvements with code examples
4. **Refactoring Opportunities**: Where refactoring eliminates comment needs

### Example Output

**Overall Assessment**: Needs Improvement

**Issues Found**:

1. Line 12: Redundant comment `// Calculate total price` → Remove
2. Line 34: Missing JSDoc for `export function applyDiscount()` → Add documentation
3. Line 56: Complex logic needs refactoring → Extract to `calculateBulkDiscount()`

**Recommended Changes**: Add JSDoc, remove redundant comments, extract helper function

## Quick Reference

| Situation                | Comment?                 | Alternative               |
| ------------------------ | ------------------------ | ------------------------- |
| Simple operation         | ❌ No                    | Self-explanatory code     |
| Public API (exported)    | ✅ Yes (JSDoc)           | N/A - Required            |
| Complex algorithm        | ✅ Yes (high-level)      | + Good naming             |
| Performance optimization | ✅ Yes (with metrics)    | N/A                       |
| Business logic           | ❌ No                    | Named constants/functions |
| Library workaround       | ✅ Yes (with link)       | N/A                       |
| Type information         | ❌ No                    | TypeScript types          |
| Magic number             | ❌ No                    | Named constant            |
| TODO note                | ✅ Yes (specific + link) | Issue tracker             |

## Remember

> "Don't comment bad code—rewrite it." - Robert C. Martin

The best comment is the one you don't need to write.
