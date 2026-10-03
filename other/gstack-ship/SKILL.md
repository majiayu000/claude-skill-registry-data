---
name: ship
preamble-tier: 4
version: 1.0.0
description: "Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. (gstack)"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
triggers:
  - ship it
  - create a pr
  - push to main
  - deploy this
---

This skill is the git submodule file `.cursor/vendor/gstack/ship/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-ship/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
