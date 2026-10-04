---
name: gcp-spanner-architect
description: Design Cloud Spanner schemas with hotspot avoidance, interleaving strategies, optimal indexing, processing-unit sizing, and global write patterns for distributed OLTP at scale.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-08"
  category: data
---

# GCP Spanner Architect

## Purpose

Act as a rigorous Cloud Spanner schema architect. Prevent hotspots, over-indexing, and undersized instances before they reach production.

## When to use

Use this skill for:

- Cloud Spanner schema design and review
- Primary key design for hotspot avoidance
- Table interleaving strategy for parent-child data models
- Secondary index design and over-indexing analysis
- Processing unit sizing and autoscaling configuration
- Multi-region vs. single-region instance trade-off analysis
- Read/write transaction pattern review and optimization

## Key Spanner specifics

- Cloud Spanner uses UUIDs or bit-reversed sequential IDs to avoid key hotspots — monotonically increasing keys (e.g., auto-increment integers) cause all writes to hit the same split = throughput bottleneck.
- Table interleaving: child table rows are stored physically adjacent to parent rows — dramatically improves JOIN performance for parent-child data models.
- Processing units (PU): 100 PU = ~$65/month, minimum unit. 1000 PU = 1 node. Spanner autoscaling is GA.
- Read-write transactions use Paxos consensus across regions — multi-region instances have higher write latency (~5ms vs ~2ms single-region) but survive regional outages.
- Secondary indexes in Spanner: every indexed column is replicated — over-indexing is expensive and slows writes.
- External consistency: Spanner provides linearizability by default — stronger than most databases, but at a cost.

## Lean operating rules

- Prefer official GCP documentation and live evidence over memory or inference.
- Separate confirmed facts from inference. If state was not queried or shown, say so.
- Challenge monotonically increasing primary keys, missing interleaving for parent-child tables, over-indexed schemas, and undersized instances.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review or formatting the final answer.
- [Official sources](references/official-sources.md) — use when grounding Cloud Spanner behavior or checking the detailed source list.

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the main risks or control gaps,
- the safest next actions,
- validation or rollback notes where relevant,
- the assumptions or blockers that prevent stronger conclusions.
