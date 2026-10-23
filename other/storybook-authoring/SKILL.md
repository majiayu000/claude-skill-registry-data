---
name: storybook-authoring
description: Author component stories and browser coverage for real states.
---

# Storybook authoring

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/storybook-authoring/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Apply [test-authoring](../test-authoring/SKILL.md).

- Show a meaningful supported state with realistic args and fixtures.
- Keep story data local and deterministic.
- Expose an important visual or interaction variant.
- Add browser-mode coverage where it catches behavior a unit test cannot see.
- Do not use a story as end-to-end setup or as production data handling.
- Read [component coverage](references/component-coverage.md) for direct stories and browser
  isolation.

Consumer wrapper owns: Storybook configuration, exclusions, visual baselines, and commands.
