---
name: sam-scan
description: Search SAM.gov for live notices matching a pursuit row (agency, incumbent, NAICS keywords) and save results to sam_scan.md. Use for admin monitor setup, presolicitation watch, or when user asks what is live on SAM for an expiring contract.
metadata:
  title: SAM Scan
  category: pursuit-workspace
  status: active
  origin: capture-insights
  mcps:
    - sam-gov-mcp
  invoke: workspace,agent
  runtime: legacy
  supports_llm: false
  output: pursuits/{slug}/02_intel/sam_scan.md
compatibility: Requires SAM_API_KEY or sam-gov-mcp
---

# SAM Scan

Single-purpose live SAM pull. One file out. Pair with `sam-monitor-builder` if user wants pipeline tracking.