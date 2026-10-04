---
name: setup-council
description: Compatibility alias for Cobbler external-agent setup. Use when the user types /setup-council.
disable-model-invocation: true
---

<!-- elves-managed-alias: claude-skill-alias v1 -->

# Setup Council (Cobbler compatibility)

This is an Elves-managed Claude Code compatibility alias for `/setup-council`.

It delegates to the same Cobbler **model onboarding / setup** contract as `/setup-cobbler`,
`references/model-onboarding.md`, and
`python3 scripts/cobbler_agents.py onboard plan|show|apply|probe` and
`python3 scripts/cobbler_agents.py setup`. Council is a compatibility gathering name; Cobbler is the
coordinator.

Rules:

1. Setup must not require OpenRouter or external keys.
2. Do not print credentials or run paid model turns by default (live smoke is opt-in).
3. Write only ignored local `.elves/models.toml` preferences; Never stage secrets or that file.
4. Keep native-first defaults and host-native fallbacks.
5. Interview → apply → probe; re-run to update choices later.
6. Use the main `elves` skill for full setup wording and operator CLI flags.

Codex equivalent: `$elves setup-council` or natural language — not a top-level Codex slash command.
