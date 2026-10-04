---
name: memories-housekeeping
description: Audit .agents/memories/ for staleness, duplicates, and orphan facts. Mark stale entries, propose archive moves, surface near-duplicates. Use for monthly accuracy passes.
triggers:
  - memory audit
  - memory housekeeping
  - audit memories
  - trim memories
tools:
  - read_file
  - list_dir
  - grep
  - write_file
  - search_replace
  - delete_file
argument-hint: "Optional scope: 'all' (default) or 'stale-only'"
user-invocable: true
---

This skill is defined in `.agents/skills/memories-housekeeping/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
