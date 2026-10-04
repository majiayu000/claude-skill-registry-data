---
name: llm-wiki-lint
description: Validate Wiki and source note health. Use before commits, after ingests, or when notes were edited by hand.
---

# LLM Wiki Lint

Run the deterministic checks and fix what they report.

## Steps

1. Run the full check suite:

   ```bash
   python scripts/wiki_tool.py doctor
   python scripts/wiki_tool.py build
   python scripts/wiki_tool.py lint
   python scripts/wiki_tool.py source-lint
   python scripts/audit_public.py
   ```

2. For every lint failure, open the offending note and fix the root cause:
   - wrong or missing tag → set exactly one allowed tag matching the folder
   - `source_count` mismatch → recount `sources` entries
   - broken source link → fix the path or restore the missing Raw source
   - missing source frontmatter → fill in `Title`, `Reference`, `Created`,
     `Processed`, `tags`
   - processed-but-uncovered source → either compile it into Wiki notes or
     set `Processed: false`
3. Re-run until everything passes.
4. See `Schema/lint-checklist.md` for the full rule list, including the
   manual checks lint cannot automate (claim support, no invented citations).

## Rules

- Fix causes, not symptoms: do not silence a check by deleting `sources` or
  downgrading a note's frontmatter.
- Never hand-edit generated files (`Wiki/catalog.jsonl`, index files,
  `Schema/source-manifest.jsonl`); regenerate them instead.
