---
name: implement-screen-manager
description: "Use when generating screen/scene manager code from screen architecture spec. Supports Phaser 3 (2D) and Three.js (3D). Triggers: 'implement screen manager', 'generate scene code', 'screen switching code', 'scene transitions', 'implement screens'."
---

## 1. Overview

Reads `screen_architecture_spec.md` + `rendering_target.md`, then generates engine-specific screen manager code in `{TARGET_FOLDER}/src/screens/`.

## 2. Quick Reference

| Engine | Manager Pattern | Key Files |
|--------|-----------------|-----------|
| Phaser 3 (2D) | Wraps Phaser.SceneManager; start/launch/stop scenes | screen_manager.ts, screens.ts, base_screen.ts, transitions.ts, persistent_layers.ts |
| Three.js (3D) | Custom ScreenManager with push/pop/replace; dispose lifecycle | screen_manager.ts, screens.ts, base_screen.ts, transitions.ts, persistent_layers.ts |
| Other | Placeholder with TODO comment | screen_manager.ts stubs |

BaseScreen hooks: onEnter / onExit / onPause / onResume. Always dispose on exit.

## 3. Core Pattern

Read `screen_architecture_spec.md` + `rendering_target.md` (REQUIRED). Detect language (TS/JS).

### 2.3 Screen Manager Code Generation

**Phaser 3 (2D)** — in `{TARGET_FOLDER}/src/screens/`:

| File | Content |
|------|---------|
| `screen_manager.ts` | Wraps Phaser.SceneManager, handles transitions, lifecycle hooks |
| `screens.ts` | Screen enum/registry mapping screen IDs to Phaser Scene keys |
| `base_screen.ts` | Abstract base class extending Phaser.Scene with onEnter/onExit/onPause/onResume |
| `transitions.ts` | Transition effects (fade, slide, cut) using Phaser cameras/tweens |
| `persistent_layers.ts` | HUD/overlay scenes running in parallel |
| `index.ts` | Barrel export |

Key patterns: `this.scene.start(key)`, `this.scene.launch(key)` for parallel, `this.scene.stop(key)`

**Three.js (3D)** — in `{TARGET_FOLDER}/src/screens/`:

| File | Content |
|------|---------|
| `screen_manager.ts` | Custom ScreenManager class with push/pop/replace, dispose lifecycle |
| `screens.ts` | Screen enum/registry |
| `base_screen.ts` | Abstract BaseScreen with scene graph root, onEnter/onExit/onPause/onResume, dispose() |
| `transitions.ts` | Transition effects using GSAP/tween or custom shader transitions |
| `persistent_layers.ts` | Overlay management (separate render pass or HTML overlay) |
| `index.ts` | Barrel export |

Key patterns: dispose old scene graph, create new scene graph, transition animation between

**Non-Supported Engine** — Generate a placeholder `screen_manager.ts` with a `TODO: implement for <engine>` comment and export stubs so downstream code compiles.

### 2.4 State Machine Integration

Wire the screen state machine from spec. Add guards for invalid transitions so switching to an unreachable screen throws a descriptive error at runtime.

### 2.5 Asset Loading

Implement per-screen preload hooks. Wire a loading screen that displays while assets load, then transitions to the target screen on completion.

### 2.6 Game Loop Integration

Initialize ScreenManager during bootstrap before the first frame. Call the active screen's `update(delta)` each frame from the main game loop.

## 3. Output File Structure

```
src/screens/
├── screen_manager.ts      # Core manager with transition logic
├── screens.ts             # Screen ID enum + registry
├── base_screen.ts         # Abstract base with lifecycle hooks
├── transitions.ts         # Transition effect implementations
├── persistent_layers.ts   # HUD/overlay management
└── index.ts               # Barrel export
```

## 4. Validation Checklist

- [ ] All files exist under `src/screens/`
- [ ] Lifecycle hooks (onEnter, onExit, onPause, onResume) implemented on base class
- [ ] Transitions match effects defined in spec
- [ ] Persistent layers (HUD/overlays) handled without blocking screen switches
- [ ] Cleanup/dispose called on screen exit (no memory leaks)
- [ ] Correct engine API used (Phaser scene keys vs Three.js scene graph)
- [ ] ScreenManager callable from game loop's update cycle

## 5. Red Flags

- **Required Input Present**: Read screen_architecture_spec.md before generating any code
- **Correct Engine API**: Use engine-specific APIs matching rendering_target.md
- **Complete Cleanup**: Call dispose() and release resources on screen exit
- **Connected Screens**: Every screen in the enum has at least one transition target
- **Async Transitions**: Handle transitions with async/promise to avoid freezing the render loop

## 6. Execution Command

Command: `/implement-screen-manager`
