---
name: SaveContext
description: Persistent memory for AI coding agents. USE WHEN user says "save context", "remember this", "checkpoint", "resume session", "prepare for compaction", "wrap up", OR when starting work on a project that may span sessions.
---

# SaveContext

Save decisions, track progress, and maintain continuity across coding sessions.

## Quick Actions

For most requests, use these patterns directly:

| User Says | Do This |
|-----------|---------|
| "save this decision" | `context_save key="..." value="..." category="decision"` |
| "remember this" | `context_save key="..." value="..." category="note"` |
| "checkpoint" | `context_checkpoint name="..."` |
| "wrap up" | See [WrapUp workflow](#wrap-up) |
| "resume [topic]" | Search sessions, then `context_session_resume` |

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **QuickSave** | "save", "remember", "note this" | `Workflows/QuickSave.md` |
| **SessionStart** | Starting work, "begin session" | `Workflows/SessionStart.md` |
| **WrapUp** | "wrap up", "end of day", "checkpoint everything" | `Workflows/WrapUp.md` |
| **Resume** | "resume", "continue", "pick up where I left off" | `Workflows/Resume.md` |
| **Compaction** | "prepare for compaction", context getting long | `Workflows/Compaction.md` |
| **IssueTracking** | "create issue", "track this bug" | `Workflows/IssueTracking.md` |
| **Planning** | "plan this feature", "implement [complex]", multi-task work | `Workflows/Planning.md` |

## Examples

**Example 1: Quick save during work**
```
User: "remember that we chose JWT over sessions for auth"
→ context_save key="auth-decision" value="Chose JWT over sessions for stateless scaling" category="decision" priority="high"
→ Saved. No session management needed.
```

**Example 2: Starting a work session**
```
User: "let's work on the payment feature"
→ context_session_start name="payment-feature" description="Implementing Stripe integration"
→ Session started (or resumed if exists)
```

**Example 3: Wrapping up**
```
User: "wrap up for today"
→ Invokes WrapUp workflow
→ Saves progress, creates checkpoint, pauses session
```

## Do NOT Automatically

- Start sessions for quick saves (just save the item)
- Run multiple tools when one suffices
- Load full reference docs unless user asks how something works

## Reference

Full tool documentation: `Workflows/Reference.md`
