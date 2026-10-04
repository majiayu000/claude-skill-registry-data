---
name: xsq-setup
description: Configure xSquad squad models per role (orchestrator, implementer subagents, reviewers) from the model lists of Claude Code, Pi, or Codex, and write .xsquad/config.json. Use for /xSq-setup, /xsq-setup, "configure xsquad models", "pick squad models".
---

# /xSq-setup

This is the model-configuration command of the **xSquad** skill. This file lives inside
the xSquad package (its root holds `SKILL.md`, `commands/`, `agents/`, `references/`).

Read `commands/setup.md` from the package root — two levels up from this file
(`<package>/commands/setup.md`) — and follow that procedure exactly. It detects installed
runners, enumerates each one's model list (pi: `pi --list-models`; codex: config.toml +
docs + probe; claude: aliases + probe), asks for the per-role models, validates every
slug, and writes `.xsquad/config.json`.

If the package cannot be located from this file's own path, ask the user for the xSquad
package path; do not improvise the procedure.