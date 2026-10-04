---
name: libgdx-box2d
description: Use when writing libGDX Java/Kotlin code involving Box2D physics — World creation/stepping, Body/BodyDef (Static/Kinematic/Dynamic), Fixture/FixtureDef, Shape types (PolygonShape/CircleShape/EdgeShape/ChainShape), collision filtering (categoryBits/maskBits/groupIndex), ContactListener callbacks, joints (Revolute/Distance/Prismatic/Weld/Mouse), Box2DDebugRenderer, pixels-to-meters conversion, or fixed timestep patterns. Use when debugging tunneling, bodies not colliding, crashes in contact callbacks, or sluggish physics movement.
---

# libGDX Box2D Physics

Quick reference for the libGDX Box2D JNI wrapper (`com.badlogic.gdx.physics.box2d.*`). Covers World, Body, Fixture, Shape, filtering, contacts, joints, debug rendering, and the PPM pattern.

## Units — Box2D Works in Meters

Box2D is tuned for objects **0.1–10 meters**. Using pixel coordinates causes sluggish movement (internal velocity cap is 2 units/timestep).

**Approach 1 — PPM constant:**
```java
public static final float PPM = 100f; // 100 pixels = 1 meter

// Creating bodies:    bodyDef.position.set(pixelX / PPM, pixelY / PPM);
// Rendering sprites:  sprite.setPosition(body.getPosition().x * PPM, body.getPosition().y * PPM);
// Debug renderer:     debugRenderer.render(world, camera.combined.cpy().scl(PPM));
```

**Approach 2 — Camera in meters (cleaner):**
```java
camera = new OrthographicCamera();
camera.setToOrtho(false, viewportWidthMeters, viewportHeightMeters);
// All game logic in meters. Debug renderer uses camera.combined directly.
debugRenderer.render(world, camera.combined);
```

## World

```java
World world = new World(new Vector2(0, -10f), true); // gravity, doSleep
```

**Fixed timestep — the accumulator pattern (REQUIRED):**
```java
private static final float TIME_STEP = 1 / 60f;
private static final int VELOCITY_ITERATIONS = 6;
private static final int POSITION_ITERATIONS = 2;
private float accumulator = 0;

private void stepPhysics(float deltaTime) {
    float frameTime = Math.min(deltaTime, 0.25f); // cap to prevent spiral of death
    accumulator += frameTime;
    while (accumulator >= TIME_STEP) {
        world.step(TIME_STEP, VELOCITY_ITERATIONS, POSITION_ITERATIONS);
        accumulator -= TIME_STEP;
    }
}
```

DO NOT pass `Gdx.graphics.getDeltaTime()` directly to `world.step()` — variable timestep causes tunneling and non-deterministic behavior.

**Key methods:**
```java
world.setContactListener(listener);                // ContactListener
world.setContactFilter(filter);                    // ContactFilter — boolean shouldCollide(Fixture, Fixture)
world.setGravity(new Vector2(0, -10f));
world.getGravity();                                // returns REUSED Vector2 — copy if storing
world.isLocked();                                  // true during step — cannot modify world

// Queries — coordinates in meters (world units)
world.QueryAABB(callback, lowerX, lowerY, upperX, upperY);  // note: capital Q
world.rayCast(callback, point1, point2);                     // Vector2 or float overloads

// Bulk retrieval — clears array first, then populates
Array<Body> bodies = new Array<>();
world.getBodies(bodies);                           // NOT a return-value method

world.dispose();                                   // MUST call when done
```

**QueryCallback:**
```java
world.QueryAABB(fixture -> {
    // return false to stop query, true to continue
    return true;
}, lowerX, lowerY, upperX, upperY);
```

**RayCastCallback** — method is `reportRayFixture` (NOT `reportFixture`):
```java
world.rayCast((fixture, point, normal, fraction) -> {
    // point and normal are REUSED — copy if storing
    // Return: -1=ignore fixture, 0=terminate, fraction=clip to closest, 1=continue
    return fraction; // closest-hit
}, startPoint, endPoint);
```

## Body

```java
BodyDef bodyDef = new BodyDef();
bodyDef.type = BodyDef.BodyType.DynamicBody; // StaticBody | KinematicBody | DynamicBody
bodyDef.position.set(x, y);                  // meters, NOT pixels
bodyDef.angle = 0;                           // radians, NOT degrees
bodyDef.fixedRotation = false;
bodyDef.bullet = false;                      // enable CCD for fast-moving bodies
bodyDef.gravityScale = 1;                    // per-body gravity multiplier (0 = no gravity)
Body body = world.createBody(bodyDef);
```

Also available on BodyDef: `linearDamping`, `angularDamping` (air resistance).

| BodyType | Moves? | Responds to forces? | Collides with |
|---|---|---|---|
| **StaticBody** | No | No | Dynamic only |
| **KinematicBody** | Yes (via velocity) | No — use `setLinearVelocity()` | Dynamic only |
| **DynamicBody** | Yes | Yes | All types |

**Position:** `body.getPosition()` (REUSED Vector2 — copy if storing!), `body.getAngle()` (radians), `body.setTransform(x, y, angleRadians)`, `body.getLinearVelocity()` (REUSED), `body.setLinearVelocity(vx, vy)`.

**Forces** (continuous, call every frame): `applyForceToCenter(vec, wake)`, `applyForce(vec, worldPoint, wake)`, `applyTorque(torque, wake)`. **Impulses** (instantaneous): `applyLinearImpulse(vec, worldPoint, wake)`, `applyAngularImpulse(impulse, wake)`.

**Other key methods:** `setUserData(obj)` / `getUserData()`, `getFixtureList()` (NOT getFixtures()), `setActive(false)` (NOT setEnabled()), `setSleepingAllowed(false)` (NOT setAllowSleep()), `setType()`, `setGravityScale(0)`.

## Fixture & Shape

```java
FixtureDef fixtureDef = new FixtureDef();
fixtureDef.shape = shape;             // REQUIRED
fixtureDef.density = 1f;             // default: 0 (no mass)
fixtureDef.friction = 0.3f;          // default: 0.2
fixtureDef.restitution = 0.1f;       // default: 0 (bounciness)
fixtureDef.isSensor = false;         // sensors detect overlap but don't collide
Fixture fixture = body.createFixture(fixtureDef);
// Convenience: body.createFixture(shape, density);
```

**CRITICAL: Dispose shapes after creating fixtures.** Box2D clones the shape internally — your Shape leaks native memory if not disposed.

### Shape Types

**PolygonShape** — max 8 vertices, must be convex, wound CCW:
```java
PolygonShape poly = new PolygonShape();
poly.setAsBox(halfWidth, halfHeight);             // HALF-extents, NOT full size!
poly.setAsBox(hx, hy, center, angleRadians);      // offset + rotated
poly.set(new float[]{x1,y1, x2,y2, x3,y3});      // arbitrary convex polygon
poly.dispose();
```

**CircleShape:** `setRadius(meters)`, `setPosition(offsetVec2)`. **EdgeShape:** single line segment — use ChainShape for terrain instead. **ChainShape:** `createChain(float[])` (open) or `createLoop(float[])` (closed), prevents ghost collisions at seams. All shapes must be disposed.

**Fixture methods:** `setUserData()` / `getUserData()`, `getBody()`, `getShape()` (do NOT dispose — owned by Box2D), `setSensor()`, `testPoint(worldX, worldY)`, `setFilterData(filter)` (MUST call to propagate changes), `setDensity()` (must call `body.resetMassData()` after).

## Collision Filtering

Three fields on `FixtureDef.filter` (type `short`):

| Field | Default | Purpose |
|---|---|---|
| `categoryBits` | `0x0001` | What this fixture IS |
| `maskBits` | `-1` (0xFFFF) | What this fixture COLLIDES WITH |
| `groupIndex` | `0` | Override: positive=always collide, negative=never |

**Algorithm (priority order):**
1. If both fixtures share the same **non-zero** `groupIndex`: positive = collide, negative = never
2. Otherwise: `(A.mask & B.category) != 0 && (B.mask & A.category) != 0` — both must accept each other

**Example — 16 categories max (short = 16 bits):**
```java
static final short PLAYER = 0x0001;
static final short ENEMY  = 0x0002;
static final short BULLET = 0x0004;
static final short WALL   = 0x0008;

// Player collides with enemies and walls, not own bullets
fixtureDef.filter.categoryBits = PLAYER;
fixtureDef.filter.maskBits = ENEMY | WALL;

// Bullet collides with enemies and walls only
fixtureDef.filter.categoryBits = BULLET;
fixtureDef.filter.maskBits = ENEMY | WALL;
```

**Runtime filter changes:**
```java
Filter filter = new Filter();
filter.categoryBits = BULLET;
filter.maskBits = WALL;
fixture.setFilterData(filter); // MUST call — modifying getFilterData() fields without this is undefined
```

Use `-1` for maskBits (collide with everything), not `(short)0xFFFF`. Both are equivalent but `-1` is idiomatic and avoids the cast.

## ContactListener

```java
world.setContactListener(new ContactListener() {
    @Override public void beginContact(Contact contact) {
        Fixture a = contact.getFixtureA();
        Fixture b = contact.getFixtureB();
        // Order is NOT guaranteed — check both directions
    }
    @Override public void endContact(Contact contact) { }
    @Override public void preSolve(Contact contact, Manifold oldManifold) {
        // Can disable contact for this step (one-way platforms):
        contact.setEnabled(false);
    }
    @Override public void postSolve(Contact contact, ContactImpulse impulse) {
        float[] normals = impulse.getNormalImpulses(); // float[2]
        int count = impulse.getCount();                // how many points valid
    }
});
```

**CRITICAL: Do NOT create/destroy bodies or joints inside ANY callback.** Box2D is mid-step (`world.isLocked() == true`). Queue changes and apply after `world.step()`:

```java
private Array<Body> bodiesToDestroy = new Array<>();

// In ContactListener:
bodiesToDestroy.add(contact.getFixtureA().getBody());

// After world.step():
for (Body b : bodiesToDestroy) {
    world.destroyBody(b);
}
bodiesToDestroy.clear();
```

## Joints

All joints share: `JointDef.bodyA`, `JointDef.bodyB`, `JointDef.collideConnected` (default `false`). Create with `world.createJoint(def)` — cast result to specific joint type.

**MouseJoint** — drag body to point (most common, no `initialize()`):
```java
MouseJointDef def = new MouseJointDef();
def.bodyA = groundBody;       // static body (required anchor)
def.bodyB = draggedBody;
def.target.set(touchWorldX, touchWorldY);
def.maxForce = 1000f * draggedBody.getMass();
def.frequencyHz = 5f;
def.dampingRatio = 0.7f;
MouseJoint joint = (MouseJoint) world.createJoint(def);
// Update target each frame: joint.setTarget(newWorldPoint);
```

**Other joints** — all use `def.initialize(bodyA, bodyB, ...)` unless noted:
- **RevoluteJoint** (pin/hinge): `initialize(bodyA, bodyB, worldAnchor)`. Supports `enableMotor`/`motorSpeed`/`maxMotorTorque`, `enableLimit`/`lowerAngle`/`upperAngle`.
- **DistanceJoint** (spring/rod): `initialize(bodyA, bodyB, anchorA, anchorB)`. Uses `frequencyHz`/`dampingRatio` (NOT stiffness/damping).
- **PrismaticJoint** (slider): `initialize(bodyA, bodyB, worldAnchor, axisDirection)`. Supports motor and translation limits.
- **WeldJoint** (glue): `initialize(bodyA, bodyB, worldAnchor)`. `frequencyHz=0` for rigid (may flex under stress).
- **RopeJoint** (max distance): no `initialize()` — set `bodyA`/`bodyB`/`localAnchorA`/`localAnchorB`/`maxLength` directly.

**Destroying joints:** `world.destroyJoint(joint)`. Destroying a body auto-destroys its joints — do NOT destroy the joint separately afterward.

## Box2DDebugRenderer

```java
Box2DDebugRenderer debugRenderer = new Box2DDebugRenderer();
// Or: new Box2DDebugRenderer(drawBodies, drawJoints, drawAABBs,
//                             drawInactiveBodies, drawVelocities, drawContacts);

// In render():
debugRenderer.render(world, camera.combined); // if camera is in meters
// OR with PPM:
debugRenderer.render(world, camera.combined.cpy().scl(PPM));

debugRenderer.dispose(); // MUST dispose — uses internal ShapeRenderer
```

## Common Mistakes

1. **Using pixel coordinates in Box2D** — Bodies at `(400, 300)` pixels behave as 400-meter objects. Use meters (typically 0.1–10 range). Convert with PPM constant or use a camera in meter units.
2. **Variable timestep** — Passing `getDeltaTime()` directly to `world.step()` causes tunneling and jitter. Use the fixed-timestep accumulator pattern with `1/60f`.
3. **Destroying bodies in ContactListener** — Crashes with native error. World is locked during callbacks. Queue bodies and destroy after `world.step()`.
4. **Forgetting shape.dispose() after createFixture()** — Box2D clones the shape data. Your Java Shape still holds a native pointer that leaks if not disposed.
5. **setAsBox(width, height) with full dimensions** — `PolygonShape.setAsBox()` takes **half-extents**. `setAsBox(2, 3)` creates a 4x6 meter box.
6. **Storing body.getPosition() reference** — Returns a REUSED Vector2 that changes on every call. Copy the values: `new Vector2(body.getPosition())`.
7. **Not checking both fixtures in ContactListener** — `getFixtureA()`/`getFixtureB()` order is arbitrary. Always check both directions when identifying collision pairs.
8. **Applying forces to KinematicBody** — Kinematic bodies ignore forces and impulses entirely. Control them with `setLinearVelocity()` / `setTransform()`.
9. **Using EdgeShape for terrain** — Adjacent EdgeShapes cause ghost collisions at seams. Use ChainShape instead.
10. **Modifying filter without setFilterData()** — Getting `fixture.getFilterData()` and changing fields without calling `fixture.setFilterData(filter)` does not propagate to native Box2D.
11. **PolygonShape with >8 vertices or concave shape** — Box2D silently fails or crashes. Max 8 vertices, must be convex, wound counter-clockwise.
12. **Calling getFixtures() instead of getFixtureList()** — The method is `body.getFixtureList()` returning `Array<Fixture>`. `getFixtures()` does not exist.
