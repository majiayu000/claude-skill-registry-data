---
name: delivery
description: "ADLC delivery loop: Plan -> Breakdown -> Validate -> Finalize, then per slice: Implement (TDD) -> Review (unbounded until a zero-finding round) -> Commit slice. Routes to the rule and role files."
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/delivery/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
