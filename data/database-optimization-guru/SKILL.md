---
name: database-optimization-guru
description: Database expert for query optimization, indexing, schema design, and performance tuning
license: Proprietary
---

# Database Optimization Guru
> **Status**: ✅ Research complete
> **Last validated**: 2025-11-08
> **Confidence**: 🟡 Medium — Research-backed tuning playbook – audit semi-annually

## How to use this skill
1. Start with [modules/core-guidance.md](modules/core-guidance.md) to classify workload, risks, and timelines.
2. Run baselines via [modules/workload-profiling.md](modules/workload-profiling.md).
3. Adjust physical design using [modules/indexing-and-schema-design.md](modules/indexing-and-schema-design.md).
4. Tune queries with [modules/query-tuning.md](modules/query-tuning.md).
5. Apply operational practices from [modules/operations-and-observability.md](modules/operations-and-observability.md).
6. Track open research or platform-specific follow-ups in [modules/known-gaps.md](modules/known-gaps.md) and refresh quarterly with [modules/research-checklist.md](modules/research-checklist.md).

## Module overview
- [Core guidance](modules/core-guidance.md) — triage checklist, workload classification, stakeholder alignment.
- [Workload profiling](modules/workload-profiling.md) — baseline metrics, tooling, sampling approaches.
- [Indexing & schema design](modules/indexing-and-schema-design.md) — normalization, partitioning, indexing strategies.
- [Query tuning](modules/query-tuning.md) — execution plans, rewrite patterns, optimizer hints.
- [Operations & observability](modules/operations-and-observability.md) — capacity planning, caching, incident response.
- [Known gaps](modules/known-gaps.md) — targeted research backlog.
- [Research checklist](modules/research-checklist.md) — semi-annual refresh workflow.

## Research status
- Content reflects current PostgreSQL, MySQL, Aurora, and Spanner guidance (2024–2025).
- Schedule next validation for 2026-05-01 or sooner if major engine releases occur.
- Known gaps highlight distributed SQL deep dives and automated tuning comparisons still pending.
