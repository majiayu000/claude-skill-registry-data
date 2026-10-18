---
name: capsule-compact
agent: none
description: Compact a long capsule chain. Walks parent_capsule_id backward from a head capsule; if chain >= 5, summarizes oldest 3 into a chain-summary capsule. Manual invocation.
allowed-tools: Bash, Read
user-invocable: true
triggers:
  - capsule compact
  - compact chain
  - chain compaction
  - compact capsules
  - /capsule-compact
  - chain too long
---

# /capsule-compact

Run `python3 daemons/capsule-compact.py <head_capsule_id>` from the vault root.

The script:
1. Walks `parent_capsule_id` chain backward from the head
2. If chain length >= 5, summarizes the oldest 3 capsules into a single `chain-summary-<head>-<date>.md` capsule
3. Updates pointers: boundary capsule's parent → summary; summary's parent → original chain root's parent
4. Marks each compacted capsule with `compacted_into: <summary_id>` (they stay on disk for archeology)

## When to run

- /close Step 0.5 PART E (v0.4.5) emits `[CADDY:context] CHAIN — capsule chain length N` when threshold hit
- Manually before a session-heavy week to keep /open Step 2.5 fast
- After narrative-reconstruction archeology when the chain has grown unwieldy

## Defaults

- Threshold: 5 capsules
- Summarize-count: 3 oldest

Override via `--threshold N` and `--summarize-count N` flags.

## What it does NOT do

- Does not auto-compact at /close. Hints, you decide.
- Does not delete compacted capsules. Each gets `compacted_into:` marker.
- Does not LLM-summarize. Concatenates structured fields (objective, open_threads still live, held decisions).
- Does not walk forks. parent_capsule_id is strictly linear.

## Cross-links

- [[concepts/Somatic v0.4.5 Chain Compaction]] — spec
- [[concepts/context-capsule]] — base capsule schema
