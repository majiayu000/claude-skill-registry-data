---
name: verify-change
description: Mechanical Go verification of a scoped mivia change. Run test, vet, build, race, invariant and contract gates, then report mivia-report/v1. Use after implementation or before merge.
triggers:
  - verify change
  - verify this
  - run verification
  - pre-merge verify
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - run_command
---

This skill is defined in `.agents/skills/verify-change/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
