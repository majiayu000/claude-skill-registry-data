---
name: coherence-rpc-routing
description: Use when designing networked events or RPC dispatch in coherence — picking MessageTarget, ordered vs unordered, request/response, paired on/off commands stuck in the wrong state, transferring large payloads, or passing nullable args (string/byte[]/entity refs) that must use the (typeof(T), value) tuple form. Covers SendOrderedCommand for toggle pairs, Channel.Fragmented for big data, request → validate → broadcast → ack patterns, and null-argument serialization.
metadata:
  topic: networking
  engine: coherence
---

# RPC routing and command patterns

## When to use this skill

- The developer is calling `SendCommand` / `SendOrderedCommand` and wondering which `MessageTarget` to pick.
- "My command fires on the sender too and double-applies the effect."
- "Two players triggered the same thing and got conflicting outcomes."
- Sending a payload bigger than ~1 KB ("MTU exceeded" errors).
- Building a request/response flow where the requester needs to know the outcome.
- Designing a one-shot world event everyone must see exactly once.
- A command takes a `string`, `byte[]`, or entity-reference (`CoherenceSync`/`GameObject`/`Transform`) argument that *can be null* — passing `null` directly throws or mis-resolves; see Pattern 7.

## The core idea

A command is a method on a component that, when called via `SendCommand<T>`, runs on a *subset of clients you choose*. The choice has three dimensions:

1. **Who** — `MessageTarget` (All / StateAuthorityOnly / InputAuthorityOnly / Other)
2. **Ordering (the command API)** — `SendCommand` (best effort, unordered) vs `SendOrderedCommand` (reliable, in-order)
3. **Channel (the transport)** — default (small, fast), `Channel.Fragmented` (big, unordered), `Channel.FragmentedOrdered` (big, ordered)

(The command-API choice and the channel choice are independent dimensions. `SendOrderedCommand` rides an ordered channel under the hood, but you don't pick the channel directly when calling it — that only matters when you reach for `SendCommandOverChannel` for big payloads.)

Picking the right combination is the whole game. Wrong combinations give you double-fires, missing effects, and "works in editor, drops in production."

## Pattern 1: MessageTarget cheat sheet

```
Authority decides → broadcast to viewers       : MessageTarget.Other
Client asks the authority to do something      : MessageTarget.StateAuthorityOnly
Everyone runs it including the sender          : MessageTarget.All
Send to the specific player who controls input : MessageTarget.InputAuthorityOnly

(MessageTarget.AuthorityOnly is the deprecated name — replaced by StateAuthorityOnly in SDK 1.8.)
```

**First question before writing any command:** do the authority and remote clients do the *same* mutation on this signal, or *different* work?

- **Same mutation** (both sides apply the same change) → one self-forwarding `[Command]` method.
- **Different work** (authority validates/decides, remotes react with their own effect) → two methods: a sender and a `[Command]` handler.

If you grep this project you'll find `SharedHoldInteractable` using a two-method shape (`AddContribution` + `[Command] ReceiveContribution`). That's the accumulation case — many writers merging contributions into one synced total — not a default. Don't copy it for simple mutations; the result is duplicate code that does nothing the single-method form doesn't.

### Same mutation — self-forwarding single method

```csharp
[Command]
public void IncrementScore()
{
    if (_sync.HasStateAuthority)
    {
        Score++;        // [Sync] field — coherence replicates the new value to everyone
        return;
    }
    _ = _sync.SendCommand<Scoreboard>(nameof(IncrementScore), MessageTarget.StateAuthorityOnly);
}
```

The method calls itself: a non-authority client routes the command to the authority, the authority re-enters the same method with `HasStateAuthority==true` and applies the mutation. One method, no paired handler, no duplicated body.

### Different work — authority decides, others react

```csharp
public void OpenDoor()
{
    if (!_sync.HasStateAuthority)
    {
        // I'm not the authority — ask them to do it.
        _ = _sync.SendCommand<Door>(nameof(OpenDoor), MessageTarget.StateAuthorityOnly);
        return;
    }

    // I am the authority. Do it locally and tell everyone else.
    _isOpen = true;
    PlayOpenAnimation();
    _ = _sync.SendCommand<Door>(nameof(OnDoorOpened), MessageTarget.Other);
}

[Command]
public void OnDoorOpened()
{
    // runs on every non-authority client
    PlayOpenAnimation();
}
```

This three-step shape (request to authority → authority decides → broadcast to others) eliminates double-application: the authority doesn't include itself in the broadcast (`Other` excludes the sender), and the requester doesn't preemptively apply the effect. The second `[Command]` exists because the *remote effect* (the animation) is genuinely different from the *authority work* (flipping `_isOpen`) — if the two sides did the same thing, you'd be in the single-method case above.

## Pattern 2: Ordered vs unordered

`SendOrderedCommand` guarantees:
- The command is delivered (reliable).
- Multiple commands from the same sender arrive in send order.

`SendCommand` is unreliable best-effort — fire and forget.

**Use `SendOrderedCommand` for:**
- Race-sensitive events (item pickup, scoring, "first to grab wins")
- State-machine transitions where order matters (open → close → open)
- Paired commands that mutate the same state — see Pattern 3.

**Use `SendCommand` (unordered) for:**
- High-frequency visual effects (footstep dust, muzzle flashes)
- Optional UX juice that can drop without consequence
- Anything where missing one is fine because the next one will overwrite the effect

Ordered commands cost more bandwidth and latency. Don't use them by default; use them when the cost of misordering is real.

(Big payloads are a separate axis — `SendCommandOverChannel` with `Channel.Fragmented` is reliable-but-unordered, `Channel.FragmentedOrdered` is reliable-and-ordered. See Pattern 5.)

## Pattern 3: Paired commands that mutate the same state both need `SendOrderedCommand`

When you build a feature out of *two* commands that act on the same networked state — `RemoteApplyX` / `RemoteRemoveX`, `Subscribe` / `Unsubscribe`, `Lock` / `Unlock`, `Enter` / `Exit` — they both need to be sent with `SendOrderedCommand` so coherence preserves their relative order on the receiver. Otherwise the reverse-arrival case leaves the system in an incoherent state nothing ever cleans up.

**The failure mode (worth naming):**

```
Sender:    Apply  ───▶  Remove
                                  ↓ (SendCommand — unordered)
Receiver:  Remove (no-op, nothing to remove) → Apply → dangling state forever
```

This is harder to spot than a double-fire or a missed broadcast because the symptom is "a buff/lock/subscription stuck on forever long after the player did the obvious thing to clear it." Often discovered weeks later when QA reports "the icon never goes away."

**Diagnostic question before adding a second command:** *if these two commands arrived in the reverse order from how I sent them, would the system end up in an incoherent state?* If yes — both `SendOrderedCommand`. If no (e.g. two idempotent visual effects) — `SendCommand` is fine on both.

**The fix is one keyword on each:**

```csharp
public void RequestApply(EffectPrefab prefab)
{
    if (!_sync.HasStateAuthority)
    {
        // Ordered channel — pairs with RequestRemove below.
        _ = _sync.SendOrderedCommand<EffectProxy>(
            nameof(RemoteApply), MessageTarget.StateAuthorityOnly, prefab.Id);
        return;
    }
    Apply(prefab);
}

public void RequestRemove(EffectPrefab prefab)
{
    if (!_sync.HasStateAuthority)
    {
        // Same ordered channel as RequestApply — preserves relative send order.
        _ = _sync.SendOrderedCommand<EffectProxy>(
            nameof(RemoteRemove), MessageTarget.StateAuthorityOnly, prefab.Id);
        return;
    }
    Remove(prefab);
}

[Command] public void RemoteApply(int id) { /* authority adds effect */ }
[Command] public void RemoteRemove(int id) { /* authority removes effect */ }
```

Both commands use `SendOrderedCommand` → coherence delivers them in send order. Apply→Remove arrives as Apply→Remove. Remove→Apply arrives as Remove→Apply.

**Why two ordered commands aren't enough on their own:** the gotcha at the bottom of this file ("`SendOrderedCommand` is not a barrier") still applies. If a third command in this feature uses *unordered* `SendCommand`, it can still arrive interleaved with the two ordered ones. Every command in the lifecycle that mutates the same state needs to use `SendOrderedCommand`. Half-measures don't work.

**When this is overkill:**

- Effects whose final state converges regardless of intermediate order — e.g. a player health bar driven by a `[Sync] float`, where every update writes the absolute value rather than a delta. Reverse-order arrival of two updates leaves the *latest* value, which is correct by definition. Don't `SendOrderedCommand` state replication.
- Idempotent visual effects — re-applying "play muzzle flash" or "spawn footstep dust" twice is harmless. Plain `SendCommand`.
- Anything where you'd unconditionally re-emit the apply if the remove arrived first (rare in practice, but logically distinct).

**When it's mandatory:**

- Bitmask-style state where bit-flips aren't commutative (set-bit-X then clear-bit-X vs clear-bit-X then set-bit-X end in opposite states).
- Reference counts and stack counters that increment/decrement.
- Lifecycle pairs: open/close, lock/unlock, claim/release, subscribe/unsubscribe, mount/dismount.
- Anything where "the remove no-ops because there's nothing to remove yet" is a possible code path that would leave the apply uncancelable.

**Better still — when the state is just a value, sync it instead.** A `[Sync] bool` or `[Sync] enum` self-heals on reconnect and converges by construction; a command pair doesn't. Reach for paired-ordered-commands only when the receiver mutates derived state on the *transition*, not on the *value*.

## Pattern 4: Request → validate → broadcast → ack

For shared-consumable events where exactly one player should "win" and every client must agree on the outcome:

```csharp
public class SharedConsumable : MonoBehaviour
{
    [Sync] public bool IsClaimed { get; set; }
    private readonly HashSet<uint> _pendingAcks = new();
    private float _ackDeadline;

    // 1. Anyone can request to claim
    public void TryClaim()
    {
        _ = _sync.SendCommand<SharedConsumable>(
            nameof(RequestClaim),
            MessageTarget.StateAuthorityOnly,
            _sync.CoherenceBridge.ClientID);
    }

    // 2. Authority validates and broadcasts
    [Command]
    public void RequestClaim(uint claimerID)
    {
        if (!_sync.HasStateAuthority || IsClaimed) return;

        IsClaimed = true;
        _pendingAcks.Clear();
        foreach (var c in _sync.CoherenceBridge.ClientConnections.GetAll())
            _pendingAcks.Add(c.ClientId);
        _ackDeadline = Time.time + 1.5f;

        _ = _sync.SendOrderedCommand<SharedConsumable>(
            nameof(ApplyClaim),
            MessageTarget.All,            // everyone runs effect (including authority)
            claimerID);
    }

    // 3. Effect runs everywhere identically
    [Command]
    public void ApplyClaim(uint claimerID)
    {
        ApplyVisualEffect(claimerID);
        _ = _sync.SendCommand<SharedConsumable>(
            nameof(Ack),
            MessageTarget.StateAuthorityOnly,
            _sync.CoherenceBridge.ClientID);
    }

    // 4. Authority waits for acks before recycling
    [Command]
    public void Ack(uint clientId)
    {
        _pendingAcks.Remove(clientId);
        if (_pendingAcks.Count == 0) ReturnToPool();
    }

    private void Update()
    {
        if (_pendingAcks.Count > 0 && Time.time > _ackDeadline)
            ReturnToPool();  // timeout
    }
}
```

Worth the ceremony when "every client missed it" is a worse outcome than "some clients applied late." For best-effort effects this is overkill — just `SendCommand(Other)` and move on.

## Pattern 5: Big payloads via fragmented channel

Default-channel commands target the RS MTU (~1200 bytes). Above that, use one of the two fragmented channels with `SendCommandOverChannel`:

- **`Channel.Fragmented`** — reliable but **unordered**. Each call is reassembled correctly, but two consecutive fragmented sends from the same client may arrive in either order.
- **`Channel.FragmentedOrdered`** — reliable and ordered. Pick this when the payloads are part of a sequence and the receiver must apply them in send order (multi-chunk hand-off, replay-style streams).

```csharp
// One-shot big payload — order vs other fragmented sends doesn't matter.
_ = _sync.SendCommandOverChannel<MyClass>(
    nameof(ReceiveBigPayload),
    MessageTarget.StateAuthorityOnly,
    Channel.Fragmented,
    payloadBytes);

[Command]
public void ReceiveBigPayload(byte[] payload)
{
    // up to several MB, reassembled for you
}
```

Reassembly always reconstructs each individual payload correctly — *within* one fragmented command, fragments arrive ordered (they have to, to reassemble). The unordered/ordered distinction is *between* fragmented commands. Latency is higher in either case (multiple round-trips for reassembly).

For details on what to *put* in the payload, see [coherence-persistence](../coherence-persistence/SKILL.md).

## Pattern 6: Targeted send to a specific client

When you need to send only to one player (private message, "you're now host," personalized state):

```csharp
// Find the recipient's CoherenceClientConnection
var conn = _sync.CoherenceBridge.ClientConnections.Get(recipientID);
if (conn == null) return;

// Use *their* connection sync as the target — StateAuthorityOnly then resolves to them
_ = conn.Sync.SendCommand<CoherenceClientConnection>(
    nameof(CoherenceClientConnection.RPC_PrivateMessage),
    MessageTarget.StateAuthorityOnly,
    messageText);
```

The trick: a `CoherenceClientConnection`'s state authority *is* that specific client, so `StateAuthorityOnly` routes to exactly one recipient.

## Pattern 7: Nullable command arguments must be sent as `(typeof(T), value)` tuples

If a command parameter can ever be `null` — `string`, `byte[]`, or an entity reference (`CoherenceSync`, `GameObject`, `Transform`) — you **cannot pass a bare `null`** in the args. coherence resolves each argument's wire type from the *runtime type of the object you hand it*, and a bare `null` carries no type, so the send either throws or serializes against the wrong type. The fix is to pass the argument as a `ValueTuple<Type, object>` — `(typeof(ParamType), value)` — so the type is explicit even when the value is null.

**It's all-or-nothing: the moment one argument needs the tuple form, *every* argument in that call must be a `(typeof(T), value)` tuple — value types included.** You can't mix bare values and tuples in the same `SendCommand` call.

```csharp
// ❌ Throws / mis-resolves — null has no runtime type to infer the wire format from.
_ = _sync.SendCommand<Chat>(nameof(Receive), MessageTarget.Other, (string)null);

// ✅ Tuple carries the type explicitly, so a null string serializes correctly.
_ = _sync.SendCommand<Chat>(nameof(Receive), MessageTarget.Other, (typeof(string), (string)null));

// ❌ Mixed: one tuple + bare values in the same call is NOT allowed.
_ = _sync.SendCommand<Inventory>(
    nameof(Give),
    MessageTarget.StateAuthorityOnly,
    slotIndex,                                  // bare value type
    (typeof(byte[]), payloadOrNull));           // tuple — illegal alongside the bare arg above

// ✅ If ANY arg needs the tuple form, wrap them ALL — value types included.
_ = _sync.SendCommand<Inventory>(
    nameof(Give),
    MessageTarget.StateAuthorityOnly,
    (typeof(int), slotIndex),                   // wrap it too, even though int is never null
    (typeof(byte[]), payloadOrNull),            // byte[] — might be null
    (typeof(CoherenceSync), targetSyncOrNull)); // entity ref — might be null
```

This applies to the ordered and over-channel variants identically (`SendOrderedCommand`, `SendCommandOverChannel`).

**Rule of thumb:** if *any* argument of a command call could be null on some code path, send *every* argument of that call in `(typeof(T), value)` tuple form. It costs nothing when the values are non-null and is the only thing that works when one is null. (If no argument can ever be null, pass them all bare as usual — value types like `int`, `float`, `bool`, `Vector3` are never null.)

**The receiving side must tolerate the round-trip default, too.** A `null` argument can arrive at the receiver as the *non-null default* for its type — a null `string` may deserialize as `""`, a null `byte[]` as a zero-length `byte[0]`. So the `[Command]` handler must treat "null" and "empty" as the same case:

```csharp
[Command]
public void Receive(string text)
{
    if (string.IsNullOrEmpty(text)) return;   // handles both null and "" arrivals
    Append(text);
}

[Command]
public void ReceiveBlob(byte[] payload)
{
    if (payload == null || payload.Length == 0) return;  // null and byte[0] are equivalent
    Apply(payload);
}
```

Don't write `if (text == null)` alone — it will miss the empty-string arrival and you'll process a "present but empty" payload as if it were real.

(coherence docs: *Commands → Sending null values in command arguments*.)

## When each combination fits

| Need | Target | Command API | Channel |
|---|---|---|---|
| "Trigger an animation on remotes" | `Other` | `SendCommand` | Default |
| "Ask authority to apply game effect" | `StateAuthorityOnly` | `SendOrderedCommand` | Default |
| "Broadcast result of authority decision" | `Other` | `SendCommand` | Default |
| "Race-critical pickup result" | `All` | `SendOrderedCommand` | Default |
| "Private message to one player" | `StateAuthorityOnly` on their `CoherenceClientConnection` | `SendOrderedCommand` | Default |
| "Bulk state hand-off on join (multi-chunk)" | `StateAuthorityOnly` on the joiner's connection | `SendCommandOverChannel` | `FragmentedOrdered` |
| "One-shot big payload" | `StateAuthorityOnly` | `SendCommandOverChannel` | `Fragmented` |
| "Footstep audio" | `Other` | `SendCommand` | Default |
| "Player input → simulator" | `StateAuthorityOnly` | `SendOrderedCommand` usually | Default |

## Gotchas

- **`MessageTarget.All` includes the sender** — your local code runs twice if you don't guard. Either use `Other` for "broadcast" and call the local effect explicitly before sending, or accept it and make the command idempotent.
- **`StateAuthorityOnly` silently drops if there's no current authority** (orphaned entity). Check `IsOrphaned` and `Adopt()` first.
- **`MessageTarget.AuthorityOnly` is deprecated** (SDK 1.8, 07/2025) — replaced by `MessageTarget.StateAuthorityOnly`. The deprecated symbol still compiles and maps to the same value, but warn.
- **Commands have a per-method arg limit** (a few hundred bytes for default channel including overhead). If you're passing a `string` longer than ~200 chars, switch to `SendCommandOverChannel` with `Channel.Fragmented` / `Channel.FragmentedOrdered`, or pass a reference (e.g., an enum index into a lookup table).
- **`SendOrderedCommand` is not a barrier.** Earlier unordered `SendCommand` calls from the same client can still arrive after a later `SendOrderedCommand`. Don't mix when sequencing matters. See Pattern 3 for why every command in a lifecycle must use the same API.
- **Fragmented commands consume more bandwidth on join** because the receiver may be re-syncing many other entities simultaneously. Show a loading state.
- **Entity-reference command arguments (`CoherenceSync`, `Transform`, `GameObject`) arrive as `null` if the receiver doesn't yet have that entity in its query area.** Either guard the receiver, or pass a stable unique-ID string and resolve on receive.
- **Passing a bare `null` for a nullable arg (`string`, `byte[]`, entity ref) throws or mis-serializes** — coherence can't infer the wire type from a typeless `null`. Send it as `(typeof(T), value)` instead — and it's all-or-nothing: once one arg is a tuple, *every* arg in that call must be a `(typeof(T), value)` tuple, value types included (you can't mix bare and tuple args). On receive, a null often arrives as the type's empty default (`""`, `byte[0]`), so guard with `IsNullOrEmpty` / `.Length == 0`, not `== null`. See Pattern 7.

## Anti-patterns

- Defaulting everything to `MessageTarget.All` "just in case." It's the most expensive option and usually wrong.
- Using `SendCommand` for state changes that *must* land. Use `SendOrderedCommand`, or sync a `[Sync]` field and let coherence's state-replication handle reliability.
- Stuffing a 4 KB JSON blob through the default channel and wondering why it drops. Fragmented exists for a reason.
- Round-tripping `StateAuthorityOnly` → `Other` → `StateAuthorityOnly` to "confirm" simple state. If the authority's `[Sync]` field is the source of truth, just read it on the client; no confirmation command needed.
- Writing a paired `void Foo() / [Command] void ReceiveFoo()` where both bodies apply the same mutation. Merge into one `[Command] void Foo()` that self-forwards via `SendCommand(StateAuthorityOnly)` when not authority — the duplicate is the smell. See Pattern 1's "Same mutation" example.
- Modelling toggle state as an `On`/`Off` command pair when a `[Sync] bool` would do. State sync self-heals; command pairs don't. See Pattern 3's "Better still" note.

## See also

- `Behaviours/NetworkManager.md` — `ClientConnections` API for targeted sends.
- [coherence-persistence](../coherence-persistence/SKILL.md) — fragmented commands for join-in-progress payloads.
- [coherence-authority-handoff](../coherence-authority-handoff/SKILL.md) — request flows that use `StateAuthorityOnly`.
- coherence docs: command routing rules, ordered vs unordered guarantees.
