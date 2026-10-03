---
name: land-and-deploy
preamble-tier: 4
version: 1.0.0
description: Land and deploy workflow. (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
triggers:
  - merge and deploy
  - land the pr
  - ship to production
---

This skill is the git submodule file `.cursor/vendor/gstack/land-and-deploy/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-land-and-deploy/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
