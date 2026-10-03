---
name: teaming-finder
description: Find adjacent vendors and subs (not top market primes) who fill a capability gap against a displacement target using USASpending flows and SAM entity signals. Use when user defines a teaming gap and wants vault-ready partner shortlist with citations.
metadata:
  title: Teaming Finder
  category: market-competitive
  status: active
  origin: capture-insights
  mcps:
    - usaspending-gov-mcp
    - sam-gov-mcp
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 8
  output: pursuits/{slug}/03_capture/teaming_candidates.md
---

# Teaming Finder

Original capture-insights skill — gap-fill teaming, exclude headline incumbents/primes.

## Capture-insights context (no KG)

- **Run** from Agent Skills or ask in chat ("find teaming partners for…").
- Uses **DuckDB USASpending bulk** for adjacent primes at shared buyers; SAM/USASpending MCP enrichment in a later slice.
- Needs a **displacement target** (pursuit incumbent, brain competitor, or name in chat).
- Output: `pursuits/<slug>/03_capture/teaming_candidates.md` in Studio.