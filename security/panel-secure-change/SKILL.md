---
name: panel-secure-change
description: Security and privacy review of a delivered change for the review panel. Read-only. Check authz, secrets, injection, SSRF, prompt injection, and fail-closed defaults. JSON report only.
user-invocable: false
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/panel-secure-change/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
