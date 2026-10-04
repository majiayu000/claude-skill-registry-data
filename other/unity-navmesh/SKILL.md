---
name: unity-navmesh
description: >
  Add AI navigation in Unity 6.3 LTS: bake a NavMesh with the AI Navigation package (NavMeshSurface),
  move agents with NavMeshAgent.SetDestination, and handle dynamic obstacles. Use when setting
  up pathfinding, making an enemy chase the player, baking navigation, or when the user
  mentions NavMesh, NavMeshAgent, NavMeshSurface, NavMeshObstacle, or Unity pathfinding.
---

# Unity NavMesh (AI Navigation)

Give NPCs pathfinding in Unity 6.3 LTS: bake walkable surfaces and move agents around obstacles.
Targets **Unity 6.3 LTS (6000.3)** with the **AI Navigation package 2.x**.

> **Version trap (Unity 2022+/6):** the old built-in **Navigation window** (Object/Bake tabs)
> is gone. Baking is now **component-based** via the **AI Navigation package**
> (`com.unity.ai.navigation`): add a **NavMeshSurface** to your level geometry and click
> **Bake**. The *runtime* `NavMeshAgent`/`NavMesh` API stays in built-in `UnityEngine.AI`.

## When to use

- Use when an agent needs to walk/chase/patrol to a target, when baking a navigable surface,
  adding dynamic blockers (`NavMeshObstacle`), or checking whether a destination is reachable.
- Use when the project has the AI Navigation package, a `NavMeshSurface` component, or scripts
  using `UnityEngine.AI.NavMeshAgent`.

**When *not* to use:** the *decision* logic of when/where to move (FSMs, behaviour trees,
steering) → `game-ai` (this skill is the Unity movement/pathing mechanism). Force-driven or
kinematic movement that isn't pathfinding → `unity-physics`.

## Core workflow

1. **Install the AI Navigation package** (Package Manager → `com.unity.ai.navigation`).
2. **Bake a surface:** select the static level geometry, **Add Component → Navigation → NavMesh
   Surface**, set the agent type/area settings, and click **Bake**. Re-bake whenever geometry,
   `NavMeshModifier`s, or agent settings change.
3. **Add a `NavMeshAgent`** to each moving NPC; its radius/height/speed must match the baked
   agent type, and it must spawn *on* the baked mesh.
4. **Drive it from script** with `SetDestination(targetPos)`; the agent steers and avoids other
   agents automatically. Detect arrival with `remainingDistance`/`pathPending`.
5. **Handle dynamic blockers** with `NavMeshObstacle` (carving) so closed doors/crates block
   paths without a full re-bake.
6. **Verify** with the AI Navigation overlay (the baked mesh is drawn in the Scene view) and by
   watching agents path around obstacles to the goal; check `NavMeshPath.status` for
   unreachable targets.

## Patterns

### 1. Chase/seek with a NavMeshAgent

```csharp
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Chaser : MonoBehaviour
{
    [SerializeField] private Transform target;
    private NavMeshAgent _agent;

    private void Awake() => _agent = GetComponent<NavMeshAgent>();

    private void Update()
    {
        if (target) _agent.SetDestination(target.position);   // re-path toward the target
    }

    // Arrived? pathPending guards the first frame before a path exists.
    private bool HasArrived() =>
        !_agent.pathPending && _agent.remainingDistance <= _agent.stoppingDistance;
}
```

### 2. Check reachability before committing

```csharp
using UnityEngine.AI;

public bool CanReach(NavMeshAgent agent, Vector3 destination)
{
    var path = new NavMeshPath();
    agent.CalculatePath(destination, path);
    return path.status == NavMeshPathStatus.PathComplete;   // vs Partial / Invalid
}
```

### 3. Bake at runtime (for procedurally built or streamed levels)

```csharp
using Unity.AI.Navigation;   // the package namespace (NavMeshSurface)

[SerializeField] private NavMeshSurface surface;

// After spawning level geometry, build the navmesh in code.
public void RebuildNav() => surface.BuildNavMesh();
```

### 4. Dynamic obstacle that carves the mesh

```csharp
// Add a NavMeshObstacle (Carve = true) to a door/crate. While present it cuts a hole in the
// navmesh so agents route around it; remove/disable it to reopen the path — no re-bake needed.
```

### 5. Connect separate mesh pieces with a NavMeshLink (jumps, doors, gaps)

```csharp
// Two baked surfaces that don't touch (a ledge and the floor below, two platforms across a
// gap) are separate islands — an agent can't path between them. Add Component > Navigation >
// NavMesh Link to bridge them: assign Start/End Transforms, set Width (0 = point-to-point),
// and toggle Bidirectional for one-way vs two-way. NavMeshLink lives in Unity.AI.Navigation.
// It replaces the deprecated built-in OffMeshLink (see pitfalls).
```

## Pitfalls

- **Looking for the Navigation window** — it no longer exists in Unity 6. Use the AI Navigation
  package's `NavMeshSurface` component + Bake.
- **Agent doesn't move / warps to origin** — it isn't on the baked mesh, or no surface was
  baked. Bake the surface and spawn the agent on it (`NavMesh.SamplePosition` to snap).
- **Agent ignores new geometry** — the navmesh is baked; runtime-spawned obstacles need a
  `NavMeshObstacle` (carving) or a `surface.BuildNavMesh()` re-bake.
- **`SetDestination` every frame is wasteful** — for a slow-moving target, re-path on a timer
  (e.g. every 0.2s) instead of each frame.
- **Agent radius/height mismatch** — if the `NavMeshAgent`'s size differs from the baked agent
  type, it gets stuck in gaps or floats; keep them consistent.
- **Agents jitter against each other** — tune `avoidancePriority` and quality, or use an
  obstacle for truly static blockers rather than relying on agent avoidance.
- **Reaching for `OffMeshLink`** — the built-in `OffMeshLink` component is **deprecated** in
  AI Navigation 2.0 and can no longer be added from the Add Component menu. Use a
  **`NavMeshLink`** (from the package, `Unity.AI.Navigation`) instead — it adds Transform-based
  endpoints and a runtime `activated` property. Migrate any existing `OffMeshLink`s.
- **`CalculatePath` returns `PathPartial`** — the destination sits on a *different* baked
  island than the agent (a gap the mesh doesn't cross). Bridge the two with a `NavMeshLink`
  (pattern 5) or extend the geometry so one surface covers both; a partial path only reaches
  the near edge.

## References

- Primary docs: AI Navigation package manual
  (`https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/index.html`),
  the `NavMeshLink` page
  (`https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/NavMeshLink.html`)
  and its "What's new" note on the `OffMeshLink` deprecation
  (`https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/whats-new.html`), plus
  `ScriptReference/AI.NavMeshAgent`, `ScriptReference/AI.NavMesh`.

## Related skills

- `game-ai` — engine-agnostic decision-making (FSM, behaviour trees, steering) that *uses* this.
- `unity-csharp-scripting` — the MonoBehaviour structure around the agent.
- `tower-defense` / `fps-shooter` — genres that compose pathfinding with gameplay.
