---
name: flecs-dylib-modules
description: Hot-reloadable Flecs modules as Rust dylibs. Covers module architecture, component vs system modules, and inter-module dependencies.
---

# Flecs Dylib Modules

Hot-reloadable Flecs modules as Rust dylibs.

## When to Use

Use this skill when you need to:
- Create a new hot-reloadable module
- Understand how modules depend on each other
- Debug singleton/component registration issues

## Idiomatic Flecs: Separate Components from Systems

In Flecs, it's idiomatic to separate:
- **Component modules** - define components/singletons only, no systems
- **System modules** - import component modules, define systems that use them

This separation enables:
- Hot-reload systems without breaking component data
- Multiple system modules sharing the same components
- Cleaner dependency graphs

### Example Structure

```
crates/module/
├── time-components/     # WorldTime, TpsTracker (components only)
├── time-systems/        # Systems that tick WorldTime (imports time-components)
├── network-components/  # Connection, PacketBuffer, etc.
├── network-systems/     # Ingress/egress systems
└── play/                # Game systems (imports time-components, network-components)
```

## Component Module Pattern

```rust
// crates/module/time-components/src/lib.rs
use flecs_ecs::prelude::*;

#[derive(Component, Debug)]
pub struct WorldTime {
    pub world_age: i64,
    pub time_of_day: i64,
}

#[derive(Component)]
pub struct TimeComponentsModule;

impl Module for TimeComponentsModule {
    fn module(world: &World) {
        world.module::<TimeComponentsModule>("time::components");

        // Register component and singleton
        world.component::<WorldTime>().add_trait::<flecs::Singleton>();
        world.set(WorldTime::default());

        // NO SYSTEMS HERE - just components
    }
}
```

## System Module Pattern

```rust
// crates/module/time-systems/src/lib.rs
use flecs_ecs::prelude::*;
use module_time_components::{TimeComponentsModule, WorldTime};

#[derive(Component)]
pub struct TimeSystemsModule;

impl Module for TimeSystemsModule {
    fn module(world: &World) {
        world.module::<TimeSystemsModule>("time::systems");

        // Import component module (ensures components exist)
        world.import::<TimeComponentsModule>();

        // Define systems
        world.system_named::<&mut WorldTime>("TickWorldTime")
            .each(|time| {
                time.world_age += 1;
                time.time_of_day = (time.time_of_day + 1) % 24000;
            });
    }
}
```

## Module Dependencies via Cargo

System modules depend on component modules via Cargo:

```toml
# crates/module/time-systems/Cargo.toml
[lib]
crate-type = ["dylib"]

[dependencies]
flecs_ecs.workspace = true
module-time-components = { path = "../time-components" }
```

## Module Interface (Rust ABI)

Each module dylib exports:

```rust
#[unsafe(no_mangle)]
pub fn module_load(world: &World) {
    world.import::<MyModule>();
}

#[unsafe(no_mangle)]
pub fn module_unload(world: &World) {
    if let Some(e) = world.try_lookup("::my_module") {
        e.destruct();
    }
}

#[unsafe(no_mangle)]
pub fn module_name() -> &'static str { "my_module" }

#[unsafe(no_mangle)]
pub fn module_version() -> u32 { 1 }
```

## Critical: Singleton Setup

```rust
// WRONG - just registers component
world.component::<WorldTime>();

// RIGHT - register as singleton AND set value
world.component::<WorldTime>().add_trait::<flecs::Singleton>();
world.set(WorldTime::default());
```

## Critical: world.import() for Dependencies

`world.import::<Module>()` is idempotent - safe to call multiple times:

```rust
impl Module for PlayModule {
    fn module(world: &World) {
        world.import::<TimeComponentsModule>();  // Ensures components exist
        world.import::<NetworkComponentsModule>();
        // Now safe to query WorldTime, PacketBuffer, etc.
    }
}
```

## Shared Libraries Required

All modules must link to the SAME shared flecs libraries:
- `libflecs.dylib` (C library)
- `libflecs_ecs.dylib` (Rust wrapper)

## Development Workflow

Symlink dylibs to modules/ directory:

```bash
ln -s target/debug/libmodule_time_components.dylib modules/
ln -s target/debug/libmodule_time_systems.dylib modules/
```

Rebuild updates dylib, file watcher triggers hot-reload.

## Hot-Reload Benefits

With component/system separation:
- Reload `time-systems` → systems restart with existing component data
- Reload `time-components` → resets singletons (use sparingly)
- Add new system module → extends functionality without touching existing modules
