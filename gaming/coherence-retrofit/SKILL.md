---
name: coherence-retrofit
description: Use when adding coherence multiplayer to an existing single-player Unity game — keeping solo and MP modes from one codebase with minimal gameplay-code changes. Covers the proxy pattern that keeps gameplay unaware of authority, dual-mode static checks for solo-vs-MP branching, and save migration.
metadata:
  topic: networking
  engine: coherence
---

# Retrofitting multiplayer onto an existing single-player game

## When to use this skill

- The developer has a working single-player game and is adding multiplayer.
- They're worried about "littering authority checks through every gameplay file."
- They want solo and multiplayer to share a single codebase, not a fork.
- A large codebase already exists that wasn't designed with networking in mind.
- Saves from solo mode should survive entering multiplayer (or at least not be destroyed).

## The core idea

Single-player code assumes it has authority over everything. Multiplayer code can't. Bridging the two without rewriting either is a *delegation* problem: gameplay code stays naive ("I am doing this action"), and a thin network layer intercepts and either runs locally (solo or you-are-authority) or forwards to the authority (multiplayer and you-aren't).

Three structural choices make this manageable:

1. A **two-level proxy** that wraps each networked entity — the logical entity stays unaware; a companion proxy holds `[Sync]`/`[Command]` plumbing.
2. **Static-mode predicates** (`IsSinglePlayerOrHost`, `IsOnlineClient`) that gameplay code reads to make the rare needed branching choices.
3. **Save format isolation** so multiplayer never overwrites the solo save.

## Pattern 1: Two-level proxy

Split each networked thing into a *logical entity* (the gameplay-facing class, unchanged) and a *network proxy* (the coherence-aware companion). The logical entity holds a reference to its proxy and falls back to "I have authority" when none exists (solo mode).

```csharp
public abstract class NetworkProxiedEntity : MonoBehaviour
{
    public NetworkEntityProxy NetworkProxy { get; set; }  // null in solo

    // Solo (null proxy) → treat as authority. MP → ask coherence.
    public bool IsNetworkAuthority => NetworkProxy?.HasStateAuthority ?? true;

    // Convenience: returns the proxy only if we'd be the one sending RPCs.
    protected NetworkEntityProxy AuthProxy
        => IsNetworkConnected && IsNetworkAuthority ? NetworkProxy : null;

    public void PlaySound(string clip)
    {
        // Always play locally — non-authority clients want to hear it too.
        AudioManager.Instance.PlayOneShot(clip, gameObject);
        // If we're authority, broadcast to others. If we're a remote, do nothing
        // (we already received this command from authority).
        AuthProxy?.RemotePlaySound(clip);
    }
}

public abstract class NetworkEntityProxy : MonoBehaviour
{
    private CoherenceSync _sync;
    public bool HasStateAuthority => _sync.HasStateAuthority;

    [Command]
    public void RemotePlaySound(string clip)
    {
        // Authority sends; remote clients receive and play locally
        if (HasStateAuthority)
        {
            _ = _sync.SendCommand<NetworkEntityProxy>(
                nameof(RemotePlaySound), MessageTarget.Other, clip);
            return;
        }
        // Remote: play through the logical entity
        GetComponent<NetworkProxiedEntity>()?.PlaySound(clip);
    }
}
```

Result: a gameplay programmer calls `entity.PlaySound("Roar")` from anywhere. In solo it just plays. In multiplayer it plays locally and replicates correctly. The networking logic lives in one base class, not scattered through gameplay.

## Pattern 2: Static-mode predicates

For the genuinely-different cases (host-only spawning, host-only economy mutations) expose a small set of statics that gameplay code can check. Two or three predicates cover almost everything:

```csharp
public static class NetworkMode
{
    private static NetworkManager Instance => /* your singleton accessor */;

    /// True in solo play and when running as the host.
    public static bool IsSinglePlayerOrHost
        => Instance == null || !Instance.IsConnected || Instance.IsHosting;

    /// True only in multiplayer as a non-host.
    public static bool IsOnlineClient
        => Instance != null && Instance.IsConnected && !Instance.IsHosting;

    /// True only when running as the host in an active session.
    public static bool IsOnlineHost
        => Instance != null && Instance.IsConnected && Instance.IsHosting;
}
```

Then gameplay reads:

```csharp
public void SpawnQuestNPC()
{
    if (!NetworkMode.IsSinglePlayerOrHost) return;  // clients defer to host
    // ... spawn logic unchanged from solo
}
```

The vast majority of solo code needs zero changes. Only spawn points, save writes, and economy mutations need the gate.

## Pattern 3: Save format isolation

Solo saves should survive multiplayer. The straightforward rule: **never write a multiplayer session's state back to the solo save slot.**

```csharp
public static class SaveSlot
{
    public static string ForSession() =>
        NetworkMode.IsOnlineClient
            ? Path.Combine(Application.persistentDataPath, "session_temp.save")
            : Path.Combine(Application.persistentDataPath, "solo.save");
}
```

On joining a multiplayer session, *clients* receive the host's state via fragmented command (see [coherence-persistence](../coherence-persistence/SKILL.md)) and write it to a temp slot. When the session ends, the temp slot is discarded. The solo save is untouched.

On the host, two options:
- **Sessions are throwaway** — host plays from a fresh state every session. Simple, fits party games and quick co-op.
- **Sessions persist on the host** — host writes back to a multiplayer-specific save (`coop.save`, not `solo.save`). Their solo file stays clean.

## Pattern 4: Toggling network behaviour by entity, not globally

Sometimes only *some* entities need networking. A combat enemy maybe; a UI tutorial popup definitely not. Don't add `CoherenceSync` to everything — add it only to things that need to be visible/mutable across clients, and let everything else stay client-local.

```csharp
public class NetworkAwareSpawner : MonoBehaviour
{
    [SerializeField] private GameObject _soloPrefab;        // no CoherenceSync
    [SerializeField] private GameObject _networkedPrefab;   // with CoherenceSync

    public GameObject Spawn(Vector3 pos)
    {
        var prefab = NetworkMode.IsSinglePlayerOrHost
            ? (NetworkMode.IsOnlineHost ? _networkedPrefab : _soloPrefab)
            : null;  // clients don't spawn directly; host does
        return prefab != null ? Instantiate(prefab, pos, Quaternion.identity) : null;
    }
}
```

## Pattern 5: Get/set passthrough proxies (the mechanism behind Pattern 1)

The proxy gotcha — "don't put `[Sync]` on gameplay classes" — names the rule, but doesn't name the *mechanism* that makes the rule painless: the proxy's `[Sync]` property is a **plain get/set passthrough to the underlying gameplay field.** coherence polls the getter on the authority each tick, detects changes, and pushes them; on remotes, the setter writes straight back into the gameplay field. Gameplay code never references the proxy, never calls a `.Push()`, never knows the field is networked.

**On naming.** Multiple shipped coherence projects independently converged on `Network<X>Proxy` for this component — both because "proxy" is the established term in networking literature (Unreal's `SimulatedProxy`/`AutonomousProxy`, gRPC/CORBA stubs) and because it disambiguates from coherence's *baked* bindings (the generated schema-glue code, a different thing). "Binding" works as a synonym, but **Proxy** is the convention. Examples below use the Proxy naming.

```csharp
// Gameplay enum — completely network-naive. Used by solo-mode logic
// untouched; in MP, both authority and remote replicas read the same
// values because the proxy keeps them in sync.
public enum EntityState { Idle, Acting, Stunned, Defeated }

// Gameplay class stays a normal field — no setter hook, no callback, no
// network awareness. Solo mode works unchanged.
public class Entity : MonoBehaviour
{
    public EntityState State;   // mutated by authority-side state machine
}

// Proxy lives in a separate networking layer and is added to the prefab
// as its own component. Gameplay class never references it.
public class NetworkEntityStateProxy : MonoBehaviour
{
    [SerializeField] Entity _entity;

    [Sync] public EntityState SyncedState
    {
        get => _entity != null ? _entity.State : EntityState.Idle;
        set { if (_entity != null) _entity.State = value; }
    }

    void Awake()
    {
        if (_entity == null) TryGetComponent(out _entity);
    }
}
```

(coherence can bake enums directly — no need to cast to `int`. The bake picks the minimum number of bits.)

### Why this pattern matters

1. **Pure addition.** Delete the proxy file, remove the component, gameplay still works. The field is the source of truth; the proxy is a network *observer*. This is what makes "additive multiplayer" actually additive.
2. **No write-site coverage problem.** You don't have to find every line that writes to the field and hook it. If gameplay writes the field in N places — internal transitions, external overrides, custom scripts — all N sync for free because the polling getter catches every change.
3. **Field-to-property refactors are safe.** Gameplay code can change *how* it reads/writes the field (caching, validation, computed property, splitting into multiple fields) without breaking the proxy, as long as the getter returns the current value.
4. **Reverse direction is symmetric.** On a remote, the setter writes into the gameplay field whenever a new synced value arrives. Existing read sites — equality checks, helper predicates — automatically see the right value with zero authority awareness, and gameplay code stays free of `_sync.HasStateAuthority` branches.

### Why you reach for this pattern

The trigger is a class of bug: **local-only gameplay state that gates per-frame effects on remote replicas, where the authority-side update loop is disabled.**

Concrete symptom: a timed effect (damage-over-time, regen tick, decay timer) is a `MonoBehaviour` that runs `Update` on every client where its GameObject exists. Its update gates on a check like `if (target.IsDefeated()) return;` to stop ticking when the target dies. On the authority, the state machine flips the gameplay field and the gate fires. On remote replicas, the authority-side update loop is *disabled* (whether by your own remote-configurator component, a `NetRemoteConfigurator` pattern, or just because the relevant `Update` is wrapped in an `if (HasStateAuthority)` check), so the state transition never runs locally, the field stays at its old value, the gate never fires, and the effect keeps ticking forever — pushing ghost commands back to the authority and showing ghost visuals locally.

You'll see the same shape anywhere a `MonoBehaviour.Update` running on remote reads a local-only field that only the authority's tick maintains:
- Per-tick effects gating on death / knockout / disabled
- HUD elements gating on alive-state
- VFX controllers reading a "current behavior" enum
- Audio loops checking an "is moving" / "is acting" flag

The reflex fix is to fall back to a *synced animator parameter* (e.g. `animator.GetBool("Dead")`) because animator parameters happen to be `[Sync]`'d via coherence's animator binding. That works, but it's the wrong abstraction — it ties gameplay correctness to "the animator happens to mirror this state," which can drift any time someone restructures the animator. **The clean fix is to sync the gameplay field itself via a passthrough proxy** and let gameplay code keep reading the field.

### Worked example: applying this to an existing gameplay enum

You have:

```csharp
public class Entity : MonoBehaviour
{
    public EntityState State;   // set by an authority-side state machine
    public bool IsDefeated() => State == EntityState.Defeated;
}

public class TimedEffect : MonoBehaviour    // lives as a child of Entity
{
    public Entity Target;
    void Update()
    {
        if (Target.IsDefeated()) return;   // works on authority, broken on remote
        // ... tick effect ...
    }
}
```

**Steps to fix without touching either class:**

1. Create `NetworkEntityStateProxy.cs` with the get/set passthrough above.
2. Add the proxy component to every prefab variant of `Entity`. (One-time prefab edit; no script changes.)
3. Done. `TimedEffect` is unchanged. `IsDefeated` is unchanged. Both now work on remote replicas because the proxy mirrors `State` over the wire.

If gameplay code was previously using a synced animator-parameter fallback (e.g. `IsDefeated() || animator.GetBool("Dead")`), you can now delete the fallback — the field itself is authoritative on every client.

### Variations and constraints

- **Prefer the gameplay type directly in the `[Sync]` property.** coherence bakes enums and compresses them to the minimum bit width. Casting to `int` is usually unnecessary and obscures intent. *Exception:* if you need a tri-state representation that a bool/enum can't express (e.g. `true` / `false` / `not-yet-set`), an `int` with a sentinel — `Open = 1, Closed = 0, Null = -1` — is a legitimate use, e.g. on a `NetworkDoorProxy` for state that's meaningfully *absent* until the authority decides.
- **No backing field in the proxy.** The getter pulls live from gameplay each tick; the setter writes live into gameplay. The proxy holds no state of its own — it's a window onto the gameplay field.
- **Null-guard the getter.** Bake-time and Awake-order edge cases can call the getter before the gameplay reference is wired. Return a sensible default (the enum's first value, `0`, `null`, the sentinel, etc.) so coherence doesn't NRE during initial sync.
- **Polling cost is per-property, not per-write.** coherence checks each `[Sync]` getter at its configured sample rate. For coarse state (an enum that changes a few times per minute), this is free. For high-churn numeric fields (HP that updates every tick) the same pattern works, but be aware you're paying a poll cost — see [coherence-bandwidth-at-scale](../coherence-bandwidth-at-scale/SKILL.md).
- **Don't combine passthrough with a setter-side `OnValueChanged` callback in the gameplay class.** If gameplay code reacts to its own field changing, the remote setter will fire that callback on every received value — possibly re-entering systems that assume authority. Keep state mutation in the field and put reactions in a separate, authority-gated update path.

### When you'd *not* use this

- **Events, not state.** Damage spikes, sound triggers, one-shot effects — those want `[Command]` (see Pattern 1's `RemotePlaySound`). Polling a getter to detect "did a thing happen" leaks events that arrive on the same frame.
- **Massive state.** Don't passthrough-sync a 200-entry inventory list as one big `[Sync]` field — diff each change instead, or use a bitmask sync for presence-style state (one bit per slot, only the diff is wired).
- **State that legitimately differs between authority and remote.** A predicted local position, an interpolated visual angle, a UI-only highlight — these are *supposed* to drift. Don't try to flatten them with a passthrough.

## When this approach fits

**The proxy pattern works when:**
- The single-player code is structured enough that you can identify networked entities and put proxies on them. Spaghetti code with global singletons is harder.
- Audio/VFX side-effects can run locally on every client (typical for games).
- The "authority" mapping is clear — usually one host plus N clients, or a simulator.

**It struggles when:**
- The game relies on lockstep determinism (RTS with fog-of-war). Different paradigm; see other coherence patterns for input-replication models.
- Authority needs to migrate frequently (host-leaves-mid-session in a peer-hosted setup). Solvable but adds complexity.
- The single-player save format is opaque (encrypted, third-party plugin) — you may not be able to serialize it for hand-off.

## Gotchas

- **Don't put `[Sync]` fields directly on existing gameplay classes.** That couples them to coherence forever. Always go through the proxy.
- **`AuthProxy?.X()` returns silently if there's no authority** — easy to miss when debugging. Add an assert or log in development builds if a command was expected to send.
- **Singletons that hold "the player" in solo mode break in MP** where there are multiple players. Refactor to lookup-by-id (see the player registry pattern).
- **Existing pause logic that freezes `Time.timeScale = 0` is a problem.** The network keeps running; remote players see a frozen avatar. Either disable pause in MP or freeze locally without touching time scale.
- **Save format changes need migration.** If you bumped the solo save format in v2 and a v1 file shows up over the multiplayer payload, handle it the same as a local v1 load.
- **`[Sync]`-decorated properties auto-register; you don't need to add them in the CoherenceSync window.** The bake discovers them from the attribute. Manual binding in the inspector is only required for Unity built-ins that aren't decorated — `Transform` position/rotation/scale, `Animator` parameters, audio source state, etc. Agents guiding someone through wiring up a new networked prefab routinely overshoot by telling them to add the `[Sync]` properties manually — skip that step.

## Anti-patterns

- Forking the codebase into "solo" and "MP" variants. The maintenance burden is brutal and features drift.
- Wrapping every method call in `if (IsHost) ... else ...`. The proxy pattern eats most of these.
- Spawning networked entities directly in gameplay code (`Instantiate(prefab)`). On clients this is wrong — the host must spawn and the client receives. Route through a spawner that knows the mode.
- Sending a `[Command]` for every gameplay event when a `[Sync]` field would do. Commands are for events; persistent state belongs as fields. Mixing them up bloats bandwidth.
- Adding `CoherenceSync` to UI/HUD elements. UI is client-local; only sync the *data* it displays.

## See also

- `Behaviours/NetworkManager.md` — the `IsConnected`/`IsHosting` predicates the static-mode helpers wrap.
- [coherence-persistence](../coherence-persistence/SKILL.md) — host-state hand-off for catching joining clients up to the existing single-player state.
- [coherence-authority-handoff](../coherence-authority-handoff/SKILL.md) — for objects that need contested ownership (pickups, doors) in the retrofit.
- coherence docs: entity lifetime (session vs persistent), CoherenceSync inspector overview.
