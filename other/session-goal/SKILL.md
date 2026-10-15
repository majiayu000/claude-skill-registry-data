---
name: session-goal
description: "Pin session objectives to prevent scope creep. Use for alignment across long multi-agent sessions."
context: fork
globs: []
alwaysApply: false
---

# Session Goal — Alignment Anchor

Use this skill to pin a session objective at the start of a long or complex session. All subsequent todos, delegation decisions, and verification steps must align with the pinned goal.

---

## Usage

Invoke via the `/focus` command:

```
/focus Implement JWT authentication with refresh token rotation
```

Or state it explicitly at the start of a session:

```
SESSION GOAL: Add product review feature with backend, frontend, and database layers.
All work in this session must serve this goal.
```

---

## What Pinning a Goal Does

1. **Focuses todos** — every todo added must relate to the goal
2. **Focuses delegation** — Zeus only invokes agents relevant to the goal
3. **Focuses verification** — Themis checks that implementations serve the goal
4. **Surfaces drift** — if a task drifts from the goal, flag it before proceeding

---

## Goal Format

A good session goal has 4 components:

```
GOAL: <What to build>
SCOPE: <Which layers/modules are in scope>
SUCCESS CRITERIA: <How we know it's done>
OUT OF SCOPE: <What to explicitly exclude>
```

**Example:**
```
GOAL: Add email verification to the registration flow
SCOPE: Backend (POST /auth/verify, token model), Frontend (VerifyEmail page), DB (verification_tokens table)
SUCCESS CRITERIA: User can register, receive a verification email link, click it, and have their account marked as verified. All layers tested >80% coverage.
OUT OF SCOPE: Password reset, 2FA, email template design
```

---

## Alignment Check Pattern

Before each major delegation or decision, run this quick check:

> "Does this task directly serve the pinned goal?"
> - **Yes** → proceed
> - **Partial** → flag the out-of-scope portion and ask for clarification
> - **No** → defer to a future session, note it as a separate task

---

## Cross-Session Persistence

For goals that span multiple sessions, write the goal to `/memories/session/`:

```
/memories/session/current-goal.md

# Active Session Goal
Goal: Implement JWT authentication
Started: 2026-05-15
Status: Phase 2 of 3 (backend done, frontend in progress)
Next: POST /auth/refresh endpoint
```

This ensures the goal survives context compaction and session restarts.

---

## When to Update the Goal

- When the user explicitly redirects the session
- When a phase completes and the next phase has a different scope
- When an unexpected blocker changes the scope

Never silently drift from the goal — always confirm with the user before changing it.

---

## Session Reuse (Cross-Task Continuity)

Reuse agent sessions between related delegations to avoid re-reading files and re-building context.

### When to Reuse

Prefer reusing an existing session when:
- Follow-up task touches the **same files** or **same feature thread** as a previous delegation
- The specialist already loaded relevant file context in the prior session
- Debugging continues on the same stack trace or module

### When to Start Fresh

Force a new session when:
- Unrelated feature or different part of the codebase
- Previous session has too much noise from an abandoned investigation
- The specialist's accumulated context would mislead the new task

### How to Signal Reuse

When dispatching a follow-up task, include the session reuse context explicitly:

```
@hermes — continuing the auth endpoint work from the previous session.
Files already explored: backend/routers/auth.py, backend/services/auth_service.py.
New task: add refresh token rotation.
```

### Session Tracking

Zeus tracks active sessions with a `task_id` per delegation:

| Agent | Active Session | Files in Context | Max Age |
|-------|---------------|-----------------|---------|
| hermes | ses_abc123 | 4 files | 15 min |
| aphrodite | ses_def456 | 3 files | 15 min |

When `session_max: 2` is set in routing.yml, Zeus keeps the last 2 sessions for that agent and discards older ones. This prevents stale context from accumulating.
