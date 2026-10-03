---
name: competitive-snapshot
description: Build a USASpending relationship snapshot for the incumbent and buying agency on a pursuit row. Use when user needs award flows and rel counts before battlecard or teaming work — deterministic from DuckDB bulk.
metadata:
  title: Competitive Snapshot
  category: pursuit-workspace
  status: active
  origin: capture-insights
  mcps:
    - usaspending-gov-mcp
  invoke: workspace,agent
  runtime: legacy
  supports_llm: false
  output: pursuits/{slug}/03_capture/competitive_snapshot.md
---

# Competitive Snapshot

USASpending-only. No LLM required. Citations reference DuckDB bulk ingest.