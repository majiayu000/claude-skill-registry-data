---
name: always-learning
description: Use at the start of every user turn, and whenever the user starts, pauses, resumes, practices, reviews, or checks progress on a long-term learning subject.
---

# Always Learning

Build durable knowledge through relevant everyday work. Demonstrated retrieval, not exposure, drives progress.

## Route

Run `python3 scripts/state.py status` from this skill directory. State location precedence is `--home`, `ALWAYS_LEARNING_HOME`, `XDG_DATA_HOME/always-learning`, then `~/.local/share/always-learning`.

If registry status fails, report the error and stop stateful teaching. Never repair or overwrite state automatically. Ignore subject issues outside the current semantic scope; report an issue only when its subject is relevant.

If state is unconfigured and the user is not explicitly managing a learning subject, stop silently.

For starting, pausing, resuming, or inspecting subjects, read [subject management](references/subject-management.md).

Otherwise:

1. Treat semantic relevance to an enabled subject as a hard gate. Lexical overlap and overdue status alone never trigger teaching.
2. Among relevant items, prefer overdue, then weaker or older evidence. Never choose randomly.
3. On a clear, non-urgent match, read [the teaching loop](references/teaching-loop.md) and make exactly one smallest useful learning move. Ask for a short prediction before explanation when safe. On ambiguity, stop silently.
4. For urgent or blocking work, complete the task first; use one brief retrospective move only if still relevant.

Honor `skip`, `pause`, and `just answer` immediately. Never delay urgent or safety-critical work. Never promise continuity until state is written and validated. Never record progress before observing the learner's response.
