---
name: Concise Rule Writing
description: "This skill should be used when the user asks to 'write a rule', 'create a rule', 'make rule shorter', 'keep rules minimal', 'reduce rule size', 'optimize rule', or needs guidance on writing precise, context-efficient rules for CLAUDE.md."
version: 1.0.0
---

# Concise Rule Writing

Guide for writing precise, short rules that minimize context usage while maximizing clarity and enforceability.

## Core Principle

**Every token counts.** Rules load into context on every interaction. Verbose rules waste tokens and reduce available context for actual work.

### Target Metrics

| Metric | Target | Maximum |
|--------|--------|---------|
| Words per rule | <30 | 50 |
| Characters per rule | <200 | 350 |
| Lines per rule | 1-2 | 3 |
| Total CLAUDE.md | <500 words | 1000 words |

## Rule Anatomy

A good rule has three components in minimal space:

```
[CONSTRAINT] [ACTION] [CONTEXT (optional)]
```

**Examples:**
```
Never commit .env files                     # 4 words
Use snake_case for Python variables         # 5 words
Run tests before commit                     # 4 words
```

## Writing Techniques

### 1. Remove Filler Words

**Remove:** actually, basically, essentially, really, very, definitely, certainly, obviously, simply, just

| Before | After |
|--------|-------|
| "You should always make sure to run tests" | "Run tests before commit" |
| "It's really important to never commit secrets" | "Never commit secrets" |
| "Basically, all API endpoints should have auth" | "All endpoints require auth" |

### 2. Use Imperative Form

Start with verb. No "you should", "make sure to", "always remember to".

| Before | After |
|--------|-------|
| "You should use TypeScript for type safety" | "Use TypeScript" |
| "Make sure to validate user input" | "Validate all input" |
| "Always remember to add error handling" | "Add error handling" |

### 3. Eliminate Redundancy

| Before | After |
|--------|-------|
| "Never ever commit any secrets or API keys" | "Never commit secrets" |
| "Use consistent naming conventions throughout" | "Consistent naming" |
| "All functions should have proper error handling" | "Handle errors in functions" |

### 4. Use Standard Terms

Replace verbose descriptions with known terms:

| Verbose | Concise |
|---------|---------|
| "Make sure passwords are scrambled" | "Hash passwords" |
| "Check that data is correct before saving" | "Validate before persist" |
| "Write code that can be tested" | "Write testable code" |
| "Don't repeat the same code" | "DRY code" |

### 5. Scope Implicitly

Don't over-specify when context makes it clear:

| Before | After |
|--------|-------|
| "In this Python project, use snake_case" | "Use snake_case" |
| "When writing React components, use hooks" | "Use React hooks" |
| "For all database queries, use parameterized queries" | "Parameterized queries only" |

## Rule Patterns

### Security Rules

```markdown
Never commit secrets
Never log passwords
Sanitize all user input
Parameterized queries only
Validate auth on all endpoints
```

### Code Style Rules

```markdown
snake_case for Python
camelCase for TypeScript
Max 100 chars per line
One class per file
```

### Git Rules

```markdown
Feature branches only
Run tests before commit
Conventional commit messages
No force push to main
```

### Architecture Rules

```markdown
Services in /services
Components in /components
No business logic in controllers
Dependency injection for testing
```

## Placement Decision

| Rule Type | Location | Example |
|-----------|----------|---------|
| Security-critical | CLAUDE.md | "Never commit secrets" |
| Universal (80%+ tasks) | CLAUDE.md | "Run tests before commit" |
| Language-specific | .claude/rules/[lang].md | "Use Pydantic for validation" |
| Framework-specific | .claude/rules/[framework].md | "Use React Query for API calls" |
| With examples needed | .claude/rules/[domain].md | Complex patterns |

## Optimization Process

### Step 1: Draft

Write the rule naturally:
```
"When working with the database, you should always make sure to use
parameterized queries to prevent SQL injection attacks"
```

### Step 2: Extract Core

Identify the essential constraint:
```
Use parameterized queries
```

### Step 3: Add Minimal Context

Only if ambiguity exists:
```
Parameterized queries for all DB access
```

### Step 4: Verify

- Is it clear? ✓
- Is it actionable? ✓
- Is it <50 words? ✓ (6 words)
- Could it be shorter without losing meaning? No

### Step 5: Final

```
Parameterized queries for all DB access
```

## Anti-Patterns

### Avoid: Explanatory Rules

```markdown
# Bad - includes explanation
Never commit .env files because they contain sensitive information
that could be exposed if the repository is public

# Good - just the rule
Never commit .env files
```

### Avoid: Conditional Chains

```markdown
# Bad - too many conditions
If working on frontend, use React, and if using React, use hooks,
and if using hooks, prefer useCallback for functions

# Good - separate rules
Use React hooks
Prefer useCallback for callback functions
```

### Avoid: Vague Rules

```markdown
# Bad - not actionable
Write good code
Be careful with security
Think about performance

# Good - specific and actionable
Max cyclomatic complexity: 10
Sanitize all user input
Index foreign keys
```

### Avoid: Duplicate Intent

```markdown
# Bad - same intent, different words
Never expose secrets
Don't commit API keys
Keep credentials out of code

# Good - one comprehensive rule
Never commit secrets (keys, tokens, passwords)
```

## Context File Rules

Rules in `.claude/rules/*.md` can be slightly longer since they load on-demand. Still aim for brevity:

```markdown
# .claude/rules/python.md

## Patterns

- Pydantic for API validation
- AsyncIO for I/O operations
- Type hints on public functions
- Pytest for testing

## Avoid

- Global mutable state
- Bare except clauses
- String concatenation for SQL
```

## Measuring Success

### Before Optimization

```markdown
# CLAUDE.md - 847 words

You should always make sure that whenever you're working with this
project, you remember to never commit any files that contain secrets,
API keys, passwords, or any other sensitive information...

[continues for pages]
```

### After Optimization

```markdown
# CLAUDE.md - 127 words

## Security
- Never commit secrets
- Sanitize user input
- Hash passwords

## Git
- Feature branches only
- Run tests before commit

## Code
- snake_case (Python)
- camelCase (TypeScript)
- Max 100 chars/line

## Context
| Task | Read |
|------|------|
| Python | .claude/rules/python.md |
| React | .claude/rules/react.md |
```

**Result:** 85% token reduction, same coverage.

## Quick Reference

### Rule Checklist

- [ ] <50 words
- [ ] Starts with verb (imperative)
- [ ] No filler words
- [ ] Specific and actionable
- [ ] Not duplicating existing rule
- [ ] Correct placement (critical vs context)

### Word Budget Guide

| Component | Words |
|-----------|-------|
| Single rule | 3-10 |
| Rule with qualifier | 10-20 |
| Rule with example | 20-40 |
| Maximum | 50 |
