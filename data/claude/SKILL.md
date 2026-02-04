---
name: get-shit-done
description: Structured spec-driven workflow for planning and executing software projects with Claude Code.
---

# Get Shit Done (GSD) Skill for Claude Code

## When to use
- Use this skill when the user asks for GSD or uses a `{{COMMAND_PREFIX}}*` command.
- Use it for structured planning, phase execution, verification, or roadmap work.


## How to run commands
Claude Code supports custom slash commands. Commands starting with `{{COMMAND_PREFIX}}` are custom skills.

Commands are installed as individual skills in `{{PLATFORM_ROOT}}/skills/`. Load the corresponding skill:

`{{PLATFORM_ROOT}}/skills/gsd-<command>/SKILL.md`

Example:
- `{{COMMAND_PREFIX}}new-project` -> `{{PLATFORM_ROOT}}/skills/gsd-new-project/SKILL.md`
- `{{COMMAND_PREFIX}}help` -> `{{PLATFORM_ROOT}}/skills/gsd-help/SKILL.md`


## File references
Command files and workflows include `@path` references. These are mandatory context. Use the Read tool to load each referenced file before proceeding.

## Tool mapping
- "Bash tool" → use the Bash tool
- "Read/Write" → use Read/Write tools
- "AskUserQuestion" → ask directly in chat and provide explicit numbered options
- "Task/subagent" → prefer a matching custom agent from `{{PLATFORM_ROOT}}/agents` when available; otherwise adopt that role in-place


## Output expectations
Follow the XML or markdown formats defined in the command and template files exactly. These files are operational prompts, not documentation.

## Paths
Resources are installed under `{{PLATFORM_ROOT}}/get-shit-done`. Individual skills are under `{{PLATFORM_ROOT}}/skills/gsd-*/`. Use those paths when command content references platform paths.
