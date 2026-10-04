---
name: concurrency-review
description: Review concurrency design for races, leaks, and cancellation bugs. Portable, language-agnostic. In-process concurrency is the default; process fan-out is not.
triggers:
  - concurrency review
  - race review
  - parallel agents architecture
  - thread safety review
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/concurrency-review/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
