---
name: ak-help
description: "Open the AgentKit help index of skills, commands and workflows."
when_to_use: "Invoke when users ask how to use ak or which workflow to run."
category: meta
keywords: [help, index, commands, skills, usage]
argument-hint: "[topic|skill|command]"
metadata:
  author: agentkit
  version: "1.0.1"
---

# Help

Open the AgentKit help index when users ask how to use `ak`, what skills are available, or which workflow fits their task.

Use the runtime's installed-skill catalog when available. Otherwise discover
current `SKILL.md` files from the active project and user skill roots, then read
frontmatter only for relevant candidates. Do not rely on a bundled catalog,
copied count, or remembered skill list.

Summarize only the candidates that fit the request. Route to the most specific
installed skill when the user's task is clear; state plainly when a referenced
skill is not installed.

When the user needs a command, read current `ak --help` or the relevant command
help and keep examples scoped to the installed AgentKit kit. Help prose is not a
command registry.

If aliases collide or project/user skills shadow each other, identify the runtime-resolved owner and scope before routing. Explain ambiguity from the live catalog instead of invoking the first matching name. Command-help questions need only that command’s help, not the full skill catalog.
