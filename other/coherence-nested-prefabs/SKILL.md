---
name: coherence-nested-prefabs
description: Use when authoring a CoherenceSync prefab whose hierarchy contains a reference to another prefab that is itself CoherenceSync (one networked prefab nested inside another in the prefab asset, at edit time) in coherence. Covers detecting that asset-level nesting and synchronizing the nested entities with PrefabSyncGroup. NOT for runtime parenting/reparenting of independent networked entities — that is CoherenceNode / parent-child sync, a different concern.
metadata:
  topic: networking
  engine: coherence
---

# Nested networked prefabs

## When to use this skill

- A `CoherenceSync` prefab contains, in its hierarchy, a **reference to another
  prefab that is itself a `CoherenceSync`** — i.e. one networked prefab nested
  inside another at edit time (gate containing a harvestable, encounter
  containing a spawner, vehicle containing a turret, …).
- You are authoring such a composite prefab and need its nested networked child
  to behave correctly online.

This is strictly about **edit-time nesting inside the prefab asset**. It does
**not** cover:

- A prefab with `CoherenceSync` but **no** nested CoherenceSync prefab — ordinary
  single-entity setup.
- **Runtime parenting** — making one networked entity a child of another at
  runtime (e.g. picking up an item, mounting a vehicle). That is `CoherenceNode`
  / parent-child sync, not PrefabSyncGroup.

## The core idea

coherence networks one `CoherenceSync` as one entity. A `CoherenceSync` prefab
nested inside another `CoherenceSync` prefab is not automatically one shared
entity: when the parent is instantiated on each client, **each client also
instantiates its own copy of the nested child as a separate network entity**,
and coherence has no edit-time record tying those copies together. Their
lifetime and identity are not coordinated across clients.

`Coherence.Toolkit.PrefabSyncGroup` is the SDK mechanism that records the
nesting at edit time so coherence can keep the nested entities' structure and
lifetime synchronized at runtime — collapsing the per-client copies onto one
shared, host-authoritative child.

## Detecting the nesting (edit time, at the asset level)

Detect it from the **prefab assets**, before any runtime symptom. The signature
is: *a CoherenceSync prefab whose hierarchy references another prefab that also
has CoherenceSync, with no `PrefabSyncGroup` on the parent root.*

Process:

1. Find the `CoherenceSync` script's GUID (from `CoherenceSync.cs.meta` in the
   SDK). Call it `CS_GUID`.
2. Build the set `S` of prefabs that contain a MonoBehaviour referencing
   `CS_GUID` — these are the CoherenceSync prefabs.
3. For each prefab in `S`, find nested prefab references. In Unity prefab YAML a
   nested prefab instance is a `PrefabInstance` block with
   `m_SourcePrefab: {... guid: <childGuid>}`. Resolve each `childGuid` to its
   prefab asset.
4. If a resolved child prefab is **also in `S`**, the parent nests a networked
   prefab. If the parent root has no `PrefabSyncGroup`, it is unsynchronized.

This is exact (it keys off the actual CoherenceSync script reference and real
nested-prefab references), unlike runtime symptoms — duplicated entities or
"no client has authority" can arise from several unrelated uniqueness issues, so
they confirm a problem but do not identify this specific cause. Use the
asset-level scan to find it early.

## Fixing it with PrefabSyncGroup

Add `Coherence.Toolkit.PrefabSyncGroup` to the **parent prefab's root**, then
bake (the synced `ids` field must enter the schema). Behavior, per
`Coherence.Toolkit/PrefabSyncGroup.cs`:

- It declares `[Sync, OnValueSynced(nameof(OnReceivedIds))] public byte[] ids`.
  On `OnEnable` it discovers the nested child `CoherenceSync`s
  (`GetComponentsInChildren`, excluding the root), assigns each a deterministic
  id (a `Guid` hash, 4 bytes per child) packed into `ids`, sets each child to
  `uniquenessType = NoDuplicates` with a corresponding `ManualUniqueId`, and
  disables the child until the parent entity is established.
- `EnableChildrenRoutine` enables the children once this client has authority,
  or — on a remote — once the host's child entity has been received, so a local
  create can't reach the Replication Server first and steal authority.
- `OnReceivedIds` (remotes only) rewrites each child's `ManualUniqueId` to the
  host's id from the synced `ids`, so `NoDuplicates` collapses the copies onto
  the single host-owned entity.

Constraints (enforced by the component):

- `[RequireComponent(CoherenceSync)]`, `[DisallowMultipleComponent]`, and it
  **must be on the prefab root** — `OnValidate` errors otherwise.
- A nested child needs a `CoherenceNode` only if it is **2+ levels deep**.
- If a PrefabSyncGroup prefab is itself nested as an instance inside another
  PrefabSyncGroup, **disable** the component on that nested instance.

Scope: PrefabSyncGroup is for **runtime-instantiated** nesting. For a
**scene-placed** nested entity, set the child's `Uniqueness = NoDuplicates`
directly instead.

## Alternatives to nesting

- **De-nest:** make the child a top-level networked prefab that the host
  instantiates and reparents under the parent at runtime. The child is then an
  independent, unambiguously host-owned entity; no shared-id machinery.
- **Fold into the parent:** if the child only needs a few synced values, remove
  its `CoherenceSync` and add those `[Sync]` fields to the parent's binding —
  one entity, no nesting.

Prefer PrefabSyncGroup when authoring the composite prefab in one place is
valuable and the child is a genuine entity with its own bindings; prefer
de-nesting when the child's lifetime and authority should be explicit and
independent.

## See also

- `coherence-baking` — the bake/schema workflow this fix depends on.
- coherence docs: *Parenting network entities → Nesting prefabs at edit time*.
- SDK: `Coherence.Toolkit/PrefabSyncGroup.cs`.
