---
name: bevy-ecs-patterns
category: architecture
description: Use when writing Bevy (Rust ECS) game code - pin and respect the repo's minor version, plugins/systems/queries/resources, schedules with FixedUpdate and Time, states and run conditions, messages vs observers across versions, required components, testing systems with App::update and a manual time strategy, compile-time and allocation hygiene.
tech_stack: Bevy
source: informed by the Bevy documentation, examples and per-release migration guides; own wording
---
# Bevy ECS Patterns

## Overview

Bevy is a code-first Rust engine built on an ECS: entities are IDs, components are plain structs, systems are ordinary functions whose parameters declare the data they touch, and the scheduler runs them in parallel where it can. Bevy also ships a breaking release every few months — the API you remember may not be the API the repository pins.

**Core principle:** The repository's pinned Bevy minor is the API. Systems are small functions over queries, simulation runs in `FixedUpdate`, and every system is testable by building an `App` and calling `update()`.

## Version first

```toml
# Cargo.toml — for 0.x crates "0.18" already means >=0.18.0, <0.19.0: the minor is pinned
bevy = "0.18"
```

Read `Cargo.lock` for the resolved version and that version's migration guide before writing code. Never bump the minor in a feature task. Changes that bite code written from memory:

| Since | Change |
|---|---|
| 0.15 | `Time::delta_seconds()` → `delta_secs()`; required components (`#[require(...)]`) replace most bundles; `Single<...>` system parameter |
| 0.16 | `Query::single()` / `get_single()` return `Result`; systems may return `Result` and use `?` |
| 0.17 | Buffered events renamed to **messages**: `#[derive(Message)]`, `MessageWriter::write`, `MessageReader::read`, `app.add_message::<T>()`; observers use `On<T>` for entity events |

## Plugins, components, systems

```rust
use bevy::prelude::*;

#[derive(Component, Default)]
#[require(Transform, Velocity)]
pub struct Player;

#[derive(Component, Default, Deref, DerefMut)]
pub struct Velocity(pub Vec2);

#[derive(Resource)]
pub struct MoveTuning { pub speed: f32 }

#[derive(Message)]
pub struct PlayerHit { pub damage: u32 }

pub struct MovementPlugin;

impl Plugin for MovementPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(MoveTuning { speed: 220.0 })
            .insert_resource(Time::<Fixed>::from_hz(60.0))
            .add_message::<PlayerHit>()
            .add_systems(Update, read_input.run_if(in_state(GameState::Playing)))
            .add_systems(FixedUpdate, (apply_velocity, resolve_hits).chain());
    }
}

fn read_input(keys: Res<ButtonInput<KeyCode>>, tuning: Res<MoveTuning>, mut player: Single<&mut Velocity, With<Player>>) {
    let x = keys.pressed(KeyCode::KeyD) as i8 as f32 - keys.pressed(KeyCode::KeyA) as i8 as f32;
    player.0 = Vec2::new(x * tuning.speed, player.0.y);
}

fn apply_velocity(time: Res<Time>, mut q: Query<(&mut Transform, &Velocity)>) {
    for (mut t, v) in &mut q {
        t.translation += (v.0 * time.delta_secs()).extend(0.0);   // in FixedUpdate, Time is the fixed clock
    }
}
```

- One plugin per feature; `main.rs` only adds plugins.
- Systems are small and named for what they do; order with `.chain()`, `.before()/.after()` or `SystemSet`s, not by hoping.
- Read input in `Update`, simulate in `FixedUpdate` (default 64 Hz; set it explicitly), render-side smoothing in `Update`/`PostUpdate` (game-loop-and-time).
- `Commands` are deferred: an entity spawned in a system is visible to queries only after the command flush (the next sync point), not later in the same system.
- Use change detection (`Changed<T>`, `Added<T>`, `Ref<T>::is_changed`) instead of recomputing every frame; filter queries (`With`, `Without`) so systems touch only what they need.
- `Res<T>` reads run in parallel; `ResMut<T>` serialises every system that touches `T` — keep shared mutable resources few.
- Tuning values in resources or assets loaded from RON/JSON (data-driven-gameplay-design), not literals in systems.

## States and conditions

```rust
#[derive(States, Default, Debug, Clone, PartialEq, Eq, Hash)]
pub enum GameState { #[default] Loading, Menu, Playing, Paused }

app.init_state::<GameState>()
   .add_systems(OnEnter(GameState::Playing), spawn_level)
   .add_systems(OnExit(GameState::Playing), despawn_level);
```

Entities spawned for a state are cleaned up on exit (a marker component plus a despawn system, or the state-scoped entity helpers of the pinned version).

## Testing systems

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use bevy::time::TimeUpdateStrategy;
    use std::time::Duration;

    fn app() -> App {
        let mut app = App::new();
        app.add_plugins(MinimalPlugins)
            .insert_resource(TimeUpdateStrategy::ManualDuration(Duration::from_secs_f64(1.0 / 60.0)))
            .insert_resource(Time::<Fixed>::from_hz(60.0))
            .add_systems(FixedUpdate, apply_velocity);
        app.update();                     // the first update has zero delta; prime the clock
        app
    }

    #[test]
    fn moves_by_speed_times_elapsed_time() {
        let mut app = app();
        let e = app.world_mut().spawn((Transform::default(), Velocity(Vec2::new(60.0, 0.0)))).id();
        for _ in 0..60 { app.update(); }
        let x = app.world().get::<Transform>(e).unwrap().translation.x;
        assert!((x - 60.0).abs() < 1.5, "x = {x}");
    }
}
```

- `MinimalPlugins` gives time and the schedule runner without a window or GPU — runs anywhere `cargo test` runs.
- Control time with `TimeUpdateStrategy::ManualDuration`; never sleep.
- Send messages in a test through the world (`write_message` on the pinned version, `send_event` before 0.17) and read results back with queries or a resource.
- `world.run_system_once(my_system)` for a one-off system call in a test.
- Pure math (damage, steering) as plain functions with ordinary unit tests.

## Build hygiene

- `cargo test && cargo clippy -- -D warnings` before hand-off (rule game-build-check); Bevy projects commonly allow `clippy::too_many_arguments` and `clippy::type_complexity` — follow the repository's lint config.
- Fast iteration: `opt-level = 1` for the crate and `opt-level = 3` for dependencies in `[profile.dev]`/`[profile.dev.package."*"]`; the `dynamic_linking` feature only in dev, never in release builds.
- First compile takes minutes: give `run_terminal` a long timeout or run it detached to a log.
- Allocation in hot systems: reuse buffers with `Local<Vec<T>>` instead of collecting into a new `Vec` every frame.
- Headless runs: `MinimalPlugins` + `ScheduleRunnerPlugin`, or `DefaultPlugins` with no primary window; screenshots need a GPU and a window (game-visual-self-review).

## Common Mistakes

- Code from an older or newer Bevy version (`delta_seconds`, `EventWriter`, `get_single`) that does not compile on the pinned one.
- Movement in `Update` with `Time` and physics in `Update` — frame-rate dependent.
- Expecting a just-spawned entity in the same system's query.
- One giant system per feature with `ResMut` on everything, killing parallelism.
- Bumping Bevy "while here".

## Red Flags

- `bevy = "*"`, a `>=` range, or a version change in `Cargo.toml` the task did not ask for.
- `std::thread::sleep` or `Instant::now()` inside systems or tests.
- A system test that opens a window.
