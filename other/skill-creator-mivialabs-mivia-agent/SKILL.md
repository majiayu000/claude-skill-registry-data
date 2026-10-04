---
name: skill-creator
description: Author a new project skill with valid frontmatter, a usable procedure, a matching Claude alias, and passing repository gates.
triggers:
  - create a skill
  - author a new skill
  - write a SKILL.md
  - add a project skill
  - make a skill for this repository
  - scaffold a skill procedure
short-description: Author and validate a project skill
argument-hint: "Skill purpose, users, and required tools"
user-invocable: true
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - run_command
---

This skill is defined in `.agents/skills/skill-creator/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
