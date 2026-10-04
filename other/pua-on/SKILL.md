---
name: pua-on
description: "PUA on alias for Codex. Codex subcommand mapping for Claude Code /pua:on style usage; invoke with $pua-on."
license: MIT
---

# pua-on

This is a Codex CLI alias for the Claude Code `/pua:on` command.

Enable PUA always-on mode by preserving ~/.pua/config.json and setting always_on=true. If feedback_frequency is 0, restore it to 5. Then report [PUA ON].

When this alias changes `~/.pua/config.json`, preserve unknown fields and create `~/.pua/` if missing. Do not claim completion without command/output evidence.
