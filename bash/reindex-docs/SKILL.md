---
name: reindex-docs
description: Regenerate generated docs/*.md index files and check whether AGENTS.md guidance needs follow-up. Use after adding, removing, renaming, or reordering docs collections or docs headings, especially when conventions or decisions change.
compatibility: Cursor-compatible Agent Skill. Requires Node.js. No network access.
---

# Reindex Docs

## Purpose

Keep the generated `docs/*.md` index files in sync with the folder-local `index.json` files under `docs/`.

## Inputs

None. The script discovers all folders under `docs/` that contain an `index.json` file.

## Workflow

1. Run the script from the repo root:

   ```bash
   npx nx run @pz-web/skills:reindex-docs
   ```

2. The script rewrites the full generated index files. Keep human-written guidance in `docs/README.md`, not in
   generated index files.

3. Review the diff with `git diff`.

4. If `docs/conventions/**` or `docs/decisions/**` changed, compare the updated docs against `AGENTS.md`:
   - Check whether the routing table, required-read list, skill list, or project guidance should mention the changed
     convention or decision.
   - Suggest a concrete `AGENTS.md` update when the generated docs reveal new or renamed agent-facing guidance.
   - State explicitly when no `AGENTS.md` update appears necessary.

5. Commit the generated indexes and any requested follow-up edits.

## Collections

- `docs/conventions/`: H2 rule index, ordered by numeric prefix descending.
- `docs/decisions/`: file index, ordered by numeric prefix descending.
- `docs/instructions/`: file index, ordered by most recent git change date when no numeric prefixes are used.

## Notes

- `docs/README.md` stays hand-written and intentionally shallow.
- The `test` target checks only index freshness.
