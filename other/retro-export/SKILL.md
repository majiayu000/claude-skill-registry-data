---
name: retro-export
description: Export gstack /retro metrics as stable JSON schema v1.0 for downstream tooling.
compatibility: |
  - Runtime: Node.js 18+, TypeScript
  - Dependencies: (see package.json)
---

# Retro Export

Thin wrapper that exports gstack `/retro` metrics as JSON schema v1.0. `/retro`
is an external, prompt-only gstack skill and isn't modifiable directly — this
skill accepts the metrics it produces and writes them to a stable JSON file
for downstream tooling (dashboards, reporting agents) to consume.

## Trigger

After a `/retro` run, when its metrics need to be written to a stable,
machine-readable file.

## Flow

1. Accept `testsRun`, `testsPassed`, `blockers`, `workSummary`.
2. Write JSON schema v1.0 to `%APPDATA%\Claude\retro-export.json` (Windows)
   or `~/.config/Claude/retro-export.json` (macOS/Linux).
3. Never throws on export failure — returns `{ success: false, error }`.

See [README.md](README.md) for the full schema and quick-start example.
