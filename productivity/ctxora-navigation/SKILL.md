---
name: ctxora-navigation
description: Route a CTXORA task to the smallest useful skill, command, agent role, and MCP tool set. Use when the user asks how to use CTXORA, which workflow to choose, or where a CTXORA capability lives.
---

# CTXORA Navigation

Read `docs/COMMAND-SKILL-MAP.md` when the repository checkout is available. Choose one primary workflow; do not load every CTXORA skill.

For non-trivial implementation work, automatically call `route_skills` first (or `prepare_context` which performs metadata-only routing automatically under `diagnostics.skills`). The selected profile is a candidate boundary, and the router ranks only enabled skills. Read the highest-ranked relevant `SKILL.md` files, perform self-evaluation upon task completion, and submit `skill_feedback` after validation.

- Setup or client connection: use `ctxora-setup`.
- Repository discovery, retrieval, or planning: use `ctxora-repository-context`.
- Stale indexes, diagnostics, repair, or CI context checks: use `ctxora-context-health`.
- Capturing a verified lesson: use `ctxora-continuous-learning`.
- Selecting and customizing the vendored ECC skill catalog: use `ctxora-workflow-profiles`.

Prefer skills as the canonical workflow. Commands are compatibility entry points, and agent files are bounded role prompts. Never assume a command, skill, agent, hook, or MCP tool is installed merely because it exists in the source repository.

For implementation work, retrieve the smallest relevant context, inspect cited files, edit, validate, then save only durable lessons. For review work, report findings without silently switching into implementation.
