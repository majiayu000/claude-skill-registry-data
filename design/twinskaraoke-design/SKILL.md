---
name: twinskaraoke-design
description: Twinskaraoke's own UI, motion and haptics rules — the Apple Music–style design tokens (AM), website themes, the AppMotion spring scale, the ActiveAnimationClock pattern for perpetual animation, AppHaptic roles, the custom Now Playing presentation, and how to verify UI on this project's simulators. Use for any change in this repo that touches how something looks, moves or feels — layout, typography, colour, spacing, shelves, section headers, animation, transitions, haptics, the mini player or full-screen player, glass — and when reviewing such a change.
---

# Twinskaraoke design, motion and haptics

This skill is owned by the repository, unlike the third-party skills in
`.agents/skills/`. It records the house rules no outside skill can know: which
token to pick, which "obvious cleanup" has already been tried and broke
something, and which effects cannot be checked in the simulator.

## Precedence

1. `AGENTS.md` and any nearer `AGENTS.md` (approval gates, localization,
   large-file limits, one concern per PR).
2. This skill, for how Twinskaraoke looks, moves and feels.
3. Apple's Human Interface Guidelines (fetch through the Sosumi skill or MCP)
   for anything this skill does not decide.
4. `swiftui-pro` and the topic skills (`swiftui-liquid-glass`,
   `swiftui-performance-audit`, …) for how to write the SwiftUI.

When a third-party skill's snippet uses a raw colour, font, radius, spacing
value or spring, translate it to the tokens below instead of copying it.

## Workflow

1. Read the reference file for each area the task touches (router below).
   Read the doc comment on any type you change: most of the traps listed here
   are also explained at the code.
2. Find an existing component that already does it (`AMSectionHeader`,
   `InsetGroupedList`, `PressableButtonStyle`, `MarqueeText`, `EqualizerBars`,
   `trackingWidth(into:)`, …) before you build a new one.
3. Pick tokens **by role**, not by the size or feel you want at one call site.
   If no role fits, say so in the plan; don't invent a one-off value.
4. Changes to the Now Playing presentation, tab bar or navigation shell need
   approval first (AGENTS.md: navigation and playback).
5. Verify as described in `references/verification.md`, and say in the PR what
   still needs a device (haptics, glass rendering, audio-driven UI, feel).

## Rules that apply to every UI change

- **Tokens (iOS, iPadOS, Mac idiom):** type, radius, spacing, layout and
  shadow come from `AM` (`Apps/iOS/Components/Shared/AppTheme.swift`);
  colours from the `Color.app*` tokens
  (`Packages/UI/Themes/iOS/AppThemePalette.swift`, `AppTheme.swift`).
- **Tokens (watch, TV, Mac app, `Apple/` code):** `AM` doesn't exist there.
  Use `Color.appAccent` (`Packages/UI/DesignSystem/Apple/AppAccent.swift`),
  system text styles and semantic colours, and the default spacing of system
  containers. Follow the spacing and type already used in that app's folder
  instead of inventing values; propose a shared token in `Packages/UI/` when
  one is missing.
- **Never bulk-replace** font or radius literals across a file. Change each
  call site on purpose; the one real visual regression of the token migration
  came from a find-and-replace.
- **Motion:** use `AppMotion.snap/quick/standard/gentle/playful` and give
  every movement a Reduce Motion path (`appReduceMotion` → `crossFade` or no
  animation). Perpetual decoration uses `ActiveAnimationClock` and pauses on
  `appReduceEffects`.
- **Haptics:** one `AppHaptic` role per interaction, chosen by what happened.
  Never both an action haptic and a style haptic on the same button.
- **Dynamic Type:** fixed heights that hold text scale with `@ScaledMetric`.
  Check the largest accessibility size before you call a layout done.
- **Text:** user-facing strings follow AGENTS.md's localization rules;
  components that take a `String` title get `String(localized:)` from the
  caller and draw it with `Text(verbatim:)`.

## Reference router

| Task touches | Read |
| --- | --- |
| Fonts, radii, spacing, shelves, grids, headers, colours, themes, lists | `references/design-system.md` |
| Animations, transitions, springs, Reduce Motion, looping effects, gradients | `references/motion.md` |
| Haptics, button styles, toggles, pickers, scrubbing | `references/haptics.md` |
| Mini player, full-screen player, artwork morph, tab bar, overlays, menus | `references/now-playing-and-shell.md` |
| Screenshots, simulator checks, what needs a device | `references/verification.md` |

## Platform scope

`AM`, the website themes, `AppHaptic` playback and the Now Playing shell are
iOS (and iPadOS / Mac-idiom) only. The watch, TV and Mac apps use
`Color.appAccent`, system styles and `AppMotion` from `Packages/UI/`. Code in
an `Apple/` folder must not reach for `AM` or the iOS themes.
