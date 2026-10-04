---
name: coherence-bandwidth-at-scale
description: Use when many networked entities (50+) cause bandwidth or CPU stress in coherence — crowds, swarms, bullet hells, large open worlds, simulators with many AI agents. Covers deterministic local sim with seeded state, CreationOnly sync, PredictionMode tuning, and interest management via CoherenceLiveQuery.
metadata:
  topic: networking
  engine: coherence
---

# Bandwidth at scale

## When to use this skill

- The developer says "lag," "stutter," or "high bandwidth" with many networked entities on screen.
- They are syncing transforms of dozens-to-thousands of entities (enemies, projectiles, particles, props).
- They are designing a bullet hell, horde survival, RTS, MMO, or factory sim.
- They are hitting the 20 Hz RS send rate ceiling or the 32,768-entities-per-client cap.
- A simulator is sending many `[Sync]` updates per tick.

## The core idea

The cheapest packet is the one you don't send. coherence is designed for replication, but at scale the right answer is often **not to replicate** — instead, sync a tiny *seed* once and let each client compute the rest locally. Reserve continuous sync for state that genuinely diverges across clients (player input, decisions made on the authority).

Four levers, in order of impact:

1. **Don't sync transforms** for entities whose motion is deterministic from initial state.
2. **`SyncMode.CreationOnly`** for anything that doesn't change after spawn.
3. **`CoherenceLiveQuery` / area-of-interest** so distant entities don't replicate at all.
4. **`PredictionMode` tuning** per binding for the entities that *do* need transform sync.

## Pattern 1: Deterministic local simulation from a seed

Spawn an entity with a seed and a target reference. Every client runs the same simulation; nothing else needs to sync.

```csharp
public class Swarmer : MonoBehaviour
{
    [Sync(DefaultSyncMode = SyncMode.CreationOnly)] public uint Seed { get; set; }
    [Sync(DefaultSyncMode = SyncMode.CreationOnly)] public CoherenceSync Target { get; set; }

    private System.Random _rng;

    private void Start()
    {
        _rng = new System.Random((int)Seed);
    }

    private void Update()
    {
        // Every client runs this — produces identical motion from identical seed.
        var jitter = new Vector3(
            (float)_rng.NextDouble() - 0.5f,
            0f,
            (float)_rng.NextDouble() - 0.5f);
        transform.position += (Target.transform.position - transform.position).normalized
                              * Time.deltaTime * 3f + jitter * 0.1f;
    }
}
```

The `Target` reference is a `CoherenceSync` — this is a schema-level entity primitive, so it transmits as an ID, not the target's full state. If the target leaves the client's query area, the reference becomes null on that client only; handle it.

## Pattern 2: CreationOnly for spawn-time configuration

Anything that's decided when the entity is born and never changes afterwards.

```csharp
[Sync(DefaultSyncMode = SyncMode.CreationOnly)] public int EnemyTypeIndex { get; set; }
[Sync(DefaultSyncMode = SyncMode.CreationOnly)] public uint DeathSeed { get; set; }
[Sync(DefaultSyncMode = SyncMode.CreationOnly)] public byte AppearanceVariant { get; set; }
```

Cost: one packet at creation, zero thereafter. Pair with a lookup table that's identical on every client (`ScriptableObject` index, enum value, etc.).

## Pattern 3: Interest management via CoherenceLiveQuery

Place a `CoherenceLiveQuery` on each player's avatar with a sensible extent. The query defines an axis-aligned box centered on its transform; entities outside the box are destroyed on that client and the RS doesn't even send the updates.

```csharp
// On the player prefab
var query = gameObject.AddComponent<CoherenceLiveQuery>();
query.Extent = 30f;   // half-side of the box, in metres (so total side = 60m)
```

Rules of thumb:
- The shape is a box, not a sphere — `Extent` is the half-side length. Pick a value slightly bigger than the player's visual range, not 10× bigger.
- Tag entities (`CoherenceTagQuery`) so global things (the boss, the goal, the host player) always replicate regardless of distance.
- A client can have at most 15 active queries — don't make queries per-entity.
- `ExtentUpdateThreshold` controls hysteresis — the query won't re-fire until the player moves more than this distance, preventing churn at the boundary.

## Pattern 4: PredictionMode for locally-simulated bindings

`PredictionMode` is a per-binding setting that controls **whether incoming network samples are applied to that binding, or discarded in favour of locally-predicted values.** It is *not* an interpolation/extrapolation setting — those are configured separately.

The three values (`Coherence.PredictionMode`):

- **`Never`** *(default)* — incoming network samples are always applied. Use for everything where the authority is the source of truth and you want each client to see exactly what the authority sends.
- **`Always`** — incoming network samples are *never* applied; the binding stays on whatever the local simulation/Update writes. Use when each client computes the value locally (e.g. deterministic local simulation under Pattern 1) and you don't want sparse network samples to overwrite it.
- **`InputAuthority`** — behaves like `Always` only on entities the local client has input authority over; like `Never` everywhere else. Use for locally-controlled prediction on inputs (typically combined with `CoherenceInput`).

The pattern that ties this to bandwidth-at-scale: when you're running deterministic local sim under Pattern 1, you want the *seeded inputs* to replicate (`CreationOnly` is enough) but the *per-frame derived state* to stay locally predicted, not get periodically yanked back to a stale authoritative sample. Flip those bindings to `Always`:

```csharp
// Find a specific binding by descriptor name and switch it to local-prediction-wins.
var positionBinding = sync.Bindings.Find(b => b.Descriptor.Name == "position");
positionBinding.predictionMode = PredictionMode.Always;
```

(Use the public `Bindings` list off `CoherenceSync`. The field on `Binding` is `predictionMode` lowercase; you can also set it via the Configure window per-binding at author time.)

For locally-controlled players that run client-side prediction over input commands, prefer `InputAuthority` — predicted only on the owning client, replicated normally on observers.

## When it works / when it doesn't

**Deterministic local simulation works when:**
- The simulation depends only on inputs that *are* synced (target position, seed, time).
- The simulation uses a deterministic RNG (don't use `UnityEngine.Random` from multiple places — it shares state with other systems).
- The cost of a small visual drift between clients is acceptable.

**It doesn't work when:**
- The simulation reads `Physics.Raycast` against geometry that differs between clients (streamed scenes, destructibles).
- The entity needs to interact with another client's input authority (then you need to replicate the interaction, not the motion).
- You need exact agreement on damage/hit registration — those go through the authority anyway.

**CreationOnly works when** the field is set once and never reassigned. If you ever change it after creation, replicas won't see the new value.

## Late joiners

`CreationOnly` fields *are* sent to late joiners as part of the initial entity replication. Deterministic local simulation needs a way to fast-forward: either include a `[Sync(CreationOnly)] uint StartSimFrame` and skip ahead, or accept that late joiners see slightly different state until the next state-changing event arrives.

## Gotchas

- **`UnityEngine.Random` is global state.** A second system rolling random numbers will desync deterministic sims. Use `System.Random` instances seeded per-entity.
- **`Time.time` differs slightly per client.** For frame-synchronized events, use a `[Sync] uint StartSimFrame` and compare against a synced authority clock, not wall clock.
- **`CoherenceLiveQuery.Extent` bigger than RS visibility limits won't help** — the RS imposes its own limits; check `Project Settings > coherence`.
- **Schema fields are capped at 32 per CoherenceSync.** If you're adding many `CreationOnly` fields, split across multiple sibling components (see [coherence-animation-networking](../coherence-animation-networking/SKILL.md) for the sharding pattern).
- **`PredictionMode` is not interpolation.** Position smoothness at low send rates is governed by the binding's interpolation settings (linear/catmull-rom, sample-time tolerance), not by `PredictionMode`. Setting `PredictionMode = Always` to "make it smoother" is the wrong knob — it just stops applying network samples.

## Anti-patterns

- Syncing transforms for projectiles. Projectiles are cheaper to fire-and-simulate locally and validate hits on the authority.
- Syncing every property of an entity "just in case." Audit which fields actually need to change at runtime.
- One giant `CoherenceLiveQuery` covering the whole scene. That's the same as no query.
- Using `[Sync]` for visual-only state (particle counts, screen-shake amplitude). Drive those from the synced game state, not over the network.

## See also

- `Behaviours/MovingPlatform.md` — deterministic motion driven by `Time.timeAsDouble`, no transform sync.
- coherence docs: archetypes (LOD groups for distance-based field reduction) — complementary to interest management.
