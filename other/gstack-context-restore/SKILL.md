---
name: context-restore
preamble-tier: 2
version: 1.0.0
description: Restore working context saved earlier by /context-save. (gstack)
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
triggers:
  - resume where i left off
  - restore context
  - where was i
  - pick up where i left off
  - context restore
---

This skill is the git submodule file `.cursor/vendor/gstack/context-restore/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-context-restore/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
