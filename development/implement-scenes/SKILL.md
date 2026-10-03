---
name: implement-scenes
description: "Use when generating individual scene/screen skeleton classes from screen_architecture_spec.md. Each screen gets its own file with lifecycle hooks, asset manifests, event wiring, and UI stubs. Triggers: 'implement scenes', 'generate scenes', 'create screen classes', 'scene skeletons', 'screen scaffolding'."
---

## 1. Overview

Reads `screen_architecture_spec.md` + `rendering_target.md` + `events_spec.md` + `visual_style.md`, inspects existing `base_screen.ts`, then generates one skeleton class per screen in `{TARGET_FOLDER}/src/screens/scenes/`.

Screens extend the project's `BaseScreen` and implement all lifecycle hooks. Each skeleton includes screen-specific behavior stubs tailored to its role (see §3.4).

## 2. Quick Reference

**Output**: `{TARGET_FOLDER}/src/screens/scenes/{ScreenName}Screen.ts` — one per screen in spec.

| Screen Type | Unique Stubs |
|-------------|--------------|
| Loading | Progress bar, asset preload queue, transition-on-complete |
| MainMenu | Play/Settings/Credits buttons, menu navigation, BGM start |
| Gameplay | `update(delta)` hook, HUD wiring, pause trigger, ECS entity spawning |
| Pause | Resume button, settings shortcut, dim overlay, time scale pause |
| GameOver | Score display, restart/menu buttons, death animation trigger |
| Settings | Volume sliders, control rebinding stubs, save-settings-on-exit |
| Credits | Scrolling text/tween, skip button, return-to-menu |

Engine branching: Phaser 3 → `this.add.*`, Three.js → DOM overlay + `dispose()`. Always update `screens.ts` enum + registry and create `scenes/index.ts` barrel export.

## 3. Core Pattern

### 2.1 Configuration Detection (MANDATORY)

Read `.game-dev-config.json` → extract `target_folder`, `specs_dir`. Read `{TARGET_FOLDER}/docs/rendering_target.md` → extract Platform, Engine, Language. Read `{TARGET_FOLDER}/docs/visual_style.md` → extract Palette for UI color stubs.

### 2.2 Spec Extraction (MANDATORY)

Read `screen_architecture_spec.md` → extract screen list, descriptions, allowed transitions per screen.
Read `events_spec.md` → map events to relevant screens (e.g., PLAYER_DIED → GameOver, SCORE_UPDATED → Gameplay).
Read existing `base_screen.ts` → extract class name, constructor signature, abstract methods, lifecycle hook signatures.
Read existing `screens.ts` → extract current enum values and registry structure.

### 2.3 Scene File Generation

**Phaser 3 (2D)** — for each screen in spec, create `{TARGET_FOLDER}/src/screens/scenes/{ScreenName}Screen.ts`:

| Element | Content |
|---------|---------|
| Class | `export class {Name}Screen extends BaseScreen` |
| Constructor | Calls `super()` with screen key from enum |
| Asset manifest | Private object declaring `images`, `audio`, `fonts` arrays (empty with TODO) |
| `onEnter()` | Load assets, call `setupUI()`, register screen-specific events |
| `onExit()` | Unregister ALL event listeners, destroy UI elements, reset state |
| `onPause()` | Pause tweens/audio, disable input |
| `onResume()` | Resume tweens/audio, re-enable input |
| `setupUI()` | Screen-specific UI stubs using `this.add.*` (see §3.4) |

**Three.js (3D)** — same structure but:
- Asset manifest uses `models`, `textures`, `audio` arrays
- UI via DOM overlay (`HTMLElement`) or Canvas Texture
- Cleanup calls `dispose()` on Three.js objects (geometries, materials, textures)

**Non-Supported Engine** — generate placeholder class with `TODO: implement for <engine>` and export stubs so downstream compiles.

### 2.4 Screen-Specific Behavior (CRITICAL)

Each screen type receives unique stubs matching its lifecycle needs:

| Screen Type | Unique Stubs |
|-------------|-------------|
| Loading | Progress bar update method, asset preload queue, transition-on-complete |
| MainMenu | Button creation (Play, Settings, Credits), menu navigation, BGM start |
| Gameplay | Game loop `update(delta)` hook, HUD wiring, pause trigger, ECS entity spawning |
| Pause | Resume button, settings shortcut, dim overlay, time scale pause |
| GameOver | Score display, restart/menu buttons, death animation trigger |
| Settings | Volume sliders, control rebinding stubs, save-settings-on-exit |
| Credits | Scrolling text/tween, skip button, return-to-menu |

For screens not in the table, infer behavior from their `description` in `screen_architecture_spec.md`.

### 2.5 Registry & Barrel Export

Update `screens.ts`: add new enum values and factory entries for each generated screen.
Create `{TARGET_FOLDER}/src/screens/scenes/index.ts`: barrel export all scene classes.

### 2.6 Interaction Protocol

| Mistake | Recovery |
|---------|----------|
| All screens have identical code | Re-read §3.4, add screen-specific stubs |
| Event listeners without matching cleanup | Every `on()` in `onEnter` MUST have matching `off()` in `onExit` |
| Hardcoded asset paths | Use asset manifest object, not inline strings |
| Missing screens from spec | Re-read `screen_architecture_spec.md`, generate ALL listed screens |
| Wrong engine API | Re-check `rendering_target.md` Engine field |

## 3. Output File Structure

```
src/screens/scenes/
├── {ScreenName}Screen.ts   # One per screen from spec
└── index.ts                # Barrel export
```

Plus updated: `src/screens/screens.ts` (enum + registry)

## 4. Validation Checklist

- [ ] One file per screen from `screen_architecture_spec.md`
- [ ] All classes extend `BaseScreen` with correct constructor
- [ ] All four lifecycle hooks implemented (onEnter/onExit/onPause/onResume)
- [ ] Asset manifest declared per screen (even if empty)
- [ ] Screen-specific stubs present (§3.4) — not identical generic code
- [ ] Event listeners registered in `onEnter`, unregistered in `onExit`
- [ ] `screens.ts` updated with all new screens in enum + registry
- [ ] `scenes/index.ts` barrel exports all scene classes
- [ ] Engine-correct API used (Phaser `this.add.*` / Three.js `dispose()`)
- [ ] `tsc --noEmit` passes
- [ ] Code style matches existing `base_screen.ts`

## 5. Red Flags

- **Required Input Present**: Read screen_architecture_spec.md before proceeding; run implement-screen-manager if base_screen.ts is missing
- **Correct Engine API**: Use engine-specific APIs matching rendering_target.md
- **Screen-Specific Stubs**: Generate unique stubs per screen type (§3.4) instead of identical generic code
- **Complete Event Cleanup**: Unregister all event listeners in onExit to prevent memory leaks
- **Manifest-Based Assets**: Reference assets through manifest object instead of hardcoded paths

## 6. Execution Command

Command: `/implement-scenes`
<!-- OMO_INTERNAL_INITIATOR -->
