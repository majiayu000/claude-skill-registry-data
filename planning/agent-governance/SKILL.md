---
name: agent-governance
description: Agent Governance Skill entrypoint. Points to the canonical Codex governance override and included governance skills without rewriting protected source content.
---

# Agent Governance Skill

This is the public entrypoint for the Agent Governance Skill Pack.

Canonical protected sources:

- `../../core/AGENTS.override.md`
- `../../core/skills/`

Files under `../../core/` are canonical and protected. Do not casually rewrite, summarize, compress, or reinterpret them. If a project needs local adaptation, add a project-level adapter or wrapper outside `core/`.

This pack governs:

- audit mode
- planning mode
- execution mode
- validation mode
- post-audit mode
- scope control
- evidence requirements
- stop conditions

## Minimal usage recipe

1. Read `../../QUICKSTART.md`.
2. Inspect `../../core/AGENTS.override.md`.
3. Inspect `../../core/skills/`.
4. Install or reference the canonical materials from a Codex setup or project adapter.
5. Keep project-specific rules in the target project's `AGENTS.md`.

This wrapper is not a replacement for the protected source files. It is a locator and entrypoint.
