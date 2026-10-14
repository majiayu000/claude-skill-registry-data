---
name: networking
description: Godot networking developer — use when implementing multiplayer, RPC calls, scene replication, or lobby systems.
type: implementation
---

# Godot Networking

> You are an expert Godot 4.7 networking programmer who designs authoritative-server multiplayer systems using ENet, RPCs, and the high-level MultiplayerAPI.

## Overview

Godot 4.x uses a high-level multiplayer API built on top of `ENetMultiplayerPeer` (or WebRTC/WebSocket alternatives). The server holds authority over game state; clients send input and receive replicated state. Peer ID `1` is always the server by convention. The `MultiplayerSynchronizer` and `MultiplayerSpawner` nodes handle automatic property sync and scene replication, replacing the manual RPC patterns common in Godot 3.

## Key Nodes & APIs

| Node / API | Purpose |
|---|---|
| `ENetMultiplayerPeer` | UDP-based peer; call `create_server()` or `create_client()`, then assign to `multiplayer.multiplayer_peer` |
| `MultiplayerSpawner` | Replicates scene instantiation and removal across all peers |
| `MultiplayerSynchronizer` | Syncs node properties to peers on a configured tick interval |
| `SceneReplicationConfig` | Per-property sync config attached to a `MultiplayerSynchronizer`; controls which properties sync and with what `ReplicationMode` |
| `@rpc` | Annotation that marks a function as remotely callable; configures mode, transfer mode, and channel |
| `multiplayer.get_unique_id()` | Returns this peer's integer ID (`1` = server) |
| `multiplayer.get_peers()` | Returns array of all connected peer IDs (server-side) |
| `multiplayer.peer_connected` / `peer_disconnected` | Signals emitted when peers join or leave |
| `Node.set_multiplayer_authority(peer_id)` | Grants a peer authority over a node |
| `Node.is_multiplayer_authority()` | Returns `true` if the local peer owns this node |
| `MultiplayerAPI.set_replication_authority()` | Sets which peer drives replication for an object |

## RPC Mode Reference

| Mode | Who Can Call | Who Receives | Use Case |
|---|---|---|---|
| `"authority"` | Authoritative peer only (server by default) | All other peers | Server broadcasting state changes |
| `"any_peer"` | Any connected peer | The node's authority (server) | Client sending input or requests to server |
| `"call_local"` | Any peer | All peers including the caller | Authority triggering effects on everyone including itself |
| `"call_remote"` | Any peer | All peers except the caller | Broadcasting from server without re-triggering locally |

Combine with transfer modes: `"reliable"` (ordered, retried), `"unreliable"` (fire-and-forget), `"unreliable_ordered"` (latest packet wins).

## Core Patterns

### Pattern 1 — Lobby Setup with ENetMultiplayerPeer

```gdscript
# server.gd
func host_game(port: int, max_clients: int) -> void:
    var peer := ENetMultiplayerPeer.new()
    var err := peer.create_server(port, max_clients)
    assert(err == OK, "Failed to create server: %s" % error_string(err))
    multiplayer.multiplayer_peer = peer
    multiplayer.peer_connected.connect(_on_peer_connected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)

func _on_peer_connected(peer_id: int) -> void:
    print("Peer connected: ", peer_id)

func _on_peer_disconnected(peer_id: int) -> void:
    print("Peer disconnected: ", peer_id)

# client.gd
func join_game(address: String, port: int) -> void:
    var peer := ENetMultiplayerPeer.new()
    var err := peer.create_client(address, port)
    assert(err == OK, "Failed to connect: %s" % error_string(err))
    multiplayer.multiplayer_peer = peer
```

### Pattern 2 — Authority Guard + RPC State Mutation

```gdscript
# player.gd — set_multiplayer_authority(peer_id) called on spawn
extends CharacterBody2D

@rpc("any_peer", "call_local", "reliable")
func request_move(direction: Vector2) -> void:
    # Only the server should process this
    if not multiplayer.is_server():
        return
    velocity = direction * SPEED
    move_and_slide()

func _physics_process(_delta: float) -> void:
    # Authority guard — only the owning client sends input
    if not is_multiplayer_authority():
        return
    var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    request_move.rpc(dir)
```

### Pattern 3 — Client-Side Prediction with Server Reconciliation

```gdscript
# player.gd
var _pending_inputs: Array[Dictionary] = []
var _input_sequence: int = 0

func _physics_process(delta: float) -> void:
    if not is_multiplayer_authority():
        return
    var input := {
        "seq": _input_sequence,
        "dir": Input.get_vector("move_left", "move_right", "move_up", "move_down"),
    }
    # Apply locally (prediction)
    _apply_input(input, delta)
    _pending_inputs.append(input)
    _input_sequence += 1
    # Send to server
    send_input.rpc_id(1, input)

@rpc("any_peer", "unreliable_ordered")
func send_input(input: Dictionary) -> void:
    if not multiplayer.is_server():
        return
    _apply_input(input, get_physics_process_delta_time())
    # Broadcast authoritative state back
    reconcile_state.rpc(global_position, input["seq"])

@rpc("authority", "unreliable_ordered")
func reconcile_state(server_pos: Vector2, acked_seq: int) -> void:
    if is_multiplayer_authority():
        # Remove acknowledged inputs
        _pending_inputs = _pending_inputs.filter(func(i): return i["seq"] > acked_seq)
        # Snap to server position then re-apply unacked inputs
        global_position = server_pos
        for input in _pending_inputs:
            _apply_input(input, get_physics_process_delta_time())

func _apply_input(input: Dictionary, delta: float) -> void:
    velocity = input["dir"] * SPEED
    move_and_slide()
```

### Pattern 4 — MultiplayerSynchronizer with SceneReplicationConfig

```gdscript
# Attach a MultiplayerSynchronizer node to your player scene.
# In _ready(), configure it in code (or use the inspector):

@onready var sync: MultiplayerSynchronizer = $MultiplayerSynchronizer

func _ready() -> void:
    # Tick rate: sync every 50 ms (20 Hz)
    sync.replication_interval = 0.05

    var config := SceneReplicationConfig.new()
    # Always-sync properties (sent every tick)
    config.add_property(NodePath(".:global_position"))
    config.property_set_replication_mode(
        NodePath(".:global_position"),
        SceneReplicationConfig.REPLICATION_MODE_ALWAYS
    )
    # On-change properties (sent only when value changes)
    config.add_property(NodePath(".:health"))
    config.property_set_replication_mode(
        NodePath(".:health"),
        SceneReplicationConfig.REPLICATION_MODE_ON_CHANGE
    )
    sync.replication_config = config
```

### Pattern 5 — Interest Management (Visibility Per Peer)

```gdscript
# Called server-side to control what each peer sees
func update_visibility_for_peer(peer_id: int, node: Node, visible: bool) -> void:
    if not multiplayer.is_server():
        return
    var sync: MultiplayerSynchronizer = node.get_node("MultiplayerSynchronizer")
    sync.set_visibility_for(peer_id, visible)

# Optionally use a custom visibility filter callback
func _ready() -> void:
    $MultiplayerSynchronizer.add_visibility_filter(_is_peer_in_range)

func _is_peer_in_range(peer_id: int) -> bool:
    var peer_player := _get_player_node(peer_id)
    if peer_player == null:
        return false
    return global_position.distance_to(peer_player.global_position) < 1000.0
```

### Pattern 6 — Server-Authoritative Scene Change

```gdscript
# Only the server calls change_scene_to_file(); clients follow via RPC.

func load_level(path: String) -> void:
    if not multiplayer.is_server():
        return
    _change_scene.rpc(path)

@rpc("authority", "call_local", "reliable")
func _change_scene(path: String) -> void:
    get_tree().change_scene_to_file(path)
```

## Common Pitfalls

- **Using `@rpc("any_peer")` for state mutations.** Any client can call these freely, enabling trivial cheats. Reserve `"any_peer"` for client-to-server input submission only; validate and apply on the server, then broadcast results with `"authority"` RPCs.
- **Forgetting the authority guard.** Every function that mutates game state must begin with `if not is_multiplayer_authority(): return`. Without it, both server and clients execute the mutation, causing desyncs.
- **Calling `change_scene_to_file()` on all peers directly.** Only the server should trigger scene transitions; clients follow via a reliable `"authority"` RPC to guarantee ordering and prevent clients from forcing a scene change.
- **Sending full state every frame via RPCs.** Use `MultiplayerSynchronizer` with `replication_interval` and `REPLICATION_MODE_ON_CHANGE` instead of hand-rolled RPCs. Manual per-frame RPCs saturate bandwidth and ignore Godot's built-in delta compression.
- **Spawning nodes on clients manually.** Always use `MultiplayerSpawner` for scene replication. Manual `instantiate()` on a client creates a local-only node not tracked by the multiplayer API, breaking authority assignment and synchronization.
- **Assuming peer ID is stable across reconnects.** ENet assigns peer IDs dynamically. Store player identity (e.g., username or token) separately and re-map on `peer_connected`.
- **Not accounting for RTT in lag compensation.** Naively applying server corrections without replaying pending inputs produces rubber-banding. After snapping to the server-confirmed position, re-simulate all unacknowledged inputs stored in `_pending_inputs`.

## Performance

### Tick Rate
Control sync frequency with `MultiplayerSynchronizer.replication_interval` (seconds). Common budgets:
- `0.016` (~60 Hz) — fast-paced action, high bandwidth cost
- `0.05` (20 Hz) — standard for most games
- `0.1` (10 Hz) — strategy/slow-paced, lowest bandwidth

### MultiplayerSynchronizer Tuning
- Use `REPLICATION_MODE_ON_CHANGE` for properties that change infrequently (health, inventory, flags) to avoid sending unchanged values every tick.
- Use `REPLICATION_MODE_ALWAYS` only for high-frequency properties like `position` and `rotation`.
- Use `REPLICATION_MODE_NEVER` for properties you replicate manually via RPC for custom logic.

### Interest Management
Limit which peers receive updates for distant or irrelevant objects:
```gdscript
# Disable sync to a peer
synchronizer.set_visibility_for(peer_id, false)

# Add a per-peer filter function (called automatically each tick)
synchronizer.add_visibility_filter(func(peer_id: int) -> bool:
    return _peer_is_nearby(peer_id)
)
```
This prevents the server from sending position updates for objects a client cannot see, reducing both bandwidth and client-side processing.

### Lag Compensation
For hit detection, the server rewinds game state by approximately `RTT / 2` (half the round-trip time) before evaluating collisions. This allows clients to aim at visually accurate positions despite network delay. Implement by storing a rolling history of authoritative positions and indexing by timestamp:
```gdscript
# Simplified server-side position history
var _position_history: Array[Dictionary] = []  # [{time, pos}, ...]
const HISTORY_SECONDS := 0.5

func _physics_process(_delta: float) -> void:
    if not multiplayer.is_server():
        return
    _position_history.append({"time": Time.get_ticks_msec() / 1000.0, "pos": global_position})
    _position_history = _position_history.filter(
        func(e): return Time.get_ticks_msec() / 1000.0 - e["time"] < HISTORY_SECONDS
    )

func get_position_at(timestamp: float) -> Vector2:
    for entry in _position_history:
        if entry["time"] >= timestamp:
            return entry["pos"]
    return global_position
```

## Anti-Patterns

| Wrong | Right |
|---|---|
| `@rpc("any_peer")` on a state-mutation function | `@rpc("any_peer")` only for input; mutate state behind an `is_server()` check |
| `get_tree().change_scene_to_file(path)` called on all peers | Server-only call, clients follow via `@rpc("authority", "call_local", "reliable")` |
| Spawning nodes with `instantiate()` on clients | Use `MultiplayerSpawner` so the API tracks the node and assigns authority |
| Hand-rolled position RPC every `_physics_process` | `MultiplayerSynchronizer` with `replication_interval = 0.05` and `REPLICATION_MODE_ALWAYS` |
| State mutation without authority check | Every mutation begins: `if not is_multiplayer_authority(): return` |
| Sending full game state to every peer | Use `set_visibility_for(peer_id, false)` / `add_visibility_filter()` for interest management |

## References

- [High-level multiplayer overview](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)
- [MultiplayerSynchronizer](https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html)
- [MultiplayerSpawner](https://docs.godotengine.org/en/stable/classes/class_multiplayerspawner.html)
- [SceneReplicationConfig](https://docs.godotengine.org/en/stable/classes/class_scenereplicationconfig.html)
- [ENetMultiplayerPeer](https://docs.godotengine.org/en/stable/classes/class_enetmultiplayerpeer.html)
- [@rpc annotation](https://docs.godotengine.org/en/stable/tutorials/networking/remote_procedure_calls.html)
- [MultiplayerAPI](https://docs.godotengine.org/en/stable/classes/class_multiplayerapi.html)
- [RPCs and node authority](https://docs.godotengine.org/en/stable/tutorials/networking/remote_procedure_calls.html#remote-procedure-calls)

## Delegate to

| Task | Skill |
|---|---|
| GDScript implementation | `godot:coder` |
| Architecture decisions | `godot:architect` |
| API lookup | `godot:docs` |
