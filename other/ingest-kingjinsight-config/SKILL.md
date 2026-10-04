---
name: ingest
description: Use when the user runs /ingest <url|file|path|text> or asks to ingest a new source (article, paper, podcast, note, image, link) into the vault. Reads the source, files it in Resources/, then updates Knowledge/ pages, Knowledge/_index.md, and Knowledge/_log.md.
---

# Ingest — Source → Wiki Propagation

When the user runs `/ingest <arg>`, take a new source and propagate its content through the knowledge-compounding layer:
1. File the source as immutable raw material in `~/Documents/Obsidian/personalOS/Resources/`
2. Update (or create) relevant `~/Documents/Obsidian/personalOS/Knowledge/` pages in King's voice
3. Keep `Knowledge/_index.md` and `Knowledge/_log.md` current

`<arg>` is one of:
- **URL** — fetch with WebFetch
- **File path** — read with Read (markdown, txt, image, pdf)
- **Raw text** — user pastes content inline
- **Existing file in `Resources/`** — re-process or finish a partial ingest

One source per invocation. Max one `/ingest` run at a time.

## Step 1 — Identify input and determine source_type

Parse `<arg>`:
- Starts with `http://` or `https://` → `source_type: web` (or `article`/`video` if URL shape gives it away — youtube → `video`, arxiv → `paper`)
- Ends with `.pdf` → `source_type: paper`
- Ends with `.png|.jpg|.jpeg|.webp|.gif` → `source_type: image`
- Ends with `.md` or `.txt` inside `Resources/` → existing source, re-ingest
- Otherwise if it looks like a filesystem path → read as file, infer source_type from content
- Otherwise treat as raw pasted text → `source_type: note`

## Step 2 — Fetch and read

| Input | How |
|---|---|
| URL | WebFetch with a prompt asking for full article text, title, author, date |
| Local markdown / txt | Read tool |
| Local PDF | Read tool (Claude Code handles PDFs natively) |
| Local image | Read tool (multimodal) |
| Raw text | use as-is |

If the source is markdown with inline image links and images matter for understanding, Read the markdown first for text, then Read each referenced image separately. Do not try to read markdown + images in one pass.

## Step 3 — Extract

Pull out:
- **Title** (for the source filename slug)
- **Author** (if any)
- **Published date** (if any)
- **3–5 key claims / points** in King's voice
- **Entities and concepts** the source touches (people, techniques, topics)
- **Suggested tags** (match existing vault tags where possible)

## Step 4 — Discuss with the user (mandatory)

Before writing any files, post a short message:

> **Source:** `<title>` (`<source_type>`)
> **Key points:**
> - <point 1>
> - <point 2>
> - <point 3>
> **Topics touched:** [[Existing Knowledge Page]], [[Another Page]], (new concept) X
> **Plan:** create `Resources/YYYY-MM-DD-<slug>.md`; update [[Page A]], [[Page B]]; create [[X]].
> Proceed?

Wait for confirmation or steering. If the user says `no` / redirects, revise and re-confirm. Do not skip this step even for obvious sources.

## Step 5 — File the source in `Resources/`

Filename: `YYYY-MM-DD-<kebab-slug>.md` where `<kebab-slug>` is derived from the title (lowercase, alphanumerics + hyphens, max 60 chars).

Write to `~/Documents/Obsidian/personalOS/Resources/YYYY-MM-DD-<slug>.md`:

```markdown
---
type: source
source_type: <article|paper|podcast|book|video|web|note|image>
date: 2026-04-05
url: <url if any>
title: <title>
author: <author if any>
tags: [<tag1>, <tag2>]
ingested: true
---

## Summary
<3–5 sentence distillation in King's voice>

## Key points
- <point 1>
- <point 2>
- <point 3>

## Connections
- [[Relevant Knowledge Page]] — one-line reason
- [[Another Page]] — one-line reason

## Raw content
<pasted text for web/note sources; excerpt + link for videos; caption + alt-text for images; arxiv abstract for papers>
```

Rules:
- After writing, never mutate a source file again except to flip `ingested: false` → `true` or fix a typo in frontmatter on user request
- If the source is already in `Resources/` (re-ingest case), overwrite only the frontmatter and `## Summary` + `## Key points` — never the `## Raw content`

## Step 6 — Read the wiki index

Read `~/Documents/Obsidian/personalOS/Knowledge/_index.md`. Identify existing Knowledge pages relevant to the source's topics. Do not scan the whole `Knowledge/` folder — the index is the shortcut.

If the index looks stale (missing a page that exists in `Knowledge/`), flag it in the final report but don't rebuild the index from scratch mid-run.

## Step 7 — Update Knowledge pages

For each relevant existing page:
1. Read the page
2. Decide what to add — a new insight, a clarifying example, a counter-claim, a cross-link
3. Edit the page using the Edit tool with a minimal diff
4. Add a back-link to the source at the bottom under a `## Sources` section (create the section if it doesn't exist):
   ```markdown
   ## Sources
   - [[Resources/YYYY-MM-DD-slug|<title>]] — <one-line relevance>
   ```
5. If the new insight contradicts an existing claim on the page, **do not silently overwrite**. Add a `> [!warning] Contradiction (2026-04-05)` callout quoting both claims, and flag it in the final report.

For new concepts that have no existing home:
1. If the concept is small (1–2 paragraphs of content), add it to the closest existing page instead of creating a new one
2. If it genuinely deserves its own page, create `~/Documents/Obsidian/personalOS/Knowledge/<Title>.md`:

```markdown
---
type: knowledge
tags: [<tags>]
created: 2026-04-05
---

# <Title>

## What is this
<1–2 sentences>

## My understanding
<King's voice synthesis — not a source summary>

## Why it matters
<1 paragraph>

## Sources
- [[Resources/YYYY-MM-DD-slug|<title>]]

## Connections
- [[Related Knowledge Page]]
```

Rules for Knowledge pages:
- Write in King's voice — first person, his synthesis, not a paraphrase of the source
- Chinese / English: match the existing page's language; for new pages, default to English unless the source is Chinese
- Never touch `Knowledge Home.md`, `_index.md` (that's Step 8), or `_log.md` (that's Step 9)

## Step 8 — Update `_index.md`

Edit `~/Documents/Obsidian/personalOS/Knowledge/_index.md`:
- Bump `last_updated:` in frontmatter to today
- For each Knowledge page you updated: increment its source count (e.g. `— 2 sources` → `— 3 sources`)
- For each Knowledge page you created: add a new entry in the correct category (or under `## Orphans` if unsure) with the one-line summary and `— 1 sources`
- If you updated the summary substance of an existing page, revise its one-line summary in the index

## Step 9 — Append to `_log.md`

Append to `~/Documents/Obsidian/personalOS/Knowledge/_log.md`:

```markdown
## [2026-04-05] ingest | <title>
- source: [[Resources/YYYY-MM-DD-slug]]
- created: [[New Page]], [[Another New Page]]
- updated: [[Existing Page A]], [[Existing Page B]]
- contradictions: [[Page with conflict]] (if any)
```

Use `## [YYYY-MM-DD]` prefix exactly — the log is meant to be grep-parseable.

If a section has no entries (e.g. no created pages), omit that bullet rather than leaving it empty.

## Step 10 — Report

Output to the user:

```
Ingested: <title>
Source: [[Resources/YYYY-MM-DD-slug]]

Knowledge updates:
- created: [[Page X]], [[Page Y]]
- updated: [[Page A]] (<what you added in one phrase>)
- updated: [[Page B]] (<what you added>)
- contradictions flagged: [[Page Z]] (if any)

Index: +N entries, M modified
Log: appended 1 entry

<anything the user should double-check>
```

## Rules

- **One source per invocation.** Never batch.
- **Always get user confirmation at Step 4** before writing any files.
- **King's voice.** Knowledge pages are his synthesis, not source summaries. If you find yourself quoting the source verbatim, stop and rewrite.
- **Minimal diffs.** Edit existing pages with the Edit tool, don't rewrite them.
- **Scope.** Primary writes go to `Resources/` (source file) and `Knowledge/` (wiki pages, index, log). Also add cross-links in soul files (Values, Beliefs, Goals, Anti-Goals), Daily Notes, or any other vault note where a genuine connection exists — the goal is a strongly interconnected Personal OS, not isolated sections. Never rewrite soul files; only append links.
- **Contradictions surface, never silence.** Use a warning callout; flag in the report.
- **Chinese/English.** Match existing page language. Preserve Chinese originals when quoting.
- **Images.** Read markdown text first, then read referenced images separately — don't try to do both in one Read.
- **Idempotency.** Re-ingesting an existing `Resources/` file should only refresh its summary/key-points and re-propagate — never duplicate log entries for the same source on the same day.
