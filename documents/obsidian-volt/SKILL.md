---
name: llm-wiki
description: Search, ingest, create, and maintain notes in a topic-specific personal wiki (raw sources + cited wiki pages), following the "LLM Wiki" pattern (raw/ + wiki/ + index.md + log.md) described in the project's CLAUDE.md. Use when the user wants to ingest a new source into raw/, answer a question from the wiki, create or update a wiki page, or lint/audit the wiki -- regardless of the wiki's subject matter.
---

# LLM Wiki

A reusable pattern for a personal knowledge base maintained by Claude, based on Andrej Karpathy's LLM Wiki pattern. The subject of the wiki is defined entirely by that specific project's `CLAUDE.md` -- this skill only covers the mechanics that stay the same across every topic.

Before doing anything, read the project's `CLAUDE.md` to learn the wiki's actual purpose/topic. Everything below is topic-agnostic; substitute the real subject matter wherever this doc says "the topic" or gives a generic example.

## Project location

All paths below are relative to the project root (the directory containing `CLAUDE.md`, `raw/`, and `wiki/`):

```
raw/          -- source documents (immutable -- never modify these)
wiki/         -- markdown pages maintained by Claude
wiki/index.md -- table of contents for the entire wiki
wiki/log.md   -- append-only record of all operations
```

If the current working directory isn't the project root, locate it first (look for the directory that contains `raw/`, `wiki/index.md`, and `CLAUDE.md`).

## Naming conventions

- **Wiki pages**: lowercase-hyphen filenames, e.g. `some-concept.md`, `some-entity.md` -- named after whatever the topic's key ideas/entities are
- **Folders matter here**: unlike a flat vault, sources live in `raw/` and are never touched; everything Claude writes lives in `wiki/`
- **No per-topic "Index" notes** -- `wiki/index.md` is the single table of contents for the whole wiki, not one index per subtopic
- The in-file `# Page Title` heading can be human-readable (e.g. `# Some Concept`), but the filename itself stays lowercase-hyphen

## Page format

Every page in `wiki/` must follow this template exactly, no matter the topic:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.
**Sources**: List of raw source files this page draws from.
**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.
Link to related concepts using [[wiki-links]] throughout the text.

## Related pages

- [[related-concept-1]]
- [[related-concept-2]]
```

## Linking

- Use Obsidian `[[wikilinks]]` syntax, referencing the target page's lowercase-hyphen filename without `.md`: `[[some-concept]]`
- Link related concepts inline in the body where it's natural, and repeat them under `## Related pages` at the bottom
- `wiki/index.md` is the hub: a table of contents listing every page in `wiki/` with a one-line description

## Citation rules

- Every factual claim needs a source reference in the form `(source: filename.ext)`
- If two sources disagree, note the contradiction explicitly rather than silently picking one
- If a claim has no source, mark it clearly, e.g. `[needs verification]`

## Workflows

### Ingest a new source

When the user adds a file to `raw/` and asks you to ingest it:

1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `wiki/` named after the source (lowercase-hyphen filename)
4. Create or update concept pages for each major idea or entity the source touches on
5. Add `[[wiki-links]]` connecting related pages
6. Update `wiki/index.md` with the new/changed pages and a one-line description each
7. Append an entry to `wiki/log.md`: date, source name, and what changed

A single source touching 10-15 wiki pages is normal -- don't hesitate to fan out across many pages.

### Answer a question

1. Read `wiki/index.md` first to find relevant pages
2. Read those pages and synthesize an answer
3. Cite the specific wiki pages used in the response
4. If the answer isn't in the wiki, say so clearly rather than guessing
5. If the answer is valuable and not already captured, offer to file it back into the wiki as a new or updated page

### Search for notes

```bash
# Search by filename
find wiki/ raw/ -name "*.md" -o -name "*.pdf" | grep -i "keyword"
# Search by content (wiki pages only, raw/ is source material not for editing)
grep -rl "keyword" wiki/ --include="*.md"
```

Or use the Grep/Glob tools directly on `wiki/` and `raw/`.

### Create or update a wiki page

1. Use lowercase-hyphen for the filename
2. Follow the page format above exactly: header (Summary / Sources / Last updated), then content, then `## Related pages`
3. Cite every factual claim per the citation rules above
4. Add `[[wikilinks]]` to related pages
5. Update `wiki/index.md` and append an entry to `wiki/log.md`

### Find related notes / backlinks

```bash
grep -rl "\[\[page-name\]\]" wiki/
```

### Lint the wiki

When asked to lint or audit the wiki, check for:

1. Contradictions between pages
2. Orphan pages -- no inbound `[[links]]` from other pages, and/or missing from `wiki/index.md`
3. Concepts mentioned in pages that don't have their own page yet
4. Claims that may be outdated given newer sources in `raw/`
5. Pages that don't follow the page format template above

Report findings as a numbered list with a suggested fix for each.

## Rules

- Never modify anything in `raw/`
- Always update `wiki/index.md` and `wiki/log.md` after any change to `wiki/`
- Keep wiki page filenames lowercase-hyphen (not Title Case)
- Write in clear, plain language
- Ask the user when uncertain how to categorize a new concept
- Organize `wiki/` in whatever subgrouping makes sense for the topic at hand (by entity, by theme, by category...) as long as `wiki/index.md` stays the authoritative table of contents
- This skill's mechanics (folder layout, page format, citation style, workflows) are fixed across projects; only the subject matter changes per-project, as defined by that project's own `CLAUDE.md`
