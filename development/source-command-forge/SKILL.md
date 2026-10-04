---
name: "source-command-forge"
description: "Run queen-wasp-stinger's seven-stage forge pipeline end to end for a brand-new Wasp Nest component, starting with mandatory topic elicitation before any work begins. Trigger with \"forge a new stinger\", \"build a new drone\", \"we need a new command for X\", \"create a skill for Y\", \"make a new rule for Z\"."
license: "AGPL-3.0-or-later"
---

# source-command-forge

Use this skill when the user asks to run the migrated source command `forge`.

Read [the command procedure](../../commands/forge.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.

This command maintains The Wasp Nest itself. Require a writable source checkout and read its live `src/commands/forge.md` before making changes; never edit the installed plugin cache.
