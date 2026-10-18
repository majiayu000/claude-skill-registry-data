---
name: writing-beats
description: Turns fragments or raw material into an ordered journey of reader-facing beats. Use when shaping public docs, articles, guides, or docs-ingest writer artifacts from fragments into a narrative or instructional path.
---

# Writing Beats

## Quick Start

Read the fragment/raw-material file first. Produce beats one move at a time: each beat sets a scene, lands a point, asks a question, introduces an example, or pivots the reader.

Do not write the final article. Do not choose the full page shape yet.

## Modes

### Standalone Writing

Use this when the user wants to assemble an article interactively.

1. Read the raw material end-to-end.
2. Offer 2-3 candidate starting beats.
3. After the user picks one, write only that beat.
4. Re-read the article file before each write.
5. Offer 2-3 next-beat options.
6. Repeat until the journey naturally ends.

### Docs-Ingest Artifact

Use this when called by `docs-ingest-phase`.

1. Read `fragments.md` from the private writer artifact bundle.
2. Write `beats.md` in the same bundle.
3. Include traceability: target public page, source change/spec/run, fragments artifact, updated date.
4. Preserve rejected or parked beats when useful for future passes.
5. Link forward to the final public page when known.

Docs-ingest artifact shape:

```md
---
title: "<Topic> Beats"
type: writer-artifact
artifact: beats
target: "<public page path or pending target>"
source:
  - "fragments.md"
updated: YYYY-MM-DD
---

# <Topic> Beats

## Accepted Beat Path

1. <reader move>
2. <reader move>
3. <reader move>

## Parked Beats

- <usable later, but not in this pass>
```

## Beat Rules

- One beat does one job.
- Split beats that need several subheadings or multiple unrelated moves.
- The journey ends when the reader has what the page promised, not when every fragment is used.
- Pull from the fragment pile freely: paraphrase, split, merge, or quote as needed.
- Name gaps when the beats need an example, warning, proof, or transition that the fragments do not contain.
