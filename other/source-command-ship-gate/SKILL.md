---
name: "source-command-ship-gate"
description: "Run the Ship Gate on demand against the current diff, security-stinger first, then quality-stinger, then a hard reminder to load github-repo-health-stinger. Trigger with \"run the ship gate\", \"gate this before I commit\", \"security and quality pass on this branch\", \"is this safe to push\", \"check my diff before I ship it\"."
license: "AGPL-3.0-or-later"
disable-model-invocation: true
---

# source-command-ship-gate

Use this skill when the user asks to run the migrated source command `ship-gate`.

Read [the command procedure](../../commands/ship-gate.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.
