---
name: maintain-designs
description: Skill for maintaining clear, DRY, and easy-to-navigate design documents for architect agents.
---

## Objects

Clarity, easy discovery, minimal redundancy, low upkeep designs with clear canonicals and minimal code.

## Principles

One topic per page; one canonical per topic. Prefer deletion with consolidation instead of duplicates. Keep pages skimmable. Stay high-level and include minimal code.

## Workflow

### Inventory (quick)

List all docs with a one-line summary and note overlaps. No metadata beyond that. Cluster by theme Group loosely (e.g., UI, backend, parsing, patterns, specs). Keep flexible. Choose canonicals For overlapping topics, pick the clearest/most current as the canonical.

### Consolidate

Pull unique, still-relevant bits into the canonical. Rewrite for skim: Title, TL;DR, When to use, How, Gotchas, Links. Split only if a page becomes unwieldy.

### Prune

Delete or replace overlaps with a one-line stub linking to the canonical. Move rough-but-useful notes to a lightweight WIP area; drop the rest. Delete obsolete docs and references. Design docs should never reference plans.

### Organize

Arrange under a small set of theme folders or keep flat. Use nesting sparingly and only when it clearly aids navigation.

### Index

Add or update a minimal top-level index (and optional per-theme) with curated links and one-liners. Remove drift and new duplicates.

### Done when

No obvious duplicates. Everything is discoverable from a minimal index. Docs are short, skimmable, and easy to maintain.
