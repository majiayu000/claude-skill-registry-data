---
name: simplification-review
description: Review landed code or a diff for over-engineering, pattern fitness, abstraction cost, and dead weight. Use for merged or working code; architecture-review owns proposed designs. Report-only.
triggers:
  - simplification review
  - is this code over-engineered
  - simplify this code
  - pattern check
  - unnecessary complexity
  - dead code review
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/simplification-review/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
