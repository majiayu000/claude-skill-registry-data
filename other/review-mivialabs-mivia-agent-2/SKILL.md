---
name: review
description: Meta-skill that routes a diff to the right per-lens review skill by blast radius. Does not duplicate any lens; it composes them. Use when you have a diff and want to know which skill to run.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/review/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
