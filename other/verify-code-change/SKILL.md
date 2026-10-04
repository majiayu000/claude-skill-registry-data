---
name: verify-code-change
description: Verify an implemented code or config change with evidence scaled to risk and blast radius. Portable, language-agnostic. Use after an executable artifact changes, before claiming completion.
triggers:
  - verify code change
  - verify this change
  - did this change work
  - pre-merge verify
  - check before merge
  - is this ready to merge
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - run_command
---

This skill is defined in `.agents/skills/verify-code-change/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
