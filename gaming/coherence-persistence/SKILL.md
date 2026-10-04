---
name: coherence-persistence
description: Use for persistent coherence worlds — cross-session saves, rejoinable rooms, growth/decay/cooldown timers, or any state a late-joining client must catch up to. Covers time-anchored state, unique-ID preservation across save/load, host state handoff via fragmented commands, and late-joiner ack patterns.
metadata:
  topic: networking
  engine: coherence
---

# Persistence and join-in-progress catch-up

## When to use this skill

- "How do I save a multiplayer game and load it next session?"
- "A player joins mid-session and doesn't see the current world state."
- The world has timers — crops growing, fires burning down, cooldowns ticking.
- Pre-placed objects in the scene must survive being destroyed and respawning in the same place across sessions.
- The developer mentions `UniquenessManager`, `ManualUniqueId`, or `IsOrphaned` in a save/load context.

## The core idea

coherence offers two long-lived state stores: **Worlds** (persistent across sessions until shutdown) and **Rooms** with persistence (entity lifetime configured per-prefab). Either way, three classes of state need attention:

1. **Mutable game state** the authority owns and freshly-joined clients receive via live query (free, automatic).
2. **Time-based state** that derives from "when did X happen" — sync the timestamp, not the current value.
3. **Bulk session state** (save files, inventories, level seeds, world maps) too large for `[Sync]` fields — ship via fragmented command on join.

## Pattern 1: Time-anchored state

For anything that progresses on a clock — plants growing, fires burning, cooldowns — sync the *start time* once, then derive the current state locally from `DateTime.UtcNow` (or the synced authority time).

```csharp
public class GrowingPlant : MonoBehaviour
{
    [Sync(DefaultSyncMode = SyncMode.CreationOnly)] public uint PlantedAtUnixTime { get; set; }

    private static readonly TimeSpan SproutAfter = TimeSpan.FromMinutes(2);
    private static readonly TimeSpan BloomAfter  = TimeSpan.FromMinutes(10);

    private void Update()
    {
        var planted = DateTimeOffset.FromUnixTimeSeconds(PlantedAtUnixTime).UtcDateTime;
        var age = DateTime.UtcNow - planted;

        if      (age >= BloomAfter)  SetStage(Stage.Bloom);
        else if (age >= SproutAfter) SetStage(Stage.Sprout);
        else                         SetStage(Stage.Seed);
    }
}
```

Cost: one synced field forever. Late joiners get the right state immediately. No "current stage" enum to keep in sync, no callbacks firing for missed transitions.

## Pattern 2: Preserving network identity across save/load

When you save a scene-placed networked object and reload it, coherence assigns a *new* unique ID by default — references and persistent entity links break. Fix: persist the existing ID and re-register it with the bridge's `UniquenessManager` *before* you instantiate the object.

```csharp
[Serializable]
public class SavedNetworkObject
{
    public Vector3 position;
    public Quaternion rotation;
    public string coherenceUniqueId;  // preserved from the original instance
    // ... other gameplay state
}

public static class NetworkSaveIdentity
{
    public static SavedNetworkObject Capture(GameObject instance, Vector3 pos, Quaternion rot)
    {
        var sync = instance.GetComponent<CoherenceSync>();
        return new SavedNetworkObject
        {
            position = pos,
            rotation = rot,
            coherenceUniqueId = (sync != null && sync.IsUnique) ? sync.ManualUniqueId : null,
        };
    }

    public static GameObject Restore(GameObject prefab, SavedNetworkObject saved, CoherenceBridge bridge)
    {
        if (!string.IsNullOrEmpty(saved.coherenceUniqueId))
            bridge.UniquenessManager.RegisterUniqueId(saved.coherenceUniqueId);

        var instance = UnityEngine.Object.Instantiate(prefab, saved.position, saved.rotation);
        return instance;
    }
}
```

This works because `CoherenceSync` reads `ManualUniqueId` during its own `Awake`/`Start`, and the registered ID takes precedence. Result: the same logical entity survives a save/load cycle, and persistent-entity adoption finds it again.

## Pattern 3: Host state hand-off on join

For bulk catch-up data — a save file, a procedural world seed plus stamped tile overrides, an inventory snapshot — `[Sync]` fields are wrong (too big, too slow). Have the joiner ask, then the authority answers over a fragmented command. The joiner pulls so the request never fires before the entity exists on both ends.

```csharp
public class HostStateChannel : MonoBehaviour
{
    private CoherenceSync _sync;
    private Action<byte[]> _onPayloadReceived;
    private bool _requested;

    private void Awake() => _sync = GetComponent<CoherenceSync>();

    private void Update()
    {
        // Non-authority side: once this entity is local and the bridge is connected,
        // ask the authority for the payload. One-shot per local lifetime.
        if (_requested || _sync == null || _sync.CoherenceBridge == null) return;
        if (!_sync.CoherenceBridge.IsConnected) return;
        if (_sync.HasStateAuthority) return;

        _requested = true;
        _ = _sync.SendCommand<HostStateChannel>(
            nameof(RequestHostPayload), MessageTarget.StateAuthorityOnly, _sync.CoherenceBridge.ClientID);
    }

    [Command]
    public void RequestHostPayload(ClientID requester)
    {
        if (!_sync.HasStateAuthority) return;
        byte[] payload = BuildHostPayload();           // your serialization
        _ = _sync.SendCommandOverChannel<HostStateChannel>(
            nameof(ReceiveHostPayload),
            MessageTarget.Other,
            Channel.Fragmented,
            requester,
            payload);
    }

    [Command]
    public void ReceiveHostPayload(ClientID recipient, byte[] payload)
    {
        if (recipient != _sync.CoherenceBridge.ClientID) return; // not for me
        _onPayloadReceived?.Invoke(payload);
    }

    public void SetReceiver(Action<byte[]> handler) => _onPayloadReceived = handler;

    private byte[] BuildHostPayload()
    {
        // Recommended structure:
        //   [version:int][length:int][compressed-body:bytes]
        // Compress with DeflateStream for >1 KB payloads.
        // ...
        return Array.Empty<byte>();
    }
}
```

Why `Channel.Fragmented`: default channel commands are capped near MTU (~1200 bytes). Fragmented commands are split, sent, and reassembled — designed for kilobyte-to-megabyte payloads. For a single one-shot hand-off the unordered `Channel.Fragmented` is fine; if the hand-off is multi-chunk and the receiver must apply chunks in send order, use `Channel.FragmentedOrdered` instead.

Why version prefix: future-proof schema migrations. A v2 client receiving a v1 payload should detect and adapt or refuse cleanly.

If the host can ever have *nothing* to hand off, never pass a bare `null` `byte[]` — and because of coherence's all-or-nothing tuple rule, you must then send *every* argument of that call in `(typeof(T), value)` form: `(typeof(ClientID), requester)` **and** `(typeof(byte[]), payloadOrNull)`, not a mix. On the receiver, treat a `null`/`byte[0]` arrival as "no payload" (a null can deserialize as an empty array). See [coherence-rpc-routing](../coherence-rpc-routing/SKILL.md) Pattern 7.

## Pattern 4: Acknowledgement before pool return

If multiple clients need to receive a one-shot event (consumable pickup, gift drop) and you can't afford to lose it on a flaky client, broadcast the event and wait for acks before recycling the entity.

```csharp
private readonly HashSet<uint> _pendingAcks = new();
private float _ackDeadline;

private void Broadcast()
{
    foreach (var conn in _sync.CoherenceBridge.ClientConnections.GetAll())
        _pendingAcks.Add(conn.ClientId);
    _ackDeadline = Time.time + 1.5f;
    _ = _sync.SendOrderedCommand<MyThing>(nameof(Event), MessageTarget.Other, /* args */);
}

[Command]
public void Ack(uint clientId)
{
    _pendingAcks.Remove(clientId);
    if (_pendingAcks.Count == 0) ReturnToPool();
}

private void Update()
{
    if (_pendingAcks.Count > 0 && Time.time > _ackDeadline)
        ReturnToPool();  // timeout — accept loss
}
```

Tradeoff: 1.5 s ceiling on pool reuse vs. guaranteed delivery on the happy path.

## When it works / when it doesn't

**Time-anchored state works when** the rules are pure functions of elapsed time. Branching state (grew → was eaten → respawned) needs the timestamp to update on each transition.

**Save/load identity preservation works when** you reload into the *same* coherence room/world. Across worlds, IDs aren't meaningful.

**Host state hand-off works when** the host is reliable (a simulator, ideally). Peer hosts can disconnect mid-payload; design the receiver to tolerate truncation or use the orphan-adoption path on the receiver to retry from a new host.

## Gotchas

- **`DateTime.UtcNow` differs by milliseconds between clients.** Fine for minute-scale timers, bad for sub-second events. For tight timing use a synced `[Sync] uint StartSimFrame` and a known tick rate.
- **`ManualUniqueId` must be set *before* the entity registers with the bridge.** If you Instantiate first and assign later, you've already lost.
- **Registering a duplicate unique ID throws.** If the entity might already exist (came in via live query), check first or wrap in try/catch.
- **Fragmented commands are reliable but not free.** A 1 MB payload takes time to ship over a 100 KB/s link. Show a "loading" UI; don't assume instant.
- **Payloads larger than a few MB are usually a smell.** Consider streaming via a CDN/HTTPS endpoint with the URL passed over coherence, instead of in-band transfer.
- **`OnClientConnected` fires before that client's live query has finished syncing.** Don't reference their entities yet; wait for their `onLiveQuerySynced` if you need to send entity references.

## Anti-patterns

- Polling `DateTime.UtcNow` in `Update` to update synced state. The authority computes; clients read the timestamp and derive — they don't sync the derived value.
- Saving the runtime CoherenceSync entity ID (the network ID) instead of the prefab's stable `ManualUniqueId`. Network IDs are per-session.
- Sending bulk state as many small `[Sync]` fields. One fragmented command is cheaper and atomic.
- Forgetting that a re-joined client's first frame has *no* networked entities yet. Wait for `onLiveQuerySynced` before assuming the world is populated.

## See also

- `Behaviours/NetworkManager.md` — connection lifecycle events (`OnLiveQuerySynced`, `OnClientConnected`) you'll hook into.
- `Synced/README.md` — `SyncedList`/`SyncedDictionary` for medium-sized collections that change occasionally.
- coherence docs: persistent entities, Worlds vs Rooms, `Channel.Fragmented`.
