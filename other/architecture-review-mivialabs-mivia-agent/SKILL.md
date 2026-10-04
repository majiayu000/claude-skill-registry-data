---
name: architecture-review
description: Review architecture for boundary fitness, dependency direction, abstraction cost, reachability, tradeoffs, and evolution risk. Use for proposed designs and pre-merge structural reviews.
triggers:
  - architecture review
  - design review
  - review this plan
  - is this design over-engineered
  - package boundaries
  - abstraction check
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/architecture-review/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
