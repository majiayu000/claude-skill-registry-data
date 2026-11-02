---
name: manage-bevy-assets
description: Use when a Bevy game loads sprites, audio, levels or custom data — a loading state with handles, one asset-table seam, custom loaders, hot reload in dev, optional processing, and embedded assets so web and single-file builds work.
---

# Manage Bevy Assets

Bevy 0.20 native asset API. Rationale: [asset-patterns.md](asset-patterns.md). Versions and the `bevy_asset_loader` status: [stack-versions](../_shared/stack-versions.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null                  # does the target include web?
ls assets assets/* 2>/dev/null | head -30; ls src/assets.rs 2>/dev/null
grep -rnE 'asset_server\.load|AssetServer' src/ | grep -v "src/assets.rs"       # loads outside the seam
grep -nE 'file_watcher|embedded_watcher|asset_processor|AssetMetaCheck|AssetMode' Cargo.toml src/ -r
grep -rnE 'Screen::Loading|LoadState|is_loaded_with_dependencies|recursive_dependency_load_state' src/
grep -n "bevy_asset_loader\|bevy_common_assets" Cargo.toml
```

## 2. Decide what to do
- No loading state and loads scattered across plugins → build the seam and the loading state (steps 5–6).
- Seam exists → add only what is missing (custom loader, hot reload, web meta check).
- Seam, loading gate, `dev` hot reload all present → "already in place", stop.
- `bevy_asset_loader` already in `Cargo.toml` → check its `bevy` requirement against the project's Bevy line; keep it only if it matches.

## 3. Detect track
- **Desktop** → files on disk in `assets/`; hot reload via the `dev` feature.
- **Web** → no filesystem: set `AssetMetaCheck::Never`, never use `AssetMode::Processed`, embed what the first frame needs.
- **Single-file release** → `embedded_asset!` for the few assets that must ship inside the binary; everything else stays in `assets/`.
- **Custom data (levels, config, tables)** → a custom `AssetLoader` (step 5). Use `bevy_common_assets` only if its stable release targets your Bevy line.

## 4. Install only what's missing
Nothing by default. Native loading covers handles, folders, custom loaders and hot reload.
`bevy_asset_loader` and `bevy_common_assets`: on 2026-10-09 only release candidates targeted Bevy 0.20 ([stack-versions](../_shared/stack-versions.md)). Re-check crates.io; do not add a release candidate to a production project.

## 5. Generate the seams

**Asset table (`src/assets.rs`)** — the only module that calls `asset_server.load`. Strong handles keep assets alive.

```rust
#[derive(Resource)]
pub struct GameAssets {
    pub player: Handle<Image>,
    pub jump: Handle<AudioSource>,
}

pub struct AssetsPlugin;

impl Plugin for AssetsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(Screen::Loading), start_loading).add_systems(
            Update,
            finish_loading
                .run_if(in_state(Screen::Loading))
                .run_if(resource_exists::<GameAssets>),
        );
    }
}

fn start_loading(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.insert_resource(GameAssets {
        player: asset_server.load("sprites/player.png"),
        jump: asset_server.load("audio/jump.ogg"),
    });
}

fn finish_loading(
    assets: Res<GameAssets>,
    asset_server: Res<AssetServer>,
    mut next: ResMut<NextState<Screen>>,
) {
    let ids = [assets.player.id().untyped(), assets.jump.id().untyped()];
    let mut all_loaded = true;
    for id in ids {
        match asset_server.recursive_dependency_load_state(id) {
            RecursiveDependencyLoadState::Loaded => {}
            RecursiveDependencyLoadState::Failed(error) => panic!("asset failed to load: {error}"),
            _ => all_loaded = false,
        }
    }
    if all_loaded {
        next.set(Screen::Menu);
    }
}
```
(`use bevy::asset::RecursiveDependencyLoadState;`.) A failed load stops the game with the file in the message: a broken path never becomes a silent invisible sprite.

**Custom asset and loader** — template in [asset-patterns.md](asset-patterns.md#rule-custom-data-is-an-asset-with-a-loader): `#[derive(Asset, TypePath)]`, `impl AssetLoader`, `init_asset::<T>().init_asset_loader::<L>()`.

**Load settings** (pixel art, per asset): `asset_server.load_builder().with_settings(|s: &mut ImageLoaderSettings| { s.sampler = ImageSampler::nearest(); }).load("sprites/player.png")`. Global default: `DefaultPlugins.set(ImagePlugin::default_nearest())`.

## 6. Wire it
- `AssetsPlugin` into `GamePlugin`; `Screen::Loading` is the default state ([structure-bevy-app](../structure-bevy-app/SKILL.md)).
- Other plugins take `Res<GameAssets>`; none calls `asset_server.load` directly.
- Hot reload: `dev = ["bevy/dev", ...]` already enables `file_watcher`. Add `bevy/embedded_watcher` for embedded assets. Run `cargo run --features dev`; edit a file in `assets/`.
- Web: `DefaultPlugins.set(AssetPlugin { meta_check: AssetMetaCheck::Never, ..default() })` (`use bevy::asset::AssetMetaCheck;`).
- Embedded: in the plugin `embedded_asset!(app, "src/", "splash.png");` then load `"embedded://<crate_name>/splash.png"`.
- Reacting to reloads: read `MessageReader<AssetEvent<T>>`; `Modified` fires only on real mutation since 0.19.

## 7. Verify

```bash
cargo clippy --all-targets -- -D warnings && cargo nextest run
cargo run --features dev    # starts in Loading, reaches Menu; touching assets/<file> logs/shows a reload
grep -rn "asset_server.load" src/ | grep -v "src/assets.rs"; echo "exit $?"
```

Expected: tests pass; the game leaves `Loading`; the grep prints nothing and `exit 1`. A headless loader test ([test-bevy-systems](../test-bevy-systems/SKILL.md)) loads a fixture file and asserts its content. Rename an asset file: the game must stop with `asset failed to load`.

Contracts: [engineering principles](../../core/_shared/engineering-principles.md) (fail fast, one seam), [security baseline](../../core/_shared/security-baseline.md) (no secrets in `assets/`; it ships to players).
