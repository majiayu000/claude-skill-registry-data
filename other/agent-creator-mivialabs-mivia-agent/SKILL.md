---
name: agent-creator
description: Author a safe project agent definition with valid frontmatter, bounded authority, skill-tool closure, and passing repository gates.
triggers:
  - create an agent
  - author a named agent
  - write an agent definition
  - add a subagent role
  - create an agents md file
  - configure a project agent
short-description: Author and validate a project agent
argument-hint: "Agent purpose, authority, skills, and boundaries"
user-invocable: true
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - search_replace
  - run_command
---

This skill is defined in `.agents/skills/agent-creator/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
