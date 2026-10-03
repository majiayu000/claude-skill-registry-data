---
name: document-release
preamble-tier: 2
version: 1.0.0
description: Post-ship documentation update. (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - update docs after ship
  - document what changed
  - post-ship docs
---

This skill is the git submodule file `.cursor/vendor/gstack/document-release/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-document-release/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
