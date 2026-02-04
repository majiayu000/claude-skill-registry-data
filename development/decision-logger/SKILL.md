---
name: decision-logger
description: |
  Logs architectural decisions to docs/DECISIONS.md in ADR format.
  Use when: making significant architectural or technology choices.
  Integrates with /craft and /why commands.
---

# Decision Logger

Automatically logs architectural decisions in ADR (Architecture Decision Record) format.

## When to Use

Log a decision when:
- Choosing a technology stack
- Selecting a library over alternatives
- Defining project structure
- Making trade-off decisions
- Changing established patterns

## ADR Format

```markdown
## ADR-{number}: {title}

**Date:** {YYYY-MM-DD}
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX

### Context
{What is the issue we're seeing that motivates this decision?}

### Decision
{What is the change we're proposing/have agreed to implement?}

### Consequences

**Positive:**
- {benefit_1}
- {benefit_2}

**Negative:**
- {tradeoff_1}
- {tradeoff_2}

**Neutral:**
- {implication}

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| {option_1} | {reason} |
| {option_2} | {reason} |
```

## Process

### 1. Check for docs/DECISIONS.md

```bash
test -f docs/DECISIONS.md || mkdir -p docs && touch docs/DECISIONS.md
```

If file doesn't exist, create with header:
```markdown
# Architecture Decision Records

This document captures significant architectural decisions made during development.

Format: [ADR (Architecture Decision Record)](https://adr.github.io/)

---
```

### 2. Determine Next ADR Number

Parse existing file for highest ADR number:
```
ADR-001, ADR-002, ... → next is ADR-003
```

### 3. Gather Decision Details

Required fields:
- **title**: Short description (e.g., "Use SQLite for storage")
- **context**: Why this decision is needed
- **decision**: What was chosen
- **consequences**: Impact of the decision
- **alternatives**: What else was considered

### 4. Append to File

Add new ADR at the end of docs/DECISIONS.md.

## Integration Points

### With /craft
During project creation, automatically log:
- ADR-001: Technology Stack
- ADR-002: Project Structure
- ADR-003: Database Choice (if applicable)

### With /why
`/why` reads from docs/DECISIONS.md to provide context for past decisions.

### With /next
When implementing features that require architectural choices, prompt to log decision.

## Example Decisions

### Technology Stack
```markdown
## ADR-001: Rust + Axum for Backend

**Date:** 2025-01-15
**Status:** Accepted

### Context
Building a notes app that needs fast response times (<50ms) and single-binary deployment.

### Decision
Use Rust with Axum web framework.

### Consequences

**Positive:**
- Sub-millisecond response times achievable
- Single binary, no runtime dependencies
- Memory safety guarantees

**Negative:**
- Steeper learning curve than Go or Node.js
- Longer compile times
- Smaller ecosystem for web libraries

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Go + Chi | Less type safety, wanted stronger guarantees |
| Node + Hono | Not single binary, runtime required |
| Python + FastAPI | Too slow for <50ms requirement |
```

### Database Choice
```markdown
## ADR-002: SQLite for Persistence

**Date:** 2025-01-15
**Status:** Accepted

### Context
Single-user notes app needs persistent storage. Simplicity and portability are priorities.

### Decision
Use SQLite with sqlx for database operations.

### Consequences

**Positive:**
- Zero configuration required
- Database is a single file (portable)
- Fast for single-user workloads
- Compile-time SQL checking with sqlx

**Negative:**
- No concurrent write support
- Limited to single machine
- Manual migration management

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| PostgreSQL | Overkill for single-user, requires setup |
| In-memory | Data lost on restart, requirement violation |
| File-based JSON | No query capabilities, slow for large data |
```

## Output

After logging, confirm:
```
Logged: ADR-{number} "{title}"
View: docs/DECISIONS.md
Query: /why {topic}
```
