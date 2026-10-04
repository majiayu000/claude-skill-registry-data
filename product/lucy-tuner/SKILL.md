---
name: lucy-tuner
description: Launch, inspect, and use the interactive Lucy position and zoom tuner HUD in Skill Heaven Hero A.
---

# Lucy Tuner Dev Skill

Interactive tuning harness for Lucy's framing, position (`x`, `y` in `vh`), and zoom scale across the four Hero A motifs (`zero`, `heaven`, `hell`, `ultra`).

## Trigger & Access

The Lucy tuner is disabled by default on production hero loads to maintain a pristine visitor experience. You can activate it anytime through any of the following methods:

1. **URL Parameter**:
   - Open `http://localhost:5178/?tuner=lucy` (or `/#/?tuner=lucy`).
2. **Keyboard Shortcut**:
   - Press **`Cmd + Shift + L`** (macOS) or **`Ctrl + Shift + L`** (Windows/Linux) anywhere on the hero page.
3. **Browser Console**:
   ```javascript
   localStorage.setItem('lucy-tuner', 'true'); location.reload();
   ```
   (To turn off: `localStorage.removeItem('lucy-tuner'); location.reload();`)

## Features & Controls

- **Interactive Dragging**:
  - Click and drag anywhere across Lucy's upper body / viewfinder box to reposition her horizontally and vertically.
  - Offsets are calculated in viewport units (`vh`), matching the engine's `figX` and `figY`.
- **Trackpad Pinch-to-Zoom**:
  - Pinch on any desktop trackpad to smoothly zoom Lucy in or out, pivoting on her face anchor.
  - Double-click the background or figure to reset zoom to `1.0`.
- **Scene Switcher Bar**:
  - Click `[ ZERO ]`, `[ HEAVEN ]`, `[ HELL ]`, `[ ULTRA ]` directly inside the HUD or click the ladder rungs on screen (the ladder sits cleanly on top of the dragger at `z-index: 50+`).
- **Dynamic Synchronization**:
  - `Sync: ALL`: Drag and zoom adjustments apply across all motifs dynamically so you can inspect consistent scaling across Zero → Ultra.
  - `Sync: SOLO`: Tune coordinates for the active motif only.
- **Copy Configurations**:
  - **`COPY SCENE`**: Copies the single active scene object:
    ```ts
    heaven: { zoom: 1.59, x: -3.25, y: -1.63, origin: '49% 27%' }
    ```
  - **`COPY ALL`**: Copies the full `FIG_CONFIG` block ready to paste into `packages/site/src/variations/hero/useHeroEngine.ts`.

## Locked Preset Authority (`FIG_CONFIG`)

Location: `packages/site/src/variations/hero/useHeroEngine.ts`

```ts
export const FIG_CONFIG = {
  zero:   { zoom: 1.00, x:  0.60, y:  3.68, origin: '47% 30%' },
  heaven: { zoom: 1.59, x: -3.25, y: -1.63, origin: '49% 27%' },
  hell:   { zoom: 1.68, x:  2.66, y: -0.25, origin: '47% 30%' },
  ultra:  { zoom: 1.40, x:  3.55, y:  2.00, origin: '45% 24%' },
} as const;
```
