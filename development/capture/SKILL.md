---
name: capture
description: Write a durable decision, gotcha, or correction to .agents/memories/ as one Markdown file. Use after non-obvious decisions, corrected assumptions, or debugging detours.
triggers:
  - capture decision
  - remember this
  - log a memory
  - capture gotcha
tools:
  - read_file
  - grep
  - glob
  - write_file
argument-hint: "Title or one-sentence statement (required)"
user-invocable: true
---

This skill is defined in `.agents/skills/capture/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
