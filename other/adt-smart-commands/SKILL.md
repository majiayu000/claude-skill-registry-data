---
name: smart-commands
description: Decision guide for when to proactively use Claude Code slash commands — /think, /model, /compact, /clear. Use when choosing whether to invoke a command before or during a task, or when a complexity-classifier hook has flagged a task as high or critical. Pairs with the complexity-classifier UserPromptSubmit hook.
triggers:
  - smart commands
  - when to use /think
  - when to compact
  - should I switch models
  - use extended thinking
  - /think
  - /compact
  - /model
  - /clear
  - slash commands
---

# smart-commands

When to invoke Claude Code slash commands — and when not to.

## /think — Extended reasoning

**Use before:**
- Designing something you'll have to live with (API contracts, schema, auth flow)
- Debugging a non-obvious issue where first guess is likely wrong
- Security-sensitive decisions (anything touching auth, secrets, permissions)
- When the complexity-classifier fires `[AUTO] CRITICAL`

**Skip when:**
- The task is mechanical (rename, format, add field)
- You already know the answer with high confidence
- It's a lookup or grep task

**How:** Type `/think` before your first action on the task.

---

## /model — Switch model

| Switch to | When |
|-----------|------|
| `/model claude-opus-4-7` | Sustained security/architecture work (>5 turns), incident response, risky migrations |
| `/model claude-sonnet-4-6` | Normal coding work (default) |
| `/model claude-haiku-4-5` | Repetitive formatting, bulk triage, quick lookups across many files |

**Rules:**
- Switch back to Sonnet after finishing a critical section — Opus is expensive
- For Agent tool calls, always set `model:` explicitly; the session model is independent
- `CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5-20251001` is the default for subagents

---

## /compact — Context compression

**Use when:**
- Switching to a different feature or codebase area
- Context is at 50%+ and the current task is logically complete
- You're about to start a long phase and want a clean baseline

**Don't use when:**
- Mid-task — compaction may lose intermediate reasoning you need
- The previous turns contain decisions you'll need to defend in the next turn

---

## /clear — Full reset

**Rarely needed.** Use only when:
- Starting a completely unrelated task after a compact is insufficient
- The session has persistent tool failures and state is corrupt

**Never use mid-task** — you'll lose all accumulated context.

---

## Decision tree (quick)

```
Is this security/arch/migration/production?
  YES → /think first, consider /model opus
  NO  → Is this >3 phases or complex debugging?
         YES → /think at key decision points
         NO  → Is context >50% and task is done?
                YES → /compact before next task
                NO  → proceed normally
```

---

## Installation

This skill is paired with a zero-cost `complexity-classifier.sh` hook that auto-injects guidance.

1. Copy `complexity-classifier.sh` to `~/.claude/hooks/`
2. Make it executable: `chmod +x ~/.claude/hooks/complexity-classifier.sh`
3. Add to `settings.json`:

```json
"UserPromptSubmit": [{
  "matcher": "*",
  "hooks": [{
    "type": "command",
    "command": "~/.claude/hooks/complexity-classifier.sh",
    "timeout": 5
  }]
}]
```

The hook fires on every prompt, classifies low/medium/high/critical, and injects `[AUTO]` guidance into systemMessage. No API calls, zero cost.
