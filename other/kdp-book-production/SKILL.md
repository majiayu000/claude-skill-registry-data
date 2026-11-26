---
name: kdp-book-production
description: Architect and produce a KDP book from a validated niche — reader pain-point discovery, title/subtitle generation, chapter-outline structures, section-by-section drafting standards, anti-AI-detection discipline, and cover geometry for print. Use when the user wants to plan, outline, draft, or prepare a book for Amazon KDP after niche validation.
triggers:
  - kdp book outline
  - book architect
  - manuscript drafting
  - kdp cover
  - paperback cover
  - spine width
  - كتابة كتاب
personas:
  - DOC
  - MARKETING
  - FREELANCE
tech_stack: []
derived_from: original — methodology facts synthesized from public KDP practitioner frameworks
---

# KDP Book Production

[OBJ] Turn a validated niche into a publishable book: pain-point-driven architecture, disciplined drafting, and print-correct covers.

## Phase 1 — Pain-point architecture (before any prose)

1. List the target reader's biggest pain points: what they feel, fear, and want. 8–12 ranked by severity.
2. Cross-check against **negative reviews of competitor books** — reader complaints are your table of contents.
3. Non-fiction structure that sells: 8 chapters × 3 subchapters × 3 sections. Fiction: use the vendored story skills (`story-long-write`, `novelist-longform`).
4. Titles: generate 10 candidates embedding the primary keyword. Rules: instantly clear (a reader who must pause to decode the title scrolls past), short, benefit-forward. Then 10 subtitles that carry secondary keywords + the promise.

## Phase 2 — Drafting discipline

- Target length for standard non-fiction: ~30,000 words (120–150 print pages). Per chapter ~3,750 words, per section ~1,250 words.
- Draft **one section at a time** — small sections keep quality high and context focused. Never generate a whole chapter in one pass.
- Prose style: practical advice, no list-speak, no filler transitions.

## Phase 3 — The safe-publishing workflow (non-negotiable order)

| Step | Action | Why |
|------|--------|-----|
| 1. Generate | AI draft per section | raw material only |
| 2. Rephrase + enrich | rewrite in your voice, add personal knowledge, stories, fact-checks | this is what makes it a book, not output |
| 3. Verify | AI-pattern audit (use `avoid-ai-writing` / `ai-writing-detector` / `sepia-review` skills) + plagiarism check | Amazon blocks unmodified AI slop; accounts get banned |
| 4. Publish | only after 2–3 pass | account safety is the asset |

Skipping steps 2–3 risks the entire publishing account. Two extra hours per book is the insurance premium.

## Phase 4 — Cover production

### Ebook cover
- Genre signals matter more than art: study the top 10 covers in the niche — the reader must recognize the genre in a thumbnail.
- Test at thumbnail size: if title + genre aren't readable at postage-stamp scale, it fails.

### Paperback full-wrap cover geometry
- One PDF containing **back cover + spine + front cover**, in that order.
- **Spine width depends on page count** and paper type (cream ≈ 0.0025 in/page, white ≈ 0.002252 in/page — always confirm against KDP's current calculator).
- Full cover width = back width + spine + front width + bleed (0.125 in) on all outer edges.
- Spine text: title + author, sized to fit spine width; skip spine text entirely under ~80 pages.
- Back cover content: hook headline, 3–5 benefit bullets, closing tagline — same doctrine as the book description.
- The vendored `kindle-book-formatter` skill handles interior EPUB3/print-PDF conversion; pair them.

## Rules

1. [REQ] Pain points before prose, outline before drafting, sections before chapters.
2. [REQ] The 4-step safe-publishing order is mandatory — no exceptions for deadlines.
3. [REQ] Cover decisions start from niche top-10 analysis, not personal taste.
4. [PROHIBIT] Publishing raw unedited AI output to KDP — account-level risk.
5. [REQ] Page count final BEFORE building the paperback wrap — spine width is derived from it.
