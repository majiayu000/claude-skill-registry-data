---
name: handoff
description: "Generate session handoff documents for work continuation. Use when transitioning between sessions."
context: fork
globs: []
alwaysApply: false
---

# Handoff — Session Continuation Summary

Use this skill to generate a structured handoff summary when transitioning work to a new session.

**Policy-safe storage:** keep handoffs in `/memories/session/` during the conversation. Do not create ad-hoc `.md` files in the repository root.

---

## When to Use

- Session is ending but work is incomplete
- Computer crash or logout mid-feature
- Switching to a different machine
- User wants to start fresh but continue the same work
- Context window is getting full and a fresh session would help

---

## Handoff Format

```markdown
# Handoff: <Feature Name>

## Current Status
- Wave N completed (<description>)
- Wave N+1 pending (<description>)
- Current task: <what was being worked on>

## What Was Completed
- <file/path> — <what was implemented>
- <file/path> — <what was implemented>
- <file/path> — <what was implemented>

## Remaining Work
- <remaining task 1>
- <remaining task 2>
- <remaining task 3>

## Key Decisions
- <decision 1> (rationale)
- <decision 2> (rationale)

## Learnings (from wisdom accumulation)
- <convention 1>
- <gotcha 1>
- <failure to avoid 1>

## Relevant Files
- <path/to/file1>
- <path/to/file2>
- <path/to/file3>

## Tasks Status (if using Task System)
- T-001 [completed] <subject>
- T-002 [completed] <subject>
- T-003 [in_progress] <subject>
- T-004 [pending] <subject>

## Next Steps
1. <immediate next action>
2. <following action>
3. <eventual action>
```

---

## How to Persist Handoff (Policy-Compliant)

When user runs `/handoff`:

```
1. Mnemosyne reads current session state
2. Mnemosyne reads /memories/session/* (if relevant)
3. Mnemosyne generates handoff summary
4. Mnemosyne saves to /memories/session/handoff-<timestamp>.md
5. Mnemosyne outputs the summary in chat
6. At sprint close, promote only durable context to .pantheon/memory-bank via explicit @mnemosyne action
```

---

## How New Session Uses Handoff

When starting a new session:

```
1. User pastes handoff document (or references file path)
2. New session reads handoff
3. Agent resumes from "Next Steps"
4. Tasks continue from last known state
5. Learnings are re-injected
```

---

## Example

```markdown
# Handoff: Product Reviews

## Current Status
- Wave 2 completed (backend endpoints + frontend with mocks)
- Wave 3 pending (real API integration)
- Current task: Connecting ReviewCard to real GET /reviews API

## What Was Completed
- src/routes/reviews/post.py — POST /reviews endpoint
- src/routes/reviews/get.py — GET /reviews with pagination
- src/components/ReviewCard.tsx — ReviewCard with mocked data
- alembic/versions/xxx_reviews.py — reviews table migration

## Remaining Work
- Connect ReviewCard to real GET /reviews API
- Add ReviewForm component
- Integration tests
- Error handling for 404/500

## Key Decisions
- Use Redis for review cache (TTL 5min) — decided after Wave 2 performance testing
- Cursor-based pagination, not offset — better for large datasets

## Learnings
- Convention: API returns snake_case, frontend converts to camelCase
- Gotcha: Reviews table needs composite index on (product_id, created_at)
- Failure: Don't use session.commit() in async — use await session.flush()

## Arquivos relevantes
- src/routes/reviews/
- src/components/ReviewCard.tsx
- src/components/ReviewForm.tsx (not created yet)
- alembic/versions/xxx_reviews.py

## Tasks Status
- T-001 [completed] Create reviews schema
- T-002 [completed] Implement POST /reviews
- T-003 [completed] Implement GET /reviews
- T-004 [completed] Build ReviewCard component
- T-005 [pending] Connect to real API
- T-006 [pending] Build ReviewForm
- T-007 [pending] Integration tests

## Next Steps
1. Update ReviewCard to call GET /reviews API (replace mock data)
2. Create ReviewForm component with POST /reviews integration
3. Write integration tests for full review flow
```

---

## Relationship with Memory Bank

| System | Scope | Duration |
|--------|-------|----------|
| `/memories/repo/` | Permanent facts | Forever |
| `.pantheon/memory-bank/` | Project context | Sprint |
| **`/memories/session/handoff-*.md`** | **Session handoff snapshot** | **Until session ends** |

Handoff is the most temporary — it's a snapshot of the current session for seamless continuation.
