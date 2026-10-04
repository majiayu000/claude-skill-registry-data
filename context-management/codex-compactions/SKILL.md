---
name: codex-compactions
description: Show how many context compactions the current or other terminal-attached Codex sessions have undergone. Use when the user asks how many times this session has compacted or requests a summary of attached Codex sessions.
---

# Codex Session Compactions

Use the `codex-compactions` command as the source of truth.

- For "this session" or "current session", pass the session's own ID with `codex-compactions --session "$CODEX_SESSION_ID"`. If that variable is unavailable, use `CODEX_THREAD_ID`; do not select a session by recency.
- For up to 100 terminal-attached sessions, run `codex-compactions`.

Report the session name, compaction count, and last activity shown by the command. Every listed session is terminal-attached; do not infer anything about detached sessions.

Interpret the count with the same local health heuristic as the command:

- 0-5 is green. Report the count without a warning.
- 6-11 is yellow. Say the session is in the yellow range and suggest preparing a handoff if focus, constraints, or completed state begin to drift.
- 12 or more is red. Say the session is in the red range and recommend handing off to a fresh session before continuing work that depends heavily on accumulated session state.

These ranges are workflow guidance, not official Codex limits. When reporting multiple sessions, summarize the yellow and red sessions without repeating the full guidance for every row.

If the command is unavailable, report that the tool is not installed or not on `PATH` instead of estimating from session age or transcript size.
