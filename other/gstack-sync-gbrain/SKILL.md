---
name: sync-gbrain
preamble-tier: 2
version: 1.0.0
description: Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. (gstack)
triggers:
  - sync gbrain
  - refresh gbrain
  - reindex repo
  - update gbrain
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

This skill is the git submodule file `.cursor/vendor/gstack/sync-gbrain/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-sync-gbrain/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
