---
name: book-chunk
description: >
  Phase 04a of the books pipeline — produce the canonical `chunks.jsonl` for
  a book using structure-then-recursive chunking with late chunking and
  Anthropic-style contextual prefixes. Heading-aware (split on H2/H3, never
  break a paragraph or footnote), 512-token target with 64-token overlap,
  embeds the full chapter once and mean-pools per chunk to preserve
  cross-paragraph anaphora. Output feeds both pgvector and the three external
  providers via `/book-rag-push`. Use after `/book-ingest` reports changed
  chapters. Trigger phrases: "chunk this book", "build chunks.jsonl",
  "phase 04 chunker", "generate retrieval units".
allowed-tools: Read, Write, Bash, Grep, Glob
metadata:
  pipeline_phase: "04a"
  reference: "docs/html/books-pipeline.html#phase-4"
---

# Book Chunk — Phase 04a: Canonical chunks.jsonl

## Purpose

Generate the **single source of truth** for retrieval — `<book-dir>/.ingest/chunks.jsonl`. This file feeds pgvector, OpenAI Vector Stores, Gemini File Search, and Claude Files (via `/book-rag-push`). One JSONL line per chunk; the only thing that varies per provider is the upload format.

The chunker uses the April-2026 SOTA combination:

- **Structure-first** — split on H2 / H3 headings; never break a paragraph, footnote, code block, or blockquote mid-content.
- **Recursive target** — 512 tokens per chunk, 64-token overlap (~12.5%).
- **Late chunking** (Jina, 2024) — embed the full chapter once with a long-context model, then mean-pool token vectors per chunk. Preserves cross-paragraph anaphora (proven +10–12% on documents with pronoun chains).
- **Contextual prefix** (Anthropic, Sept 2024) — prepend a 50–100 token LLM-generated context that situates the chunk in book + chapter; embed the prefixed text. Cuts retrieval failure ~67% per Anthropic's own benchmarks.

## Invocation

`$ARGUMENTS`:

- **`<book-slug-or-dir>`** — Required.
- **`--target-tokens <N>`** — Default: `512`. From `book.json:rag.chunk_target_tokens`.
- **`--overlap-tokens <N>`** — Default: `64`. From `book.json:rag.chunk_overlap_tokens`.
- **`--changed-only`** — Only re-chunk chapters whose `content_sha256` differs from the last `chunks.jsonl` entry. Default: `true`.
- **`--out <path>`** — Default: `<book-dir>/.ingest/chunks.jsonl`.

## Process

### Step 1 — Read inputs

1. Load `<book-slug>-book.json` → `manifest`.
2. Walk every `<book-slug>-ch*.md` file → frontmatter + body.
3. Verify each frontmatter parses against `ChapterFrontmatter` Zod schema; abort if not.

### Step 2 — Structure split

For each chapter:

1. Parse with `remark` + `unist-util-visit`.
2. Walk the AST collecting groups: each group starts at an h2 or h3 heading and contains the heading + all content nodes until the next h2/h3.
3. Track `heading_path` per group (e.g. `["Missional DNA", "The Latent Code"]`).
4. Capture page-marker `<!-- page: N -->` boundaries; each chunk records `page_start` (first marker in group) and `page_end` (last marker before next group).

### Step 3 — Recursive split within groups

For groups exceeding `target-tokens`:

1. Split on paragraph boundaries first (blank lines).
2. If a paragraph alone exceeds target, split on sentence boundaries (NLP sentence tokenizer; never break inside a footnote, blockquote, or code block).
3. Apply `overlap-tokens` by repeating the last N tokens of chunk K at the start of chunk K+1.

Use `tiktoken` (`cl100k_base`) for token counting.

### Step 4 — Generate contextual prefix per chunk

Use a small Claude model (e.g. `claude-haiku-4-5`) for cost. Prompt:

```
You are generating a 50-100 token context to prepend to a passage from a book,
to improve retrieval. Output ONLY the context (no preamble, no quotes).

Book: <manifest.title>
Chapter: <chapter_title>
Section path: <heading_path joined with " > ">
Page range: <page_start>-<page_end>

Passage:
<chunk text>

Context (50-100 tokens):
```

Cache the chapter-level summary to avoid regenerating shared context across chunks of the same chapter.

### Step 5 — Late chunking embedding (optional, recommended)

Generate embeddings for `pgvector` ingestion:

1. Embed the **full chapter** (truncated to 8K tokens if needed) with `voyage-3-large` (or `text-embedding-3-large` if Voyage unavailable).
2. For each chunk, mean-pool the token vectors that fall within the chunk's character range.
3. Store the per-chunk embedding alongside the chunk.

If the embedding model does not return token-level vectors (most don't), fall back to per-chunk embedding of `context_prefix + "\n\n" + text`. This is what most providers actually use; "late chunking" with mean-pooling is only available for specific Jina / Voyage long-context endpoints.

### Step 6 — Emit chunks.jsonl

One line per chunk:

```jsonl
{"id":"<book-slug>-ch03-0007","book_slug":"<book-slug>","chapter":3,"chapter_slug":"missional-dna","section_anchor":"#latent-code","page_start":79,"page_end":80,"heading_path":["Missional DNA","The Latent Code"],"text":"…the six elements of mDNA …","context_prefix":"From Hirsch's *The Forgotten Ways*, chapter 3 (\"Missional DNA\"), section \"The Latent Code\". This passage introduces the six elements of mDNA as the recoverable code beneath every Jesus movement.","token_count":498,"sha256":"a31b…","metadata":{"language":"en","key_concepts":["mdna","apostolic-genius"],"is_preview":false}}
```

Field reference:

- `id` — `<book-slug>-ch<NN>-<NNNN>` (zero-padded chapter + chunk ordinal). Stable across re-runs.
- `book_slug`, `chapter`, `chapter_slug`, `section_anchor`, `page_start`, `page_end`, `heading_path` — addressable provenance.
- `text` — the chunk body.
- `context_prefix` — Anthropic-style situating context.
- `token_count` — cl100k tokens.
- `sha256` — hash of `context_prefix + "\n\n" + text`. Used by `/book-rag-push` to detect what's changed since last upload.
- `metadata` — language, key_concepts, is_preview, mentions_figures, mentions_scriptures.

### Step 7 — Diff against previous run

If `<book-dir>/.ingest/chunks.jsonl` already exists:

1. Read the previous chunks; map `id → sha256`.
2. For each new chunk, compare. Mark `__diff: "added" | "modified" | "unchanged"` in a side-file `.ingest/chunks.diff.json` (do not modify the canonical jsonl with diff metadata).
3. Print a summary: `+12 added, ~7 modified, 4218 unchanged`.

### Step 8 — Report

```
Phase 04a — Chunking
  Chapters chunked:    18 / 18
  Total chunks:        4237 (+12 added, ~7 modified, 4218 unchanged)
  Tokens / chunk:      avg 487, p95 511, max 528 (target 512)
  Overlap:             62 tokens avg (target 64)
  Context prefix gen:  $0.84 in API spend
  Output:              corpus/alan_hirsch/<book-slug>/.ingest/chunks.jsonl

  Verdict: PASS — advance to /book-rag-push
```

## Quality Checks

- Every chunk's `text` is non-empty and under 600 tokens.
- Every chunk has a non-empty `context_prefix` between 50 and 150 tokens.
- No chunk crosses an h2 boundary (i.e., `heading_path[0]` is consistent within a chunk).
- No chunk breaks mid-footnote (verify by checking `[^N]` opens have matching closes within the same chunk).
- Every `id` is unique book-wide.
- Sum of chunk `token_count` ≥ 0.95 × sum of source chapter `word_count` × 1.3 (rough word→token ratio).

## Out of Scope

- Pushing to providers — `/book-rag-push`.
- Inserting into `book_chunks` table — the next phase.

## References

- [docs/html/books-pipeline.html#phase-4](../../../docs/html/books-pipeline.html#phase-4)
- [Late chunking paper](https://arxiv.org/pdf/2409.04701)
- [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [PreMAI 2026 chunking benchmark](https://blog.premai.io/rag-chunking-strategies-the-2026-benchmark-guide/)
