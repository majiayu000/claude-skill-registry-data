---
name: gsd
description: Wrapper skill for the Get Shit Done (GSD) multi-agent workflow system. Provides install + usage pointers for OpenCode/Codex/Claude.
---

# GSD (Get Shit Done) — Wrapper Skill

This is a wrapper around the upstream project:
- Upstream: https://github.com/gsd-build/get-shit-done

## What it is
A multi-agent software development workflow system (research → plan → execute → verify) with ports for multiple runtimes.

## Install (recommended)
Use the upstream installer:

```bash
npx get-shit-done-cc --opencode --global
# or --claude / --codex
```

## Notes
- For OpenCode community port: https://github.com/rokicool/gsd-opencode
- This repo also includes one OpenCode-related skill: `gsd-oc-select-model`.
