---
name: unity-dots-ecs
category: architecture
description: Use when working in a Unity project that uses Entities (DOTS) or when a task needs thousands of simulated objects - when ECS is worth it, components/bakers/ISystem with IJobEntity and Burst, entity command buffers for structural changes, native memory rules, and testing systems in a test World.
tech_stack: Unity
source: wshobson/agents unity-ecs-patterns (MIT), adapted; Unity Entities 1.x docs cited
---
# Unity DOTS / ECS

## Overview

Unity's Entities package stores data in tightly packed chunks and runs Burst-compiled jobs over it in parallel. It scales to tens of thousands of entities where GameObjects choke — and it makes simple gameplay code more verbose. Use it where the scale needs it, follow the project's existing split between GameObjects and entities, and never introduce DOTS into a GameObject project on your own initiative.

**Core principle:** Components are plain data, systems are Burst-compiled `ISystem`s scheduling jobs, and structural changes go through an entity command buffer.

## When it is worth it

| Situation | Use |
|---|---|
| Thousands of similar units, projectiles, boids, crowd agents | ECS (or Jobs + Burst over native arrays first) |
| Heavy simulation with little per-object uniqueness | ECS |
| UI, menus, a handful of characters, bespoke scripted moments | GameObjects |
| Mixed game | Hybrid: entities for the swarm, GameObjects for the player, UI and cameras |

## The pieces

```csharp
// Data: unmanaged structs
public struct Speed : IComponentData { public float Value; }
public struct Target : IComponentData { public float3 Position; }

// Authoring + baking: designers edit a MonoBehaviour in a subscene; the baker turns it into components
public sealed class SpeedAuthoring : MonoBehaviour {
    public float value = 5f;
    sealed class Baker : Baker<SpeedAuthoring> {
        public override void Bake(SpeedAuthoring a) {
            var e = GetEntity(TransformUsageFlags.Dynamic);
            AddComponent(e, new Speed { Value = a.value });
        }
    }
}

// Behaviour: a Burst-compiled ISystem scheduling a parallel IJobEntity
[BurstCompile]
public partial struct SeekSystem : ISystem {
    [BurstCompile] public void OnCreate(ref SystemState state) => state.RequireForUpdate<Speed>();

    [BurstCompile] public void OnUpdate(ref SystemState state) {
        new SeekJob { Dt = SystemAPI.Time.DeltaTime }.ScheduleParallel();
    }
}

[BurstCompile]
partial struct SeekJob : IJobEntity {
    public float Dt;
    void Execute(ref LocalTransform transform, in Speed speed, in Target target) {
        var to = target.Position - transform.Position;
        var dist = math.length(to);
        if (dist > 0.01f) transform.Position += to / dist * math.min(speed.Value * Dt, dist);
    }
}
```

## Rules

- **`ISystem` with `[BurstCompile]`** over `SystemBase` for new systems; `SystemBase` only where managed objects are unavoidable.
- **Burst everything on the hot path:** no managed types (classes, strings, `List<T>`) in components or jobs that should be Burst-compiled; use `FixedString`, `NativeArray`, `DynamicBuffer`.
- **`in` for read-only, `ref` for written** components in `Execute` — it drives the dependency system and parallelism.
- **Structural changes** (create/destroy entities, add/remove components) are recorded in an entity command buffer, not done inside jobs:

```csharp
var ecb = SystemAPI.GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
                   .CreateCommandBuffer(state.WorldUnmanaged).AsParallelWriter();
new ExpireJob { Ecb = ecb, Now = (float)SystemAPI.Time.ElapsedTime }.ScheduleParallel();
// in the job: void Execute([ChunkIndexInQuery] int key, Entity e, in Lifetime l) { if (Now > l.EndsAt) Ecb.DestroyEntity(key, e); }
```

- **Frequent on/off states** use enableable components (`IEnableableComponent`) instead of add/remove, which moves the entity between chunks.
- **Archetype hygiene:** many tiny component combinations fragment chunks; check chunk utilisation in the Entities windows.
- **Native memory:** every `NativeArray`/`NativeList` is disposed — `Allocator.Temp` inside a frame, `TempJob` within four frames, `Persistent` in `OnDestroy`. Leak warnings are bugs.
- **Aspects** (`IAspect`) are deprecated in recent Entities releases — use explicit component parameters and queries instead of adding new ones.
- Physics (Unity Physics / Havok) runs in its own fixed-step group — gameplay that reacts to physics runs in or after that group, not in an arbitrary `Update` system.

## Testing systems

```csharp
public class SeekSystemTests {
    World _world; EntityManager _em;

    [SetUp] public void SetUp() { _world = new World("Test"); _em = _world.EntityManager; }
    [TearDown] public void TearDown() => _world.Dispose();

    [Test] public void Update_EntityWithSpeed_MovesTowardTarget() {
        var e = _em.CreateEntity(typeof(LocalTransform), typeof(Speed), typeof(Target));
        _em.SetComponentData(e, LocalTransform.FromPosition(float3.zero));
        _em.SetComponentData(e, new Speed { Value = 2f });
        _em.SetComponentData(e, new Target { Position = new float3(10, 0, 0) });
        var system = _world.CreateSystem<SeekSystem>();

        _world.SetTime(new TimeData(elapsedTime: 0.5, deltaTime: 0.5f));
        system.Update(_world.Unmanaged);
        _em.CompleteAllTrackedJobs();

        Assert.That(_em.GetComponentData<LocalTransform>(e).Position.x, Is.EqualTo(1f).Within(1e-4));
    }
}
```

- A fresh `World` per test, disposed in teardown; create only the systems under test.
- Complete jobs before asserting.
- Keep the math in static Burst-compatible functions so it can also be tested as a plain function.

## Netcode for Entities (if the project uses it)

Ghost components replicate state; prediction runs in the predicted simulation group; input travels as `IInputComponentData`. Server-authority rules from game-networking still apply — validate input on the server world.

## Common Mistakes

- Converting a small game to ECS for "performance" with no profiler evidence.
- Structural changes inside a job, or `EntityManager` calls in a hot loop on the main thread.
- Managed components in a system that is supposed to be Burst-compiled; Burst silently falls back or errors.
- Forgetting `RequireForUpdate`, so a system runs (and throws) before its data exists.

## Red Flags

- `SystemBase` + `Entities.ForEach` in new code (legacy API).
- Native containers without a matching `Dispose`.
- A system that reads and writes the same component from two jobs without dependencies.
