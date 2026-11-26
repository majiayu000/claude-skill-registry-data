---
name: skill-authoring
description: Creates portable Agent Skills (SKILL.md) for Cursor, Claude Code, Codex and similar tools. Use when creating a new skill or converting a workflow into SKILL.md.
license: MIT
---

# Skill authoring (multi-IA)

## Instructions

1. Confirm purpose, trigger (“use when…”), and output format.
2. Write YAML frontmatter: `name` (kebab-case), `description` (what + when), `license`.
3. Body: steps, examples, edge cases — **neutral** language (no “open Cursor panel X” as required).
4. Prefer markdown-only. If scripts are needed, isolate under `scripts/` and warn about review.
5. Validate: name matches folder; description ≥ 40 chars; no secrets.

## Install hints (tell the user)

- Cursor: `.agents/skills/<name>/` or `.cursor/skills/<name>/`
- Claude Code: `.claude/skills/<name>/`
- Generic: `.agents/skills/<name>/`
