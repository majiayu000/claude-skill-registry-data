---
name: writing-fragments
description: Mines raw writing material into a durable fragments document. Use when developing public-facing docs or articles before structure, when the user mentions fragments, ideation, raw material, claims, examples, or when docs-ingest-phase needs the first public-doc writer stage.
---

# Writing Fragments

## Quick Start

Create or update a `fragments.md` file. Capture raw material only: claims, examples, vignettes, sharp sentences, objections, source-backed facts, snippets, and half-thoughts.

Do not impose outline, beats, final page shape, or polished prose yet.

## Modes

### Standalone Writing

Use this when the user is ideating an article or page interactively.

1. If no output path is provided, ask once where to save the fragments.
2. Re-read the file before every write.
3. Append new fragments separated by horizontal rules.
4. Preserve user edits exactly.
5. Edit a specific fragment only when the user asks.

Standalone first write:

```md
# Working title

First fragment.

---

Second fragment.
```

### Docs-Ingest Artifact

Use this when called by `docs-ingest-phase`.

1. Write to the private writer artifact bundle for the target public page or docs pass.
2. Use the repo's private docs metadata convention when one exists.
3. Include traceability: target public page, source change/spec/run, artifact stage, updated date.
4. Capture source-backed claims and reader-facing raw material.
5. Link forward to the final public page when known.

Docs-ingest artifact shape:

```md
---
title: "<Topic> Fragments"
type: writer-artifact
artifact: fragments
target: "<public page path or pending target>"
source:
  - "<source path or change>"
updated: YYYY-MM-DD
---

# <Topic> Fragments

Fragment text.

---

Another fragment.
```

## Fragment Rules

- A fragment is readable by the author, not necessarily by a cold reader.
- Keep fragments heterogeneous: sentence, claim, vignette, quote, complaint, example, code snippet, or clustered observation.
- Prefer concrete material over abstractions.
- Do not sort or outline unless the user asks.
- Do not discard leftovers; later stages decide what survives.
