---
name: ios-sync
preamble-tier: 2
version: 1.0.0
description: Regenerate the iOS debug bridge against the latest upstream gstack templates. (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
triggers:
  - resync the ios debug bridge
  - regenerate ios accessors
  - update the gstack ios instrumentation
---

This skill is the git submodule file `.cursor/vendor/gstack/ios-sync/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-ios-sync/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
