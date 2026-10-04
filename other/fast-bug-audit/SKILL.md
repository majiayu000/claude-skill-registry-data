---
name: fast-bug-audit
description: Fast, opportunistic hunt for reachable, confirmed bugs. Read-only. Trades exhaustiveness for speed. For the slow adversarial audit, use bug-audit instead. Not for implementation.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/fast-bug-audit/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
