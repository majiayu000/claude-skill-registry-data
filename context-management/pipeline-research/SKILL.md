---
name: pipeline-research
description: >
  Full research pipeline: auto-researcher → firecrawl-agent → graphify → notebooklm-memory.
  Turns a research question or topic into a structured knowledge asset — multi-source synthesis,
  crawled source content, knowledge graph, and NotebookLM notebook. Trigger when: the user asks
  to research a topic in depth; before starting a project that requires external context
  (competitor analysis, market research, technical investigation); when auto-researcher alone
  is insufficient and deep web crawling + long-term memory storage is also needed.
  Key capabilities: confidence-tiered synthesis (CONFIRMED / SUPPORTED / INFERRED / SPECULATIVE),
  selective crawling of high-value source pages, graph-based relationship mapping, and
  persistent NotebookLM storage for future retrieval. Do NOT chain auto-researcher, firecrawl-agent,
  graphify, or notebooklm-memory separately after running this pipeline — they all run inside.
---

# Pipeline: Research

Full research pipeline. Five stages, sequential. Each builds on the previous.

**Anti-redundancy:** This pipeline calls auto-researcher, firecrawl-agent, graphify, and
notebooklm-memory internally. Do NOT add them as separate steps after running this pipeline.

---

## Inputs

Required from user or calling context:
- **Topic / question**: what to research (required)
- **Depth**: `quick` (30 min), `standard` (2 hours), `deep` (half-day). Default: `standard`
- **Output path**: where to save research files. Default: `{project}/memory/research/{topic-slug}/`
- **Sources to crawl**: optional list of URLs to deep-crawl. If none given, auto-researcher selects.

---

## Stage 1 — Multi-Source Research (auto-researcher)

Invoke `/auto-researcher`:
- Topic: {topic}
- Depth: {depth}
- Output confidence tiers: CONFIRMED / SUPPORTED / INFERRED / SPECULATIVE

Collect:
- Key facts with confidence tier
- Source URLs (categorized: primary, secondary, opinion)
- Knowledge gaps identified
- Recommended URLs for deep crawl

Write synthesis to `{output-path}/synthesis.md`.

---

## Stage 2 — Deep Crawl High-Value Sources (firecrawl-agent)

From Stage 1, select top 3-5 source URLs:
- Prioritize: official docs, primary sources, detailed technical writeups
- Skip: aggregators, news reposts, thin content

Invoke `/firecrawl-agent` on each selected URL:
- Mode: structured extraction
- Extract: key claims, data points, quotes, links to deeper pages
- Depth: 1 level deep per URL (avoid crawling entire sites)

Write extracted content to `{output-path}/sources/` (one file per URL).

---

## Stage 3 — Build Knowledge Graph (graphify)

Invoke `/graphify`:
- Input: synthesis.md + all files in sources/
- Extract: entities, relationships, concepts, contradictions
- Output: knowledge graph at `{output-path}/graph.json`

Identify and flag:
- Contradictions between sources
- High-confidence vs speculative claims
- Key entities and their relationships

Write graph summary to `{output-path}/graph-summary.md`.

---

## Stage 4 — Sync to NotebookLM (notebooklm-memory)

Invoke `/notebooklm-memory`:
- Topic: {topic}
- Sources: synthesis.md, graph-summary.md, and top 3 source files
- Action: create notebook if not exists, add sources, write index note

This creates a persistent, queryable NotebookLM notebook for long-term retrieval.

---

## Stage 5 — Produce Research Report

Write `{output-path}/research-report.md`:

```markdown
# Research Report — {topic}

**Date:** {date}
**Depth:** {depth}
**Sources crawled:** {N}

## Key Findings (CONFIRMED)
{bullet list of high-confidence findings}

## Supporting Evidence (SUPPORTED)
{bullet list of findings backed by multiple sources but not definitive}

## Inferred / Speculative
{bullet list with explicit confidence labels}

## Knowledge Gaps
{what remains unknown or unresolvable from available sources}

## Source Quality
{brief assessment of source diversity and reliability}

## Files
- Synthesis: {output-path}/synthesis.md
- Sources: {output-path}/sources/
- Knowledge graph: {output-path}/graph.json
- NotebookLM: {notebook-url or "synced — search via /notebooklm-memory"}
```

Print summary:
```
PIPELINE-RESEARCH COMPLETE
Topic: {topic}
Sources: {N crawled}
Findings: {N confirmed, M supported, K inferred}
Report: {output-path}/research-report.md
NotebookLM: {synced / failed}
```

---

## Quality Gates

- Stage 1 must produce at least 3 CONFIRMED findings before proceeding to Stage 2.
  If fewer than 3: widen search scope or flag insufficient public information.
- Stage 2 must successfully crawl at least 1 source before proceeding.
  If all crawls fail: proceed with Stage 1 synthesis only, note in report.
- Stage 3 graph must have at least 5 nodes. If fewer: note sparse graph in report.
- Stage 4 failure (NotebookLM unavailable): skip and note in report. Do not block.

---

## Depth Presets

| Depth | auto-researcher | Sources to crawl | Graph depth |
|-------|----------------|-----------------|-------------|
| quick | 30 min cap, top 5 sources | 1-2 URLs | shallow |
| standard | 2h cap, top 10 sources | 3-5 URLs | standard |
| deep | no cap, exhaustive | 5-10 URLs | deep |
