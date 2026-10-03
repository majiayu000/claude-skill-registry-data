---
name: godot
description: >
  Router for ShatterLess Godot 4 engine work. Pick the matching sub-skill(s)
  under references/godot-*/ and follow its SKILL.md. Covers procedural generation,
  multiplayer/rollback/headless servers, 3D physics & raycasting, inventory & data
  resources, enemy AI & state machines, shooters & combat, lighting/shaders/
  materials, checkpoints/revival/save-load, autoloads & signals, project layout &
  conventions, GDScript idioms & profiling, UI containers/theming/rich-text,
  audio, camera, particles, input, economy, abilities, secrets, collection &
  harvest loops, genre blueprints, testing, and exports. Obey the `tdd` skill
  over any pattern here. Trigger keywords: Godot, GDScript, GridMap, NavigationAgent,
  RigidBody3D, RayCast3D, MultiplayerSynchronizer, GPUParticles, StandardMaterial3D,
  DirectionalLight3D, Container, Theme, AudioStreamPlayer, FastNoiseLite, HSM,
  Hitbox, GdUnit4, export_preset.
---

# Godot skill router

Match the task to a row, then read `references/<sub-skill>/SKILL.md` (and its notes in `scripts/` / `references/`). 

| Task | Sub-skills |
|---|---|
| Procedural room layout / WFC / noise / BSP | `godot-procedural-generation`, `godot-3d-world-building` |
| Roguelike run structure, permadeath, meta-progression, relics | `godot-genre-roguelike` |
| Genre scaffold / bootstrap order / pause modes / PCK DLC / feature tags | `godot-project-templates` |
| Rollback / P2P / desync / headless / dedicated server | `godot-multiplayer-networking`, `godot-adapt-single-to-multiplayer`, `godot-server-architecture` |
| Rapier3D bodies, ragdolls, joints, physics queries | `godot-physics-3d`, `godot-raycasting-queries` |
| 4-slot inventory + item behaviours | `godot-inventory-system`, `godot-resource-data-patterns` |
| Enemies / entity behaviour / detection | `godot-state-machine-advanced`, `godot-navigation-pathfinding`, `godot-ai-navigation`, `godot-genre-horror`, `godot-genre-stealth` |
| Weapons / hip-fire / suppressor / hitscan / recoil | `godot-genre-shooter-fps`, `godot-genre-shooter`, `godot-combat-system` |
| Abilities, cooldowns, combos, skill trees | `godot-ability-system` |
| Flashlight, drone light, room lighting, GI, shadows | `godot-3d-lighting` |
| PSX/CRT look, hitflash, dissolve, post-process, foliage | `godot-shaders-basics` |
| PBR surfaces, ORM packing, transparency, material tuning | `godot-3d-materials` |
| Checkpoints / revive / downed / corpse-run / ghost | `godot-mechanic-revival` |
| Save / load / settings / versioned migration | `godot-save-load-systems` |
| Managers, autoloads (`NetworkTime`, `NetworkRollback`), init order | `godot-autoload-architecture` |
| Decoupling, event bus, typed signals, one-shot connections | `godot-signal-architecture` |
| Project layout, naming, `.gitignore`/`.gdignore` | `godot-project-foundations` |
| Entity-Component "Has-A" composition | `godot-composition` |
| Scene loading, transitions, async/background load, caching | `godot-scene-management` |
| GDScript idioms, static typing, `@onready`/`%Unique`, Callables, await | `godot-gdscript-mastery` |
| Frame drops, leaks, draw calls, object pooling, MultiMesh | `godot-performance-optimization` |
| Orphan nodes, Visual Profiler, headless CI QA, custom monitors | `godot-debugging-profiling` |
| HUD / inventory UI / responsive menus / virtual lists | `godot-ui-containers` |
| Consistent styling, StyleBoxes, fonts, dark mode | `godot-ui-theming` |
| Dialogue, BBCode, RichTextEffect | `godot-ui-rich-text` |
| Music, SFX, buses, spatial audio, crossfade, procedural audio | `godot-audio-systems` |
| Player/cinematic camera, follow, shake, deadzone, SpringArm | `godot-camera-systems` |
| Explosions, weather, trails, VFX feedback | `godot-particles` |
| InputMap, gamepad, rebinding, deadzones, input buffering | `godot-input-handling` |
| Currency, shops, dynamic pricing, loot tables, sinks | `godot-economy-system` |
| Cheat codes, hidden interactions, unlockable meta-content | `godot-mechanic-secrets` |
| Collectible IDs, scavenger hunts, completion archives, compass UI | `godot-game-loop-collection` |
| Mining / logging / foraging, tool tiers, respawn, offline progress | `godot-game-loop-harvest` |
| GdUnit4 test-layer choice, headless runners, snapshots, mock networks | `godot-testing-patterns` |
| Multi-platform exports, headless export, codesign, CI/CD, size trim | `godot-export-builds` |
