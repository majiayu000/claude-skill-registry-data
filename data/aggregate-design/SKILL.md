---
name: aggregate-design
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P019
  - P043
  - P044
  - P045
  - P004
  - P042
  - P021
  claims:
  - C00139
  - C00140
  - C00142
  - C00143
  - C00144
  - C00145
  - C00141
  - C00146
  - C00147
  - C00148
  - C00149
  - C00085
  evidence:
  - E00088
  - E00089
  - E00091
  - E00092
  - E00093
  - E00094
  - E00090
  - E00095
  - E00096
  - E00097
  - E00098
  - E00048
  source_anchors:
  - 9e0c1e6c6dd6-c0007
  - 9e0c1e6c6dd6-c0004
  authored_from_digest: 0d38c448a0e5da28c5b1e9d379d03abec05e64eb1f5eb1a19f2a2724b20a1d41
---

# Aggregate Design

## Purpose

Review and define the internal composition of an Aggregate: classify domain
objects as Entities or Value Objects using identity and immutability criteria,
draw a single consistent boundary around the cluster, designate one root Entity
as the sole external access point, and verify that all invariants are enforced
through the root rather than by outside callers.

## When to use

- A domain model contains a cluster of related objects and the reviewer must
  determine whether the boundary and root are correctly placed.
- Existing code allows external objects to hold references to objects inside an
  Aggregate boundary, bypassing the root.
- A Repository exists for a non-root object, exposing internals to direct
  database queries.
- Attributes on an Entity are candidates for extraction into a Value Object, or
  an existing Value Object exposes mutation methods.
- Invariants that span several closely related objects are difficult to enforce
  consistently.

## Procedure

### Step 1 — Classify each domain object

For every object in the cluster under review, decide whether it is an Entity or
a Value Object before drawing any boundary.

**Entity test (P004 / C029 / C030):**
- Ask: is this object distinguished by who or what it is, independently of its
  current attribute values? Does the system need to track this object across
  state changes?
- If yes, it is an Entity. Verify that a unique identity operation is defined
  (a single attribute, a combination, or a purpose-made identifier) and that
  equality is based on that identity, not on attribute comparison.
- Flag as a defect: two objects with the same identity treated as different, or
  identity missing entirely from an object that requires tracking.

**Value Object test (P005 / C032 / C033):**
- Ask: does this object describe an aspect of a concept solely through its
  attributes, with no need for individual tracking?
- If yes, it is a Value Object. Verify immutability: the object must be
  constructable from its attributes and must expose no mutation methods. Any
  change in value must produce a new instance.
- Flag as a defect: a Value Object with setters or in-place modification
  methods; or a set of conceptually related attributes scattered as individual
  fields on an Entity that could form a Value Object.

### Step 2 — Draw the Aggregate boundary

Group the Entities and Value Objects that share invariants and whose lifecycle
is controlled as a unit (P007 / C043).

- The boundary encloses objects that cannot maintain their invariants
  independently of each other.
- Objects outside the boundary — including roots of other Aggregates — must not
  be enclosed.
- Keep Aggregates as small as the invariants allow; a boundary that is too wide
  increases contention and makes invariant enforcement harder.

### Step 3 — Select and verify the root Entity

Designate exactly one Entity inside the boundary as the Aggregate root (P007 /
C043 / C044).

- The root must have global identity (meaningful and unique across the entire
  system).
- Internal Entities have only local identity, meaningful within the boundary
  alone; flag any internal Entity whose identity is referenced or resolved
  outside the boundary.
- All access from outside the boundary must flow through the root. Flag every
  external reference that points to an internal Entity or Value Object held
  persistently.

### Step 4 — Enforce the access rule

Review how external objects interact with the Aggregate (P007 / C044).

- External objects may hold a persistent reference only to the root.
- The root may pass a transient reference to an internal member for use within
  a single operation (for example, supplying a copy of a Value Object). That
  reference must not be stored by the external caller.
- Flag: external code that stores a persistent reference to an internal Entity;
  external code that mutates internal state without going through the root.

### Step 5 — Verify invariant enforcement through the root

Because all state changes enter through the root, the root is responsible for
maintaining every invariant across the cluster (C044 / C045).

- Confirm that the root's methods check invariants before committing internal
  state changes.
- Flag: internal state that can be changed by calling methods directly on an
  internal Entity without the root being involved; invariant checks duplicated
  in client code rather than centralised in the root.

### Step 6 — Check persistence and deletion scope

Verify Repository and deletion rules (P007 / C046).

- A Repository must exist for the root and must not exist for any internal
  object. Flag any Repository whose subject is a non-root internal Entity.
- Database queries must return only root objects; internal objects are reached
  by navigating associations from the root, not by direct query.
- When the root is deleted, all internal objects are deleted with it. Flag
  designs where internal objects survive root deletion or are cleaned up by
  external callers.
- Objects inside this Aggregate may reference the roots of other Aggregates but
  must not reference their internals.

## Inputs

- The set of domain objects (Entities and Value Objects) and their associations
  that are candidates for inclusion in the Aggregate.
- Stated invariants: rules that must hold across any data change touching the
  cluster.
- Persistence and deletion requirements for the cluster.
- Existing code or design diagrams showing current reference topology.

## Output

For each Aggregate reviewed, a structured finding containing:

- **Boundary**: which objects are inside and which are outside.
- **Root**: the chosen root Entity, with its global identity scheme noted.
- **Internal members**: Entities (local identity only) and Value Objects, with
  immutability status confirmed or flagged.
- **Access violations**: any external persistent references to internal objects,
  with corrective steps (redirect reference to root, or extract a separate
  Aggregate if the reference reflects genuine cross-boundary lifecycle
  independence).
- **Repository violations**: any Repositories for non-root objects, with
  corrective steps.
- **Invariant gaps**: invariants not enforced by the root, with corrective
  steps.
- **Value Object defects**: mutation methods found, or scattered attributes that
  should be consolidated into a Value Object.

## Provenance

Grounded in principles P008, P019, P043, P044, P045, P004, P042, P021 of this package, derived from Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003). Representative chunk anchors: `9e0c1e6c6dd6-c0007`, `9e0c1e6c6dd6-c0004`. Source rights: `distillation-only` — all content is paraphrased; no verbatim quotation.
