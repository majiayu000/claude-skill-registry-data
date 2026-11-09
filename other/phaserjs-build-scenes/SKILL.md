---
name: phaserjs-build-scenes
description: Build Phaser scene, loader, camera, scale and world lifecycles with explicit ownership of shared game resources.
engines: [PHASERJS]
---

# Build Phaser Scenes

## When to use

Create or refactor Phaser boot/preload/gameplay scenes, world loading or scene transitions.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh phaserjs-build-scenes`; require compatibility and honor task override scope. Read the host's locked Phaser major/revision, renderer, plugins, world contract and budgets. Respect Phaser 3 or 4 as selected: renderer internals differ. Do not use Phaser 2/CE recipes, upgrade implicitly, install packages or inject CDN scripts.

## Workflow

1. Own one `Phaser.Game` per intended runtime; centralize renderer, parent, scale, physics and plugin configuration. Avoid duplicate game instances during remount/hot reload. Permanent unmount destroys the owning game.
2. Separate boot, loading, gameplay and persistent services where their lifetimes differ. Use `init`, `preload`, `create`, `update` and Scene events deliberately. Shutdown permits restart; destroy ends scene ownership. Install restart-scoped listeners anew and release them on shutdown.
3. Use `LoaderPlugin`, cache and texture keys through an asset manifest. Define missing/failed asset behavior and transition cancellation. Game-level caches, animation definitions and sound resources can outlive scenes: remove them only when their final user leaves.
4. Configure Scale Manager and cameras with explicit logical size, viewport, safe areas and world bounds. Bound per-frame work after tab resume and separate gameplay state from display objects.
5. Convert validated map/spawn/content IDs into runtime instances. Keep navigation, enemy decisions and versioned saves in project systems; Phaser scene objects and the global registry are not automatically a persistence schema or AI framework.
6. Own timers, tweens, camera effects, event subscriptions and asynchronous completions. Late results must verify the scene activation token before mutation; stop scene-owned work without cancelling shared services.

## Output and verification

Deliver lifecycle/configuration changes, asset ownership and world adapters. Test boot failure, restart, scene replacement during loading, shared textures, resize/orientation, pause/sleep/wake and repeated teardown. Measure load/frame/memory budgets in the actual renderer. Structural tests cannot prove visual readiness. Check the [scene lifecycle](https://docs.phaser.io/phaser/concepts/scenes) and the [Phaser 3/4 migration boundaries](https://phaser.io/news/2026/05/phaser-3-vs-phaser-4).
