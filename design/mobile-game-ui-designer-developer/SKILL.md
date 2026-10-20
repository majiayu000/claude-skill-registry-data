---
name: mobile-game-ui-designer-developer
description: Comprehensive React Native + Three.js game UI/UX design and development framework. Covers responsive layouts, HUD systems, modal navigation, gesture handling, accessibility, visual effects, and performance isolation for cross-device mobile games.
tags:
- react-native
- three.js
- game-ui
- responsive-design
- accessibility
- hud
- mobile-games
user-invocable: true
---

# Mobile Game UI Designer & Developer — RN + Three.js

A comprehensive, general-purpose skill for designing and building mobile game UI/UX with React Native overlays on Three.js canvases. Targets cross-device experiences (phone/tablet, 16:9–21:9) with accessible, performant, and visually rich interfaces.

**Tech Stack:** React Native 0.80+, Expo SDK 54+, @react-three/fiber (native), @react-three/drei, react-native-reanimated, react-native-safe-area-context, zustand

---

## ⚡ QUICK COMMAND REFERENCE

| Command | Focus | Research Doc |
|---------|-------|-------------|
| `/game-ui-paradigm` | UI Paradigms & Visual Hierarchy | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-arch` | Navigation & Screen Architecture | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-button` | Buttons, Touch & Feedback | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-responsive` | Responsive Layout & Safe Area | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-perf` | UI Performance & Render Isolation | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-hud` | Game HUD & World-Space UI | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-shader` | Visual Effects & Post-Processing | `researches/rn_responsive_ui_game_hud.md` |
| `/game-ui-a11y` | Accessibility & Localization | `researches/rn_responsive_ui_game_hud.md` |

---

## 🔗 SKILL COORDINATION MATRIX

```
[User Request]
      │
      ├──> /game-ui-paradigm   ──> UI paradigm selection (Diegetic/Spatial/Meta/Non-diegetic)
      │
      ├──> /game-ui-arch       ──> Screen stack, modal state machine, gesture navigation
      │
      ├──> /game-ui-button     ──> Pressable, spring animations, haptic+audio feedback
      │
      ├──> /game-ui-responsive ──> SafeArea, Dimensions, PixelRatio, multi-device layout
      │
      ├──> /game-ui-perf       ──> React.memo, useMemo, Zustand selectors, render isolation
      │
      ├──> /game-ui-hud        ──> Score/combo widgets, HUD overlays, world-space UI
      │
      ├──> /game-ui-shader     ──> Post-processing, CSS filters, Reanimated, Three.js effects
      │
      └──> /game-ui-a11y       ──> AccessibilityInfo, screen reader, WCAG contrast, RTL, i18n
```

---

## 1. /game-ui-paradigm — UI Paradigms & Visual Hierarchy

Select and implement the appropriate UI paradigm for game elements:

- **Diegetic:** UI exists within the game world (health bar as a hologram, score floating in 3D)
- **Spatial:** UI positioned in 3D space but not part of the game world (damage numbers, waypoints)
- **Meta:** UI as screen-space effects (red vignette on damage, blur on pause)
- **Non-diegetic:** Traditional 2D overlays (score counter, combo meter, buttons)

Key concepts: WCAG contrast ratios (4.5:1 normal text, 3:1 large text), color blindness safe palettes, visual hierarchy for glanceability.

→ [Sub-skill reference](subskills/game-ui-paradigm.md)

---

## 2. /game-ui-arch — Navigation & Screen Architecture

Design game screen flow using phase-based state machines instead of full navigation stacks:

- Phase state machine: `'menu' | 'playing' | 'paused' | 'settings' | 'gameover' | 'revive' | 'result'`
- Modal overlay pattern with scrim and animated transitions
- Back handler management for Android hardware back button
- Gesture-based navigation (swipe to dismiss modals)

→ [Sub-skill reference](subskills/game-ui-arch.md)

---

## 3. /game-ui-button — Buttons, Touch & Feedback

Build responsive, accessible interactive elements:

- `Pressable` with spring-animated press feedback
- Haptic feedback via `expo-haptics` (selection, impact, notification)
- Audio feedback synchronized with visual state changes
- Cooldown states to prevent rapid-fire inputs
- Minimum 44×44pt touch targets

→ [Sub-skill reference](subskills/game-ui-button.md)

---

## 4. /game-ui-responsive — Responsive Layout & Safe Area

Ensure pixel-perfect layouts across all device form factors:

- `useSafeAreaInsets()` for notch/dynamic island/home indicator avoidance
- `useWindowDimensions()` for reactive layout on rotation/fold
- `PixelRatio` for crisp rendering and optimal asset sizing
- Device tier classification: phone-small / phone / tablet / tablet-large
- Aspect ratio adaptation from 16:9 to 21:9 ultrawide
- Canvas sizing relative to HUD and tray regions

→ [Sub-skill reference](subskills/game-ui-responsive.md)

---

## 5. /game-ui-perf — UI Performance & Render Isolation

Prevent cascading re-renders in 60fps game environments:

- `React.memo` for HUD components and Canvas wrapper
- Granular Zustand selectors: `useGame((s) => s.score)` instead of destructuring
- `useGame.subscribe()` for side-effect-only updates without re-render
- `useMemo` for expensive computations (piece bounds, PanResponder creation)
- Component-level state for local animations (ScoreCounter owns its display state)

→ [Sub-skill reference](subskills/game-ui-perf.md)

---

## 6. /game-ui-hud — Game HUD & World-Space UI

Build game-specific HUD systems and bridge 3D world positions to 2D overlays:

- Animated score counter with ease-out cubic count-up and pulse effect
- Combo meter with escalating color tiers and continuous pulse at high combos
- Health bars, currency displays, distance/coin counters
- Screen-projected positioning: convert 3D world coords to RN overlay positions
- Ref-based communication pattern: Three.js `useFrame` → shared ref → RN overlay
- Genre-specific patterns: Puzzle (score/tray), Runner (distance/coins), Idle (currency panel), Tower Defense (build menu)

→ [Sub-skill reference](subskills/game-ui-hud.md)

---

## 7. /game-ui-shader — Visual Effects & Post-Processing

Implement visual effects using RN and Three.js rendering pipelines:

- CSS filters and RN `Animated` for screen-space meta effects (blur, tint, vignette)
- `react-native-reanimated` for 60fps worklet-based animations
- Three.js post-processing: bloom, chromatic aberration, scanlines
- Shader-based damage indicators, combo flash, screen shake
- Performance considerations: cap DPR at 2x, prefer native driver animations

→ [Sub-skill reference](subskills/game-ui-shader.md)

---

## 8. /game-ui-a11y — Accessibility & Localization

Make games accessible and support multiple languages:

- `AccessibilityInfo` for screen reader detection and adaptation
- `accessibilityRole`, `accessibilityLabel`, `accessibilityHint` on all interactive elements
- WCAG 2.1 AA color contrast enforcement (4.5:1 / 3:1)
- RTL layout support via `I18nManager` with game-element LTR overrides
- Localization pattern with string tables
- Reduce motion support for vestibular sensitivity

→ [Sub-skill reference](subskills/game-ui-a11y.md)

---

## Research Documents

| Document | Path |
|----------|------|
| Responsive UI, Game HUD & Input Handling | [`researches/rn_responsive_ui_game_hud.md`](researches/rn_responsive_ui_game_hud.md) |

---

## Sources

- [React Native Safe Area Context](https://github.com/AppAndMusic/react-native-safe-area-context)
- [React Native Dimensions API](https://reactnative.dev/docs/dimensions)
- [React Native PanResponder](https://reactnative.dev/docs/panresolver)
- [React Native Gesture Handler](https://docs.swmansion.com/react-native-gesture-handler/)
- [React Native AccessibilityInfo](https://reactnative.dev/docs/accessibilityinfo)
- [WCAG 2.1 Color Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [React Three Fiber Native](https://docs.pmnd.rs/react-three-fiber/getting-started/installation#expo)
- [Zustand Subscribe Pattern](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [React.memo](https://react.dev/reference/react/memo)
