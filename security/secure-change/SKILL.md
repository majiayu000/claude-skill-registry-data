---
name: secure-change
description: Security and privacy review for a scoped mivia change. Check authz, secrets, SSRF, injection, path safety, prompt-injection, and fail-closed defaults. Report with mivia-report/v1.
triggers:
  - secure change
  - security review
  - privacy review
  - threat check
  - secrets
  - auth
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/secure-change/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
