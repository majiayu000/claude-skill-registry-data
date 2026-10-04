---
name: memory
description: Persist decisions, preferences, and project state across sessions using structured memory types
triggers:
  - memory
  - remember this
  - save for next session
  - persist
  - cross-session
---

# Memory

Sync important context to persistent storage so future sessions start informed.

## Memory Types

| Type            | What it stores                                       | Storage location                |
| --------------- | ---------------------------------------------------- | ------------------------------- |
| **Decisions**   | Architecture choices, API design, naming conventions | `.agents/memory/decisions.md`   |
| **Preferences** | Code style, commit format, PR template               | `.agents/memory/preferences.md` |
| **Blockers**    | Known issues, dependency constraints, quirks         | `.agents/memory/blockers.md`    |
| **Episodic**    | Timestamped event log — what happened and why        | `.agents/memory/episodes.md`    |
| **Semantic**    | Domain concepts, entity relationships, glossary      | `.agents/memory/semantic.md`    |

## What to Remember

| Category        | Priority | Examples                                                 |
| --------------- | -------- | -------------------------------------------------------- |
| Decisions       | high     | Architecture choices, API design, naming conventions     |
| Preferences     | high     | Code style, commit format, PR template                   |
| Blockers        | high     | Known issues, dependency constraints, environment quirks |
| Episodic events | medium   | What was tried, what failed, what succeeded and why      |
| Progress        | medium   | Completed phases, shipped PRs, release history           |
| Context         | medium   | Team members, repo relationships, deployment targets     |

## What NOT to Remember

- Transient debugging output
- Tool execution logs
- Completed todo items (already in git history)
- Session-specific file reads
- Information derivable from reading the codebase

## Episodic Memory Pattern

Record significant events with context so future sessions can learn from them:

```markdown
## 2026-04-10 — Auth middleware rewrite

- **What**: Replaced JWT validation middleware with JWKS-based approach
- **Why**: Compliance requirement from legal (session token storage)
- **Outcome**: 3 tests added, all green, deployed to staging
- **Gotcha**: `validateToken()` now async — callers needed await
```

## Semantic Memory Pattern

Store domain knowledge and entity relationships:

```markdown
## Domain: Payments

- Order → has many → LineItems
- Payment → belongs to → Order
- Refund → references → Payment.id
- Rule: never delete a Payment; set status = 'refunded' instead
```

## Steps

1. Identify decisions, preferences, blockers, or events from the current session
2. Check if they already exist in memory (avoid duplicates)
3. Write to the appropriate storage location with today's date
4. Remove entries that are no longer true

## Rules

- Write memory at session end, not continuously
- Keep entries concise — one line per decision, dated entries for episodes
- Date-stamp all entries for staleness detection
- Remove entries that are no longer true
- Memory is supplementary — the codebase is the source of truth
- Never store credentials, tokens, or secrets in memory files
