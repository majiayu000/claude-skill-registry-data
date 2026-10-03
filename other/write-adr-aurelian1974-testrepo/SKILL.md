---
name: write-adr
description: Draft an ADR for a decision with options, consequences, enforcement and profile diff. Manual command.
argument-hint: "<decision or question>"
disable-model-invocation: true
---
Delegate to architect with a pointer prompt: decision = text after the command. The architect copies `.claude/skills/adr/assets/adr-template.md` to `docs/adr/NNNN-<slug>.md` with a shell command, then fills sections. Status `proposed`. Relay the architect OUT block only.
