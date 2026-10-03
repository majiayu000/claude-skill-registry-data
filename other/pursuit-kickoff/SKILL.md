---
name: pursuit-kickoff
description: Thin orchestrator — runs capture-brief, sam-scan, and competitive-snapshot in order for a new pursuit row. Use when user wants standard admin kickoff without running three buttons manually.
metadata:
  title: Pursuit Kickoff
  category: orchestrators
  status: orchestrator
  origin: capture-insights
  invoke: workspace,agent
  runtime: orchestrator
  orchestrates:
    - capture-brief
    - sam-scan
    - competitive-snapshot
---

# Pursuit Kickoff

Orchestrator only — no bespoke logic. Each step remains a separate skill for quality and testing.