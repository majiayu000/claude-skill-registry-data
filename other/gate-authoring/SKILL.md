---
name: gate-authoring
description: Author or tighten a mechanical gate so a defect class cannot recur. Use after fixing a bug whose class will return, or when a review found a contract nothing enforces.
triggers:
  - add a gate
  - tighten the gates
  - make this enforceable
  - stop this class recurring
  - why did the gates miss this
  - add a semgrep rule
  - add a conformance suite
  - this check is self-attested
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - run_command
  - write_file
  - search_replace
---

This skill is defined in `.agents/skills/gate-authoring/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
