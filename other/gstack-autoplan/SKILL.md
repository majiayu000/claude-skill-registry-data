---
name: autoplan
preamble-tier: 3
version: 1.0.0
description: Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisions using 6 decision principles. (gstack)
triggers:
  - run all reviews
  - automatic review pipeline
  - auto plan review
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - AskUserQuestion
---

This skill is the git submodule file `.cursor/vendor/gstack/autoplan/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-autoplan/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
