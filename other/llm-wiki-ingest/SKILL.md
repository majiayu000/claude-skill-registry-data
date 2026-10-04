---
name: llm-wiki-ingest
description: Compile a Raw source into concise, linked Wiki notes. Use when a new source lands in Raw/Sources/ or when a source is marked Processed:false.
---

# LLM Wiki Ingest

Turn a Raw source into short, reusable, source-linked Wiki notes.

## Steps

1. Confirm the source file lives in `Raw/Sources/` and has valid source
   frontmatter (`Title`, `Reference`, `Created`, `Processed`, `tags: [source]`).
2. Search the catalog before opening anything broad:

   ```bash
   python scripts/wiki_tool.py search-catalog --query "<source topic>"
   ```

3. Open only the most relevant existing Wiki notes. Prefer updating an
   existing note over creating a near-duplicate.
4. Read the Raw source and extract its distinct, reusable claims.
5. Create or update focused notes under `Wiki/` using the templates in
   `_templates/`. One idea per note. Use the correct folder and tag
   (see `Schema/naming-conventions.md`).
6. In every note you create or touch, add the Raw source path to `sources`
   and keep `source_count` equal to `len(sources)`. Bump `updated`.
7. Rebuild and validate:

   ```bash
   python scripts/wiki_tool.py build
   python scripts/wiki_tool.py lint
   python scripts/wiki_tool.py source-scan --update --accept-covered
   python scripts/wiki_tool.py source-lint
   ```

8. If the ingest meaningfully changed the Wiki, add a log entry:

   ```bash
   python scripts/wiki_tool.py log --title "Ingested <source>" --details "<what changed>"
   ```

## Rules

- Never invent claims the source does not support.
- Never edit the Raw source content itself (frontmatter `Processed` is
  managed by `source-scan --update --accept-covered`).
- Keep the transformation visible: a small source becomes a few focused notes,
  not one giant dump.
