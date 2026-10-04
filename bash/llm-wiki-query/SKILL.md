---
name: llm-wiki-query
description: Answer questions from the compiled Wiki. Use whenever the user asks a knowledge question that this vault might cover.
---

# LLM Wiki Query

Answer from compiled knowledge first; open Raw sources last.

## Steps

1. Start with `Wiki/index.md` to orient.
2. Search the catalog:

   ```bash
   python scripts/wiki_tool.py search-catalog --query "<user topic>"
   ```

3. Open the most relevant compiled Wiki notes (usually 1–3).
4. Answer from the compiled notes. Only open files under `Raw/Sources/` when:
   - the compiled note is insufficient, or
   - the user asks for source-level verification.
5. When the answer depends on source material, cite both the compiled note
   and the Raw source path.

## Rules

- Do not scan `Raw/Sources/` wholesale — that defeats the purpose of the Wiki.
- If the catalog has no match, say so, then optionally check
  `Schema/source-manifest.jsonl` for unprocessed sources that might cover it.
- If you find a gap worth filling, suggest an ingest rather than answering
  from memory.
