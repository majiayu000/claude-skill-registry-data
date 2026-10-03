---
name: why
description: "Recover why a Roblox design or implementation exists from project decisions, source history, current code, and authored context."
---

# Explain why the Roblox design exists

Build an evidence chain in this order:

1. Repository design, architecture, security, authoring, and handoff documents.
2. Current source and the constraints visible in its call sites, data shapes, remotes, lifecycle, and tests.
3. Git history for the relevant files, commits, and blame lines when the current tree does not preserve the reason.
4. Roblox Studio context inspection, or scoped non-playtest fallback edits when Repository mode is unavailable and the task explicitly requires an authored change.
5. External sources only when the user asks or the decision depends on current Roblox platform behavior.

Return the decision, supporting evidence, rejected or likely alternatives, current tradeoff, and confidence. Label inference. Do not turn absence of evidence into a confident rationale. Use `$how` when the question is about runtime behavior rather than motivation. Never use Roblox Studio MCP playtest controls.
