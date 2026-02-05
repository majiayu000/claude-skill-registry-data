---
name: "systematic-code-review"
description: "Structured code review framework using Conventional Comments for clear, actionable feedback."
tags:
  - code-review
  - quality
version: 2.0.0
---

# Systematic Code Review

## Purpose

Deep code reviews that protect architecture, catch correctness issues, and provide mentoring-quality feedback using **Conventional Comments**.

## Review Workflow

Follow this order—don't jump to nits.

### 1. Understand Context
- What problem is this solving?
- Is there a linked ticket/design doc?

### 2. Scan High Level
- Files/directories touched
- New public APIs or endpoints
- New dependencies
- Migrations and data changes
- **Size check:** 200-400 lines optimal, >1000 recommend splitting

### 3. Evaluate Correctness
- Does it solve the described problem?
- Edge cases and error conditions handled?
- Assumptions explicit?

### 4. Evaluate Design
- Aligns with existing architecture?
- New pattern where existing one would work?
- Local change or architecture decision in disguise?

**Pattern Recognition:**
| Smell | Pattern to Suggest |
|-------|-------------------|
| Long method | Compose Method |
| Type-based conditionals | Replace Conditional with Polymorphism |
| Duplicate algorithm structure | Form Template Method |
| Scattered null checks | Introduce Null Object |
| Type field drives behavior | Replace Type Code with State/Strategy |

**Always name patterns explicitly.**

### 5. Evaluate Tests
- Tests for critical paths and edge cases?
- Tests read like specifications?
- Stable, isolated, fast?

**Red Flags:**
- Testing private methods instead of behavior
- Heavy mocking of own components (indicates mixed concerns—see `writing-code` skill)
- Tests slower than necessary

### 6. Evaluate Security
- User input crossing trust boundaries?
- Authorization and privacy concerns?
- Secrets handling?

### 7. Evaluate Operability
- Logging, metrics, traces where needed?
- Clear error messages?
- Impact on alerts and SLOs?

### 8. Evaluate Maintainability
- Can a mid-level engineer understand this?
- Coupling and cohesion appropriate?
- Naming, structure, comments carry weight?

### 9. Provide Feedback
- Use Conventional Comments syntax
- Classify blocking vs non-blocking
- Explain **why** each point matters
- End with clear status: approve / approve with nits / request changes

## Conventional Comments

```
<label> [decorations]: <subject>
[discussion]
```

### Labels

| Label | Use For |
|-------|---------|
| `praise:` | Highlight positives (aim for 1+ per review) |
| `nitpick:` | Trivial preferences (non-blocking) |
| `suggestion:` | Propose improvement with what and why |
| `issue:` | Concrete problem (pair with suggestion) |
| `todo:` | Small necessary changes |
| `question:` | Need clarification |
| `thought:` | Non-blocking future ideas |
| `chore:` | Process tasks before acceptance |

### Decorations

- `(blocking)` - Must resolve before merge
- `(non-blocking)` - Helpful but not required
- `(security)`, `(performance)`, `(tests)`, `(readability)` - Categories

### Examples

```
[src/validation.ts:34]
**praise**: Clean extraction of validation logic improves readability.
```

```
[api/users.py:127]
**issue (blocking, security)**: SQL injection via string interpolation.
Use parameterized queries.
```

```
[handlers/payment.js:89-105]
**suggestion (non-blocking, readability)**: Nested conditionals hard to scan.
Consider early returns to flatten.
```

```
[core/processor.go:234]
**question**: Is this on the hot path? If so, consider allocation cost in loop.
```

## Principle-Based Review

When reviewing, apply CLAUDE.md principles. Attribute by name for shared vocabulary:

```
**issue (blocking, design)**: This mutates shared state. Following Rich Hickey's
immutability principle, return new value from pure function instead.
```

```
**suggestion (non-blocking)**: Following Ousterhout's principle, pull this
complexity into the implementation. Simplify the interface.
```

## SOLID Quick Check

| Principle | Red Flag |
|-----------|----------|
| SRP | Class has multiple unrelated responsibilities |
| OCP | Must modify existing code to add behavior |
| LSP | Subclass changes expected behavior |
| ISP | Fat interface forces unused dependencies |
| DIP | High-level depends on low-level details |

## Change Size Guidelines

| Lines | Action |
|-------|--------|
| <400 | Full detailed review |
| 400-1000 | Focus on high-impact areas, suggest splitting |
| >1000 | Strong recommendation to split |

## Key Takeaways

1. **Follow 9-step workflow** - Don't skip to nits
2. **Include at least one praise** - Builds trust
3. **Use Conventional Comments** - Make intent explicit
4. **Name patterns explicitly** - "Replace Conditional with Polymorphism" not "consider polymorphism"
5. **Attribute principles** - Creates shared vocabulary
6. **200-400 lines optimal** - Larger PRs need splitting
7. **Explain why** - Not just what's wrong
