---
name: new-project
disable-model-invocation: true
description: Create a new Apeiron project and open it
argument-hint: <project name> [template]
---

Create a new Apeiron project named `$1` (template `$2` if given). Use the `ngine` MCP server:
`ngine.recipes` lists the authored workflows and `project.new` and `project.templates` create and
list templates — read `ngine.describe` for the exact arguments before calling. After it exists, open
it, then call `editor.context` and tell me the project folder, so a new Claude Code session started
there attaches to the same editor.
