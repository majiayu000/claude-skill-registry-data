---
name: roblox-gui
description: "Use when building or fixing Roblox menus, HUDs, shops, dialogs, or UI that must work on phones, tablets, desktop and console."
when_to_use: "Also when changing or reviewing any UI, or when UI overlaps, is cut off, too small, misplaced or unreadable on mobile, a phone, tablet, TV or with a controller."
last_reviewed: 2026-10-14
sources:
  - https://create.roblox.com/docs/ui
  - https://create.roblox.com/docs/ui/position-and-size
  - https://create.roblox.com/docs/ui/styling
  - https://create.roblox.com/docs/ui/list-flex-layouts
  - https://create.roblox.com/docs/input
  - https://create.roblox.com/docs/input/mobile
  - https://create.roblox.com/docs/production/publishing/console-guidelines
  - https://create.roblox.com/docs/studio/device-simulator
  - https://create.roblox.com/docs/reference/engine/classes/GuiService
  - https://create.roblox.com/docs/reference/engine/classes/ScreenGui
  - https://create.roblox.com/docs/projects/server-authority
  - https://create.roblox.com/docs/input/input-action-system
  - https://create.roblox.com/docs/reference/engine/classes/ReplicatedFirst
  - https://create.roblox.com/docs/reference/engine/classes/ContentProvider
  - https://create.roblox.com/docs/reference/engine/classes/UIPageLayout
  - https://create.roblox.com/docs/reference/engine/classes/SelectionBox
  - https://create.roblox.com/docs/reference/engine/classes/Decal
  - https://create.roblox.com/docs/reference/engine/classes/VideoPlayer
  - https://raw.githubusercontent.com/Roblox/focus-navigation/main/README.md
  - https://devforum.roblox.com/t/introducing-improvements-to-directional-ui-selection-on-gamepad/3864317
  - https://devforum.roblox.com/t/what-are-the-best-ui-screeninset-settings-for-buttons/3519333
  - https://devforum.roblox.com/t/screenguiscreeninsets-topbarinsets-regression/4047230
  - https://raw.githubusercontent.com/Roblox/react-luau/main/README.md
  - https://raw.githubusercontent.com/dphfox/Fusion/main/README.md
  - https://raw.githubusercontent.com/centau/vide/main/README.md
  - https://raw.githubusercontent.com/ffrostfall/fluid/main/README.md
  - original
---

# roblox gui

## When to Load

HUDs, menus, shops, dialogs, world UI, and layout bugs on phone, tablet, desktop or TV.

## Quick Reference

- Mobile first: design on the smallest landscape phone with touch controls, then grow (full.md §11).
- Reserve top bar, thumbstick, jump, chat; interactive UI in `CoreUISafeInsets`; place by measured `AbsolutePosition`/`AbsoluteSize`.
- Check every element pair that can show together; reflow, don't shrink.
- Gamepad: one `SelectedObject` owner, `SelectionGroup` bounds, restored focus, layered Back (§8).
- Console: TV-safe area, `ViewportDisplaySize`, no chat window.
- Layouts own repeated layout; UI shows server state; a button is not an authority boundary.
- Reactive UI: per-screen cleanup; repeat open/close to test leaks. Loading UI in `ReplicatedFirst`.
- TextBox submit, grids, truncation, RichText safety, deprecated APIs: full.md.

> Details: [references/full.md](references/full.md)
