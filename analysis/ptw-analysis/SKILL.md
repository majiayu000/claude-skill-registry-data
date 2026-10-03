---
name: ptw-analysis
description: Price-to-win lens using GSA CALC+, BLS OEWS, and incumbent USASpending award patterns for a pursuit. Use when user asks for realism checks or competitive pricing posture before proposal — draft skill, not production-verified.
metadata:
  title: Price to Win Analysis
  category: market-competitive
  status: active
  origin: capture-insights
  mcps:
    - usaspending-gov-mcp
    - gsa-calc-mcp
    - bls-oews-mcp
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 6
---

# PTW Analysis

## Capture-insights adapter (no KG)

- **Run** from Agent Skills (Configure & Run) or chat ("price to win", "PTW").
- Seeds from `competitive_intel_obligation.json` **ptw_seed** when present; else pipeline row + DuckDB.
- Best-effort **GSA CALC+** and **BLS OEWS** MCP benchmarks (deferred gracefully when offline).
- Output: `pursuits/<slug>/02_intel/ptw_analysis.{md,json}` in Studio.