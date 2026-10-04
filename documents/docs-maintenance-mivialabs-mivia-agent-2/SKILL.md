---
name: docs-maintenance
description: Maintain the mivia-agent documentation. Trigger when the user asks to update, tidy, or restructure docs, when a code change needs docs updated, or when docs are out of date, wordy, or inconsistent.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - write_file
  - search_replace
---

This skill is defined in `.agents/skills/docs-maintenance/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
