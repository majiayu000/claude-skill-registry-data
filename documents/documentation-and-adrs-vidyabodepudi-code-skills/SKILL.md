---
name: documentation-and-adrs
description: >
  Documentation standards and Architecture Decision Records (ADRs).
  Use when documenting features, APIs, or architectural decisions.
  Covers inline docs, README structure, API docs, and ADR format.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
triggers:
  - context: "writing documentation"
  - context: "recording a design decision"
  - context: "updating README"
  - command: "/ship"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
author: codehands-core
signed: true
tier: 2
---

## Overview

Documentation has two purposes: help new readers understand the system (docs) and help future readers understand why decisions were made (ADRs). Both are engineering artifacts, not afterthoughts.

## When to Use

- When completing a feature (update relevant docs)
- When making a significant design decision (write an ADR)
- When onboarding new contributors
- During `/ship` phase

## Process

### 1. Code Documentation

- **Self-documenting code first** — clear naming eliminates most need for comments
- **Comments explain WHY, not WHAT** — the code says WHAT, comments explain WHY
- **API documentation** — public functions/methods need docstrings with params, returns, errors
- **No stale comments** — if the code changes, the comment changes

### 2. ADR Format

For significant decisions, write an Architecture Decision Record:

```markdown
# ADR-NNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[What prompted this decision? What constraints exist?]

## Decision
[What did we decide? Be specific.]

## Consequences
[What are the positive and negative effects of this decision?]
```

Save to: `docs/adrs/NNN-title.md`

### 3. When to Write an ADR

- Choosing a framework, library, or tool
- Changing architecture patterns
- Defining API conventions
- Making security/compliance decisions
- Any decision future contributors might question

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The code is self-documenting" | Code shows WHAT and HOW. It never shows WHY. When someone asks "why did we use X instead of Y?", only an ADR answers that. |
| "We can document later" | Documentation written at decision time captures context that's lost within weeks. Write it now. |
| "Nobody reads documentation" | Bad documentation isn't read. Good documentation (concise, accurate, findable) saves hours. |

## Red Flags

- Comments that describe WHAT instead of WHY
- Stale comments that don't match current code
- Significant design decisions without ADRs
- README that doesn't reflect current project state

## Verification

- [ ] Public APIs have docstrings
- [ ] Comments explain WHY, not WHAT
- [ ] Significant decisions have ADRs
- [ ] README is current and accurate
- [ ] No stale comments in modified code

## See Also

- `codehands:spec-driven-development` — Specs that docs reference
- `codehands:api-and-interface-design` — API documentation
