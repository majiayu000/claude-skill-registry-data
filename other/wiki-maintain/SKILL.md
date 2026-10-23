---
name: wiki-maintain
description: Audit and conservatively maintain a configured Yarbrain vault for structural errors, stale knowledge, duplication, conflicts, unprocessed evidence, and skill drift. Use periodically or when recall quality declines; make deterministic checks first and require approval for semantic consolidation or archival.
---

# Maintain a Yarbrain Wiki

Keep the vault trustworthy without optimizing for fewer files or rewriting it
for appearance.

Treat an audit request as read-only. Write a report, rebuild an index, or change
vault content only when the user also authorizes maintenance.

## Workflow

1. Resolve ../../scripts/yarbrain.py relative to this SKILL.md and run lint.
   Record missing structure, duplicate IDs, missing provenance, and broken links
   before using model judgment.
2. Count pending session records and identify episodes with no semantic or
   procedural consumer, notes past their freshness window, overlapping aliases,
   disputed claims, oversized index content, and skills contradicted by newer
   successful episodes.
3. Classify each proposed change as fix-structure, merge, split, supersede,
   archive, reverify, or promote-procedure. Route procedure work to
   procedure-promote and semantic changes or disputes to wiki-reconcile. Leave
   ineligible procedure candidates unchanged and report them as deferred.
4. Present every proposed mutation for approval, including structural fixes,
   semantic changes, index or report writes, and archival. Never delete the only
   copy of evidence or choose between credible conflicts without support.
5. Apply only approved changes. Read every changed file back, rerun lint, and
   rebuild INDEX.md after canonical content is sound.
6. Refresh reports/wiki-health.md with the check time, deterministic results,
   approved changes, unresolved conflicts, stale items, and pending counts.

Indexes and caches are rebuildable. Episodes are evidence. Canonical notes can
evolve only through reconciliation. Keep those ownership rules intact during
cleanup.

This version does not define an episode archival operation. Report unreferenced
or old episodes as candidates, but do not move or delete them.
