---
name: cobbler
description: Invoke Elves Cobbler, the default orchestration model for fitted answers and agent routing. Use when the user types /cobbler or asks for Cobbler coordination in Claude Code.
disable-model-invocation: true
---

<!-- elves-managed-alias: claude-skill-alias v1 -->

# Cobbler

This is an Elves-managed Claude Code alias for `/cobbler`.

This alias invokes Cobbler, Elves' default orchestration model. Use the installed `elves` skill's
`## Cobbler` instructions as the source of truth. Classify the request first: one-off advice uses
Quick Cobbler, while implementation or active-run requests use Cobbler-first Elves coordination.
For non-trivial tasks, use the main skill's harness loop: capability scan, route and medium selection,
context packet, execute agents/tools/skills, collect evidence, fit answer,
present/record, and reclassify when evidence changes the task.
Use route and medium selection before dispatch.

Default behavior:

1. For one-off Quick Cobbler answers, stay read-only and stateless.
2. For implementation or active-run requests, route work through Cobbler-first Elves coordination;
   worker agents may edit scoped files under the normal Elves rules.
3. Use Claude Code subagents first when independent lenses or workers help.
4. Fall back to direct analysis or direct implementation when subagents are unavailable.
5. Return one fitted answer with `Recommendation`, `Why this fits`, `Strongest dissent`, `Risks`,
   `Next move`, and `Confidence`.

Normal Cobbler use must not require OpenRouter or any external provider key.
