---
name: cso
preamble-tier: 2
version: 2.0.0
description: Chief Security Officer mode. (gstack)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - WebSearch
  - AskUserQuestion
triggers:
  - security audit
  - check for vulnerabilities
  - owasp review
---

This skill is the git submodule file `.cursor/vendor/gstack/cso/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-cso/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
