---
name: 666ghj--mirofish
description: "MiroFish — Swarm Intelligence Engine: upload seed data → simulate thousands of agents → predict future trajectories. GraphRAG + multi-agent simulation + interactive chat."
allowed-tools: Bash, Read, Write
user-invocable: true
---

MiroFish: prediction engine dùng multi-agent swarm — build digital simulation từ seed data, run thousands of agents interact và evolve, dự đoán future trajectories.

## Use Cases

- Policy simulation trước khi triển khai thực tế
- Public opinion simulation
- Financial/political prediction
- Literary/narrative analysis (e.g., alternate storyline endings)
- Scenario testing cho hypothetical decisions

## 5-Stage Pipeline

```
Stage 1 — Graph Building
  Ingest seed data (reports, news, stories)
  Build GraphRAG structures + memory injection

Stage 2 — Environment Setup
  Extract entity relationships
  Generate agent personas
  Configure interaction rules

Stage 3 — Simulation
  Run parallel dual-platform simulations
  Dynamic temporal memory updates
  Thousands of agents interact + evolve

Stage 4 — Report Generation
  ReportAgent với specialized toolsets
  Post-simulation analysis + insights

Stage 5 — Deep Interaction
  Chat với simulated agents
  Chat với ReportAgent về findings
```

## Stack

```
Frontend: Node.js 18+ (localhost:3000)
Backend:  Python 3.11-3.12 (localhost:5001)
LLM:      Alibaba Qwen (recommended) hoặc bất kỳ OpenAI-compatible
Memory:   Zep Cloud
Deploy:   source code hoặc Docker
```

## Quick Start

```bash
git clone https://github.com/666ghj/MiroFish
cd MiroFish
# Setup .env với LLM API key
docker-compose up
# Frontend: localhost:3000
# Upload seed data → describe prediction → get report
```

## Khi nào dùng

- Cần test policy/strategy trước khi commit
- Muốn simulate public reaction cho một quyết định
- Research: agent emergent behavior từ simple rules
- Creative: explore alternate narrative outcomes

## Source

https://github.com/666ghj/MiroFish · MIT · +493⭐/day
