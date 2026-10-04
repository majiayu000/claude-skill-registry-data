---
name: universal-tween-engine
description: Use when writing Java code using Universal Tween Engine (package aurelienribon.tweenengine, version 6.3.3) — Tween.to, Tween.from, Tween.set, Tween.call, Tween.mark, Timeline.createSequence, Timeline.createParallel, TweenAccessor, TweenManager, TweenCallback, easing equations (Quad, Cubic, Back, Elastic, Bounce, etc.), or waypoints/paths. Use when debugging tweens not starting, accessor not found errors, values not interpolating, callbacks not firing, or pooling/lifecycle issues.
---

# Universal Tween Engine (6.3.3)

Quick reference for consumers of `aurelienribon.tweenengine`. Covers factory construction, accessor registration, defaults/limits, semantic traps, callbacks, pooling lifecycle, and timeline composition. Full method signatures in `references/api.md`.

## Defaults & Limits

| Setting | Default | Override |
|---|---|---|
| **Easing equation** | `Quad.INOUT` | `.ease(equation)` |
| **Path algorithm** | `CatmullRom` spline | `.path(TweenPaths.linear)` |
| **Combined attributes limit** | **3** | `Tween.setCombinedAttributesLimit(n)` at startup |
| **Waypoints limit** | **0** | `Tween.setWaypointsLimit(n)` at startup |
| **Callback trigger** | `COMPLETE` only | `.setCallbackTriggers(flags)` |
| **`Tween.call()` trigger** | `START` (overrides default) | `.setCallbackTriggers(flags)` |
| **Duration units** | Unitless (matches `manager.update(delta)`) | N/A |
| **Repeat count** | 0 (no repeat) | `.repeat(count, delay)` or `.repeatYoyo(count, delay)` |
| **Auto-remove from manager** | true | `TweenManager.setAutoRemove(tween, false)` |
| **Auto-start on manager add** | true | `TweenManager.setAutoStart(tween, false)` |
| **Tween pool initial capacity** | 20 | `Tween.ensurePoolCapacity(n)` |
| **Timeline pool initial capacity** | 10 | `Timeline.ensurePoolCapacity(n)` |

**Combined attributes limit = 3 means**: tweening 4+ float values simultaneously (e.g., RGBA) throws at runtime unless you call `Tween.setCombinedAttributesLimit(4)` first.

**Waypoints limit = 0 means**: ANY `.waypoint()` call throws unless you call `Tween.setWaypointsLimit(n)` first.

## Factory-Only Construction

Tween and Timeline have **private constructors**. All instances come from internal object pools via static factories.

```java
// Tween factories — NEVER use new Tween()
Tween.to(target, tweenType, duration)      // animate from current to target values
Tween.from(target, tweenType, duration)    // animate from target values to current (reversed)
Tween.set(target, tweenType)               // instantly set values (duration=0)
Tween.call(callback)                       // timer/callback only — no target needed
Tween.mark()                               // empty beacon for Timeline sequencing

// Timeline factories — NEVER use new Timeline()
Timeline.createSequence()                  // children play one after another
Timeline.createParallel()                  // children play all at once
```

## TweenAccessor Registration

An accessor MUST be available before any tween on that type starts. Two approaches:

**Approach 1: Register externally (most common)**
```java
// At application startup, once
Tween.registerAccessor(Sprite.class, new SpriteAccessor());

// Then anywhere:
Tween.to(mySprite, SpriteAccessor.POSITION_XY, 1f).target(100, 200).start(manager);
```

**Approach 2: Target self-implements TweenAccessor**
```java
// No registration needed — engine detects TweenAccessor on the target
public class Particle implements TweenAccessor<Particle> {
    public static final int XY = 0;
    float x, y;

    @Override
    public int getValues(Particle target, int tweenType, float[] returnValues) {
        returnValues[0] = target.x;
        returnValues[1] = target.y;
        return 2;  // MUST return count of values written
    }

    @Override
    public void setValues(Particle target, int tweenType, float[] newValues) {
        target.x = newValues[0];
        target.y = newValues[1];
    }
}
```

**`getValues()` return value contract:** The int returned is the count of float values written into `returnValues[]`. This count must be <= `combinedAttrsLimit`. The engine uses it to know how many values to interpolate. Returning 0 or forgetting the return breaks interpolation silently.

**Inheritance lookup:** If no accessor is registered for the exact class, the engine walks up the superclass hierarchy looking for a registered accessor. This lets you register one accessor for a base class.

## Semantic Traps

### `Tween.from()` reversal
The `.target()` values become the **START** position. The object's current values at initialization become the **END**. The animation runs FROM the target values TO the current values — backwards from what the name suggests.

```java
// Object currently at x=100
Tween.from(obj, X, 1f).target(0)  // animates FROM 0 TO 100 (current)
Tween.to(obj, X, 1f).target(0)    // animates FROM 100 (current) TO 0
```

### `targetRelative()` — relative offsets
`targetRelative(100)` means "100 units from wherever the object is at **initialization time**" (after the delay), not from where it was when the factory was called. The relative offset is converted to an absolute target at initialization: `finalTarget = startValue + relativeOffset`. If the object moves between factory call and initialization (e.g., another tween moves it during the delay), the final target reflects the position at initialization, not at creation.

```java
// "Move 100px to the right from current position" pattern:
Tween.to(obj, X, 1f).targetRelative(100).start(manager);

// Contrast with target() which sets an absolute destination:
Tween.to(obj, X, 1f).target(500).start(manager);  // always ends at 500, regardless of start
```

### `delay()` is additive
Multiple `.delay()` calls **stack**. They do not replace.
```java
tween.delay(1f).delay(0.5f)  // total delay = 1.5, NOT 0.5
```

### Duration is unitless
The javadoc `@param duration` says "milliseconds" — this is misleading. Duration uses whatever unit you pass to `manager.update(delta)`. Most game loop integrations pass seconds (e.g., `Gdx.graphics.getDeltaTime()`), so durations are typically in seconds.

### Always pass delta >= 0
The javadoc on `update(float delta)` advertises negative delta for backward play. **Do not use negative delta** — backward play is unreliable and a source of bugs. Always clamp delta to >= 0 before passing to `manager.update()` or `tween.update()`.

### Default easing is NOT linear
Default is `Quad.INOUT`. For linear interpolation, explicitly set `.ease(Linear.INOUT)`.

### Default path is NOT linear
Default path is `CatmullRom` spline. Only matters when using waypoints. For straight-line waypoint interpolation, use `.path(TweenPaths.linear)`.

## Callback System

```java
tween.setCallback((type, source) -> {
    // 'type' is a single flag (e.g., TweenCallback.COMPLETE), NOT a combined mask
    if (type == TweenCallback.COMPLETE) { /* ... */ }
}).setCallbackTriggers(TweenCallback.BEGIN | TweenCallback.COMPLETE);
```

**Callback trigger constants (bitmask):**

| Constant | Value | When |
|---|---|---|
| `BEGIN` | 0x01 | Right after initial delay ends (once) |
| `START` | 0x02 | At each iteration beginning |
| `END` | 0x04 | At each iteration ending, before repeat delay |
| `COMPLETE` | 0x08 | At last END (once) |
| `BACK_BEGIN` | 0x10 | First backward iteration beginning |
| `BACK_START` | 0x20 | Each backward iteration beginning |
| `BACK_END` | 0x40 | Each backward iteration ending |
| `BACK_COMPLETE` | 0x80 | Last BACK_END (once) |
| `ANY_FORWARD` | 0x0F | All forward events |
| `ANY_BACKWARD` | 0xF0 | All backward events |
| `ANY` | 0xFF | All events |

**Timing diagram (canonical reference):**
```
forward :      BEGIN                                   COMPLETE
forward :      START    END      START    END      START    END
|--------------[XXXXXXXXXX]------[XXXXXXXXXX]------[XXXXXXXXXX]
backward:      bEND  bSTART      bEND  bSTART      bEND  bSTART
backward:      bCOMPLETE                                 bBEGIN
```

**`Tween.call()` overrides default trigger to `START`** (not `COMPLETE`). All other factories default to `COMPLETE`.

## Pooling Lifecycle

Managed tweens (started via `.start(manager)`) are fire-and-forget:

1. Create via factory -> object pulled from pool
2. `.start(manager)` -> manager adds and starts it
3. `manager.update(delta)` -> two phases per call:
   - **Phase 1: Sweep** — removes tweens that finished on a *previous* update, calling `free()` on each (returns to pool)
   - **Phase 2: Update** — updates all remaining tweens with the delta

A tween that finishes during this frame's update is NOT removed until the next `update()` call. This means `isFinished()` returns true for one frame before the tween is freed.

**Holding references to finished managed tweens is unsafe.** After `free()`, the same object may be reused for a completely different tween.

To keep a tween reference alive after completion:
```java
TweenManager.setAutoRemove(tween, false);  // prevents automatic removal and pooling
// You must manually call tween.free() when done, or it leaks
```

For unmanaged tweens (`.start()` with no manager): you must call `tween.update(delta)` yourself and `tween.free()` when done.

## Timeline Composition

```java
Timeline.createSequence()
    .push(Tween.set(obj, OPACITY).target(0))           // instant set
    .beginParallel()                                     // nested parallel
        .push(Tween.to(obj, OPACITY, 0.5f).target(1))
        .push(Tween.to(obj, SCALE, 0.5f).target(1, 1))
    .end()                                               // closes beginParallel
    .pushPause(1.0f)                                     // 1-second pause
    .push(Tween.to(obj, POS_X, 0.5f).target(100))
    .repeat(5, 0.5f)
    .start(manager);
```

**Rules:**
- Every `beginParallel()` / `beginSequence()` MUST be balanced with `.end()`
- Children with infinite repeat (`Tween.INFINITY`) throw on build when pushed to a Timeline
- `pushPause()` accepts negative values for overlap with the preceding child
- Nested timelines pushed via `.push(timeline)` must have their own `end()` calls balanced before being pushed

## Parameterizable Equations

`Back` and `Elastic` have mutable parameters:

```java
Back.IN.s(2.5f)                    // overshoot amount (default 1.70158)
Elastic.IN.a(1.2f).p(0.4f)        // amplitude / period
```

**These mutate the static singleton instances.** If you call `Back.IN.s(2.5f)` in one tween, ALL subsequent tweens using `Back.IN` see the changed value. This is NOT thread-safe and persists for the application lifetime.

## Built-in Tweenables

The library includes `MutableFloat` and `MutableInteger` (in `primitives` subpackage) which self-implement `TweenAccessor` — no registration needed:

```java
MutableFloat alpha = new MutableFloat(0f);
Tween.to(alpha, 0, 1f).target(1f).start(manager);
// alpha.floatValue() will interpolate from 0 to 1 over 1 unit of time
```

## Common Mistakes

1. **`new Tween(...)` or `new Timeline(...)`** — constructors are private. Use static factories.
2. **Forgetting `Tween.registerAccessor()`** — throws "No TweenAccessor was found for the target" at `.start()` or `.build()`.
3. **`getValues()` returning 0 or wrong count** — engine interpolates 0 values; nothing visibly happens.
4. **Tweening 4+ values without raising limit** — throws at runtime. Call `Tween.setCombinedAttributesLimit(n)` at startup.
5. **Using `.waypoint()` without raising limit** — throws immediately (default limit is 0).
6. **Expecting `Tween.from()` target values to be the end** — they're the START. Current values are the end.
7. **Assuming linear default easing** — default is `Quad.INOUT`.
8. **Treating duration as milliseconds** — it's unitless; matches `update(delta)` time scale.
9. **Holding reference to managed tween after completion** — object is pooled and recycled.
10. **Unbalanced `beginParallel()`/`end()`** — throws "Nothing to end..." or "You forgot to call end()".
11. **Pushing infinite-repeat child into Timeline** — throws on build.
12. **Calling `Back.IN.s()` or `Elastic.IN.a().p()` without realizing it mutates the global static instance** — affects all future tweens using that equation.
