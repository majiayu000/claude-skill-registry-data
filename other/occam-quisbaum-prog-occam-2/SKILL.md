---
name: occam
description: Switch Occam token-economy mode (full, lite, off) for this session.
argument-hint: "[full|lite|off]"
disable-model-invocation: true
---
The Occam rules live in rules.md next to this file and are injected at session start (default level: $OCCAM_LEVEL, else full).

- `full`: follow every section of rules.md.
- `lite`: follow Work lean, Talk less and Never cut; build as usual.
- `off`: ignore the Occam rules until switched on again.

Apply the requested level for the rest of this session and confirm in one line. If rules.md is not in your context yet, Read it first. Without an argument, state the current level in one line.

Default for new sessions: `"env": {"OCCAM_LEVEL": "lite"}` in ~/.claude/settings.json.
