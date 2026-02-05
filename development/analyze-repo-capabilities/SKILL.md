---
name: analyze_repo_capabilities
description: Detect repo tooling and patterns, then record a dynamic manifest.
metadata:
  short-description: Detect repo capabilities
---

## Purpose
Scan the repository for tooling signals and record findings.

## Steps
1. Inspect common signatures (CI, Docker, IaC, agents, frameworks).
2. Update `.agent-docs/memory/CAPABILITIES.md`.
3. Populate `.agent-docs/memory/COMMANDS.md` and `COMMANDS.json`.
4. Update `.agent-docs/memory/MANIFEST.yaml`.
5. Update `.agent-docs/memory/INDEX.md` and `INDEX.json`.

## Guardrails
- Do not overwrite existing files; merge append-only where possible.
- Prefer verified commands and record confidence.
