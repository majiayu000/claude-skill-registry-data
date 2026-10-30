---
name: thatch-dedup-classifier
description: Classify the relationship between two similar memory entries for deduplication. Use when thatch_find_duplicates identifies candidate pairs.
---

You are a memory deduplication classifier. Given similar memories surfaced by
thatch_find_duplicates (as pairs, grouped into clusters), decide their
relationships and emit actions.

## Instructions

1. Read every memory in the pair or cluster with thatch_memory_show.
2. Classify the relationships.
3. Use thatch_memory_forget to remove duplicates.
4. Use thatch_memory_remember with overwrite: true to update supplemented memories.
5. For pairs you are NOT deleting (supplement, contradiction, unrelated), call
   thatch_dedup_mark_checked with the verdict so the pair stops being re-reported.
6. Call thatch_find_duplicates again afterward to verify the store is clean.

## Clusters (3+ related memories)

A cluster usually means one topic fragmented across entries. Consolidate:
rewrite the cluster as ONE self-contained memory under the best label
(thatch_memory_remember with overwrite: true), preserving every distinct fact,
then thatch_memory_forget the rest. If a cluster mixes topics, split it into
per-topic consolidations, and mark the residual cross-topic pairs checked as
"unrelated".

## Write-time warnings

thatch_memory_remember may warn that a just-saved memory resembles existing
ones. Treat that warning as a one-pair version of this workflow: read the
listed memories and reconcile immediately — merge, or mark the pair checked.

## Relationship types

- **duplicate**: Both memories say essentially the same thing. Delete the less detailed one, or merge content and re-save the better one.
- **supplement**: One memory adds useful context to the other. Update the primary one with the supplement's content, delete the supplement.
- **contradiction**: The memories make incompatible claims. Keep both, note the contradiction in a new memory.
- **unrelated**: Different topics despite high embedding similarity. No action needed.