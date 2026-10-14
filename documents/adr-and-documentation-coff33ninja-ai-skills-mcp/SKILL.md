---
name: adr-and-documentation
description: Enforces Architecture Decision Records (ADRs) and keeps docs in sync with code. Prevents "why did we do it this way?" questions six months later and stale documentation.
---

# ADR & Documentation

## Problem it solves

Without architectural documentation, teams lose context:
- Six months later, nobody remembers why a decision was made
- Docs drift from code until they're actively misleading
- New team members have no way to understand architectural rationale
- The same debates happen repeatedly because past decisions aren't recorded
- README files are either missing or years out of date

## Protocol

### 1. When to write an ADR

Write an ADR when making a decision that affects the project's architecture:
- Choosing a framework, library, or tool
- Adopting a design pattern or architecture style
- Changing a data model or API contract
- Making a trade-off between competing approaches
- Adding a significant new dependency

Do NOT write ADRs for:
- Trivial implementation details
- Bug fixes
- Standard patterns already documented elsewhere

### 2. ADR format

Each ADR is a short document following this template:

```markdown
# ADR-{NNN}: {Title}

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the problem we're solving? What constraints or forces are at play?

## Decision
What did we decide to do?

## Consequences
What becomes easier or harder? What trade-offs did we accept?
```

Keep ADRs short: 5-10 sentences total. If it's longer than a page, split it.

### 3. Keep docs in sync with code

When changing code:
- Update any related README files in the same commit
- Update API docs, config examples, and setup instructions
- If the change makes existing docs wrong, fix the docs or don't make the change

When adding a feature:
- Document configuration options
- Document environment variables
- Document usage examples

### 4. README maintenance

A README should answer:
- What is this project?
- How do I set it up?
- How do I run it?
- How do I test it?
- How do I deploy it?
- Where is the API documentation?

If a change affects any of these, update the README.

### 5. Code comments vs docs

- Code comments explain WHY, not WHAT (the code already says what)
- Docs explain HOW TO USE, not HOW IT WORKS
- ADRs explain WHY WE CHOSE THIS, not how it works

## Detection triggers

Activate when:
- Choosing between competing approaches or technologies
- Implementing a significant architectural change
- Adding, modifying, or removing a feature
- Starting a new project or component
- User says "document this", "write docs", "create ADR"
- Reviewing a PR and noticing missing documentation
- User asks "why did we do it this way?"

## When NOT to use

- Rapid prototyping or throwaway code
- Trivial changes with no architectural significance
- User explicitly says "no docs needed"

## Cross-references

- **spec-driven-development** — The spec for a feature should include what docs need updating.

- **incremental-implementation** — Each slice includes its documentation updates.

- **code-review** — Review checks that docs are updated alongside code.

- **git-workflow-conventional-commits** — Use `docs:` type for documentation changes. ADRs use `docs:` or `adr:` scope.

- **follow-existing-patterns** — ADRs must match the project's existing ADR format and numbering scheme. READMEs should match the project's documentation conventions.

- **verify-and-cite** — Verify documentation claims against actual code behavior.

- **anti-premature-termination** — Documentation updates are a completion criterion. Do not declare done until docs are updated.
