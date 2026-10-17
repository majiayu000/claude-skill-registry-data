---
name: game-networking
category: networking
description: Use when touching multiplayer code - authoritative server, client prediction and reconciliation, interpolation, lockstep and rollback, server-side validation of every RPC per engine (Netcode, Unreal replication, Godot multiplayer, Colyseus, Bevy crates), bandwidth and versioned messages.
tech_stack: Game core
source: informed by Glenn Fiedler's Gaffer on Games networking articles, Gabriel Gambetta's Fast-Paced Multiplayer series, and the Unity Netcode, Unreal replication and Godot multiplayer docs; own wording
---
# Game Networking

## Overview

In a multiplayer game every client is running on a machine you do not control. Whatever a client can send, a cheater will send — teleports, infinite ammo, a hit on someone behind a wall, a purchase with money they do not have. The server (or host) owns the truth; clients send what the player wants to do and render what the server says happened, predicting locally so it still feels instant.

**Core principle:** Clients send inputs and intents, never outcomes. The authority validates every message before it changes state.

## Pick the model the design needs (the repository has usually picked already)

| Model | Fits | Cost |
|---|---|---|
| Authoritative server + client prediction + reconciliation + interpolation of others | Shooters, action, most online games | Server hosting; prediction code |
| Deterministic lockstep (send only inputs) | RTS with thousands of units | Every peer must simulate bit-identically; latency = slowest peer |
| Rollback (predict remote inputs, rewind and re-simulate on correction) | Fighting games, precise 1v1 | Fully deterministic, cheap-to-clone state |
| Listen server / host-authoritative | Co-op, small sessions | Host can cheat; host migration |

Stacks: Unity — Netcode for GameObjects, Netcode for Entities, or the Mirror/FishNet/Photon the repo already uses; Unreal — built-in replication (Iris on newer projects that enabled it); Godot — high-level multiplayer (`@rpc`, `MultiplayerSpawner`, `MultiplayerSynchronizer`); web — Colyseus, or WebSocket/WebRTC servers; Bevy — `lightyear`, `bevy_replicon`, `bevy_ggrs` (rollback). Never add a second networking stack beside the one in use.

## Validate on the authority — per engine

```cpp
// Unreal: server RPC with validation; returning false from _Validate disconnects the caller
UFUNCTION(Server, Reliable, WithValidation)
void ServerFire(FVector_NetQuantize Origin, FVector_NetQuantizeNormal Direction, float ClientTime);

bool AShooterCharacter::ServerFire_Validate(FVector_NetQuantize Origin, FVector_NetQuantizeNormal Direction, float ClientTime) {
    return Direction.IsNormalized() && FMath::IsFinite(ClientTime);
}
void AShooterCharacter::ServerFire_Implementation(FVector_NetQuantize Origin, FVector_NetQuantizeNormal Direction, float ClientTime) {
    if (!Weapon->CanFire(GetWorld()->GetTimeSeconds())) return;                       // server's cooldown
    if (FVector::Dist(Origin, GetPawnViewLocation()) > MaxOriginError) return;        // origin near the server's view
    Weapon->FireServerAuthoritative(Origin, Direction);                               // server traces the hit
}
```

```csharp
// Unity Netcode for GameObjects: only the owner may ask, and the server decides
[Rpc(SendTo.Server)]
void RequestMoveRpc(Vector2 input, RpcParams rpcParams = default) {
    if (rpcParams.Receive.SenderClientId != OwnerClientId) return;
    if (float.IsNaN(input.x) || float.IsNaN(input.y)) return;
    _pendingInput = Vector2.ClampMagnitude(input, 1f);                     // speed applied server-side in FixedUpdate
}
```

```gdscript
# Godot 4: any peer may call it, so check who did
@rpc("any_peer", "call_remote", "reliable")
func request_buy(item_id: StringName) -> void:
    if not multiplayer.is_server():
        return
    var sender := multiplayer.get_remote_sender_id()
    var player := players.get(sender) as PlayerState
    if player == null or not Shop.has_item(item_id):
        return
    Shop.try_purchase(player, item_id)    # server checks its own balance, not the client's
```

```ts
// Colyseus: validate shape, range and rate before touching state
this.onMessage("move", (client, msg: unknown) => {
  const m = MoveSchema.safeParse(msg);                    // zod: finite numbers, |dir| <= 1
  if (!m.success || !this.rate.allow(client.sessionId)) return;
  this.state.players.get(client.sessionId)?.queueInput(m.data);
});
```

What "validate" covers: the sender owns the entity; numbers are finite (NaN and Infinity are classic exploits) and in range; enums are known values; array/string lengths are capped; message rate per client is limited; the action is legal now (cooldown, ammo, position, line of sight) according to server state.

## Prediction and reconciliation (the local player)

1. Client samples input each tick, tags it with a sequence number, applies it locally (prediction), stores it, and sends it.
2. Server applies inputs in order on its fixed step and sends back the authoritative state plus the last processed sequence number.
3. Client sets its state to the server's, drops acknowledged inputs, and re-applies the unacknowledged ones (reconciliation). Smooth small corrections visually; snap large ones.

Other players are rendered **interpolated** between two past server snapshots (about 100 ms behind), never extrapolated far. Hit detection on the server rewinds targets to what the shooter saw (lag compensation), within a capped window.

## Bandwidth and messages

- Budget bytes per client per second and per message; send state at a fixed rate (20–60 Hz), not every render frame.
- Quantize (`FVector_NetQuantize`, half floats, angles as bytes), delta-compress against the last acknowledged state, and send only what is relevant to each client (interest management) — which also stops wallhacks from reading hidden enemies.
- Unreliable channel for frequent state that will be superseded; reliable for events that must arrive (purchase, chat, match end).
- Every message type carries a protocol version (or the handshake does); a client with a different version is refused with a clear reason, not decoded wrongly.
- Loot, damage rolls and matchmaking randomness come from the server's RNG.

## Testing

- Server handlers are plain functions over state: unit-test them with a fake client — wrong owner, NaN, out-of-range, too fast, legal — and assert the state only changes for the legal case.
- Prediction/reconciliation: simulate a client and server in one test with a fake transport, inject latency and a dropped packet, assert the client converges to the server state.
- Determinism (lockstep/rollback): same input log on two simulations → same state hash every N ticks.
- Manual: two local clients plus a server with simulated latency and loss (Unity Network Simulator, Unreal `Net PktLag=150` / `Net PktLoss=5`, `tc netem` / Clumsy) — and say in the closing message which of these you could not run here.

## Common Mistakes

- A client RPC that applies damage, grants currency or sets position directly.
- Trusting a client timestamp for anything except lag-compensation bounds.
- Replicating everything every tick; sending hidden enemy positions to every client.
- Spawning or destroying networked objects on a client.
- Godot `@rpc("any_peer")` without checking `get_remote_sender_id()`.

## Red Flags

- A server handler with no validation branch.
- `ServerXxx_Validate` that always returns `true` for parameters a client controls.
- Floats from the network used without a finiteness check.
- A protocol change with no version bump.
