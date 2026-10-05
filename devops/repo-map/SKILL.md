---
description: Build a high-signal repository map useful for implementation and retrieval
---

# Repo Map

A useful repo map must identify:
- **Functional surfaces**: apps, cms, workflows, infra, db, scripts, docs
- **Entrypoints**: package.json, Dockerfile, compose files, CI triggers
- **Trust boundaries**: public/private, network segmentation
- **High-risk areas**: zero test coverage, manual processes, known debt
- **Ownership clusters**: who/what owns each surface

## Principles

- Signal over exhaustiveness
- Grouped structure over raw file dumps
- Links into Obsidian indexes
- Updated periodically, not once

## Output Locations

- `vault/90-Index/Repo Map.md` — structured map
- `vault/90-Index/By Service.md` — Docker service index
- `vault/90-Index/Entrypoints.md` — all entry points
