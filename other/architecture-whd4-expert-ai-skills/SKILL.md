---
name: architecture
description: Architectural decision-making framework. Requirements analysis, trade-off evaluation, ADR documentation. Use when making architecture decisions or analyzing system design.
allowed-tools: Read, Glob, Grep
---

# Architecture Decision Framework

> "Requirements drive architecture. Trade-offs inform decisions. ADRs capture rationale."

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `context-discovery.md` | Questions to ask, project classification | Starting architecture design |
| `trade-off-analysis.md` | ADR templates, trade-off framework | Documenting decisions |
| `pattern-selection.md` | Decision trees, anti-patterns | Choosing patterns |
| `examples.md` | MVP, SaaS, Enterprise examples | Reference implementations |
| `patterns-reference.md` | Quick lookup for patterns | Pattern comparison |

---

## 🔗 Related Skills

| Skill | Use For |
|-------|---------|
| `@[skills/database-design]` | Database schema design |
| `@[skills/api-patterns]` | API design patterns |
| `@[skills/deployment-procedures]` | Deployment architecture |

---

## Core Principle

**"Simplicity is the ultimate sophistication."**

- Start simple
- Add complexity ONLY when proven necessary
- You can always add patterns later
- Removing complexity is MUCH harder than adding it

---

## 📐 System Design Template (Staff Level)

**Don't start with boxes. Start with math and requirements.**

1. **Requirements & Constraints**
    - Functional: "User clips video", "System generates subtitles"
    - Non-Functional: "Wait time < 20s", "99.9% Availability", "Budget < $500/mo"
2. **Back-of-Envelope Math (Capacity)**
    - *Formula:* $QPS = DailyActiveUsers \times ActionsPerUser / 86400$
    - *Formula:* $Storage = WritesPerDay \times SizePerWrite \times RetentionDays$
    - *Example:* 10k users, 2GB videos = 20TB storage? -> S3 Cold Storage needed.
3. **High-Level Design (The "Blob" Phase)**
    - Client -> API Gateway -> Service -> DB.
    - Validate against constraints (Will single DB handle calc QPS? No -> Read Replica).
4. **Detailed Design (The "Hard Parts")**
    - "How exactly do we handle the video processing failure?" (Dead Letter Queue + Retry)
    - "How do we handle 1 million users?" (Sharding vs Partitioning)

## ⚖️ Decision Matrix (Trade-off Guide)

| Style | Good For | Bad For | Complexities |
|-------|----------|---------|--------------|
| **Monolith** | Speed, Simplicity, small/med teams | Independent scaling, Large teams | Tight coupling |
| **Microservices** | Independent scaling, Polyglot, 100+ devs | Complexity, Latency, Data consistency | Distrib. Tracing, Eventual Consistency |
| **Serverless** | Spiky traffic, Low ops, Event-driven | Long-running tasks, Cold starts | Vendor lock-in, Debugging |

## 📊 Capacity Planning Cheatsheet

- **QPS to Servers:** $Servers = TargetQPS / (SingleCoreQPS \times Cores \times UtilizationFactor)$
- **Bandwidth:** $Mbps = TotalBytesPerSec * 8 / 1,000,000$
- **Database:** Read-heavy? Cache/Replica. Write-heavy? Sharding/Queue-buffering.

## Validation Checklist

Before finalizing architecture:

- [ ] Requirements clearly understood
- [ ] Constraints identified
- [ ] Each decision has trade-off analysis
- [ ] Simpler alternatives considered
- [ ] ADRs written for significant decisions
- [ ] Team expertise matches chosen patterns
