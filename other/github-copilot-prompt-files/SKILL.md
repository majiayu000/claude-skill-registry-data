---
name: github-copilot-prompt-files
description: >-
  Use for creating, reviewing, or debugging GitHub Copilot reusable prompt files and slash commands in Visual Studio Code, including .github/prompts/*.prompt.md, inputs, context links, agent selection, and tool selection. Do not use for always-on rules, multi-step Agent Skills, custom personas, or VS Code extension commands.
argument-hint: "[repeatable task, inputs, expected output, and allowed tools]"
---

# GitHub Copilot prompt files

Create one manually invoked command for one focused task. Inspect the active
VS Code prompt schema and available agent/tool identifiers first.

## Workflow

1. Define the input variables, attached context, output artifact, allowed tools,
   and completion evidence.
2. Store workspace prompts as `.github/prompts/<name>.prompt.md`; use user scope
   only for a genuinely cross-project command.
3. Add only needed frontmatter: `name`, `description`, `argument-hint`, `agent`,
   `model`, and `tools` are currently supported.
4. Write an ordered task contract. Use `${input:name:placeholder}` for missing
   values and relative Markdown links for repository context.
5. Give the prompt the smallest tool list. A prompt's `tools` overrides tools
   inherited from its selected agent; unavailable tools can be ignored.
6. Run from the editor and slash menu, then verify the output rather than the
   response wording.

## Rules

- Use a prompt for deliberate one-task invocation. Use a skill for automatic
  discovery, multi-step expertise, scripts, or resources.
- Omit `model` unless the task genuinely requires a verified model capability.
- Do not hardcode current selections, secrets, absolute paths, or undocumented
  tool identifiers.
- Reference shared instructions instead of duplicating them.
- Ask only for inputs not discoverable from the workspace.

Read [the prompt contract](references/artifact-contracts.md), use [evaluated
patterns](references/patterns.md), and follow [verification](references/verification.md).

## Completion

Frontmatter parses; every input is consumed; links resolve; tools are available
and least privilege; the slash command is discoverable; positive and malformed
inputs produce the declared artifacts; a nearby non-command task stays outside.
