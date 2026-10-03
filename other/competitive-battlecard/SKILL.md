---
name: competitive-battlecard
description: Produce displace/team/ghost talk tracks for the incumbent on a recompete pursuit. Use when user wants competitive angles saved to the pursuit vault; optional multi-turn LLM for customer-facing phrasing.
metadata:
  title: Competitive Battlecard
  category: pursuit-workspace
  status: active
  origin: capture-insights
  mcps:
    - usaspending-gov-mcp
  invoke: workspace,agent
  runtime: tools
  supports_llm: true
  max_turns: 4
  output: pursuits/{slug}/03_capture/competitive_battlecard.md
---

# Competitive Battlecard

Strategy pick is deterministic from row signals. LLM optional for talk tracks only — must not invent award facts.