---
name: canary
preamble-tier: 2
version: 1.0.0
description: Post-deploy canary monitoring. (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
triggers:
  - monitor after deploy
  - canary check
  - watch for errors post-deploy
---

This skill is the git submodule file `.cursor/vendor/gstack/canary/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-canary/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
