---
name: coach
description: Read my interview method or practice it in a mock interview.
disable-model-invocation: true
---

# /coach [mock <HR | system design | topic>]

Files: `templates/`, `scripts/`, `docs/`, `examples/` and `routines/` are in the method root, `${CLAUDE_PLUGIN_ROOT}` (the clone holding this skill when that is not replaced by a path); every other relative path is in the workspace, the current folder. Before acting on the person's behalf, read `profile.md`, `docs/rules.md` and the workspace `rules.md`; the workspace one wins on conflict.

The method is `docs/interview-method.md`.

- `/coach` prints the method.
- `/coach mock <HR | system design | topic>` runs a mock in chat: you play the interviewer and ask one question at a time. After each answer, grade it against the Rubric lines in the method that apply to that answer, in three lines: what worked, what to fix, the better line. Text cannot hear silence, so ask the person to type the clarifying questions they would ask out loud before answering.
