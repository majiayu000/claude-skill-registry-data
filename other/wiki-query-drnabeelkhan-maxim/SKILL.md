---
skill_id: wiki-query
name: Wiki Query
description: "Answer a question from the structured wiki before searching the web — \"query the wiki\", \"what do we know about\", synthesis request, cross-project research. Returns cited synthesis with wikilinks and counter-arguments."
version: 1.0.0
category: knowledge-management
type: rag-pipeline
frameworks:
  - llm-wikid-pattern
  - hybrid-bm25-vector
triggers:
  - user asks a question existing wiki could answer
  - "query the wiki"
  - "what do we know about"
  - synthesis request
  - cross-project research
  - before any web search (per documents/reference/AGENTS.md)
collaborates_with:
  - wiki-ingest
  - wiki-lint
  - memory-palace
  - brand-guardian
  - content-strategist
ethics_required: false
priority: high
tags: [knowledge, rag, mempalace, query, .brand-foundation]
created: 2026-04-16
updated: 2026-04-16
---

# Wiki Query

## Purpose

Answer a question using the structured wiki (stored in MemPalace) as the knowledge source. Returns cited synthesis with `[[wikilinks]]`, mandatory Counter-Arguments, and explicit knowledge gaps.

Use BEFORE going to the web. Wiki knowledge — when present — is faster, project-aware, and brand-voice-compliant.

## When To Invoke

- User asks a question that existing wiki knowledge could answer
- Synthesis, research briefings, or pattern detection requests
- Cross-project queries ("what overlaps between iSimplification and SentinelFlow?")
- Before any external research (per `documents/reference/AGENTS.md` — wiki-first principle)

## Inputs

- `query`: The question to answer
- `filters` (optional):
  - `startup`: scope to a single startup's pages
  - `confidence_min`: high | medium | low
  - `explored_only`: boolean (default true — exclude unverified pages)
  - `tags`: array of tag filters

## Workflow

1. **Hybrid search** via MemPalace:
   - `mempalace_search(query, limit=10)` — semantic + keyword
   - Filter results: `explored: true` only (unless `--include-unexplored`)
   - Filter by `confidence_min` and tags
2. **Read top 3-7 most relevant pages** in full via `mempalace_search` (full content) or specific drawer fetch.
3. **Graph traversal** (optional, for synthesis questions):
   - `mempalace_kg_query(entity, direction="both")` to find related concepts
   - `mempalace_traverse(start_room, max_hops=2)` to discover cross-domain links
4. **Synthesize cited answer**:
   - Lead with a direct 2-sentence answer
   - Cite every claim with `[[page-name]]` inline
   - Include Counter-Arguments from cited pages (mandatory)
   - End with: "Knowledge gaps: [list any missing coverage]"
5. **Apply brand voice** (if output is for external use):
   - Load `.brand-foundation/personal/voice-profile.md`
   - Detect active startup → load `.brand-foundation/startups/{id}/positioning.md`
   - Run `.brand-foundation/personal/ai-tells.md` banned-phrase scan
6. **File substantive answers** as new wiki pages in `wing_knowledge/outputs/[query-slug]` with `explored: false`.

## Output Format

```
Wiki Query Result:
Query: "<original query>"
Pages consulted: [N]
Confidence: HIGH | MEDIUM | LOW

Direct Answer:
<2-sentence answer>

Synthesis:
<Cited body using [[page-name]] references>

Counter-Arguments (from cited pages):
- <gap 1>
- <opposing evidence 1>

Knowledge Gaps:
- <topics with weak/no wiki coverage — recommend `/mxm-wiki ingest` after web research>

Confidence: 🟢 HIGH (≥3 cited pages, all explored:true) | 🟡 MEDIUM (some pages explored:false) | 🔴 LOW (no relevant pages found — recommend web search + ingest cycle)
```

## When To Hedge

- Pages cited are `explored: false` → flag with: "⚠️ Drawing on unverified content. Run `/mxm-wiki explore` to confirm."
- `confidence: low` pages → cite as "informal" not authoritative
- Knowledge gap detected → recommend `/mxm-wiki ingest` after closing the gap externally

## MemPalace Integration

```
mempalace_search({
  query: "<query>",
  wing: "wing_knowledge",
  room: null,    // search across rooms
  limit: 10
})

mempalace_kg_query({
  entity: "<key entity from query>",
  direction: "both"
})

mempalace_traverse({
  start_room: "<most relevant room>",
  max_hops: 2
})
```

## Handoff

- Substantive answer filed as wiki page → notify `wiki-explore` (it's `explored: false` by default)
- Knowledge gaps identified → suggest research task to `innovation-researcher` or `trend-researcher`, then `wiki-ingest` after
- External-use answer → load `.brand-foundation/` + run `ai-tells.md` scan before delivery
- Compliance-sensitive answer → loop `compliance-officer` for jurisdiction validation

## Maxim Behavioral Layer

- **Confidence tagging**: 🟢 HIGH (≥3 explored:true pages, citations dense) | 🟡 MEDIUM (mixed verification) | 🔴 LOW (<2 pages or all unexplored)
- **Brand foundation enforcement**: applies to ALL externally-facing wiki-query outputs
- **Anti-hallucination**: refuse to extrapolate beyond cited pages — explicit gaps go in Knowledge Gaps section

## Source References

- `FINAL_RELEASE_CHANGES/Brandvoice-wiki-example.md` — wiki-query pattern
- `documents/reference/AGENTS.md` — wiki-first principle
- `.claude/skills/memory-palace/SKILL.md` — MemPalace tools

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
