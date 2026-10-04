---
name: libgdx-gdx-ai
description: Use when writing libGDX Java/Kotlin code involving gdx-ai — steering behaviors (Steerable, Arrive, Seek, Flee, Wander, Pursue, Evade, BlendedSteering, PrioritySteering), A* pathfinding (IndexedAStarPathFinder, Graph, Heuristic), behavior trees (BehaviorTree, LeafTask, Sequence, Selector, .tree text format, BehaviorTreeParser), finite state machines (State, DefaultStateMachine, StackStateMachine, MessageManager), or LoadBalancingScheduler. Use when debugging steering output not applied, wrong pathfinding graph setup, behavior tree not updating, or FSM message delivery issues.
---

# libGDX gdx-ai Extension

Reference for steering behaviors, A* pathfinding, behavior trees, finite state machines, and scheduling in the gdx-ai extension.

## Dependency

```gradle
// In core module only — pure Java, no native dependencies
implementation "com.badlogicgames.gdx:gdx-ai:$aiVersion"
```

Works on all backends including headless. No platform-specific jars needed.

## Steering Behaviors

### Steerable Interface

`Steerable<T extends Vector<T>>` extends `Location<T>` and `Limiter`. Your entity implements it, providing: `getPosition()`, `getOrientation()`, `setOrientation()`, `newLocation()`, `vectorToAngle()`, `angleToVector()`, `getLinearVelocity()`, `getAngularVelocity()`, `getBoundingRadius()`, `isTagged()`/`setTagged()`, and all Limiter getters/setters for max linear/angular speed/acceleration.

**`vectorToAngle`/`angleToVector` convention:** `vectorToAngle(v)` = `atan2(-v.x, v.y)`, `angleToVector(out, a)` sets `out.x = -sin(a)`, `out.y = cos(a)`. Getting this wrong causes steering to point in the wrong direction.

### SteeringAcceleration — The Output Container

`SteeringAcceleration<T>` has public fields `T linear` and `float angular`. Create ONE per entity, reuse each frame: `new SteeringAcceleration<>(new Vector2())`.

**`calculateSteering()` only fills the output container — it does NOT move the entity.** You must apply the acceleration to velocity and position yourself each frame.

### Common Setup Pattern

```java
// 1. Create behavior — target via constructor or setter
Arrive<Vector2> arrive = new Arrive<>(steerable, targetLocation)
    .setArrivalTolerance(0.5f)        // stop within this distance
    .setDecelerationRadius(3f)        // start slowing here
    .setTimeToTarget(0.1f);           // response speed (lower = snappier)
// Or set target separately:
// Arrive<Vector2> arrive = new Arrive<>(steerable)
//     .setTarget(targetLocation)
//     ...;

// 2. Each frame — calculate then apply
arrive.calculateSteering(steeringOutput);
linearVelocity.mulAdd(steeringOutput.linear, deltaTime);
if (linearVelocity.len2() > maxLinearSpeed * maxLinearSpeed)
    linearVelocity.setLength(maxLinearSpeed);
position.mulAdd(linearVelocity, deltaTime);
```

**Target is `Location<T>`, not `Steerable<T>`.** Any `Location` implementation works. Passing another `Steerable` works because `Steerable` extends `Location`.

### Individual Behaviors

Most-used: `Seek` (move toward target), `Flee` (move away), `Arrive` (decelerate to stop at target), `Wander` (random-looking movement), `Pursue`/`Evade` (predict moving target's future position).

Also available: `Face`, `LookWhereYouGoing`, `ReachOrientation`, `FollowPath`, `FollowFlowField`, `RaycastObstacleAvoidance`, `Hide` (extends `Arrive` — uses `Proximity` to find obstacles but is an individual behavior).

### Group Behaviors

Require a `Proximity<T>` to detect nearby agents: `Separation`, `Alignment`, `Cohesion`, `CollisionAvoidance`.

### PrioritySteering and BlendedSteering

**PrioritySteering** — try behaviors in order, use first that produces non-zero output:

```java
PrioritySteering<Vector2> priority = new PrioritySteering<>(steerable, 0.001f);
//                                                          epsilon ↑ threshold
// below this magnitude, output considered "zero" → try next behavior
priority.add(obstacleAvoidance);  // highest priority
priority.add(arrive);             // fallback
```

**BlendedSteering** — weighted sum of multiple behaviors:

```java
BlendedSteering<Vector2> blended = new BlendedSteering<>(steerable);
blended.add(arrive, 0.7f);         // 70% arrive
blended.add(separation, 0.3f);     // 30% separation
```

### Limiter Interface

`Steerable` extends `Limiter` (caps linear/angular speed/acceleration). Behaviors read limits from the owner. Override per-behavior via `behavior.setLimiter(customLimiter)`.

## Pathfinding

### Graph Setup

Implement `IndexedGraph<N>` with three methods: `getConnections(node)` returns `Array<Connection<N>>`, `getIndex(node)` returns a unique `int` index, `getNodeCount()` returns total node count.

`Connection<N>` has three methods: `getCost()`, `getFromNode()`, `getToNode()`. For simple weighted edges, use `DefaultConnection<N>`.

### Heuristic and Pathfinding

```java
Heuristic<TileNode> heuristic = (node, end) ->                       // Manhattan for 4-dir
    Math.abs(end.x - node.x) + Math.abs(end.y - node.y);
IndexedAStarPathFinder<TileNode> pathFinder = new IndexedAStarPathFinder<>(graph);
DefaultGraphPath<TileNode> outPath = new DefaultGraphPath<>();
boolean found = pathFinder.searchNodePath(startNode, endNode, heuristic, outPath);
outPath.clear();                                                      // MUST clear before reuse
```

`HierarchicalPathFinder` — for large maps; searches at multiple abstraction levels. Use when standard A* is too slow.

### NavMesh

**NavMesh is NOT included in gdx-ai.** Use a third-party library or build your own graph from a nav mesh. gdx-ai pathfinding works with any graph you implement — tile grids, waypoint graphs, or nav mesh triangulations — but provides no mesh generation or triangle-based nav classes.

## Behavior Trees

### BehaviorTree and Task

`BehaviorTree<E>` is the root container. `E` is the blackboard type (your data object shared by all tasks). Call `tree.step()` each frame.

```java
BehaviorTree<Enemy> tree = parser.parse(Gdx.files.internal("ai/enemy.tree"), enemy);
// In render/update:
tree.step();
```

**No GL context needed.** BehaviorTree is pure logic — works in headless, server, or testing environments.

### LeafTask

Extend `LeafTask<E>` for custom logic. Override `execute()` returning `Status`:

```java
public class IsEnemyVisible extends LeafTask<Enemy> {
    @Override
    public Status execute() {
        Enemy e = getObject();  // blackboard access
        return e.canSeePlayer() ? Status.SUCCEEDED : Status.FAILED;
    }

    @Override
    protected Task<Enemy> copyTo(Task<Enemy> task) { return task; }
}
```

**Status values:** `RUNNING` (continue next frame), `SUCCEEDED`, `FAILED`.

### Branch Tasks

**Sequence = AND** (run children in order, fail on first failure). **Selector = OR** (run children in order, succeed on first success). Also: `Parallel` (run all simultaneously), `RandomSelector`, `RandomSequence`.

### Decorator Tasks

`AlwaysFail`, `AlwaysSucceed`, `Invert` (flip SUCCEEDED/FAILED), `Repeat` (N times or indefinitely), `UntilFail`, `UntilSuccess`, `SemaphoreGuard` (limits concurrent subtree access).

**Note:** The class is `SemaphoreGuard`, not `Semaphore`. Also available: `Wait<E>` (leaf — pauses for a duration) and `Include<E>` (decorator — includes an external subtree).

### Text Format (.tree files)

`BehaviorTreeParser` loads `.tree` files. Indentation defines hierarchy. Without `import`, task names must be fully-qualified. With `import com.mygame.ai.tasks.*`, unqualified names work.

```
import com.mygame.ai.tasks.*
selector
  sequence
    isEnemyVisible
    attack damage:20
  wander
```

Task attributes use `@TaskAttribute` annotation on fields. Set in .tree as `taskName attrName:value`.

```java
BehaviorTreeParser<Enemy> parser = new BehaviorTreeParser<>();
BehaviorTree<Enemy> tree = parser.parse(Gdx.files.internal("ai/enemy.tree"), enemy);
```

### Blackboard Pattern

`E` is your blackboard — all tasks access it via `getObject()`. Can be the entity itself (`BehaviorTree<Enemy>`) or a dedicated data object (`BehaviorTree<AIContext>`).

## Finite State Machines

### State Interface

`State<E>` has four methods: `enter(E)`, `update(E)`, `exit(E)`, `onMessage(E, Telegram)`. Idiomatic pattern: implement as an **enum** (`enum EnemyState implements State<Enemy>`).

### DefaultStateMachine vs StackStateMachine

`DefaultStateMachine<E, S>` — single active state, `changeState()` replaces it. `StackStateMachine<E, S>` — each `changeState()` pushes current state onto stack; `revertToPreviousState()` pops. Arbitrary depth — use for interruptible states (stun, cutscene, pause).

```java
DefaultStateMachine<Enemy, EnemyState> fsm = new DefaultStateMachine<>(entity, EnemyState.IDLE);
// or StackStateMachine<Enemy, EnemyState> fsm = new StackStateMachine<>(entity, EnemyState.IDLE);
```

**Update each frame:** `fsm.update();`

### MessageManager

Inter-entity communication with optional delay. Entities implement `Telegraph` with `handleMessage(Telegram)` (typically delegates to `fsm.handleMessage(telegram)`).

**Sending messages — Telegraph references, NOT integer IDs:**

```java
MessageManager dispatcher = MessageManager.getInstance();
dispatcher.dispatchMessage(sender, receiver, MSG_SPOTTED);         // immediate
dispatcher.dispatchMessage(sender, receiver, MSG_DAMAGE, 25f);     // with extra data
dispatcher.dispatchMessage(2.0f, sender, receiver, MSG_BACKUP);    // delayed 2s
dispatcher.addListener(receiver, MSG_SPOTTED);                     // register for type
```

**You MUST update each frame** for delayed messages: `GdxAI.getTimepiece().update(deltaTime);` then `MessageManager.getInstance().update();`

## Scheduling

`LoadBalancingScheduler` distributes AI updates across frames. Entities implement `Schedulable` (method `run(long nanoTimeToRun)`). Add via `scheduler.addWithAutomaticPhasing(entity, framesPerRun)`. Call `scheduler.run(nanoBudget)` each frame.

## Common Mistakes

1. **Forgetting to set a target on Arrive/Seek** — Set via constructor `new Arrive<>(steerable, targetLocation)` or via `.setTarget(location)`. Without a target, `calculateSteering()` throws `NullPointerException`.
2. **Claiming NavMesh is built-in** — gdx-ai has NO NavMesh classes. Build your own graph from a nav mesh.
3. **Confusing Sequence and Selector** — Sequence = AND (all must succeed). Selector = OR (first success wins).
4. **Using `Semaphore` instead of `SemaphoreGuard`** — The decorator class is `SemaphoreGuard`.
5. **Not calling `tree.step()` each frame** — Behavior trees don't update automatically.
6. **Dispatching messages with integer IDs** — `MessageManager.dispatchMessage()` takes `Telegraph` object references as sender/receiver, not integer IDs.
7. **Not updating GdxAI timepiece** — Call `GdxAI.getTimepiece().update(deltaTime)` each frame, or delayed messages and scheduling won't work.
8. **Mixing Vector2/Vector3 generics** — All steering types for one entity must use the same vector type consistently.
9. **Thinking BehaviorTree needs GL** — BT, FSM, pathfinding, and scheduling are all pure logic. They work in headless environments.
10. **Forgetting `copyTo()` in LeafTask** — Required for tree cloning. Minimal implementation: `return task;`
11. **Calling `calculateSteering()` without applying the result** — Behaviors only compute acceleration. You must integrate it into velocity and position yourself each frame.
12. **Reusing `DefaultGraphPath` without calling `clear()`** — Old path nodes accumulate alongside new ones. Always call `outPath.clear()` before a new `searchNodePath` call.
