---
name: scalability-analysis
description: Use when user asks "will this scale", "scalability", "capacity planning", "what breaks at 10x", when projecting cost at growth milestones, when identifying the next bottleneck before it hits production, or when planning a migration from monolith to distributed architecture.
---

# Scalability Analysis

## Overview

Read `.forge/architecture.md` and produce `.forge/scalability.md` — a component-by-component analysis of where the system breaks under load, what it costs to scale, and when to migrate to different approaches. Every number must be specific, not "it depends."

## When to Use

- `.forge/architecture.md` exists and the system is approaching production
- User asks "what breaks at 10x" or "how much will this cost at scale"
- Investor pitch requires scalability story with real numbers
- Need to decide between scale-up and scale-out strategies

## When NOT to Use

- No architecture exists — run `architecture-and-contracts` first
- System is pre-MVP with zero users — premature optimization
- Performance issue in existing code — use `debugging-and-recovery`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll scale when we need to" | Scaling decisions made under pressure are expensive. Plan the triggers now |
| "The cloud scales automatically" | Auto-scaling has limits, costs, and cold-start penalties. Know them |
| "We can always add more servers" | Not every bottleneck is CPU. Databases, third-party APIs, and network have different constraints |
| "Cost projections are too speculative" | Use current pricing × growth multiplier. Wrong by 2x is better than no estimate |
| "We'll migrate to microservices later" | Define the trigger now. "Later" never comes without a specific threshold |

## Red Flags

- Component analysis says "scales horizontally" without identifying the bottleneck that prevents it
- Cost projections use optimistic growth without conservative alternative
- No mention of database scaling strategy (the most common bottleneck)
- Migration triggers are vague ("when it gets slow") instead of specific ("when p99 latency exceeds 500ms")
- Third-party API rate limits not accounted for
- No data lifecycle policy (data grows forever = costs grow forever)

## Core Process

### Step 1: Document current capacity

For each component in the architecture:
- Current capacity (requests/sec, storage, connections)
- Current cost (monthly)
- Scaling model (vertical, horizontal, or neither)
- Known limits (hard caps, rate limits, connection pools)

### Step 2: Define scale targets

With the user, define milestones:
- **10x**: first significant growth (e.g., 1K → 10K users)
- **100x**: product-market fit growth (e.g., 10K → 1M users)
- **1000x**: if applicable (mature product scale)

### Step 3: Identify bottlenecks per component

For each component at each scale target:
- What breaks first? (CPU, memory, connections, storage, rate limits)
- At what exact threshold? (e.g., "PostgreSQL single-node hits write throughput limit at ~5K writes/sec")
- What's the mitigation? (read replicas, sharding, caching, queue)

### Step 4: Calculate scale-out triggers

For each bottleneck, define the trigger:
- **Metric**: what to monitor (p99 latency, CPU %, queue depth, storage %)
- **Threshold**: specific number that triggers action
- **Action**: what to do (add replica, shard, migrate, cache)
- **Lead time**: how long the action takes to implement

### Step 5: Cost projections

For each scale target, estimate:
- Infrastructure cost (compute, storage, network)
- Third-party API costs (per-unit pricing × volume)
- Operational cost (monitoring, on-call, maintenance)
- Total monthly cost with margin analysis

### Step 6: Migration decision points

Identify architectural changes needed at each scale:
- When to add caching layer
- When to split monolith (if applicable)
- When to introduce message queues
- When to shard the database
- When to move to dedicated infrastructure

Each decision: specific trigger metric, estimated migration effort, risk if delayed.

### Step 7: Data lifecycle

For each data store:
- Growth rate (GB/month at current scale, projected at each target)
- Retention policy (how long to keep, what to archive, what to delete)
- Archival strategy (cold storage, compression, summarization)
- Cost of storage at each milestone

## Output

Write `.forge/scalability.md` with all sections above. Prepend a `forge:meta` header (`generated_by: scalability-analysis`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/architecture.md]` — paths only, never hashes, `generated_from: {.forge/architecture.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

After writing: "Scalability analysis written to `.forge/scalability.md`."

### Step 8: File feedback for architecture-impacting findings

Findings that imply architecture changes (sharding strategy, read-replica topology, cache-tier insertion, queue-based decoupling, switching to a different data store) require a human decision and cannot be auto-cascaded.

For each such finding, invoke the `feedback` skill to file `.forge/feedback/<timestamp>-scale.md`:
- `target_artifact: .forge/architecture.md`
- `severity: NEEDS_REVIEW`
- `finding:` the bottleneck + the projected scale point where it bites
- `recommended_change:` the specific architectural change (component, placement, rollout sequencing)

Do NOT edit `architecture.md` directly. The user reviews and either runs `/architect` to absorb or marks the entry DEFERRED.

## Verification

- [ ] `.forge/architecture.md` read before starting
- [ ] Every component has a breaking point identified with a specific threshold
- [ ] Cost projections use real pricing (not "it depends")
- [ ] Migration triggers are specific metrics with thresholds, not "when it gets slow"
- [ ] Third-party API rate limits accounted for
- [ ] Data lifecycle policy defined for every data store
- [ ] At least 10x and 100x scale targets analyzed
- [ ] `.forge/scalability.md` written
- [ ] For every finding that implies architecture changes: a `feedback` entry was filed targeting `.forge/architecture.md` with severity `NEEDS_REVIEW`. No direct edits to `architecture.md`.
