---
name: "source-command-register"
description: "Walk the pest-controller registration checklist for a finished Drone and Stinger pair, verifying naming and the Critical Directive blocks, adding the roster row, authoring the routing guide, cross-linking related skills, wiring multi-Drone sequences, validating, and regenerating harnesses. Trigger with \"register this drone\", \"register the new stinger pair\", \"add X to the roster\", \"finish registering Y\", \"the pair is built, wire it in\"."
license: "AGPL-3.0-or-later"
disable-model-invocation: true
---

# source-command-register

Use this skill when the user asks to run the migrated source command `register`.

Read [the command procedure](../../commands/register.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.

This command maintains The Wasp Nest itself. Require a writable source checkout and read its live `src/commands/register.md` before making changes; never edit the installed plugin cache.
