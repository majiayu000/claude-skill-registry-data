---
skill_id: wiki-ingest
name: Wiki Ingest
description: "Ingest raw sources into the structured wiki — \"ingest\", \"add this to my wiki\", new files in raw/, clippings, sources, ideas, nightly ingest. Produces pages with YAML frontmatter and a mandatory Counter-Arguments section."
version: 1.0.0
category: knowledge-management
type: rag-pipeline
frameworks:
  - llm-wikid-pattern
  - bjarne-stroustrup-relevance-filter
triggers:
  - new files in raw/ not yet in wiki
  - ingest command
  - "add this to my wiki"
  - file dropped into raw/clippings/
  - file dropped into raw/sources/
  - file dropped into raw/ideas/
  - nightly ingest cycle
collaborates_with:
  - wiki-query
  - wiki-lint
  - wiki-explore
  - memory-palace
  - operator-profile
  - knowledge-base-curator
ethics_required: false
priority: high
tags: [knowledge, rag, mempalace, .brand-foundation, ingest]
created: 2026-04-16
updated: 2026-04-16
---

# Wiki Ingest

## Purpose

Convert raw, unstructured sources into structured wiki pages stored in MemPalace. Each page has YAML frontmatter, mandatory Counter-Arguments section, bidirectional `[[wikilinks]]`, and `explored: false` until human verification.

This is one of 4 wiki skills (ingest, query, lint, explore) that together implement the Brandvoice pattern on top of MemPalace.

## When To Invoke

- New files appear in `raw/` that don't have a corresponding wiki entry
- User says "ingest", "add this to my wiki", or drops a file into `raw/`
- Nightly scheduled cycle (configured via `/mxm-tasks`)
- After any web research session (research agents auto-trigger)

## Inputs

- Source files in `raw/`:
  - `raw/clippings/` — web clips, article dumps
  - `raw/ideas/` — freeform notes, brain dumps
  - `raw/sources/` — PDFs, papers, transcripts
  - `raw/x-archive/` — social exports

## Workflow

1. **Scan** `raw/` for files not yet referenced by any MemPalace drawer (compare against `mempalace_search` results filtered by source path).
2. **For each unprocessed source:**
   - **Detect type**: tweet, article, PDF, transcript, note, bookmark, paper
   - **If URL**: fetch full content via WebFetch
   - **Extract**: key claims, concepts, entities, dates, counter-arguments, citations
   - **Apply 80% relevance filter** — skip if signal is weak (vague, redundant, off-topic)
3. **Create source summary page** in MemPalace:
   - Wing: `wing_knowledge`
   - Room: `sources`
   - Drawer: page body with YAML frontmatter (see schema below)
4. **Create or UPDATE concept/entity pages** (never overwrite — merge):
   - Concepts → wing `wing_knowledge`, room `concepts`
   - Entities (people, tools, companies) → wing `wing_knowledge`, room `entities`
5. **Add bidirectional `[[wikilinks]]`** between all related pages (use `mempalace_kg_add` to record relationships in the graph layer).
6. **Set `explored: false`** on all new/updated pages.
7. **Update wiki index**: append TLDR entries to MemPalace drawer `wing_knowledge/index/index-md`.
8. **Append to wiki log**: timestamp, source name, pages created/updated → MemPalace drawer `wing_knowledge/log/log-md`.

## Page Schema (MemPalace drawer frontmatter)

```yaml
---
title: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []                  # paths to raw/ files
confidence: high | medium | low
explored: false              # AI-generated → human verification needed
startup: null                # set if scoped to a specific startup
---
```

## Mandatory Page Sections (in order)

1. **TLDR** — 2–3 sentence summary
2. **Main Content** — H2/H3 structured body
3. **Counter-Arguments** — data gaps, opposing evidence, caveats (NEVER skip)
4. **Related** — `[[wikilinks]]` to other pages (≥2 inbound for new pages)
5. **Sources** — links back to raw/ files

## Quality Rules

- Apply 80% relevance filter — skip sources with weak signal
- Every page MUST have Counter-Arguments section
- Never duplicate pages — merge into existing pages when topic overlaps
- Confidence defaults to `medium` unless source is official/verified
- Naming: lowercase kebab-case (`agent-memory-patterns`)
- One concept per page — split any page over 500 lines

## MemPalace Integration

```
mempalace_add_drawer({
  wing: "wing_knowledge",
  room: "sources" | "concepts" | "entities" | "syntheses",
  content: "<full-page-with-frontmatter>",
  source_file: "raw/sources/<original>.pdf",
  added_by: "wiki-ingest"
})

mempalace_kg_add({
  subject: "<entity-or-concept>",
  predicate: "mentioned_in" | "related_to" | "contradicts" | "extends",
  object: "<related-entity-or-concept>",
  source_closet: "<drawer-id>"
})
```

## Output Format

```
Wiki Ingest Report:
Sources processed: [N]
Skipped (low signal): [N]
Pages created:
  - sources/[slug] (confidence: medium, explored: false)
  - concepts/[slug] (confidence: medium, explored: false)
  - entities/[slug] (confidence: high, explored: false)
KG triples added: [N]
Index entries appended: [N]
Log appended: 1 entry @ [ISO timestamp]
Next: review pending pages with `/mxm-wiki explore`
Confidence: 🟢 HIGH (relevance ≥80%, all pages have Counter-Arguments)
```

## Handoff

- Pages created → notify `wiki-explore` for the next verification pass
- Contradictions detected during ingest → escalate to `wiki-lint`
- Pages tagged with regulated topic (GDPR/HIPAA/etc.) → notify `compliance-officer` for review
- New concepts that should propagate to brand voice → notify `brand-guardian`

## Maxim Behavioral Layer

- **Confidence tagging**: 🟢 HIGH when relevance ≥80% and all pages structured correctly | 🟡 MEDIUM when partial structure | 🔴 LOW when relevance filter rejected most sources
- **Frameworks**: LLM Wikid pattern (sources → structured wiki with bidirectional links + `explored: false` default + Counter-Arguments)
- **Ethics gate**: never ingest sources containing PII without `data-privacy-officer` review

## Source References

- `FINAL_RELEASE_CHANGES/Brandvoice-wiki-example.md` — original pattern
- `documents/reference/AGENTS.md` — agent usage guide for the wiki layer
- `.claude/skills/memory-palace/SKILL.md` — MemPalace integration patterns

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
