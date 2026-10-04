---
name: second-brain-query
description: >
  Answer questions against the knowledge base wiki. Use when the user
  asks a question about their collected knowledge, wants to explore
  connections between topics, says "what do I know about X", or wants
  to search their wiki.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Second Brain — Query

Answer questions by searching and synthesizing knowledge from the wiki.

## Search Strategy

### 1. Start with the index

Read `wiki/index.md` to identify relevant pages. Scan all category sections (Sources, Entities, Concepts, Synthesis) for entries related to the question.

### 2. Use qmd for large wikis

If `qmd` is installed (check with `command -v qmd`), use it for search:

```bash
qmd search "query terms" --path wiki/
```

This is especially useful when the wiki has grown beyond ~100 pages where scanning the index becomes inefficient.

### 3. Read relevant pages

Read the wiki pages identified by the index or search. Follow `[[wikilinks]]` to pull in related context from linked pages. Read enough pages to give a thorough answer, but don't read the entire wiki.

### 4. Check raw sources if needed

If the wiki pages don't fully answer the question, check relevant source summaries in `wiki/sources/` for additional detail. Only go to files in `raw/` as a last resort.

## Synthesize the Answer

### Format

Match the answer format to the question:
- **Factual question** → direct answer with citations
- **Comparison** → table or structured comparison
- **Exploration** → narrative with linked concepts
- **List/catalog** → bulleted list with brief descriptions

### Citations

Always cite wiki pages using `[[wikilink]]` syntax. Example:

> According to [[Source - Article Title]], the key finding was X. This connects to the broader pattern described in [[Concept Name]], which [[Entity Name]] has also explored.

### Offer to save valuable answers

If the answer produces something worth keeping — a comparison, analysis, new connection, or synthesis — offer to save it:

> "This comparison might be useful to keep in your wiki. Want me to save it as a synthesis page?"

If the user agrees:
1. Create a new page in `wiki/synthesis/` with proper frontmatter
2. Add an entry to `wiki/index.md` under Synthesis
3. Append to `wiki/log.md`: `## [YYYY-MM-DD] query | Question summary`

## Conventions

- **Search the wiki first.** Only go to raw sources if the wiki doesn't have the answer.
- **Cite your sources.** Every factual claim should link to the wiki page it came from.
- **Valuable answers compound.** Encourage saving good analyses back into the wiki.
- Use `[[wikilinks]]` for all internal references. Never use raw file paths.

## Related Skills

- `/second-brain-ingest` — process new sources into wiki pages
- `/second-brain-lint` — health-check the wiki for issues
