---
name: code-simplification
description: Enforces simplicity — Chesterton's Fence (understand why before removing), Rule of 500 (keep functions/files under 500 lines), Occam's Razor for code. Counteracts the natural tendency to add unnecessary abstraction layers.
---

# Code Simplification

## Problem it solves

Agents naturally add abstraction layers — it feels like "good engineering": extract everything into a helper, add an interface, make it configurable. This causes:
- Over-engineered code with unnecessary indirection
- Premature abstraction ("we might need this later")
- Functions and files that grow beyond what a human can hold in working memory
- Removing code without understanding why it was there
- Complexity that makes future changes harder, not easier

## Protocol

### 1. Chesterton's Fence — understand before removing

Before removing any code, comment, or configuration that seems unnecessary:
1. **Read the git blame** — who added it and why?
2. **Read the commit message** — what problem did it solve?
3. **Check for callers** — is anything depending on this?
4. **Understand the intent** — what did the author think they were solving?

Only remove if you can answer: "I know why this was here, and that situation no longer applies."

If you cannot trace the origin, leave it and add a comment: `# TODO: investigate — purpose unknown`

Chesterton's Fence also applies to architecture. If a pattern looks odd, understand why it exists before "fixing" it.

### 2. Rule of 500 — size limits

| Scope | Limit | Action |
|-------|-------|--------|
| Function | ~50 lines | Split if over. Likely doing too much. |
| File | ~500 lines | Split if over. Consider extracting a module. |
| PR diff | ~400 lines | Split into multiple PRs if over. |
| Test function | ~20 lines | Split if over. Testing too much at once. |

These are guidelines, not hard limits. A 60-line function that does one thing clearly is better than 5 functions with confusing indirection.

### 3. Occam's Razor for code

When choosing between approaches:
- **Simpler is better** — more lines of straightforward code > fewer lines of clever code
- **Flat is better than nested** — prefer early returns over nested ifs
- **Explicit is better than implicit** — magic numbers > named constants only if the number is obvious (0, 1). Name everything meaningful.
- **YAGNI** — "You Aren't Gonna Need It". If you're adding code because "we might need this later", don't. Add it when you actually need it.

### 4. The abstraction audit

Before adding a new abstraction (interface, base class, factory, utility function):
1. **One use case?** — Don't abstract. Write it inline.
2. **Two use cases?** — Still consider inline. Duplication is cheaper than wrong abstraction.
3. **Three use cases?** — Now consider abstracting, but keep it minimal.

### 5. Simplification checklist

Review code for:
- [ ] Can a function be replaced with a simpler expression?
- [ ] Can conditional logic be replaced with a lookup table?
- [ ] Can a class be replaced with a function?
- [ ] Can a config parameter be replaced with a constant?
- [ ] Is there dead code (unused, commented out, unreachable)?
- [ ] Are there unnecessary defensive checks (checking the same thing twice)?

## Detection triggers

Activate when:
- Implementing any new code
- Reviewing existing code (during code-review or debugging)
- About to add an abstraction, interface, or helper
- User says "simplify this", "refactor", "clean up"
- A function exceeds 30 lines or a file exceeds 300 lines
- Feeling tempted to add something "just in case"

## When NOT to use

- Performance-critical code (sometimes complexity is necessary)
- Security boundaries (defense in depth matters)
- Public API surface (stability > simplicity)
- User explicitly asks for a specific complex pattern

## Cross-references

- **follow-existing-patterns** — Simplicity is relative to the project. Don't simplify a complex pattern if it's the project's established style.

- **code-review** — The readability and architecture axes should flag unnecessary complexity and violations of simplicity principles.

- **incremental-implementation** — Small slices naturally prevent over-engineering. You can't add unnecessary abstraction in a thin vertical slice.

- **spec-driven-development** — The spec defines scope. Don't add abstractions that go beyond what the spec requires.

- **test-driven-development** — YAGNI violations are easier to catch when you only implement what the test requires.

- **anti-premature-termination** — "Simplified" is not the same as "done". Verify the simplification didn't break anything.
