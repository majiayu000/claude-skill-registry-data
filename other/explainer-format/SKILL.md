---
name: explainer-format
description: The shape of an `explainer` knowledge entry — the synthesized "how a feature works, as it exists now" artifact. Load this before writing or amending an explainer (hero synthesize / feature-knowledge-synthesis).
---

# Explainer format

An **explainer** is a `type: explainer` knowledge entry that describes **how a
shipped feature works, end to end, as it exists now** — distinct from a
`decision` (why we chose something) or a `convention` (how we do a class of
things). It is synthesized from a cluster of completed specs and is meant to be
the single doc a newcomer reads instead of reverse-engineering the feature from
spec history.

In documentation terms this is the **explanation** (understanding-oriented)
quadrant of the [Diátaxis](https://diataxis.fr) framework — as opposed to
tutorials, how-to guides, or reference. `decision` entries are the adjacent
"why we chose" (ADR) category; explainers are the "how it works."

Explainers live at `.hero/knowledge/explainers/<slug>/spec.md`. They are
classified as knowledge (not work), so they are excluded from work rollups
(`hero` queue ranking, roadmap, in-flight strips).

## Frontmatter contract

```yaml
---
title: <human title of the feature>
type: explainer
synthesized_from:           # provenance — the spec cluster (required, >=1)
  - <spec-slug>
  - <spec-slug>
last_synthesized: <YYYY-MM-DD>   # required — when last synthesized/amended
source_initiative: <slug>        # optional — set when the boundary was an initiative
tags: [...]
---
```

`synthesized_from` and `last_synthesized` are **required**: an explainer claims to
describe current reality, so it must name what it was built from and when.
`hero check` warns on an explainer missing either.

## Section skeleton

Fill these in order. The synthesizer owns everything **above** `## Developer
Notes`; that section and below is human-owned.

1. **What it is** — one-paragraph purpose.
2. **Surfaces / entry points** — commands, MCP tools, files, UI a user touches.
3. **How it works** — the key flows, in order.
4. **Data & state** — what it reads / writes / persists.
5. **Gotchas** — non-obvious constraints, sharp edges.
6. **Related decisions** — *links* to existing `decision` entries by slug. Link,
   don't restate: a decision has one home.
7. **Developer Notes** — **human-owned. Automated synthesis must never read or
   write below this heading.**

## Rules

- **Link, don't restate.** Reference `decision`/`convention` entries by slug
  rather than duplicating their content.
- **Never touch Developer Notes.** Everything below that heading is human tribal
  knowledge; the synthesizer leaves it untouched on amend.
- **Provenance is not optional.** Always set `synthesized_from` and
  `last_synthesized` so a reader can judge staleness and an amend pass knows the
  coverage.
