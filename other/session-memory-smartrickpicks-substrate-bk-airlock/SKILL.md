---
name: session-memory
description: Per-user persistent session state management via session-manager.py
---

# Session Memory

Load, update, and persist per-user session state across conversations using the airlock-persona session layer. Enables Otto to carry behavioral context, prior decisions, and task continuity across separate Claude Code invocations.

## Integration

This skill integrates directly with the `airlock-persona` repo. It does not delegate to superpowers or ECC — it is an Airlock-native capability that wraps `sessions/session-manager.py`.

- `session-manager.py load <user>` — Read the current session state for a user
- `session-manager.py warm-start <user>` — Generate a context block to prime the conversation
- `session-manager.py begin <user>` — Initialize a new session for a user
- `session-manager.py end <user> --persona <name> --chamber <name> --summary "..."` — Close and persist a session

## Standalone Behavior

- Always call `warm-start` at the top of a new conversation if a session exists for the user
- Surface session context (active persona, chamber, recent summary) in the first presence line
- Never write to session files directly — all writes must go through `session-manager.py` to pass schema validation
- On task completion, call `end` with the active persona, chamber, and a one-sentence summary of what was accomplished
- If no session exists for a user, call `begin` before any other session operations
