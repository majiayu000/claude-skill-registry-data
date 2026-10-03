---
name: obsidian-raw-import
description: Safely import external documents, datasets, media, models, and web captures into a governed Obsidian vault raw/ area. Use when the user wants to preserve external source material before deriving or writing notes.
---

# Obsidian Raw Import

1. Locate the vault root. Require `AGENTS.md`, `raw/`, and `wiki/`; read the local policy and `wiki/index.md`.
2. Inspect only the user-selected sources. Preserve the original filename and bytes.
3. Classify each source into an existing `raw/` type folder. Propose a new category only when no existing category fits.
4. Show a plan containing each source path, target path, collision policy, and any uncertain classification. Do not copy yet.
5. Ask for explicit confirmation of that exact plan.
6. After confirmation, copy only the listed files into `raw/`. Verify byte length and SHA-256 for every source-target pair.
7. Report the verified imports and whether each item may benefit from a separate `derived/` workflow. Do not generate derived artifacts or Wiki notes in this skill.

## Boundaries

- Do not modify, rename, move, or delete existing `raw/` files.
- Do not overwrite a collision unless the confirmed plan explicitly names the target and policy.
- Do not create `derived/` artifacts, edit `wiki/`, or update logs during this workflow.
- Stop for ambiguous source ownership, destination, or rights concerns.
