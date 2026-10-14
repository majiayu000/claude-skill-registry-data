---
name: clickmax-list-segments
description: Use when the user wants to create, inspect, update, reload, or use manual lists and dynamic segments to group leads in Clickmax.
---

## When this applies

Use this skill when the user wants manual list operations or dynamic segment logic: create/update/delete lists, manage list membership, build or replace segment filters, preview segment size, reload segments, or inspect list/segment leads.

Not this skill:

- raw lead filtering without creating reusable grouping -> `clickmax-leads`
- tag-based cohort labeling -> `clickmax-tags`

## Key assumptions

- manual lists and dynamic segments are different grouping models
- segment updates also affect the synced backing list metadata and lead membership lifecycle
- upserting segment filters replaces the full tree
- segment filters are a FLAT ARRAY of `{id, order, operator, field, negation, parentId?, value*}` items, not nested objects — nesting comes from each item's `parentId` pointing at its parent GROUP item's own `id`; group items use `field: 'children'` + `operator: 'childrenAnd'`/`'childrenOr'`. Preserve every existing item (by `id`) when replacing, not just the branch being edited.
- reload queues recomputation; it is not just a cosmetic refresh
- `lists_create` makes an EMPTY list. To make a list from the contacts of opportunity cards use `opportunities_bulk_create_list` (see `clickmax-pipelines`): it creates AND fills the list, and its `affected` counts contacts.
- `suspectedFraud` (`operator: equals`, `valueBool`) is a segment field: flags possible card testing (e-mail unrelated to the name AND suspicious document), derived at read time — it works in saved segments and combines with any other item; `false` = contacts not flagged.
- `emailEngagement` (block, JSON in `valueString`) filters by opened / clicked / received-and-did-not-open, in the last N days or on one campaign, or by opened at least N of the last M campaigns received (`openedCount`), counting people only (bots excluded). A saved segment with a day window is recalculated about once a day; a broadcast to it recalculates the audience when created or scheduled, other uses read the daily list — re-measure with `segments_preview_count` right before using it. Shape in [filter model](references/filter-model.md).
- `segments_categories_metrics` also returns origin × sub-origin and a visitor journey (channels, UTM sources, referrers, landing pages, devices) that counts only contacts linked to a tracked visitor — say so when reporting "how they arrived"; Temperature × Score health is `lead_indicators_metrics`.
- Read [filter model](references/filter-model.md) before building non-trivial segment logic.

## Thought process

1. Decide whether the user needs one-off discovery or reusable grouping.
2. Prefer manual lists for explicit curated membership.
3. Prefer segments for filter-defined dynamic cohorts.
4. Preview count before broad destructive changes when the filter tree is uncertain.

## Execute guide

- Manual list lifecycle: use `mcp__plugin_clickmax_clickmax__lists_create` to create the list, then `mcp__plugin_clickmax_clickmax__lists_update_leads` to add or remove explicit lead IDs, then `mcp__plugin_clickmax_clickmax__lists_get_leads` to verify the resulting membership.
- List inspection and maintenance: use `mcp__plugin_clickmax_clickmax__lists_list` to browse lists, `mcp__plugin_clickmax_clickmax__lists_get` to inspect one list, and `mcp__plugin_clickmax_clickmax__lists_update` when the user wants to rename the list or change its emoji.
- Dynamic segment lifecycle: use `mcp__plugin_clickmax_clickmax__segments_create` to create the segment shell, `mcp__plugin_clickmax_clickmax__segments_preview_count` to estimate cohort size from a candidate filter tree, and `mcp__plugin_clickmax_clickmax__segments_upsert_filters` to replace the segment's full filter definition.
- For nested AND/OR or negation, model the filter tree from [filter model](references/filter-model.md), preview the count, then upsert the complete tree.
- Segment inspection and recomputation: use `mcp__plugin_clickmax_clickmax__segments_get` for the segment record, `mcp__plugin_clickmax_clickmax__segments_get_filters` for the current filter tree, `mcp__plugin_clickmax_clickmax__segments_reload` when the user wants membership recomputed, and `mcp__plugin_clickmax_clickmax__segments_get_leads` to inspect the resulting cohort.
- Analytics follow-up: use `mcp__plugin_clickmax_clickmax__segments_timeseries` or `mcp__plugin_clickmax_clickmax__segments_categories_metrics` when the user wants trend, category or entry-channel breakdowns for a segment instead of only raw membership.
- Order of operations: manual list = create or inspect list -> update explicit lead IDs -> verify visible leads. Dynamic segment = inspect current definition -> preview broad or uncertain logic -> replace the full filter tree -> reload when refreshed membership matters -> inspect resulting leads.

## Report

- Start with `Assumption: manual list` or `Assumption: dynamic segment` when the user's goal could fit both models.
- For lists: report the list name, membership change, current visible count, and show up to 10 notable leads followed by `+N more` when needed.
- For segments: report the filter logic, preview size, reload state, and current visible count; call out broad conditions that may over-select the cohort.
- Treat follow-up mutations as opt-in: suggest update, reload, or delete only after showing the current state or impact.

## Warnings

- Segment filter replacement is full replacement, not append/patch.
- Deleting a segment cascades filters, synced list, and membership.
- Filter-order-only changes may not trigger meaningful recomputation.

## Anti-patterns

- Using lists when the user clearly needs a self-updating segment.
- Replacing segment filters without previewing the impact when the logic is broad.
- Treating a synced segment-backed list like an arbitrary manual list.

---

Clickmax skill revision: `b8294822a4d6`
