---
name: obsi-archive-project
description: Standards for safely closing and archiving projects. Ensures zero broken links and clean knowledge harvesting.
---

# Archive Project Standards

## Purpose
To move completed work out of sight but keep it accessible (`90_Archives`), ensuring the active workspace remains focused.

## Closing Rituals (The Checklist)
1.  **Dependency Scan**: Ensure no external files link *into* this project.
2.  **Status Update**: Change `#status/active` to `#status/done`.
3.  **Knowledge Harvest**: Before archiving, extract valuable assets to `20_Learning` using `obsi-knowledge-harvester`.
4.  **Cleanup**: Delete `.DS_Store`, empty folders, and temp files.

## Archival Rules
- **Destination**: `90_Archives/Projects/{YYYY}/{Project_Name}`
- **Manifest**: Every archived project must have `_archive_meta.md` explaining *why* it was closed.
