---
name: cross-reference-management
description: |
  Conventions and helpers for lightweight relationships between entities expressed as frontmatter references (not first-class Binding entities). Use when linking two entities with a simple, unscoped, untemporal relationship — 'this work item blocks that one', 'this decision relates to that work item'. For scoped/temporal relationships, use binding-management instead.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-cross-reference-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
    provides:
      primitives: [CrossReference]
      templates: []
---

# Cross-Reference Management

## Intro

A CrossReference is a lightweight typed link between two entities, expressed
as a field in the subject's frontmatter rather than as its own file. It is
the right choice for simple, unscoped, permanent relationships — "A blocks
B", "decision X is related to work item Y". When a relationship needs scope,
time, or its own attributes, use a Binding instead.

## Overview

### CrossReference is not a file

Unlike every other primitive, CrossReference does not get its own file.
It is a **convention for frontmatter fields** — a typed list of pointers.

```yaml
# In a WorkItem's frontmatter:
spec:
  blocks: [BACK-swift-oak]
  blocked_by: [BACK-calm-fox]
  related_decisions: [DEC-023]
```

Each field name encodes the relationship type. The *fields* vary per primitive;
the *convention* is shared.

### Conventional cross-reference field names

| Field               | Meaning                                             |
|---------------------|-----------------------------------------------------|
| `parent`            | This entity is a child of another                   |
| `children`          | This entity has sub-items                           |
| `blocks`            | This entity blocks others until resolved            |
| `blocked_by`        | This entity is blocked by others                    |
| `related`           | Generic "see also" — use only when no better field fits |
| `related_workitems` | Typed relationship specifically to WorkItems        |
| `related_decisions` | Typed relationship specifically to DecisionRecords  |
| `supersedes`        | This entity replaces an older one                   |
| `superseded_by`     | This entity has been replaced by a newer one        |
| `implements`        | This entity implements something (e.g. a decision)  |
| `motivates`         | This entity motivated another (e.g. bug → decision) |

### Workflow

1. Pick the field that best fits the relationship. Prefer specific over generic.
2. Add the target ID(s) to that field in the subject's frontmatter.
3. For bidirectional relationships (`blocks` ↔ `blocked_by`), update both sides.
4. Log a declared event type such as `workitem.note` with
   `details.relation` + `details.target`; do not use undeclared
   legacy aliases such as `workitem.linked`.

### Cross-reference vs Binding

| Situation                                           | Use         |
|-----------------------------------------------------|-------------|
| "A blocks B"                                        | cross-ref   |
| "A is related to B"                                 | cross-ref   |
| "A is the parent of B"                              | cross-ref   |
| "A fills role R in scope S for time T"              | **Binding** |
| "A applies to B only on main branch"                | **Binding** |
| "A and B are linked AND the link has its own metadata" | **Binding** |

If the link has its own properties worth querying, it's a Binding. Otherwise,
it's a cross-reference.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Using a cross-reference when scope or time matters.** If the
  relationship is "Alice owns this for sprint 42" or "this gate
  applies on main only", that's a Binding, not a cross-reference.
  Cross-references can't carry temporal validity or scoping —
  reaching for one when you need a Binding silently loses the
  qualification.
- **Forgetting to add the inverse side of an asymmetric pair.**
  `blocks` / `blocked_by`, `parent` / `children`, `supersedes` /
  `superseded_by` are all bidirectional. If you set one side
  without setting the other, the index ends up with a broken
  half-edge. Always set both.
- **Cross-referencing a non-existent entity ID.** A typo in a
  reference (`BACK-1234` vs `BACK-12345`) silently breaks
  navigation and produces a dangling edge. Verify the target
  exists via `index-management.get_entity` before writing the
  reference.
- **Treating cross-references as authoritative state.** A
  cross-reference is metadata about a relationship; the
  authoritative state lives on the entity itself. If a workitem's
  `parent` says it's part of an epic but the epic's `children`
  doesn't include it, the parent reference is wrong, not the
  epic.
- **Cross-referencing aggressively just because you can.** Every
  cross-reference is graph clutter for queries. Reserve them for
  relationships a future agent or human will actually need to
  navigate, not for "these two things vaguely relate".
- **Adding cross-references to entities you don't own the schema
  for.** If you're tempted to put a custom field on a primitive's
  frontmatter, consider whether it belongs in `metadata.tags` or
  in a Binding instead. Schema drift across primitives breaks
  validation.
- **Confusing cross-references with discussions/decisions.** A
  cross-reference says "these are related"; it does not capture
  WHY. If the why matters, write a Discussion or DecisionRecord
  and cross-reference THAT, not the underlying entities directly.

## Full reference

### Bidirectional integrity

Some cross-references are inherently bidirectional (`blocks`/`blocked_by`,
`parent`/`children`, `supersedes`/`superseded_by`). Agents should update
both sides when adding or removing. The index MCP server (Phase 3) will
surface one-sided references as lint warnings.

### Typed vs generic `related`

Prefer typed fields (`related_decisions`, `related_workitems`) over the
generic `related` — they make queries and rendering much cleaner. Only fall
back to `related` when there is no natural typed field.

### Field naming convention

Cross-reference field names are lowercase snake_case, use plural form for
lists, and describe the relationship from the subject's perspective. "A
blocks B" is expressed as `blocks: [B]` on A, not `blocker_of: [B]`.

### Resolving a cross-reference

To find all entities that reference X:
- By field scan: grep all frontmatter for X's ID appearing in any list.
- Via index MCP server: `query(target=X)` returns all cross-references
  across all entity kinds.

### Migration to Binding

If a cross-reference grows attributes over time ("this block has a reason
and an expiry date"), migrate to a Binding:

1. Create a Binding with `type: blocking`, `subject: A`, `target: B`, plus
   the new attributes.
2. Remove the cross-reference field from A.
3. Log `workitem.link.migrated`.

This is the only case where removing a cross-reference is routine; normally
you keep them forever.
