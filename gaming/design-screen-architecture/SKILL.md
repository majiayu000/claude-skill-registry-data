---
name: design-screen-architecture
description: "Use when generating screen/scene management architecture from screen flow definition and rendering target. Triggers: 'screen architecture', 'scene management', 'screen manager design', 'scene switching', 'screen state machine'."
---

## 1. Template Binding

- **Output**: `{TARGET_FOLDER}/docs/screen_architecture_spec.md`
- **Inputs**: `screen_flow.md`, `rendering_target.md` (REQUIRED — abort with error if either is missing)

## 2. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/screen_architecture_spec.md`. **Inputs**: `screen_flow.md`, `rendering_target.md`.

| Engine | Scene Management |
|--------|-----------------|
| Phaser 3 | Each screen = `Phaser.Scene`; parallel scenes for HUD/overlays |
| Three.js | Custom `SceneManager`; dispose/create pattern |
| Unity | Unity Scene or Canvas prefab; `LoadSceneAsync` |
| Godot | `PackedScene`; `change_scene_to_packed` |

Lifecycle hooks (all screens): onEnter / onExit / onPause / onResume. Transition types: cut, fade, slide, custom. Persistent layers: HUD (parallel), Modal (stacked), Toast (child of HUD). Asset policies: preload / lazy / shared.

## 3. Core Pattern

### 2.1 Input Analysis

Read `screen_flow.md` and `rendering_target.md` before generating any output.

- From `screen_flow.md`: extract screen list, transition map, persistent layer declarations, and guard conditions.
- From `rendering_target.md`: extract engine name and version.
- If either file is absent, output: `ERROR: Missing required input — [filename]. Aborting.` and stop.

### 2.2 Engine Scene Mapping

| Engine | Scene Management |
|--------|-----------------|
| **Phaser 3** | Each screen = `Phaser.Scene`. `SceneManager` handles transitions. Parallel scenes for HUD/overlays. |
| **Three.js** | Custom `SceneManager` class. Each screen = scene graph root. Dispose/create pattern for cleanup. |
| **Unity** | Each screen = Unity Scene or Canvas prefab. `SceneManager.LoadSceneAsync` for transitions. |
| **Godot** | Each screen = `PackedScene`. `SceneTree.change_scene_to_packed` for transitions. |

Select the row matching the engine in `rendering_target.md`. Use it as the structural basis for all scene declarations.

### 2.3 Screen State Machine

Derive the state machine directly from `screen_flow.md`:

- **States**: one state per named screen in the flow definition.
- **Transitions**: one transition per directed edge in the transition map.
- **Guards**: encode conditional transitions as guard predicates (e.g., "can only reach PAUSE from GAMEPLAY", "GAME_OVER only reachable when lives == 0").

Output format:

```
States: [MainMenu, Loading, Gameplay, Pause, GameOver, Credits]
Transitions:
  MainMenu -> Loading : onStartPressed
  Loading -> Gameplay : onAssetsReady
  Gameplay -> Pause : onPausePressed [guard: isGameActive]
  Pause -> Gameplay : onResumePressed
  Gameplay -> GameOver : onPlayerDead
  GameOver -> MainMenu : onReturnPressed
Guards:
  isGameActive: Gameplay state is current and no modal is open
```

### 2.4 Transition Effects

Define a transition type for every edge identified in 3.3.

| Type | Description | Engine Hook |
|------|-------------|-------------|
| **cut** | Immediate swap, no animation | Direct scene replace |
| **fade** | Alpha 1→0→1 across outgoing/incoming | Tween alpha or camera fade |
| **slide** | Outgoing slides out while incoming slides in | Translate transform tween |
| **custom** | Game-defined (e.g., portal wipe, iris) | Custom shader or mask |

Assign a type to each transition edge. If `screen_flow.md` specifies a preferred effect, use it. Otherwise default to `fade` for major screen changes and `cut` for sub-screen overlays.

### 2.5 Lifecycle Hooks

Declare four lifecycle hooks per screen:

| Hook | Purpose |
|------|---------|
| `onEnter` | Initialize screen state, start animations, subscribe to events |
| `onExit` | Dispose resources, unsubscribe events, cancel tweens |
| `onPause` | Freeze timers and input; called when an overlay covers this screen |
| `onResume` | Restore timers and input; called when the covering overlay closes |

`onExit` is mandatory and must explicitly release all resources allocated in `onEnter`. Absence of `onExit` is a red flag.

### 2.6 Persistent Layer Architecture

Some screens in `screen_flow.md` are declared as persistent layers (HUD, modal dialogs, notification toasts). Map each to a rendering layer strategy:

| Layer Type | Strategy |
|------------|---------|
| **HUD** | Parallel scene (Phaser) / overlay canvas (Unity) / top-level node (Godot) — always visible during gameplay |
| **Modal/Overlay** | Pushed onto scene stack; blocks input to layers below |
| **Toast/Notification** | Spawned as child of persistent HUD layer; auto-dismissed by timer |

Specify z-order or scene priority for each persistent layer.

### 2.7 Asset Loading Strategy

For each screen, produce an asset manifest and loading policy:

| Policy | When to Use |
|--------|------------|
| **Preload** | Assets needed immediately on `onEnter`; load during Loading screen |
| **Lazy** | Assets not needed on first frame; load on demand during gameplay |
| **Shared** | Assets shared across screens; load once and persist |

List asset keys per screen and tag each with its policy. Reference the engine's asset loader API from `rendering_target.md`.

### 2.8 Output Format

Write `{TARGET_FOLDER}/docs/screen_architecture_spec.md` with the following sections in order:

1. **Overview** — engine, screen count, persistent layer count
2. **Screen State Machine** — states, transitions, guards (from 3.3)
3. **Engine Scene Mapping** — class/node per screen, engine API used (from 3.2)
4. **Transition Effects Table** — edge → effect type (from 3.4)
5. **Lifecycle Hooks** — per-screen hook definitions (from 3.5)
6. **Persistent Layers** — layer list with z-order and strategy (from 3.6)
7. **Asset Manifests** — per-screen asset keys with load policy (from 3.7)

## 3. When to Use

Run this skill after `screen_flow.md` and `rendering_target.md` are finalized. It sits between user-layer flow design and builder skills (`implement-state-machine`, `implement-renderer`). Confirm rendering target first — the engine scene mapping depends on it.

## 4. Validation Checklist (MANDATORY)

- [ ] `screen_flow.md` present and parsed
- [ ] `rendering_target.md` present and engine identified
- [ ] Every screen in the flow has a corresponding state in the state machine
- [ ] Every transition edge has an assigned effect type
- [ ] Every screen declares all four lifecycle hooks (onEnter, onExit, onPause, onResume)
- [ ] Every `onEnter` has a matching `onExit` that releases its resources
- [ ] Persistent layers assigned z-order values with no conflicts
- [ ] Every asset tagged with a load policy (preload / lazy / shared)
- [ ] Output file written to `{TARGET_FOLDER}/docs/screen_architecture_spec.md`
- [ ] All content in English

## 5. Quality Gates

- **Required Input Present**: Read screen_flow.md and rendering_target.md before generating output
- **Screen Flow Fidelity**: Every screen in the flow definition appears in the architecture; no orphan screens added
- **Correct Engine API**: Transition effects reference APIs matching the engine in rendering_target.md
- **Complete Lifecycle Hooks**: Every screen that allocates resources in onEnter releases them in onExit
- **Layer Z-Order**: Assign z-order values to all persistent layers to prevent render order conflicts
- **Asset Load Policies**: Tag every asset with a load policy (preload / lazy / shared)

## 6. Execution Command

Command: `/design-screen-architecture`
