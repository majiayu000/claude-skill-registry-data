---
name: workflow-feature-delivery
description: Deliver one scoped feature in a workflow worktree with tests, security review, host evidence gates, and an honest report.
triggers:
  - workflow feature delivery
  - workflow implementation
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - search_replace
  - multi_edit
---

This skill is defined in `.agents/skills/workflow-feature-delivery/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
