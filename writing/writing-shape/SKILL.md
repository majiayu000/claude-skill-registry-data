---
name: writing-shape
description: Chooses the final structure for a public-facing article, guide, or docs page from fragments and beats. Use when turning raw material or beats into a publishable page plan, or when docs-ingest-phase needs the final writer artifact before page writing.
---

# Writing Shape

## Quick Start

Read the available raw material first: fragments, beats, rough draft, or notes. Decide what the page is trying to do for the reader, then choose the structure that best carries that job.

Do not silently polish weak structure. Argue for the shape.

## Modes

### Standalone Writing

Use this when the user wants help shaping a publishable article.

1. Read the input pile end-to-end.
2. Draft 2-3 candidate openings or angles.
3. Force a choice or hybrid.
4. Grow the piece paragraph by paragraph.
5. Re-read the article file before every write.
6. Edit only the requested paragraph or block when revising.

### Docs-Ingest Artifact

Use this when called by `docs-ingest-phase`.

1. Read `fragments.md` and `beats.md` from the private writer artifact bundle.
2. Write `shape.md` in the same bundle.
3. Include traceability: target public page, source change/spec/run, upstream writer artifacts, updated date.
4. Define the final page structure, section order, component/callout choices, and merge notes for the final public page.
5. Link forward to the final public page when known.

Docs-ingest artifact shape:

```md
---
title: "<Topic> Shape"
type: writer-artifact
artifact: shape
target: "<public page path or pending target>"
source:
  - "fragments.md"
  - "beats.md"
updated: YYYY-MM-DD
---

# <Topic> Shape

## Page Promise

<What the reader should be able to understand or do.>

## Structure

1. <section and purpose>
2. <section and purpose>
3. <section and purpose>

## Format Decisions

- <prose/list/table/callout/code choice and reason>
```

## Shape Rules

- Pick prose for argument and lists for genuinely parallel items.
- Use tables only when the same fields repeat three or more times.
- Use callouts for warnings, tips, or asides that would derail the main thread.
- Quote when wording matters; paraphrase when only the idea matters.
- Use code blocks for multi-line, runnable, or illustrative examples.
- If the opening promises one thing and the page drifts, change the opening or re-thread the body.
