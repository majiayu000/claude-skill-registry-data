---
name: indexing
description: Design and validate database indexes from real query predicates, joins, ordering, selectivity, data distribution, write cost, storage, maintenance, and engine-specific planner behavior.
---
# Indexing

Use when query performance, uniqueness, lookup behavior, or scaling requires deliberate index design or cleanup.

## Procedure
1. Start from measured query workloads and execution plans. List the predicates, join keys, ordering/grouping, returned row counts, frequency, and latency/resource targets the index is intended to improve.
2. Inspect existing indexes, constraints, table/data size, value distribution, null rates, cardinality, update frequency, and whether similar indexes already overlap.
3. Choose the index type supported by the engine and workload: ordered/B-tree, hash, inverted/full-text, spatial, vector, partial/filtered, expression/function, or another engine-specific structure only when its semantics fit.
4. For composite indexes, choose key order based on equality/range/order requirements and actual planner behavior rather than folklore. Consider whether included/covering columns reduce costly lookups without bloating writes excessively.
5. Use partial/filtered or expression indexes when they match a stable recurring predicate and the engine can actually use them.
6. Estimate write amplification, storage, memory/cache pressure, vacuum/maintenance/rebuild cost, replication impact, and migration/creation locking before adding indexes to large or busy datasets.
7. Create the index using the safest online/concurrent mechanism available when production impact matters, and monitor build progress and resource pressure.
8. Compare representative query plans and runtime before/after, including parameter distributions where planner choices may differ.
9. Identify redundant, unused, or superseded indexes cautiously. Verify workload history and constraint dependencies before removal.
10. Revisit index strategy as data distribution and query patterns evolve; an index that once helped can become wasteful or misleading.

## Decision rules
- Indexes are workload structures, not badges every column should receive.
- More indexes improve reads only until write, storage, cache, and planner costs outweigh the gain.
- Unique constraints may use indexes internally but their correctness role is distinct from performance tuning.
- Engine documentation and measured plans outrank generic index recipes.

## Quality gate
The index decision is ready when a real workload motivates it, existing structures and data distribution are understood, creation/removal risk is controlled, before/after plans and runtime demonstrate the effect, write/storage/maintenance costs are acceptable, and no correctness constraint is accidentally removed.