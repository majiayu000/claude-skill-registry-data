---
name: review-documentation
description: |
  Use this skill when asked to review the package documentation of the Go implementation of Feather.
---

# Review Go Documentation

Review Go package documentation from a user's perspective, identifying gaps and areas for improvement.

## When to Use

Use this skill when:

- A package's public API documentation needs review
- Preparing documentation for a library release
- Evaluating whether docs are sufficient for new users

## Process

1. **Run `go doc .`** to see the package overview
2. **Run `go doc -all .`** to see all exported symbols
3. **Adopt the user's perspective**: Imagine you're a developer who just discovered this package and wants to use it

## Checklist

Review documentation against these categories:

### Essential Information

- [ ] **Purpose**: Is the package's purpose clear in one sentence?
- [ ] **Quick Start**: Can a user get something working in under 5 minutes?
- [ ] **Core Types**: Are the 2-3 most important types clearly identified?
- [ ] **Thread Safety**: Is concurrency behavior documented?
- [ ] **Error Handling**: How do errors propagate? What error types exist?
- [ ] **Lifecycle**: When to create, when to close, what happens to related objects?

### API Clarity

- [ ] **Similar Functions**: Are distinctions between similar functions clear?
  - Example: `Register` vs `RegisterType` vs `DefineType`
- [ ] **Similar Types**: Are related types differentiated?
  - Example: `TypeDef` vs `ForeignTypeDef`
- [ ] **Constants**: Are magic constants explained with context for when to use them?
- [ ] **Unexplained Types**: Does every exported type have a clear use case?

### Practical Guidance

- [ ] **Common Patterns**: Are typical usage patterns shown?
- [ ] **Anti-patterns**: Are common mistakes warned against?
- [ ] **Scope/Subset**: If implementing a standard, what subset is covered?
- [ ] **Limitations**: What can't it do?

### Internal vs Public

- [ ] **Internal Types**: Are internal-but-exported types clearly marked "do not use"?
- [ ] **Stability**: Is it clear which APIs are stable vs experimental?

## Output Format

Provide findings in these sections:

```markdown
## Critical (Users will be blocked without this)

- Issue 1
- Issue 2

## Important (Users will struggle without this)

- Issue 1
- Issue 2

## Nice to Have (Would improve experience)

- Issue 1
- Issue 2

## What's Good (Keep these)

- Strength 1
- Strength 2
```

## Example Review

For a hypothetical database driver:

```markdown
## Critical

- No mention of thread safety - can I share \*DB across goroutines?
- Close() documented but not what happens to active queries

## Important

- Query vs QueryRow vs QueryContext - when to use each?
- Error types not documented - how do I detect "connection lost"?

## Nice to Have

- Example of connection pooling configuration
- List of supported database versions

## What's Good

- Quick start example gets to working code fast
- Transaction API is well-explained with rollback semantics
```
