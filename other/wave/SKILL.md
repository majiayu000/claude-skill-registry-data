---
name: wave
description: Run one gated Codex wave — plan, you approve, Codex implements, you review
argument-hint: <slug> <brief.md>
allowed-tools: Bash, Read, Write
---

Load the `codex-claude-loop` skill and run one wave for `$ARGUMENTS`, following the
skill's cycle and its rails exactly. You are the gate, so do not hand both decisions to
`cl_wave` and walk away.

Two things this command adds on top of the skill:

1. **If no brief file was given, write one first** and show it to the user: goal,
   constraints, acceptance criteria, out of scope. The loop can only be as good as its
   brief, and a vague brief produces a plan you cannot judge.
2. **Report at the end**: what landed, what you sent back and why, what is still open.
