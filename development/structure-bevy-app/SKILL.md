---
name: structure-bevy-app
description: Use when adding a feature to a Bevy game or untangling one — plugin-per-feature layout, app states with DespawnOnExit, system sets and ordering, messages vs observers, change detection, query conflicts, and where game logic ends and rendering begins.
---

# Structure Bevy App

Bevy 0.20 APIs. Rationale and anti-examples: [architecture-patterns.md](architecture-patterns.md). Versions: [stack-versions](../_shared/stack-versions.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null                       # rust lint/test layout
ls src/ src/*/ 2>/dev/null; wc -l src/main.rs src/lib.rs 2>/dev/null
grep -rnE "EventReader|EventWriter|add_event::|StateScoped|Trigger<|On<Add,|\.set_if_neq|send_event" src/   # pre-0.17/0.20 names
grep -rnE "add_systems\(" src/ | grep -v "impl Plugin" | head    # systems registered outside a plugin
grep -rnE "derive\(.*Resource.*Component|derive\(.*Component.*Resource" src/   # both on one type: compile error since 0.19
grep -rn "States" src/ | head; grep -rnE "\.single\(\)\.unwrap|query\.single\(\)" src/
cargo clippy --all-targets -- -D warnings 2>&1 | tail -5
```

If `.claude/stack-profile.md` says `tests.layout: colocated`, put unit tests next to the plugin and keep integration tests in `tests/` anyway (Cargo requires it).

## 2. Decide what to do
- New game, empty `src/` → create `core.rs` (states, sets) + the first feature plugin.
- Existing code → fix the highest-value finding only: logic in `main.rs`, systems outside plugins, old API names, missing state scoping. One concern per change.
- Plugins, sets, and state cleanup already in place → "already in place", stop.

## 3. Detect track
- **2D or 3D, UI-heavy or world-heavy:** same structure; only the presentation plugin differs.
- **Simulation that needs determinism** (physics, lockstep netcode): put it in `FixedUpdate`; see the rule in the patterns file.
- **Old Bevy names found:** use the migration table in the patterns file; do not mix old and new in one change.

## 4. Install only what's missing
Nothing to install. Third-party crates only when the audit shows a need (physics, input mapping). Check each one's `bevy` requirement first ([stack-versions](../_shared/stack-versions.md)).

## 5. Generate the seams

```
src/lib.rs          GamePlugin: the only list of plugins
src/core.rs         Screen state, GameSystems sets, shared configure_sets
src/<feature>.rs    one Plugin: its components, messages, observers, systems, OnEnter/OnExit
src/<feature>/      only when a feature outgrows one file: mod.rs (the plugin) + components.rs + systems.rs
```

Canonical plugin:

```rust
pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_message::<Damage>()
            .add_observer(on_died)
            .add_systems(OnEnter(Screen::Playing), spawn_player)
            .add_systems(
                Update,
                (
                    apply_velocity.in_set(GameSystems::Movement),
                    apply_damage.in_set(GameSystems::Combat),
                ),
            );
    }
}
```

Canonical state + sets (in `core.rs`):

```rust
#[derive(States, Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
pub enum Screen { #[default] Loading, Menu, Playing }

#[derive(SystemSet, Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum GameSystems { Input, Movement, Combat, Cleanup }

app.init_state::<Screen>().configure_sets(
    Update,
    (GameSystems::Input, GameSystems::Movement, GameSystems::Combat, GameSystems::Cleanup)
        .chain()
        .run_if(in_state(Screen::Playing)),
);
```

State-scoped spawn: `commands.spawn((Player, DespawnOnExit(Screen::Playing)));` — no manual cleanup system.

## 6. Wire it
- Add the plugin to `GamePlugin` in `lib.rs`; add `.add_message::<M>()` for each `#[derive(Message)]` type.
- Spawn everything that belongs to one screen with `DespawnOnExit(<state>)`; use `DespawnOnEnter` to clear leftovers on the way in.
- Order systems with the shared sets, never with ad hoc `.before()/.after()` across plugins.
- Fallible systems return `Result` and use `?` (`query.single()?`); `Single<..>` for "exactly one, else skip".

## 7. Verify

```bash
cargo clippy --all-targets -- -D warnings && cargo nextest run
grep -rnE "EventReader|EventWriter|StateScoped|On<Add," src/ ; echo "exit $?"
```

Expected: clippy and tests pass; the grep prints nothing and `exit 1` (no old names). Every feature has a headless test ([test-bevy-systems](../test-bevy-systems/SKILL.md)).

Next: [manage-bevy-assets](../manage-bevy-assets/SKILL.md), [optimize-bevy-game](../optimize-bevy-game/SKILL.md). Contracts: [engineering principles](../../core/_shared/engineering-principles.md).

## Findability

| I need to find... | It lives in |
|---|---|
| The list of everything the game runs | `src/lib.rs` (`GamePlugin`) |
| Game states and their transitions | `src/core.rs` |
| System ordering inside `Update` | `GameSystems` in `src/core.rs` |
| A feature's components and systems | `src/<feature>.rs` (or `src/<feature>/`) |
| What happens when a screen starts or ends | `OnEnter`/`OnExit` calls in the owning plugin; cleanup is `DespawnOnExit` at the spawn site |
| Cross-feature communication | `Message` types in the plugin that *produces* them; observers for one-off reactions |
| Sprites, meshes, animation for a gameplay entity | the presentation plugin (`src/view.rs` or `src/<feature>/view.rs`), never the logic plugin |
| Asset handles | `src/assets.rs` ([manage-bevy-assets](../manage-bevy-assets/SKILL.md)) |
| Tests for a feature | `tests/<feature>.rs` |
