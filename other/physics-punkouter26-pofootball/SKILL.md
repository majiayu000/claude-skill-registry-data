---
name: physics
description: "Unity physics — non-allocating queries, collision layers, FixedUpdate discipline, continuous collision detection, character controllers, joints."
globs: ["**/*Physics*.cs", "**/*Collider*.cs", "**/*Rigidbody*.cs", "**/*Trigger*.cs"]
---

# Physics System

## FixedUpdate Discipline

All physics code goes in `FixedUpdate`. Input reading happens in `InputView.Update` (see architecture rules) and is forwarded to the System, which applies forces in `FixedUpdate` from the cached value.

```csharp
// InputView.cs — reads input in Update, forwards to System
private void Update()
{
    Vector2 moveInput = _controls.Player.Move.ReadValue<Vector2>();
    _playerSystem.SetMoveInput(moveInput);
}

// PlayerView.cs — applies physics in FixedUpdate from System-owned cached input
private Vector2 _moveInput;

public void SetMoveInput(Vector2 input) => _moveInput = input;

private void FixedUpdate()
{
    _rigidbody.AddForce(_moveInput * _force);
}
```

## Non-Allocating Queries

```csharp
// Pre-allocate buffers
private static readonly RaycastHit[] _hitBuffer = new RaycastHit[16];
private static readonly Collider[] _overlapBuffer = new Collider[32];

// Raycast
int hitCount = Physics.RaycastNonAlloc(origin, direction, _hitBuffer, maxDistance, layerMask);
for (int i = 0; i < hitCount; i++)
{
    RaycastHit hit = _hitBuffer[i];
    // Process hit
}

// Overlap sphere (area detection)
int overlapCount = Physics.OverlapSphereNonAlloc(center, radius, _overlapBuffer, layerMask);

// Sphere cast (fat raycast)
int castCount = Physics.SphereCastNonAlloc(origin, radius, direction, _hitBuffer, maxDistance, layerMask);
```

## Layer Collision Matrix

```csharp
// Ignore collisions between layers programmatically
Physics.IgnoreLayerCollision(playerLayer, pickupLayer, true);

// Or configure in Edit > Project Settings > Physics > Layer Collision Matrix
```

Layer organization:
```
6: Player
7: Ground
8: Enemy
9: Projectile
10: Trigger (no physics collision, triggers only)
11: Interactable
```

## Collision Detection Modes

| Mode | Use When |
|------|----------|
| Discrete | Slow objects (default) |
| Continuous | Fast objects that might tunnel through thin colliders |
| Continuous Dynamic | Fast objects colliding with other fast objects |
| Continuous Speculative | Good balance of accuracy and performance |

## Collision vs Trigger Callbacks

```csharp
// Collision (both have colliders, at least one has Rigidbody, neither is trigger)
private void OnCollisionEnter(Collision collision) { }
private void OnCollisionStay(Collision collision) { }
private void OnCollisionExit(Collision collision) { }

// Trigger (at least one collider has isTrigger = true)
private void OnTriggerEnter(Collider other) { }
private void OnTriggerStay(Collider other) { }
private void OnTriggerExit(Collider other) { }
```

## Physics.SyncTransforms

After moving a transform directly, physics queries won't reflect the new position until the next physics step. Force sync:
```csharp
transform.position = newPosition;
Physics.SyncTransforms(); // Now raycasts see the new position
```

## Rigidbody Configuration

- **Interpolation:** `Interpolate` for player (smooths between physics steps), `None` for others
- **Constraints:** Freeze rotation for 2D-like behavior in 3D
- **Collision Detection:** Continuous for fast-moving objects

## 2D Physics Equivalents

| 3D | 2D |
|----|-----|
| `Rigidbody` | `Rigidbody2D` |
| `BoxCollider` | `BoxCollider2D` |
| `Physics.Raycast` | `Physics2D.Raycast` |
| `Physics.OverlapSphereNonAlloc` | `Physics2D.OverlapCircleNonAlloc` |
| `OnCollisionEnter(Collision)` | `OnCollisionEnter2D(Collision2D)` |
| `OnTriggerEnter(Collider)` | `OnTriggerEnter2D(Collider2D)` |

## Joints

| Joint | Use |
|-------|-----|
| Fixed | Weld objects together |
| Hinge | Doors, wheels |
| Spring | Bouncy connections |
| Configurable | Full control over all axes |
| Character | Character controller with physics |
