---
name: book-ingest
description: >
  Phase 03 of the books pipeline — upsert validated MDX corpus into Supabase
  via Drizzle. Hydrates `books`, `book_chapters`, `book_sections`, and
  `book_chunks` tables. Maintains separation between display sections (stable
  bookmark anchors) and RAG chunks (regenerable retrieval units) so re-embedding
  never invalidates user bookmarks. Idempotent — only re-sections / re-embeds
  chapters whose `content_sha256` changed. Use after `/book-frontmatter`
  passes Zod validation. Trigger phrases: "ingest into supabase", "upsert
  the book", "phase 03", "load the corpus into the database".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  pipeline_phase: "03"
  reference: "docs/html/books-pipeline.html#phase-3"
---

# Book Ingest — Phase 03: MDX → Supabase

## Purpose

Land the validated corpus in Supabase so the e-reader, commerce flow, and pgvector RAG can serve from a single source of truth.

Schema (Drizzle, `src/lib/database/schema/books.ts`):

- `books` — one row per book per language; embeds `manifest` (full `book.json` snapshot), commerce fields, reader defaults, RAG config.
- `book_chapters` — one row per chapter; `mdx_content` text, `content_sha256` for drift detection, `is_preview` for paywalled chapters, generated `fts` tsvector.
- `book_sections` — display anchors (stable IDs the e-reader bookmarks against). Re-embedding does NOT regenerate sections.
- `book_chunks` — RAG retrieval units (regenerable). HNSW pgvector index on `embedding` (cosine, m=16, ef_construction=64).
- `user_book_purchases | progress | bookmarks | highlights` — user-scoped tables, RLS-protected.

## Invocation

`$ARGUMENTS`:

- **`<book-slug-or-dir>`** — Required.
- **`--dry-run`** — Print SQL without executing.
- **`--force-rechunk`** — Force chunk regeneration even if `content_sha256` unchanged.
- **`--tenant-org-id <uuid>`** — Override `process.env.TENANT_ORG_ID`. Default: Alan Hirsch tenant `6bc0fcf7-2e55-4914-b88d-c6eb49eb0d71`.

## Process

### Step 1 — Pre-flight

1. Verify Supabase env vars: `DATABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `TENANT_ORG_ID`.
2. Verify the book has passed `/book-frontmatter` (look for `<book-dir>/.ingest/frontmatter-*.json` with `verdict: "PASS"`).
3. If no `.ingest/` dir exists, run `/book-frontmatter` first.

### Step 2 — Upsert the book row

```typescript
const manifest = BookManifest.parse(JSON.parse(await Bun.file(`${bookDir}/<book-slug>-book.json`).text()));

const [{ id: bookId }] = await db.insert(books).values({
  organization_id: process.env.TENANT_ORG_ID!,
  slug: manifest.slug,
  title: manifest.title,
  author: manifest.author,
  language: manifest.language,
  manifest,
  version: manifest.version,
  // commerce, reader, rag fields from manifest
}).onConflictDoUpdate({
  target: books.slug,
  set: { manifest, updated_at: new Date() },
}).returning();
```

### Step 3 — Walk chapters, hash, upsert

For each `<book-slug>-chNN-*.md` file:

1. Parse frontmatter and body.
2. Validate frontmatter against `ChapterFrontmatter` Zod schema.
3. Compute `content_sha256` of body (post-frontmatter).
4. Insert / update `book_chapters` row.
5. Capture the previous `content_sha256` from the `RETURNING` clause to detect changes.

```typescript
const [{ id: chapterId, content_sha256: prev }] = await db.insert(bookChapters).values({
  book_id: bookId,
  chapter_number: fm.chapter_number,
  slug: fm.chapter_slug,
  title: fm.chapter_title,
  summary: fm.summary,
  word_count: fm.word_count,
  reading_time_minutes: fm.estimated_reading_time,
  page_range_start: fm.page_range_start,
  page_range_end: fm.page_range_end,
  content_sha256: fm.content_sha256,
  mdx_content: content,
  is_preview: manifest.commerce.preview_chapters.includes(fm.chapter_number),
  metadata: {
    key_concepts: fm.key_concepts,
    themes: fm.secondary_topics,
    citations: fm.citations,
    primary_topic: fm.primary_topic,
    mentions_scriptures: fm.mentions_scriptures,
    mentions_figures: fm.mentions_figures,
  },
}).onConflictDoUpdate({
  target: [bookChapters.book_id, bookChapters.chapter_number],
  set: { mdx_content: content, content_sha256: fm.content_sha256, updated_at: new Date() },
}).returning();
```

### Step 4 — Sections (only if content changed)

If `prev !== fm.content_sha256` (or `--force-rechunk`):

1. Delete existing `book_sections` for this chapter (cascade-safe via FK).
2. Walk the chapter's MD using `remark` to extract every heading and produce stable anchor IDs.
3. Insert one `book_sections` row per heading with `ordinal`, `heading_level`, `anchor`, `text`, `word_count`.

```typescript
import { remark } from "remark";
import { visit } from "unist-util-visit";

function sectionize(content: string, chapterId: string) {
  const sections: any[] = [];
  let ordinal = 0;
  remark().use(() => (tree) => {
    visit(tree, "heading", (node, _index, _parent) => {
      const text = (node.children as any[])
        .map((c) => c.value || "")
        .join("");
      const anchor = text
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "");
      sections.push({
        chapter_id: chapterId,
        ordinal: ordinal++,
        heading_level: node.depth,
        anchor: `#${anchor}`,
        text,
      });
    });
  }).processSync(content);
  return sections;
}
```

### Step 5 — Hand off to chunking + embedding

If sections changed, **do not** chunk + embed inline. Hand off to `/book-chunk` so chunking is a separate, retryable step:

```bash
/book-chunk corpus/alan_hirsch/<book-slug>/
```

This generates `<book-dir>/.ingest/chunks.jsonl`, then `/book-rag-push` uploads to providers and inserts into `book_chunks`.

### Step 6 — Report

```
Phase 03 — Supabase ingest
  Book row:           inserted | updated   (id: <uuid>)
  Chapters upserted:  18 / 18
  Chapters changed:   3 (Ch.1, Ch.4, Notes)
  Sections regenerated: 3 chapters / 47 sections
  Skipped chunks:     existing pgvector entries kept (sha unchanged)

  Verdict: PASS — advance to /book-chunk for changed chapters
```

## RLS Policy Reminder

When inserting, ensure the service-role key bypasses RLS. The runtime read path uses these policies:

```sql
-- Anyone can read preview chapters; purchasers can read all chapters of bought books.
create policy book_chapters_read on book_chapters
  for select using (
    is_preview or exists (
      select 1 from user_book_purchases p
      where p.user_id = auth.uid()
        and p.book_id = book_chapters.book_id
        and p.refunded_at is null
    )
  );

-- User-scoped tables — owner only.
create policy user_book_progress_owner on user_book_progress
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
```

Verify these are deployed before exposing the e-reader.

## Out of Scope

- Generating chunks / embeddings — `/book-chunk`.
- Pushing to OpenAI / Gemini / Claude — `/book-rag-push`.
- Stripe product / price provisioning — separate billing setup task.

## References

- [docs/html/books-pipeline.html#phase-3](../../../docs/html/books-pipeline.html#phase-3)
- [scripts/lib/frontmatter-schema.ts](../../../scripts/lib/frontmatter-schema.ts)
- Drizzle schema: see `src/lib/database/schema/books.ts` in the consuming app
