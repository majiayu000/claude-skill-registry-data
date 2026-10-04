---
name: karpathy-llm-wiki
description: "Use when building or maintaining a personal LLM-powered knowledge base. Triggers: ingesting sources into a wiki, querying wiki knowledge, linting wiki quality, 'add to wiki', 'what do I know about', or any mention of 'LLM wiki' or 'Karpathy wiki'."
---

# Karpathy LLM Wiki

Build and maintain a personal knowledge base using LLMs. You manage two directories: `raw/` (immutable source material) and `wiki/` (compiled knowledge articles). Sources go into raw/, you compile them into wiki articles, and the wiki compounds over time.

Core ideas from Karpathy:
- "The LLM writes and maintains the wiki; the human reads and asks questions."
- "The wiki is a persistent, compounding artifact."

## Architecture

Three layers, all under the user's project root:

```
your-project/
├── raw/            ← Immutable source material (you or the LLM add, never modify)
│   └── 2026-04-03-source-article.md
├── wiki/           ← Compiled knowledge (LLM maintains)
│   ├── summaries/  ← Summary files for each raw article
│   │   └── 2026-04-03-slug_summary.md
│   ├── concepts/
│   │   └── concept-name.md
│   ├── index.md    ← One-page table of contents
│   └── log.md      ← Append-only operation log
```

**raw/** — Immutable source material. You read, never modify. (e.g., `raw/`).

**wiki/** — Compiled knowledge articles. Contains:
- `wiki/summaries/` — Summary files for each raw article (e.g., `2026-04-03-slug_summary.md`)
- `wiki/concepts/` — Concept articles (e.g., `concept-name.md`)
- `wiki/index.md` — Global index. Contains:
  - `## Latest Summaries` — List of recent summary files with dates
  - `## Concept Library` — Concepts grouped by category (e.g., AI/Software Engineering, Social and Economic, Science and Philosophy)
- `wiki/log.md` — Append-only operation log.

**SKILL.md** (this file) — Schema layer. Defines structure and workflow rules.

Templates live in `references/` relative to this file. Read them when you need the exact format for raw files, articles, archive pages, or the index.

### Initialization

Triggers only on the first Ingest. Check whether `raw/` and `wiki/` exist. Create only what is missing; never overwrite existing files:

- `raw/` directory (with `.gitkeep`)
- `wiki/` directory (with `.gitkeep`)
- `wiki/index.md` — heading `# Knowledge Base Index`, empty body
- `wiki/log.md` — heading `# Wiki Log`, empty body

If Query or Lint cannot find the wiki structure, tell the user: "Run an ingest first to initialize the wiki." Do not auto-create.

---

## Ingest

Fetch a source into raw/, then compile it into wiki/. Always both steps, no exceptions.

### Fetch (raw/)

1. Get the source content using whatever web or file tools your environment provides. If nothing can reach the source, ask the user to paste it directly.

2. Save as `raw/YYYY-MM-DD-descriptive-slug.md`.
   - Slug from source title, kebab-case, max 60 characters.
   - Published date unknown → omit the date prefix from the file name (e.g., `descriptive-slug.md`). The metadata Published field still appears; set it to `Unknown`.
   - If a file with the same name already exists, append a numeric suffix (e.g., `descriptive-slug-2.md`).
   - Include metadata header: source URL, collected date, published date.
   - Preserve original text. Clean formatting noise. Do not rewrite opinions.

   See `references/raw-template.md` for the exact format.

### Compile (wiki/)

Determine where the new content belongs:

- **Same core thesis as existing article** → Merge into that article. Add the new source to Sources/Raw. Update affected sections.

These are not mutually exclusive. A single source may warrant merging into one article while also creating a separate article for a distinct concept it introduces. In all cases, check for factual conflicts: if the new source contradicts existing content, annotate the disagreement with source attribution. When merging, note the conflict within the merged article. When the conflicting content lives in separate articles, note it in both and cross-link them.

### Generate Summary Files

For each raw file, create a summary in `wiki/summaries/` :

**Filename format**: `YYYY-MM-DD_slug_summary.md`

**Content structure**:

```markdown
# [Original Title]

**Source**: [Source Name]
**Published Date**: YYYY-MM-DD
**Link**: [URL]

---

## Core Points

- **Bold summary** - 1-2 sentence explanation for each key point (2-4 total)

---

## Key Concepts

- [[Related Concept 1]]
- [[Related Concept 2]]
- [[Related Concept 3]]

---

## Quote Gems

- "Quote 1"
- "Quote 2"

---

*Compiled on YYYY-MM-DD*
```

### Cascade Updates

After the primary article, check for ripple effects:

1. Scan `wiki/index.md` entries in other articles covering related concepts.
2. Update every article whose content is materially affected. Each updated file gets its Updated date refreshed.

Archive pages are never cascade-updated (they are point-in-time snapshots).

### Post-Ingest

1. Update `wiki/index.md`: add or update entries following the structure in `references/index-template.md`:
   - Add new summaries to `## Latest Summaries` section
   - Add new concepts to the appropriate category under `## Concept Library` (create new category if needed)
   - When adding a new category, include a one-line description

2. For each raw file processed, ensure the corresponding summary exists in `wiki/summaries/` (or `wiki/summaries/`). Format:

```markdown
# [Original Title]

**Source**: [Source Name]
**Published Date**: YYYY-MM-DD
**Link**: [URL]

---

## Core Points

- **Bold summary** - 1-2 sentence explanation (2-4 points total)

---

## Key Concepts

- [[Related Concept 1]]
- [[Related Concept 2]]

---

## Quote Gems

- "Quote 1"
- "Quote 2"

---

*Compiled on YYYY-MM-DD*
```

3. Append to `wiki/log.md`:

```
## [YYYY-MM-DD] ingest | <primary article title>
- Updated: <cascade-updated article title>
- Updated: <another cascade-updated article title>
```

Omit `- Updated:` lines when no cascade updates occur.

---

## Query

Search the wiki and answer questions. Examples of triggers:
- "What do I know about X?"
- "Summarize everything related to Y"
- "Compare A and B based on my wiki"

### Steps

1. Read `wiki/index.md` to locate relevant articles.
2. Read those articles and synthesize an answer.
3. Prefer wiki content over your own training knowledge. Cite sources with markdown links: `[Article Title](wiki/article.md)` (project-root-relative paths for in-conversation citations; within wiki/ files, use paths relative to the current file).
4. Output the answer in the conversation. Do not write files unless asked.

## Lint

Quality checks on the wiki. Two categories with different authority levels.

### Deterministic Checks (auto-fix)

Fix these automatically:

**Index consistency** — compare `wiki/index.md` against actual wiki/ files (excluding index.md and log.md):
- File exists but missing from index → add entry with `(no summary)` placeholder. For Updated, use the article's metadata Updated date if present; otherwise fall back to file's last modified date.
- Index entry points to nonexistent file → mark as `[MISSING]` in the index. Do not delete the entry; let the user decide.

**Summary files** — for each raw file, ensure corresponding summary exists:
- Check `wiki/summaries/` for `YYYY-MM-DD_slug_summary.md` files.
- If raw file exists but summary is missing, flag for creation.
- If summary file exists but raw file is missing, flag as orphaned.

**Internal links** — for every markdown link in wiki/ article files (body text and Sources metadata), excluding Raw field links (validated by Raw references below) and excluding index.md/log.md (handled above):
- Target does not exist → search wiki/ for a file with the same name elsewhere.
  - Exactly one match → fix the path.
  - Zero or multiple matches → report to the user.

**Raw references** — every link in a Raw field must point to an existing raw/ file:
- Target does not exist → search raw/ for a file with the same name elsewhere.
  - Exactly one match → fix the path.
  - Zero or multiple matches → report to the user.

**See Also** — within each directory:
- Add obviously missing cross-references between related articles.
- Remove links to deleted files.

### Heuristic Checks (report only)

These rely on your judgment. Report findings without auto-fixing:

- Factual contradictions across articles
- Outdated claims superseded by newer sources
- Missing conflict annotations where sources disagree
- Orphan pages with no inbound links from other wiki articles
- Missing cross-concept references
- Concepts frequently mentioned but lacking a dedicated page
- Archive pages whose cited source articles have been substantially updated since archival

### Post-Lint

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] lint | <N> issues found, <M> auto-fixed
```

---

## Conventions

- Standard markdown with relative links throughout.
- Today's date for log entries, Collected dates, and Archived dates. Updated dates reflect when the article's knowledge content last changed. Published dates come from the source (use `Unknown` when unavailable).
- Inside wiki/ files, all markdown links use paths relative to the current file. In conversation output, use project-root-relative paths (e.g., `wiki/article.md`).
- Ingest updates both `wiki/index.md` and `wiki/log.md`. Archive (from Query) updates both. Lint updates `wiki/log.md` (and `wiki/index.md` only when auto-fixing index entries). Plain queries do not write any files.
