---
name: sync-catalog-docs
description: Synchronize skill and agent names and counts across catalog docs, README files, and packs registry.
tools: [run_command, view_file, grep_search, find_by_name, replace_file_content]
---

# Skill: Sync Catalog Docs

Internal repository workflow to keep `amiga-ia` capability counts and entries synchronized across documentation and the packs registry before commits or releases.

## Workflow

1. **Inventory Source Definitions:**
   - List all skill directories under `skills/` (excluding non-skill entries) and all agent profiles under `agents/*.md`.
   - Record exact names and totals (`<skill_count>` skills, `<agent_count>` agents, `<total>` combined).
2. **Run Automated Sync Check:**
   - Execute `npm run check:docs` (`node scripts/check-catalog-sync.js`).
   - Inspect any missing entries or count mismatches reported across:
     - `docs/catalog.md` and `docs/catalog.es.md`
     - `README.md` and `README.es.md`
     - `registry/packs.json`
3. **Update Out-of-Sync Files:**
   - Add missing `ami-*` entries to the appropriate category table in `docs/catalog.md` and `docs/catalog.es.md`.
   - Add missing `ami-*` entries to the corresponding domain pack in `registry/packs.json`.
   - Update exact counts in `README.md`, `README.es.md`, `docs/catalog.md`, and `docs/catalog.es.md`.
   - Ensure zero country flag emojis are introduced (use semantic text or ISO codes only).
4. **Verify:**
   - Re-run `npm run check:docs` and `npm test` to confirm all checks pass.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
