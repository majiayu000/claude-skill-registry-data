---
name: docs
description: "Update documentation and codemaps from the current codebase state."
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.4-mini
---

# /docs — Documentation Update

See `agents/doc-updater.md`.

1. **Analyze** — Map directory structure, entry points, framework patterns
2. **Generate codemaps** — Create/update `docs/CODEMAPS/` (INDEX, frontend, backend, database, integrations)
3. **Update docs** — README, API docs, environment variables
4. **Validate** — All paths exist, examples compile, links work, freshness timestamps updated

Principles: Generate from code (single source of truth). Under 500 lines per codemap.
Run after: new features, API changes, dependency changes, architecture changes.
