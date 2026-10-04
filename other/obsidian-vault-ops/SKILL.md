---
name: obsidian-vault-ops
description: "Operate Obsidian vaults for SCBE workflows, including discovery, inspection, and controlled note export."
---

# Obsidian Vault Ops

## Quick Workflow
1. Discover vaults first.
- Run `python scripts/list_obsidian_vaults.py`.
- Confirm the target vault path before touching notes.

2. Default to read-only inspection.
- List notes with `rg --files <vault_path> -g "*.md"`.
- Inspect structure with `rg -n "^# |^---$|^tags:|^source:" <vault_path> -g "*.md"`.

3. Normalize metadata only when requested.
- Preserve existing content.
- Add only missing frontmatter keys needed for SCBE ingestion.

4. Export for SCBE training workflows.
- Copy selected markdown notes into a staging folder in the active repo.
- Keep filenames stable and deterministic.
- Record source vault path and export timestamp in the manifest.

5. Validate before commit or upload.
- Ensure UTF-8 text.
- Ensure each exported markdown file has a clear title and source context.
- Re-run grep checks for required metadata fields.

## Safety Rules
- Never modify Obsidian vault content unless explicitly requested.
- Avoid bulk rewrites across a vault without a backup.
- Keep exports separate from source vaults to prevent accidental corruption.

## SCBE Notes Ingestion Pattern
- Prefer markdown as source of truth.
- Keep lore/story files in a dedicated export folder.
- Include provenance fields in frontmatter when available:
  - `title`
  - `source`
  - `tags`
  - `updated_at`
- When preparing training artifacts, preserve chapter boundaries and glossary sections as distinct blocks.

## Resources
- `scripts/list_obsidian_vaults.py`: detect Obsidian vaults from `%APPDATA%\\Obsidian\\obsidian.json`.
- `references/local_vaults.md`: current known local vault paths discovered on this machine.
