---
name: libgdx-bullet-physics
description: Use when writing libGDX Java/Kotlin code involving 3D physics with the Bullet wrapper — btRigidBody, btDiscreteDynamicsWorld, collision shapes, ContactListener, raycasting, MotionState, or debug drawing. Use when debugging segfaults, native memory leaks, bodies not moving, or collision detection failures in the libGDX Bullet extension.
---

# libGDX Bullet Physics Wrapper

Quick reference for the libGDX Bullet extension (`com.badlogic.gdx.physics.bullet.*`). This is a JNI wrapper around the C++ Bullet Physics library. All `bt*` objects are backed by native memory — the Java GC does NOT free them. Manual `dispose()` is mandatory.

**Not supported on HTML5/GWT.**

## Gradle Dependencies

```gradle
// core
api "com.badlogicgames.gdx:gdx-bullet:$gdxVersion"
// desktop
implementation "com.badlogicgames.gdx:gdx-bullet-platform:$gdxVersion:natives-desktop"
// android (all four)
natives "com.badlogicgames.gdx:gdx-bullet-platform:$gdxVersion:natives-armeabi-v7a"
natives "com.badlogicgames.gdx:gdx-bullet-platform:$gdxVersion:natives-arm64-v8a"
natives "com.badlogicgames.gdx:gdx-bullet-platform:$gdxVersion:natives-x86"
natives "com.badlogicgames.gdx:gdx-bullet-platform:$gdxVersion:natives-x86_64"
// ios
implementation "com.badlogicgames.gdx:gdx-bullet-platform:$gdxVersion:natives-ios"
```

## Initialization

```java
Bullet.init();  // MUST call before any bt* class. Loads native library. Segfault otherwise.
```

Three overloads:
```java
Bullet.init()                                   // useRefCounting=false, logging=true
Bullet.init(boolean useRefCounting)              // logging=true
Bullet.init(boolean useRefCounting, boolean logging)
```

Call once in `create()`, guard against double-init. Reference counting enables automatic `obtain()`/`release()` on shared objects (e.g., `btCompoundShape` child shapes).

## Dynamics World Setup

Five objects, created in this order:

```java
btDefaultCollisionConfiguration collisionConfig = new btDefaultCollisionConfiguration();
btCollisionDispatcher dispatcher = new btCollisionDispatcher(collisionConfig);
btDbvtBroadphase broadphase = new btDbvtBroadphase();
btSequentialImpulseConstraintSolver solver = new btSequentialImpulseConstraintSolver();
btDiscreteDynamicsWorld world = new btDiscreteDynamicsWorld(
    dispatcher, broadphase, solver, collisionConfig);
world.setGravity(new Vector3(0, -10f, 0));  // takes libGDX Vector3, NOT btVector3
```

Constructor: `btDiscreteDynamicsWorld(btDispatcher, btBroadphaseInterface, btConstraintSolver, btCollisionConfiguration)`. Parameter order is dispatcher, broadphase, solver, config.

### Stepping

```java
// 3-arg form (recommended):
world.stepSimulation(delta, maxSubSteps, fixedTimeStep);
// delta: frame time; maxSubSteps: catch-up limit; fixedTimeStep: physics tick (1/60f typical)

// Return value: int — number of substeps performed
float delta = Math.min(1f / 30f, Gdx.graphics.getDeltaTime());
world.stepSimulation(delta, 5, 1f / 60f);
```

**DO NOT use the 1-arg form** `stepSimulation(delta)` — it defaults `maxSubSteps=1`, so any frame taking longer than 1/60s loses simulation time. Always pass all three arguments.

### Adding / Removing Bodies

```java
world.addRigidBody(body);
world.addRigidBody(body, collisionGroup, collisionMask);  // group/mask are int (bit flags)
world.removeRigidBody(body);
```

There is NO `removeAndDestroyBody()` — you must remove then dispose separately.

## Collision Shapes

All in `com.badlogic.gdx.physics.bullet.collision`. Constructors take libGDX `Vector3` (not `btVector3`).

| Shape | Constructor | Notes |
|---|---|---|
| `btBoxShape` | `(Vector3 halfExtents)` | Half-extents, not full size |
| `btSphereShape` | `(float radius)` | |
| `btCapsuleShape` | `(float radius, float height)` | Y-axis. Also `btCapsuleShapeX`, `btCapsuleShapeZ` |
| `btCylinderShape` | `(Vector3 halfExtents)` | Y-axis. Also `btCylinderShapeX`, `btCylinderShapeZ` |
| `btConeShape` | `(float radius, float height)` | Y-axis. Also `btConeShapeX`, `btConeShapeZ` |
| `btConvexHullShape` | `()` then `addPoint(Vector3)` | Or `(FloatBuffer)` — must be direct buffer |
| `btBvhTriangleMeshShape` | `(Array<MeshPart>)` | Static concave meshes only. libGDX convenience |
| `btCompoundShape` | `()` | `addChildShape(Matrix4 localTransform, btCollisionShape)` |

**Gotchas:**
- `btBvhTriangleMeshShape` is for **static** geometry only — do not use for dynamic bodies.
- `btConvexHullShape(FloatBuffer)` requires a **direct** buffer (`ByteBuffer.allocateDirect()`).
- Capsule/Cylinder/Cone default to Y-axis. Use the `X`/`Z` suffixed classes for other axes.
- `btCompoundShape.addChildShape()` calls `obtain()` on child shapes when reference counting is enabled.

### calculateLocalInertia

```java
Vector3 localInertia = new Vector3();
shape.calculateLocalInertia(mass, localInertia);  // output parameter — writes into localInertia
```

On `btCollisionShape`. Must call for dynamic bodies (mass > 0). Static bodies use `Vector3.Zero`.

## Rigid Bodies

### Static vs Dynamic vs Kinematic

| Type | Mass | Inertia | Flags | Moved by |
|---|---|---|---|---|
| Static | 0 | `Vector3.Zero` | (auto `CF_STATIC_OBJECT`) | Nothing |
| Dynamic | > 0 | `calculateLocalInertia()` | (none needed) | Physics |
| Kinematic | 0 | `Vector3.Zero` | `CF_KINEMATIC_OBJECT` | Application code via MotionState |

### Construction

Two patterns — both work. Direct construction bypasses the info object:

```java
// Pattern 1: via ConstructionInfo (reusable for multiple bodies)
Vector3 localInertia = new Vector3();
shape.calculateLocalInertia(mass, localInertia);
btRigidBody.btRigidBodyConstructionInfo info =
    new btRigidBody.btRigidBodyConstructionInfo(mass, motionState, shape, localInertia);
info.setRestitution(0.5f);
info.setFriction(0.8f);
btRigidBody body = new btRigidBody(info);
info.dispose();  // can dispose after body creation

// Pattern 2: direct
btRigidBody body = new btRigidBody(mass, motionState, shape, localInertia);
```

`btRigidBodyConstructionInfo` is an inner class of `btRigidBody`. Constructor: `(float mass, btMotionState motionState, btCollisionShape shape, Vector3 localInertia)`. The `motionState` parameter can be `null` — set it later via `body.setMotionState()`.

### Kinematic Body Setup

```java
btRigidBody body = new btRigidBody(0f, motionState, shape, Vector3.Zero);
body.setCollisionFlags(body.getCollisionFlags()
    | btCollisionObject.CollisionFlags.CF_KINEMATIC_OBJECT);
body.setActivationState(Collision.DISABLE_DEACTIVATION);  // CRITICAL
```

Without `DISABLE_DEACTIVATION`, Bullet stops calling `getWorldTransform()` on the MotionState after the body sleeps — your kinematic body freezes.

### Key btRigidBody Methods

```java
// Forces (accumulated, applied at next step, cleared by clearForces)
body.applyCentralForce(Vector3 force);
body.applyForce(Vector3 force, Vector3 relPos);
body.applyTorque(Vector3 torque);
body.clearForces();

// Impulses (instant velocity change)
body.applyCentralImpulse(Vector3 impulse);
body.applyImpulse(Vector3 impulse, Vector3 relPos);

// Velocity
body.setLinearVelocity(Vector3 vel);
body.setAngularVelocity(Vector3 vel);

// Axis locking (e.g., 2D physics: lock Z axis)
body.setLinearFactor(new Vector3(1, 1, 0));
body.setAngularFactor(new Vector3(0, 0, 1));

// Damping
body.setDamping(float linearDamping, float angularDamping);

// Sleeping
body.setSleepingThresholds(float linear, float angular);
body.activate();  // wake up a sleeping body
```

### btCollisionObject (base class)

```java
body.setWorldTransform(Matrix4 transform);
body.getWorldTransform(Matrix4 out);    // output parameter form
Matrix4 t = body.getWorldTransform();   // allocating form

body.setUserValue(int value);           // int stored on native side — survives GC
int v = body.getUserValue();
body.userData = myObject;               // Java-only Object field — NOT on native side

body.setCollisionFlags(int flags);
body.setActivationState(int state);
body.isStaticOrKinematicObject();
```

### Collision Flags (`btCollisionObject.CollisionFlags`)

| Constant | Value | Use |
|---|---|---|
| `CF_STATIC_OBJECT` | 1 | Auto-set for mass=0 bodies |
| `CF_KINEMATIC_OBJECT` | 2 | Must set manually for kinematic |
| `CF_NO_CONTACT_RESPONSE` | 4 | Trigger/sensor (detects but no physics response) |
| `CF_CUSTOM_MATERIAL_CALLBACK` | 8 | Required for `onContactAdded` |
| `CF_CHARACTER_OBJECT` | 16 | For character controllers |

### Activation States (`com.badlogic.gdx.physics.bullet.collision.Collision`)

| Constant | Value |
|---|---|
| `Collision.ACTIVE_TAG` | 1 |
| `Collision.ISLAND_SLEEPING` | 2 |
| `Collision.WANTS_DEACTIVATION` | 3 |
| `Collision.DISABLE_DEACTIVATION` | 4 |
| `Collision.DISABLE_SIMULATION` | 5 |

## MotionState

Syncs physics transform with render transform. Bullet calls `setWorldTransform` after simulating dynamic bodies, and `getWorldTransform` for kinematic bodies.

```java
static class MyMotionState extends btMotionState {
    private final Matrix4 transform;  // share with ModelInstance.transform

    public MyMotionState(Matrix4 transform) {
        this.transform = transform;
    }

    @Override
    public void getWorldTransform(Matrix4 worldTrans) {
        worldTrans.set(transform);  // Bullet reads from your transform (kinematic)
    }

    @Override
    public void setWorldTransform(Matrix4 worldTrans) {
        transform.set(worldTrans);  // Bullet writes its result (dynamic)
    }
}

// Usage — share the ModelInstance's transform matrix:
MyMotionState motionState = new MyMotionState(modelInstance.transform);
btRigidBody body = new btRigidBody(mass, motionState, shape, localInertia);
```

`btDefaultMotionState` also exists (`com.badlogic.gdx.physics.bullet.linearmath`) but the custom pattern above is standard in libGDX because it shares the `Matrix4` directly with `ModelInstance`.

**Gotcha:** MotionState takes `com.badlogic.gdx.math.Matrix4` — the wrapper converts to/from native Bullet transforms automatically.

## Contact Detection

### ContactListener

`com.badlogic.gdx.physics.bullet.collision.ContactListener` — instantiate to enable globally. Only one overload per callback event.

Four event types, each with multiple overloads (btCollisionObject, userValue int, or btCollisionObjectWrapper variants). The `int userValue` variants are fastest (no JNI object mapping).

```java
ContactListener contactListener = new ContactListener() {
    @Override
    public boolean onContactAdded(int userValue0, int partId0, int index0,
            boolean match0, int userValue1, int partId1, int index1, boolean match1) {
        // match0/match1 = true if that object's flag matched the other's filter
        if (match0) { /* userValue0's object was matched */ }
        return true;
    }
};
```

**Filtering setup:**
```java
body.setContactCallbackFlag(1 << 1);    // this object's identity bits
body.setContactCallbackFilter(1 << 1);  // which identity bits to listen for
```

Match logic: callback fires if `(objA.callbackFilter & objB.callbackFlag) != 0` for at least one side.

**`onContactAdded` requires `CF_CUSTOM_MATERIAL_CALLBACK`** on at least one colliding body:
```java
body.setCollisionFlags(body.getCollisionFlags()
    | btCollisionObject.CollisionFlags.CF_CUSTOM_MATERIAL_CALLBACK);
```

| Callback | Returns | Fires when |
|---|---|---|
| `onContactAdded` | `boolean` | New contact point created. Needs `CF_CUSTOM_MATERIAL_CALLBACK`. |
| `onContactProcessed` | `void` | Contact processed during simulation step |
| `onContactStarted` | `void` | New manifold between two objects |
| `onContactEnded` | `void` | Manifold between two objects removed |

Enable/disable individually: `enableOnAdded()` / `disableOnAdded()`, etc.

## Raycasting

```java
// Create once, reuse:
ClosestRayResultCallback callback = new ClosestRayResultCallback(Vector3.Zero, Vector3.Z);

// Before each ray test — MUST reset:
callback.setCollisionObject(null);
callback.setClosestHitFraction(1f);
callback.setRayFromWorld(rayFrom);
callback.setRayToWorld(rayTo);

world.rayTest(rayFrom, rayTo, callback);

if (callback.hasHit()) {
    btCollisionObject hit = callback.getCollisionObject();
    Vector3 hitPoint = new Vector3();
    callback.getHitPointWorld(hitPoint);   // output parameter
    Vector3 hitNormal = new Vector3();
    callback.getHitNormalWorld(hitNormal);  // output parameter
}

// Dispose when done (NOT per-frame):
callback.dispose();
```

There is NO `set(from, to)` convenience method — you must call individual setters to reuse.

`AllHitsRayResultCallback` — same constructor pattern. Results via `getCollisionObjects()` (returns `btCollisionObjectConstArray`, iterate with `atConst(int index)`), `getHitPointWorld()` / `getHitNormalWorld()` (return `btVector3Array`).

`ClosestNotMeRayResultCallback(btCollisionObject me)` — excludes a specific object from results.

All ray callbacks must be disposed. They extend `BulletBase` which wraps native memory.

## Debug Drawing

```java
DebugDrawer debugDrawer = new DebugDrawer();  // creates its own ShapeRenderer internally
debugDrawer.setDebugMode(btIDebugDraw.DebugDrawModes.DBG_DrawWireframe
    | btIDebugDraw.DebugDrawModes.DBG_DrawContactPoints);
world.setDebugDrawer(debugDrawer);

// In render(), after your normal 3D rendering:
debugDrawer.begin(camera);
world.debugDrawWorld();
debugDrawer.end();

// In dispose():
debugDrawer.dispose();
```

`DebugDrawer` extends `btIDebugDraw`. Key debug mode flags:

| Flag | Value |
|---|---|
| `DBG_NoDebug` | 0 |
| `DBG_DrawWireframe` | 1 |
| `DBG_DrawAabb` | 2 |
| `DBG_DrawContactPoints` | 8 |
| `DBG_NoDeactivation` | 16 |
| `DBG_DrawConstraints` | 2048 |
| `DBG_DrawNormals` | 16384 |

## Memory Management

**CRITICAL.** Every `bt*` object wraps native C++ memory. The Java GC does NOT free it. You MUST call `dispose()` on every Bullet object you create.

### Disposal Order (reverse of creation)

```java
// 1. Remove all bodies/objects from world
world.removeRigidBody(body);

// 2. Dispose bodies, motionStates, constructionInfos
body.dispose();
motionState.dispose();
constructionInfo.dispose();  // can dispose earlier, after body creation

// 3. Dispose collision shapes (only after all bodies using them are disposed)
shape.dispose();

// 4. Dispose contact listeners, debug drawer, ray callbacks
contactListener.dispose();

// 5. Dispose world infrastructure in reverse creation order
world.dispose();
solver.dispose();
broadphase.dispose();
dispatcher.dispose();
collisionConfig.dispose();
```

### Preventing GC of Java Wrappers

`btCollisionObject` maintains a static `LongMap<btCollisionObject> instances` keyed by native pointer. This keeps Java wrappers alive while Bullet references them. Disposal removes the entry.

`userData` is a Java-only `Object` field — invisible to native code. Use `setUserValue(int)` for data that must survive on the native side (e.g., entity array index for fast ContactListener lookups).

### Reference Counting (optional)

```java
Bullet.init(true);  // enable ref counting
shape.obtain();     // +1
shape.release();    // -1, auto-disposes at 0
```

`btCompoundShape.addChildShape()` auto-calls `obtain()` on child shapes when enabled.

## Advanced Topics (brief)

**Constraints:** `btPoint2PointConstraint`, `btHingeConstraint`, `btConeTwistConstraint`, `btSliderConstraint`, `btGeneric6DofConstraint`, `btGeneric6DofSpringConstraint`, `btGeneric6DofSpring2Constraint`, `btFixedConstraint`. Add via `world.addConstraint(constraint, disableCollisionBetweenBodies)`. Remove before disposing world.

**Character controller:** `btKinematicCharacterController` with `btPairCachingGhostObject`. Requires `btGhostPairCallback` registered on the broadphase's overlapping pair cache (`broadphase.getOverlappingPairCache().setInternalGhostPairCallback(new btGhostPairCallback())`). Works with any broadphase including `btDbvtBroadphase`. Added to world via `world.addAction(controller)`.

**Collision-only world:** Use `btCollisionWorld` (3-arg constructor: dispatcher, broadphase, config — no solver) for collision detection without dynamics.

**InternalTickCallback:** Override `onInternalTick(btDynamicsWorld, float timeStep)` for per-substep callbacks. Attach as pre-tick or post-tick.

**Soft bodies, vehicles:** Available in the wrapper but advanced — consult the Bullet C++ documentation.

## Common Mistakes

1. **Forgetting `Bullet.init()`** — Any `bt*` class instantiated before `init()` causes a segfault. Call it once in `create()`.
2. **Not disposing `bt*` objects** — Native memory leak. Every `bt*` object, ray callback, MotionState, and ConstructionInfo needs `dispose()`. Java GC does NOT free the native allocation reliably.
3. **Wrong disposal order** — Disposing the world while bodies are still in it, or disposing shapes while bodies reference them, causes crashes. Remove all bodies first, then dispose in reverse creation order.
4. **Skipping `calculateLocalInertia()` for dynamic bodies** — Body will have zero inertia and won't rotate or respond to off-center forces correctly. Always call `shape.calculateLocalInertia(mass, outVector)` when mass > 0.
5. **Using 1-arg `stepSimulation(delta)`** — Defaults `maxSubSteps` to 1. Any frame longer than 1/60s loses simulation time. Always use the 3-arg form.
6. **Forgetting `DISABLE_DEACTIVATION` on kinematic bodies** — Bullet deactivates the body and stops calling `getWorldTransform()`. The kinematic body appears frozen.
7. **Not resetting ray callbacks before reuse** — `ClosestRayResultCallback` retains state from the previous test. Must call `setCollisionObject(null)` and `setClosestHitFraction(1f)` before each `rayTest()`.
8. **Disposing ConstructionInfo with shared MotionState/shape references** — `btRigidBodyConstructionInfo` does NOT take ownership. The MotionState and shape must outlive the body. Dispose the info early if you want, but keep the shape and MotionState alive.
9. **Expecting Box2D-style pixels-per-meter scaling** — Bullet uses real-world units (meters). No PPM conversion needed. A 1-unit box is 1 meter.
10. **Sharing `btBvhTriangleMeshShape` with dynamic bodies** — Concave triangle mesh shapes are static-only. Use `btConvexHullShape` or `btCompoundShape` for dynamic bodies.
11. **Forgetting `CF_CUSTOM_MATERIAL_CALLBACK` for `onContactAdded`** — The callback silently never fires. At least one colliding body must have this flag set.
12. **Storing Java references only in `userData`** — This field is Java-only. For ContactListener performance, use `setUserValue(int)` to store an entity index, then look up your game object from an array.
