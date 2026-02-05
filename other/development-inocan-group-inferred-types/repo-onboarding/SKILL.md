---
name: repo-onboarding
description: Repository onboarding and agent bootstrap. Use at the start of a new repo session or before any task to load AGENTS.md, architecture/skills indexes, and discover local Codex skills.
---

# Repo Onboarding

## Overview
Load repo governance and skills before acting.

## Workflow
1. Read `AGENTS.md`. Follow any "Golden Path" or referenced indexes.
2. Load architecture references:
- If `AGENTS.md` points to `.agent-docs/architecture.md`, open it.
- Otherwise open `architecture.md` and any index it references.
3. Load skills references:
- Open `.agent-docs/SKILLS.md` and `skills.md` if present.
- Scan `skills/` for `*/SKILL.md` and list available Codex skills (name + path).
4. Choose skills:
- If the task matches a skill description, load it and follow its workflow.
- Use `docs-auto-sync` whenever code changes are made.
5. Summarize: confirm which docs/skills were loaded and any constraints found.

## Resources
- `references/bootstrap-sources.md`
