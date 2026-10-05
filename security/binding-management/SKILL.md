---
name: binding-management
description: |
  Manage Binding entities — scoped, temporal, many-to-many relationships
  between v2 entity surfaces. Use when a relationship needs scope, time,
  or its own attributes — e.g. 'Alice is the tech lead for project X from
  Jan to June' or 'the security gate applies to this release WorkItem only
  on the main branch'.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-binding-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: actor-profile
        purpose: Resolve and validate Actor IDs referenced by this skill's entities.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Binding]
      mcp_tools: [create_binding, query_bindings, end_binding, resolve_bindings_for]
      templates: [binding]
---

# Binding Management

## Intro

A Binding is an entity that connects two other entities with optional scope,
temporality, and conditions. It is the junction-table pattern promoted to
a primitive, and it is the right choice whenever a relationship is more than
a simple "A references B" — for example "Alice is the tech lead on project X
for 2026," or "the security gate applies to this release WorkItem only on
the main branch."

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses may reach it directly from this skill's
> `mcp/mcp-config.json` or through the processkit gateway. Gateway
> deployments must surface only the processkit servers present in the
> installed/merged MCP configuration; this skill does not imply that
> unrelated processkit tools are available.

## Overview

### When to use a Binding vs a cross-reference

**Rule:** if a relationship has **scope**, **time**, or **its own attributes**
→ Binding. If it is just "A relates to B" → cross-reference in frontmatter.

| Situation                                                 | Binding or cross-ref? |
|-----------------------------------------------------------|-----------------------|
| "BACK-foo blocks BACK-bar"                                | cross-ref             |
| "DEC-x is related to BACK-y"                              | cross-ref             |
| "Alice is a developer" (globally, permanently)            | cross-ref (in Actor)  |
| "Alice is tech lead on project X for 2026"                | **Binding**           |
| "The security gate applies to releases generally"        | cross-ref             |
| "The security gate applies to this release WorkItem *only on main branch*" | **Binding** |
| "Sprint 42 runs from Apr 1 to Apr 14 and scopes these items" | **Binding**        |

If in doubt, prefer the cross-reference. Promote to a Binding only when you
actually need the extra dimensions.

### Binding types

`spec.type` is freeform; conventions emerge per project. Common ones:

| type                  | subject kind | target kind |
|-----------------------|--------------|-------------|
| `role-assignment`     | Actor        | Role        |
| `work-assignment`     | WorkItem     | Actor       |
| `workitem-gate`       | WorkItem     | Gate        |
| `scope-gate`          | Scope        | Gate        |
| `time-window`         | any          | any         |
| `budget-application`  | Artifact     | WorkItem/Scope |
| `constraint-scope`    | Constraint   | Scope       |
| `category-assignment` | any          | Category    |

In v2, Process and Schedule are not modeled as first-class binding
endpoints. Use the concrete entity being governed (for example a
WorkItem, Scope, Gate, or Artifact) and encode schedule-like recurrence
through a `time-window` Binding with an Artifact-backed recurrence rule.
Use `budget-application` to bind cost-policy Artifacts to the WorkItems
or Scopes they govern.

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Binding
metadata:
  id: BIND-bright-falcon
  created: 2026-04-06T00:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-alice
  target: ROLE-tech-lead
  scope: SCOPE-project-x
  valid_from: 2026-01-01
  valid_until: 2026-12-31
  conditions:
    approval_required: false
  description: "Alice fills the tech-lead role on project X for 2026."
---

Optional body: context for why this binding exists, related discussion, etc.
```

### Workflow

1. Pick the `type` — match an existing convention if possible.
2. Set `subject` (the entity "receiving" the relationship) and `target`
   (the entity "being bound to").
3. Set `scope` if the binding only applies within a particular scope.
4. Set `valid_from` / `valid_until` if the binding is time-bounded.
5. Add `conditions` for arbitrary constraints.
6. Save to `context/bindings/`.
7. Log `binding.created`.

### Ending a binding

To end a binding:

- **Preferred:** set `valid_until` to the current date, log `binding.ended`.
- **Alternative:** delete the Binding file (only if it was created in error).

Do NOT edit `subject` or `target` of an existing binding — write a new one
and end the old one. The history is what makes Bindings useful.

### Resolving "who currently fills role X in scope Y?"

1. Find Bindings where `type: role-assignment` and `target: ROLE-x` and
   (`scope: SCOPE-y` or `scope: null`).
2. Filter to those active at the current time (`valid_from ≤ now ≤ valid_until`
   or either unset).
3. Return the `subject` IDs.

The Phase 3 MCP server provides `resolve_bindings_for(entity_id, type?, at_time?)`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Using a Binding when a simple cross-reference would do.** If the
  relationship has no scope, no time bounds, and no attributes of its
  own ("this workitem relates to that decision"), use a frontmatter
  cross-reference, not a Binding. Bindings are overhead — reserve
  them for relationships that genuinely need their own lifecycle.
- **Using a cross-reference when scope or time matters.** The inverse
  trap: "Alice owns this for sprint 42 only" or "the security gate
  applies on the main branch only" must be a Binding, not an
  assignee field. Cross-references can't carry temporal validity.
- **Forgetting `valid_from` / `valid_until` on temporal Bindings.**
  A Binding without time bounds reads as "forever". If the
  relationship is bounded ("until end of quarter"), set the bounds
  at creation. Otherwise queries like "who owns X right now" return
  stale results.
- **Forgetting to end a Binding when the relationship ends.** Open
  Bindings accumulate as orphans. When the underlying relationship
  ends, call `end_binding` (or set `valid_until`) — don't just
  delete the entity, since the historical record matters.
- **Hallucinating subject or target IDs.** Always verify both the
  subject and the target exist via `index-management.get_entity`
  before creating a Binding. A Binding pointing at a non-existent
  entity is structurally invalid and breaks every later resolve
  query.
- **Querying current bindings without a time filter.** When asking
  "who is the tech lead now", filter by current time
  (`valid_from ≤ now ≤ valid_until`). A naive query returns every
  Binding ever, including expired ones.
- **Treating Bindings as RBAC enforcement.** Bindings are
  descriptive, not restrictive. They record who has which role,
  not who is allowed to do what. Authorization is out of scope —
  do not use Bindings as a permission check.

## Full reference

### Fields

| Field         | Type           | Notes                                                            |
|---------------|----------------|------------------------------------------------------------------|
| `type`        | string         | Freeform — the binding type. Conventions per project.            |
| `subject`     | string         | ID of the entity on the "from" side of the relationship.         |
| `target`      | string         | ID of the entity on the "to" side of the relationship.           |
| `scope`       | string         | Optional. Scope ID within which this binding applies.            |
| `valid_from`  | date/datetime  | Optional. When the binding starts being in effect.               |
| `valid_until` | date/datetime  | Optional. When the binding stops being in effect.                |
| `conditions`  | map            | Optional. Freeform constraints.                                  |
| `description` | string         | One-line human-readable summary.                                 |

### Why Binding is generalized from RoleBinding

DISC-001 introduced RoleBinding as the 18th primitive. DISC-002 §11 investigated
whether this should be generalized. The pattern of "put a third thing between
two things so either can change independently" is fundamental in software
design (GoF patterns, DI, junction tables) and appears in at least 7 relationship
types in processkit. Generalizing keeps the primitive count at 18 while covering
more cases. See DEC-023.

### No enforcement

Bindings are descriptive. processkit does not prevent actions based on
bindings — e.g., a WorkItem doesn't refuse to transition if the actor isn't
bound to the required role. Enforcement is a governance concern
(DEC-017).

### Indexing

In Phase 3, the index MCP server maintains a `bindings` table:

```
bindings(id, type, subject, subject_kind, target, target_kind,
         scope, valid_from, valid_until, active)
```

with `active` computed from `valid_from`/`valid_until` vs current time.
This makes "who currently holds role X" a single SQL query.

### Idempotency for "current state" bindings

When the same effective state is re-asserted (e.g. "Alice is still tech
lead"), prefer extending `valid_until` on the existing Binding rather than
creating a new one. This keeps history clean. If the underlying situation
*changed* and just happened to end up in the same place, that's a new
Binding.
