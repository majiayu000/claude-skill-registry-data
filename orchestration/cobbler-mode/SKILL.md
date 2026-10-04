---
name: cobbler-mode
description: Turn on Elves Cobbler Mode for the current Claude Code thread. Use when the user types /cobbler-mode or asks to keep chatting with the Cobbler by default.
disable-model-invocation: true
---

<!-- elves-managed-alias: claude-skill-alias v1 -->

# Cobbler Mode

This is an Elves-managed Claude Code alias for `/cobbler-mode`.

Use the installed `elves` skill's `## Cobbler` instructions as the source of truth. Cobbler is
Elves' default orchestration model. Cobbler Mode is the lowest-friction current-thread way to keep
follow-up prompts Cobbler-mediated after the user says "Cobbler Mode: on" and until the user says
"Cobbler Mode: off" or "leave Cobbler Mode."
For non-trivial tasks, use the main skill's harness loop: capability scan, route and medium selection,
context packet, execute agents/tools/skills, collect evidence, fit answer,
present/record, and reclassify when evidence changes the task.
Use route and medium selection before dispatch.

Default behavior while Cobbler Mode is active:

1. Treat follow-up prompts as Cobbler-mediated by default.
2. Answer directly when the task is simple.
3. For one-off Quick Cobbler answers, stay read-only and stateless.
4. Use Claude Code subagents first when independent lenses help.
5. For implementation or active-run requests, route work through Cobbler-first Elves coordination;
   worker agents may edit scoped files under the normal Elves rules.
6. Return one fitted answer with `Recommendation`, `Why this fits`, `Strongest dissent`, `Risks`,
   `Next move`, and `Confidence` when synthesis is useful.

Cobbler Mode is current-thread conversation state, not durable run state. It is not a daemon and
must not require OpenRouter or any external provider key.
