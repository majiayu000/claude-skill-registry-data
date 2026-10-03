---
name: capture-brief
description: Create or enrich a pursuit capture brief from USASpending bulk data, optional SAM live intel, and optional LLM narrative. Use when opening a recompete workspace, scaffolding admin paperwork, or when the user asks for a one-page pursuit snapshot with citations.
metadata:
  title: Capture Brief
  category: pursuit-workspace
  status: active
  origin: capture-insights
  mcps:
    - usaspending-gov-mcp
    - sam-gov-mcp
  invoke: workspace,agent
  runtime: legacy
  supports_llm: true
  max_turns: 3
  output: pursuits/{slug}/01_capture/capture_brief.md
compatibility: Requires DuckDB USASpending bulk; SAM optional via MCP or REST
---

# Capture Brief

Atomic admin skill — one markdown brief per pursuit. Do not merge SAM scan or competitive snapshot here; chain via `pursuit-kickoff` if needed.

## Steps

1. Resolve pursuit slug from row (agency, recipient, award_key).
2. Pull USASpending relationships/flows for incumbent + agency (DuckDB first; live MCP optional).
3. Scaffold `capture_brief.md` with signals, timing, and citation blocks.
4. If enrich/LLM requested: add SAM hits + short narrative; cite sources only.

## Output contract

- Write only under `data/knowledge/pursuits/<slug>/`
- Never write to `global/` or `brain/`