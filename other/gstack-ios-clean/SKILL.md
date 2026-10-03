---
name: ios-clean
preamble-tier: 2
version: 1.0.0
description: "Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. (gstack)"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
triggers:
  - clean the ios debug bridge
  - remove debugbridge
  - strip the gstack ios instrumentation
---

This skill is the git submodule file `.cursor/vendor/gstack/ios-clean/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-ios-clean/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
