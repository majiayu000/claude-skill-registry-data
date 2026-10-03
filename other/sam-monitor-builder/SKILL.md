---
name: sam-monitor-builder
description: Create a SAM.gov search monitor from a pursuit or expiring row — persists to Pipeline and writes sam_monitor.md in the pursuit folder. Primary admin rote task for capture managers watching recompetes.
metadata:
  title: SAM Monitor Builder
  category: pursuit-workspace
  status: active
  origin: capture-insights
  mcps:
    - sam-gov-mcp
  invoke: workspace,agent
  runtime: legacy
  supports_llm: false
  output: pursuits/{slug}/02_intel/sam_monitor.md
---

# SAM Monitor Builder

Writes pipeline entry + pursuit markdown. Does not run broad SAM research — use `sam-scan` for that.