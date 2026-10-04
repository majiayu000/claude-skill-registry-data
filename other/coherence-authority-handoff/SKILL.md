---
name: coherence-authority-handoff
description: Use for shared or contested networked objects in coherence — pickups, doors, seats, vehicles, mounts — where one client at a time owns state. Covers authority requests, orphan adoption, occupancy flags, race-condition guards, and disconnect recovery.
metadata:
  topic: networking
  engine: coherence
---

# Authority handoff for shared objects

## When to use this skill

- "Two players grabbed the same item and now it's stuck/duplicated."
- Player picks up a tool, another player wants to take it from them.
- Sitting in a chair, mounting a vehicle, claiming a turret.
- An interactable object's previous owner disconnected and now nobody can touch it.
- The developer mentions `RequestAuthority`, `IsOrphaned`, or `Adopt()`.

## The core idea

A networked entity has one *state authority* at a time. To mutate its synced fields, you must own state authority. Acquiring it is a *request* the current owner can deny — they may have legitimate reasons (already in use, mid-animation, owner-locked).

Two failure modes dominate real games:

1. **Races.** Two clients request simultaneously; both think they won.
2. **Orphans.** The owner disconnected; the object sits there with no one to ask.

Solve both with three coordinated pieces: a request flow, a synced "in use" flag, and an orphan adoption path.

## Pattern 1: Request → callback → state mutation

The base flow. The requester asks; the current authority's `OnAuthorityRequest` callback decides; on grant, the new authority sets the synced flag *atomically* with using the object.

```csharp
public class Seat : MonoBehaviour
{
    private CoherenceSync _sync;

    [Sync, OnValueSynced(nameof(OnOccupiedChanged))]
    public bool IsOccupied { get; set; }

    [Sync] public uint OccupantClientId { get; set; }   // reading this inside OnOccupiedChanged is safe — callbacks fire after all bindings apply

    private void Awake()
    {
        _sync = GetComponent<CoherenceSync>();
        _sync.OnAuthorityRequest.AddListener(OnAuthorityRequest);
    }

    public void TryOccupy()
    {
        if (_sync.HasStateAuthority)
        {
            ClaimSeat();  // already own it — just claim
            return;
        }

        if (_sync.IsOrphaned)
        {
            _sync.Adopt();  // owner left — take it (returns bool: whether the request was queued)
            return;
        }

        _ = _sync.RequestAuthorityAsync(AuthorityType.Full)
            .ContinueWith(t => { if (t.Result) ClaimSeat(); });   // implicit bool: true iff granted
    }

    private void OnAuthorityRequest(AuthorityRequest req, CoherenceSync _)
    {
        if (IsOccupied) req.Reject();   // someone already sitting
        else            req.Accept();
    }

    private void ClaimSeat()
    {
        var wasOccupied = IsOccupied;
        IsOccupied = true;
        OccupantClientId = _sync.CoherenceBridge.ClientID;
        ApplyOccupiedChanged(wasOccupied, IsOccupied); // authority-side local reaction
    }

    private void OnOccupiedChanged(bool wasOccupied, bool nowOccupied)
    {
        ApplyOccupiedChanged(wasOccupied, nowOccupied); // remote receive path
    }

    private void ApplyOccupiedChanged(bool wasOccupied, bool nowOccupied) { /* update visuals */ }
}
```

The key invariant: **`IsOccupied` is set on the same frame as authority is gained, by the new authority.** That eliminates the race window where two clients both think they won.

## Pattern 2: Captive/occupancy flag

For pickupable objects, "is this currently held by a player" is a synced bool that gates *both* the request callback and any subsequent steal attempts.

```csharp
[Sync] public bool IsBeingCarried { get; set; }

private bool ShouldAcceptAuthority(ClientID requester)
{
    if (IsBeingCarried) return false;            // hands off — owner is using it
    if (Time.time < _lastHandoffTime + 1f) return false;  // cooldown prevents thrash
    return true;
}
```

The cooldown (coyote-time) prevents two players standing close to an object from rapidly ping-ponging authority — once it changes hands, the previous owner can't immediately steal it back via collision triggers.

## Pattern 3: Orphan adoption for disconnected owners

If a player disconnects while holding an item, the entity is *orphaned* — has no authority. Any client can `Adopt()` it. This needs explicit code; nothing automatic happens.

```csharp
private void Awake()
{
    _sync.CoherenceBridge.onLiveQuerySynced.AddListener(OnLiveQuerySynced);
}

private void OnLiveQuerySynced(CoherenceBridge _)
{
    if (_sync.IsOrphaned && IsAdoptionEligible())
        _sync.Adopt();
}

private bool IsAdoptionEligible()
{
    // Examples:
    // - I'm the simulator (always adopt orphans)
    // - I'm physically closest
    // - The item is in my room/zone
    return SimulatorUtility.IsSimulator;
}
```

For persistent worlds, prefer one designated adopter (the simulator). For ad-hoc sessions without a simulator, "first client to touch it" works.

### Carried / parented objects on carrier disconnect

A held item is usually *parented* to its carrier (so it follows the hands), which makes it a **child network entity**. That introduces a second, independent failure mode beyond orphaning, and it bites silently. Four settings must line up:

1. **Parent (carrier): `Preserve Children` ON** (CoherenceSync → Advanced Settings). By default coherence **destroys child entities when the parent is destroyed**. So when the carrier disconnects, the item is destroyed *with* it — even though the item is persistent. Preserve Children unparents the child instead, leaving it in the world.
2. **Child (item): `Lifetime = Persistent`.** A session-based item is destroyed on its own authority-holder's disconnect regardless of the parent setting. Only a persistent entity survives to become an adoptable orphan.
3. **Child (item): `Auto-adopt Orphan` ON** (or a simulator running `AuthRequestable.AutoAdoptOnSimulator`). An orphan has *no* authority, so **nobody simulates it** — it freezes in mid-air and will not fall until someone takes ownership. Auto-adopt makes the RS hand it to a client immediately so simulation resumes.
4. **A resume callback on the item.** When a client gains authority over the recovered orphan (`OnStateAuthority`), reset the held/occupancy flags and decide how the item resumes. A gravity-driven rigidbody just needs to be left dynamic and it falls. **Kinematic items whose motion is scripted** need an explicit hook to start their own fall/settle routine — leaving them dynamic is wrong for them.

```csharp
private void OnStateAuthorityGained()           // CoherenceSync.OnStateAuthority UnityEvent
{
    if (_wasOccupied && _localCarrier == null)  // adopted an orphan whose carrier had vanished
    {
        ClearHeldState();                        // occupancy flag, parent ref, etc.
        ResumeAfterCarrierLost();                // gravity: leave dynamic. kinematic: drive the fall.
    }
}
```

Miss #1 and the item silently disappears on disconnect. Miss #3 and it survives but hangs frozen. Miss #4 on a kinematic game and it falls through the floor or never moves. `Behaviours/Pickupable.md` + `PickupCarrier.md` implement all four (the hook is `Pickupable.OnCarrierLost`).

## Pattern 4: Collision-driven opportunistic requests

For grab-by-touching games, the request fires on collision, not on a button press. To prevent constant thrashing as bodies overlap, gate by a recency check.

```csharp
private float _lastAuthorityChangeTime;

private void Awake()
{
    _sync.OnStateAuthority.AddListener(OnStateAuthorityGained);  // UnityEvent — fires on gain
}

private void OnCollisionEnter(Collision c)
{
    if (_sync.HasStateAuthority) return;
    if (Time.time < _lastAuthorityChangeTime + 1f) return;
    if (IsBeingCarried) return;
    _ = _sync.RequestAuthorityAsync(AuthorityType.Full);
}

private void OnStateAuthorityGained()
{
    _lastAuthorityChangeTime = Time.time;
}
```

## When it works / when it doesn't

**These patterns work when:**
- The object's transfer mode is `Request` (so callbacks fire). `Steal` mode skips the callback entirely.
- There's at least one consistent authority (an active player or a simulator).
- The synced "occupancy" flag is the *only* writer of "who owns me right now" state.

**They don't work when:**
- All clients in a room disconnect simultaneously — the entity becomes orphaned and stays that way until a new client joins and chooses to adopt.
- You need *partial* ownership (multiple players collaboratively holding an object). For that, see the cooperative-hold pattern in `Behaviours/SharedHoldInteractable.md`.
- The entity must change rapidly between owners (e.g., a ball in a sports game with constant passing). Authority transfer has latency; consider a single permanent owner (the simulator) and replicate input from each player instead.

## Gotchas

- **Setting `IsOccupied = true` *before* authority is granted is a bug.** Without authority you can't mutate synced fields; the write is dropped silently.
- **`OnValueSynced` callbacks do not fire on the authority that wrote the synced value.** They fire on remote instances receiving replication. Most of the time this is what you want — the authority already updated visuals/state inline before writing the synced field, so callbacks should be remote-only. The dual-apply pattern (`ApplyOccupiedChanged` called from both write-path and callback) is the right shape *only* when the same reaction must run identically on both sides and the authority hasn't already produced it inline. Reach for it deliberately; don't reflex-add it.
- **`OnAuthorityRequest` fires on the *current* authority, not the requester.** If you're the requester, listen to the `RequestAuthorityAsync` task result instead.
- **The legacy `OnAuthorityRequested` event is deprecated** (SDK 1.7, 05/2025) — use the UnityEvent `OnAuthorityRequest` (`UnityEventCountable<AuthorityRequest, CoherenceSync>`). The two coexist for back-compat but the deprecated one will go away.
- **`RequestAuthorityResult` has no `Granted` property.** Use the implicit `bool` conversion (`if (t.Result)` is `true` iff `Type == Success`) or check `t.Result.Type == RequestAuthorityResultType.Success`.
- **Adopting an orphan doesn't reset its state.** A half-eaten apple stays half-eaten; the new authority inherits whatever the previous one last wrote.
- **Transfer mode `Not Transferable` blocks every request silently.** Check the prefab's CoherenceSync config first if requests never seem to land.
- **A request can be both `Accept`ed and `Reject`ed if your code paths overlap.** Make `OnAuthorityRequest` early-return after one of the two.

## Anti-patterns

- Mutating the "occupied" flag in the requester before getting authority. The write doesn't replicate.
- Polling `HasStateAuthority` in `Update` every frame to decide whether to grab. Trigger by event (collision, button press) and request once.
- Multiple simultaneous `RequestAuthorityAsync` calls from the same client on the same entity. Coalesce.
- Using `Adopt()` on a non-orphan. It's a no-op; check `IsOrphaned` first.

## See also

- `Behaviours/AuthRequestable.md` — drop-in component wrapping this whole flow with occupancy, timeouts, and event hooks.
- `Behaviours/AutoAuthRequester.md` — proactively requests authority over nearby objects before the player presses the interact button (reduces perceived latency).
- `Behaviours/Pickupable.md` + `Behaviours/PickupCarrier.md` — full pickup/carry pattern using the above.
