---
name: competitor-profiling
description: Profile a competitor's vehicles, teaming posture, and recent award patterns for vault notes. Use when user clicks +brain on a recipient or asks for marketing-style competitor intel — catalog skill from coreyhaines marketingskills pattern.
metadata:
  title: Competitor Profiling
  category: marketing-growth
  status: draft
  origin: coreyhaines-marketingskills
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 6
  mcps:
    - usaspending-gov-mcp
    - sam-gov-mcp
---

# Competitor Profiling

**Run** from Agent Skills. DuckDB overlap + vault context; promote to brain/ when curated. Output: `03_capture/competitor_profile.md`.