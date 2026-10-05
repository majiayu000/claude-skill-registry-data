---
name: mde-node-cli-declaration
description: Standardize global Node CLI ownership on mise with the npm backend and bun-backed cache reuse.
---

# MDE Node CLI Declaration

Use this skill when changing global Node CLI ownership, setup flows, or validation for Node-based CLIs.

## Decision Rules

1. Global Node CLIs stay `mise`-owned.
2. Prefer direct `mise` npm backend declarations over `bun add -g` or `npm -g` loops.
3. Bun is the package manager backend under `mise`, not the authority surface.
4. Repo JavaScript dependencies remain in `package.json` and lockfiles.

## Cache Rules

- Reuse `BUN_INSTALL` and bun's package cache for all automation.
- Warm Node CLI caches with `mise install`, not ad hoc global installs.
- Do not clear bun caches in normal setup or verification flows.

## Required Reads

- `configs/mde-modernization-matrix.json`
- `configs/mde-tool-ownership.json`
- `docs/research/ecosystem-decisions/2026-03-14-node-cli-mise-cache.md`
- `.agents/skills/mde-package-cache-policy/SKILL.md`
