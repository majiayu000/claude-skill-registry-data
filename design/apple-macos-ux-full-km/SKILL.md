---
description: |
    Use when designing, scaffolding, or reviewing **native macOS** UX with **AppKit + SwiftUI**, especially for windows, menus, toolbars, sidebars, preferences, status bar apps, keyboard navigation, first-responder behavior, drag and drop, focus handling, and accessibility. Do not use for general Apple UI work that is not macOS-specific.
metadata:
    targets:
        - codex
name: apple-macos-ux-full_KM
tags:
    - macOS
    - AppKit
    - SwiftUI
    - UX
    - Toolbar
    - Menu
    - Window
    - Accessibility
    - StatusBar
    - Preferences
    - NSWindow
    - NSToolbar
    - NavigationSplitView
    - MenuBarExtra
user-invocable: false
version: 1.0.0
---
# apple-macos-ux-full

> **Purpose**: Equip Claude Agents to scaffold, review, and generate **native macOS** apps
> that feel like Finder, Settings, and Mail — not iOS ports. This skill packages repeatable
> patterns for **AppKit + SwiftUI hybrid** architecture, **window & toolbar design**, **menu bar**,
> **NavigationSplitView** sidebars, **preferences**, **status bar apps**, **drag & drop**, **keyboard
> navigation**, **first responder chain**, **focus rings**, and **accessibility**.

**Deliverables in this skill:**

- `scripts/` — Python generators for project scaffolding, menus, toolbars, status bar extras, and multi-window managers.
- `examples/` — Production-quality Swift files (AppKit, SwiftUI, and Hybrid).
- `docs/` — Focused references: window management, menu design, toolbar patterns, AppKit↔SwiftUI bridge, keyboard navigation, and gotchas.
- `templates/` — JSON/YAML specs for menus, toolbars, status bar, and windows.
- `plist/` — Sample `Info.plist` and hardened runtime entitlements.
- This `SKILL.md` — Detailed design guidance and usage.

---

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [macOS Design Principles](#macos-design-principles)
- [Liquid Glass (macOS 26)](#liquid-glass-macos-26)
- [NSWindow Architecture](#nswindow-architecture)
- [Window Management](#window-management)
- [Toolbar Design (Unified & Legacy)](#toolbar-design-unified--legacy)
- [Menu Bar Design](#menu-bar-design)
- [Sidebar Patterns](#sidebar-patterns)
- [NSTableView / NSCollectionView](#nstableview--nscollectionview)
- [Preferences Windows](#preferences-windows)
- [Status Bar Apps](#status-bar-apps)
- [Popovers & Sheets](#popovers--sheets)
- [Drag & Drop](#drag--drop)
- [Keyboard Navigation](#keyboard-navigation)
- [First Responder Chain](#first-responder-chain)
- [Focus Rings](#focus-rings)
- [SwiftUI on macOS](#swiftui-on-macos)
- [AppKit Bridges](#appkit-bridges)
- [Hybrid Architecture (AppKit + SwiftUI)](#hybrid-architecture-appkit--swiftui)
- [NavigationSplitView Patterns](#navigationsplitview-patterns)
- [Settings Scene](#settings-scene)
- [MenuBarExtra](#menubarextra)
- [macOS HIG 2025 Checklist](#macos-hig-2025-checklist)
- [Accessibility](#accessibility)
- [Best Practices](#best-practices)
- [Anti-Patterns](#anti-patterns)
- [Common Gotchas](#common-gotchas)
- [Troubleshooting](#troubleshooting)
- [Tool Reference (scripts/)](#tool-reference-scripts)
- [File Layout](#file-layout)
- [References](#references)

---

## Overview

**Native macOS** apps reward **precision**: deep keyboard control, robust multi-window behavior,
clear menus, unified toolbars, state restoration, and efficient data views. This skill teaches
Claude to **generate, critique, and evolve** production-ready Mac apps with AppKit and SwiftUI
in tandem, using battle-tested patterns seen in **Finder (source list + toolbar + path bar)**,
**Settings (sidebar navigation, split views)**, and **Mail (three-pane layout, message list with
contextual menus)**.

**Key outcomes**

- Scaffolds a hybrid AppKit + SwiftUI project with transparent titlebar, unified toolbar,
  sidebar, menu bar validation, and status bar extras.
- Produces configurable, testable **menus**, **toolbars**, **status bar UIs**, and **window managers**
  from JSON/YAML specs.
- Documents **first responder** design, **focus handling**, **keyboard shortcuts**, and **drag & drop**.
- Offers **complete Swift examples** for common app surfaces: window controllers, preference panes,
  split view navigation, and restoration.

---

## When to Use

Use this skill when you need to:

- **Start a new macOS project** with production defaults (unified toolbar, state autosave, document/window architecture).
- **Refactor an iOS port** into a real Mac app that uses menus, toolbars, and keyboard control.
- **Add advanced surfaces**: Sidebar with `NavigationSplitView`, tabbed preferences, status bar extras, popovers/sheets.
- **Enforce UX quality**: HIG-aligned menus, `validateMenuItem`, toolbar customization, accessibility, and localization.
- **Scale windows**: Multi-window coordination, restoration, autosave, tabbing behavior, and cross-window state.

---

## macOS Design Principles

- **Mac-first workflows.** Support **menus** and **toolbars** for all commands; provide shortcuts for frequent actions.
- **Discoverability via the menu bar.** Every command belongs to a menu and uses a **consistent label**.
- **Keyboard mastery.** Implement **first responder** chain, `validateMenuItem`, and predictable key equivalents.
- **Windows as workspaces.** Preserve position/size across relaunches, respect tabbing preferences, and avoid modal traps.
- **Sidebars and source lists.** Triage information hierarchically; lean on split views and `NavigationSplitView` for clarity.
- **Consistency & materials.** Use standard controls, spacing, and system materials; adopt **unified toolbars** where suitable.

---

## Liquid Glass (macOS 26)

macOS 26 introduces **Liquid Glass**, a new material system that replaces the
classic vibrancy/blur effects with a refractive, adaptive surface.  Liquid
Glass bends and focuses light rather than merely scattering it, making UI
elements float above busy backgrounds without sacrificing legibility.  The
system manages vibrancy, shadows, and tint automatically and provides
grouping and morphing behaviors when multiple glass panes are near each
other.

### NSGlassEffectView architecture

`NSGlassEffectView` is the primary AppKit API for Liquid Glass.  You embed
your content in its `contentView` and set a `cornerRadius` and optional
`tintColor`.  Multiple glass views should be wrapped in an
`NSGlassEffectContainerView` so the system can merge their surfaces and
perform a single sampling pass.  Use the container to group adjacent
toolbars, sidebars, or palettes; when spacing is minimal the panes will
morph into one organic surface.

### Glass materials & vibrancy

Liquid Glass automatically adopts the system’s **Clear** or **Tinted**
preference (System Settings → Appearance → Liquid Glass).  Clear glass is
airy and highly translucent; Tinted increases opacity and contrast to
improve legibility.  Do not hard‑code text colors on glass surfaces — rely
on the system’s vibrant colors or adjust `tintColor` for emphasis.  When
Reduce Transparency or Increase Contrast are enabled in Accessibility
settings, fall back to solid backgrounds.

### Glass in toolbars (unified style)

Toolbars can take full advantage of Liquid Glass by unifying with the
window title area (`window.toolbarStyle = .unified`) and by using
`NSToolbarItem.style = .prominent` for primary actions.  A prominent
toolbar item renders with a tinted glass background; a plain item floats
subtly on clear glass.  Group your toolbar with adjacent search fields or
palettes using an `NSGlassEffectContainerView` to ensure their surfaces
merge gracefully.

### Glass sidebars & split views

Sidebars are natural candidates for Liquid Glass.  Wrap the sidebar list
in an `NSGlassEffectView`, match the corner radius to your window’s shape
for concentricity, and group the sidebar with neighboring panels in a
container.  In SwiftUI, call `.glassEffect` on your list or sidebar
container.  When a sidebar collapses or expands, keep it inside the same
container so the glass morphs rather than snaps.

### Floating glass palettes

Inspectors, HUDs, and floating tool palettes benefit from glass because
they appear light and unobtrusive.  Use `NSPanel` with
`isFloatingPanel = true` and embed an `NSGlassEffectView` as its
contentView.  For HUD windows, apply a tinted glass (`tintColor`) to
increase opacity over busy content.  Always provide a close/dismiss
control and ensure the panel participates in the first responder chain.

### Glass popovers & sheets

On macOS 26, SwiftUI’s `.sheet` and `.popover` adopt Liquid Glass
automatically.  In AppKit, embed your popover’s content in
`NSGlassEffectView` to achieve the same effect.  Keep popovers concise and
prefer a **prominent** (tinted) glass style if the background competes
with your content.  Provide keyboard dismissal (Esc) and avoid piling
toolbars on popovers.

### SwiftUI glass on macOS

SwiftUI gains the `.glassEffect` modifier and `GlassEffectContainer` to
build glass surfaces.  Apply `.glassEffect(.regular, in: someShape)` to a
view to wrap it in Liquid Glass.  Use `GlassEffectContainer` to group
adjacent glass elements so they morph and share sampling.  Button styles
`.glass` and `.glassProminent` mirror the plain/prominent styles in AppKit.

### AppKit ↔ SwiftUI glass bridging

Hybrid apps can bridge Liquid Glass across frameworks.  Use
`NSViewRepresentable` to embed an `NSGlassEffectView` inside SwiftUI when
you need AppKit‑level control such as grouping or custom tinting.  To
embed SwiftUI glass in AppKit, wrap a SwiftUI view that uses
`.glassEffect` in an `NSHostingView` or `NSHostingController`.  This skill
includes examples in `examples/hybrid` demonstrating both directions.

### Clear/Tinted system preference

Respect the system’s **Clear** vs **Tinted** preference.  If your app
previously exposed its own translucency toggle, remove it and allow the
system to drive glass opacity.  Always support Reduce Transparency,
Reduce Motion and Increase Contrast accessibility options by falling
back to solid surfaces and disabling glass flex animations.

For a full reference on AppKit APIs, SwiftUI patterns and migration
steps, see the dedicated documents in the `docs/` folder:
`liquid-glass-macos.md`, `appkit-glass-bridge.md` and `macos-26-migration.md`.

---

## NSWindow Architecture

- **Style & chrome.** Prefer a **transparent titlebar** with `.fullSizeContentView` and `.unified` toolbar style for modern layouts.
- **Autosave & restoration.** Set `window.frameAutosaveName` to persist geometry; implement restoration for critical windows.
- **Tabbing.** Control window tabbing using `NSWindow.allowsAutomaticWindowTabbing` and per-window tabbing modes.
- **Behavior flags.** Choose appropriate `collectionBehavior`, `animationBehavior`, and full‑screen support for each window.
- **Titlebar accessories.** Use `NSTitlebarAccessoryViewController` for path controls or segmented filters in the title area.

---

## Window Management

- **State persistence.** Use `frameAutosaveName` and encode/decode restorable state for custom positions, split ratios, and visibility.
- **Multi-window orchestration.** Maintain a registry keyed by **document IDs** or **logical roles** (e.g., Inspector, Library).
- **Tab groups.** When supported by your domain, join windows into `NSWindowTabGroup` and manage default tab visibility.
- **Lifecycle.** Use `NSWindowDelegate` to save on close, and to prevent accidental data loss or dead windows.
- **SwiftUI Scenes.** Combine AppKit windows with `WindowGroup`, `Settings`, and `MenuBarExtra` scenes.

---

## Toolbar Design (Unified & Legacy)

- **Unified toolbars** (`.unified` / `.unifiedCompact`) merge title and toolbar; reduces chrome, like Finder/Photos/iWork.
- **Customization.** Use `NSToolbar` with **allowed/default** item sets; expose **Customize Toolbar…** if appropriate.
- **Validation.** Implement `NSToolbarItemValidation` to enable/disable items via the responder chain.
- **Center items.** Consider `centeredItemIdentifier` for prominent content controls (e.g., segmented filters).

  **Liquid Glass integration (macOS 26).** When targeting macOS 26 or later, use
  Liquid Glass for unified toolbars.  Assign `NSToolbarItem.style = .prominent` to
  primary actions and `.plain` to secondary actions, and set
  `backgroundTintColor` for meaningful accent colors.  Group your toolbar
  with adjacent search fields or palettes using an `NSGlassEffectContainerView`
  so their surfaces morph seamlessly.  See the `GlassToolbarWindow.swift`
  example for a complete pattern.

---

## Menu Bar Design

- **Standard menus.** Provide the Application, File, Edit, View, Window, and Help menus. Keep verbs consistent.
- **Key equivalents.** Assign lowercase `keyEquivalent` with appropriate `modifierMask`; avoid collisions.
- **Nil-target actions.** Target **nil** for shared commands; let the **first responder** handle them.
- **Dynamic titles & state.** Update labels (e.g., “Show Sidebar”) and states via `validateMenuItem`.
- **Services & roles.** Integrate **Services** when relevant; use Apple’s standard roles and separators.

---

## Sidebar Patterns

- **Source lists.** Use sidebars for navigation, not action overload. Keep items text‑first with familiar badges.
- **Split views.** Pair sidebars with detail panes; use `NavigationSplitView` for adaptive SwiftUI patterns.
- **Selection semantics.** Single selection by default; multi‑select only where it unlocks clear bulk actions.

  **Liquid Glass sidebars (macOS 26).** Wrap your sidebar’s list in an
  `NSGlassEffectView` or, in SwiftUI, apply `.glassEffect` to the sidebar.
  Match the corner radius to your window’s geometry for concentricity and
  group the sidebar with any adjacent panels in an `NSGlassEffectContainerView`.
  When collapsing or expanding the sidebar, keep it inside the same
  container to enable smooth morphing rather than abrupt snapping.  See
  `GlassSidebarWindow.swift` and `GlassSidebarNavigation.swift` in
  `examples/` for reference.

---

## NSTableView / NSCollectionView

- **Performance.** Prefer **diffable data sources** for incremental updates.
- **Interaction.** Support type‑to‑select, contextual menus, drag & drop, and keyboard reordering where relevant.
- **SwiftUI bridges.** Host SwiftUI rows in AppKit via `NSHostingView` or embed AppKit lists in SwiftUI with `NSViewRepresentable`.

---

## Preferences Windows

- **Settings vs. Preferences.** In SwiftUI, implement a `Settings` scene; for classic AppKit, provide a **tabbed** preferences window with a toolbar.
- **Focused panes.** Group related options; keep panes short and scannable; add search if there are many options.
- **Apply model.** Persist immediately; avoid **Apply** buttons unless there are explicit batch operations.

---

## Status Bar Apps

- **SwiftUI**: Use `MenuBarExtra` for a lightweight menu or mini‑window experience.
- **AppKit**: Use `NSStatusItem` for full control; ensure a **Quit** path when Dock icon is hidden; manage highlight states.
- **Behavior.** Respect system placement, autosave positions if supporting reordering, and avoid Dock/status duplication.

---

## Popovers & Sheets

- **Sheets**: Use for blocking, focused tasks; keep concise and reversible.
- **Popovers**: Use for transient tools and inspectors; anchor to controls; dismiss on focus loss when appropriate.
- **Materials**: Prefer system materials; ensure proper arrow placement and escape-to-dismiss behavior.

  **Liquid Glass (macOS 26).** On macOS 26, SwiftUI automatically applies
  Liquid Glass to `.popover` and `.sheet` surfaces.  In AppKit, embed your
  popover’s content view in an `NSGlassEffectView` to achieve the same
  effect.  Prefer a **prominent** (tinted) glass style when the
  underlying content is busy, and always respect Reduce Transparency by
  falling back to solid backgrounds.  See `FloatingGlassPalette.swift` for
  a floating example.

---

## Drag & Drop

- **AppKit**: Implement `NSDraggingDestination` on views/lists; adopt pasteboards and promised files as needed.
- **SwiftUI**: Use `Transferable` and `onDrop` for type‑safe payloads; bridge to AppKit where advanced behaviors are required.
- **Feedback**: Provide clear insertion indicators and cursor feedback; support modifier keys for copy/move/link.

---

## Keyboard Navigation

- **Shortcuts.** Assign key equivalents for frequent actions; mirror Finder/Mail where applicable.
- **Responder chain.** Route commands by targeting **nil**; implement `validateMenuItem` to enable/disable contextually.
- **Focus.** Ensure focus rings and tab order are correct; support type select in lists and jump‑to search fields.

---

## First Responder Chain

- **Concept.** Menus and toolbar items with nil targets bubble actions to the current **first responder**.
- **Validation.** Implement `validateMenuItem`/`validateUserInterfaceItem` where actions vary by selection/context.
- **Testing.** Verify responders with multiple focus targets (list vs. detail vs. search).

---

## Focus Rings

- **Visual feedback.** Use system focus rings; for custom views, implement `drawFocusRingMask` and `noteFocusRingMaskChanged`.
- **Layer-backed views.** Ensure focus rings render correctly when using Core Animation backing.

---

## SwiftUI on macOS

- **Scenes.** Use `WindowGroup`, `Window`, `Settings`, `MenuBarExtra`; coordinate with AppKit windows where needed.
- **Navigation.** Prefer `NavigationSplitView` for Mac‑style sidebars; preserve selection and column state.
- **Bridging.** Embed AppKit where SwiftUI is lacking (text inputs, complex lists, legacy views).

  **Liquid Glass (macOS 26).** SwiftUI in macOS 26 introduces `.glassEffect` and
  `GlassEffectContainer`.  Use `.glassEffect(_:, in:)` on any view to wrap
  it in Liquid Glass, specifying a shape (e.g. `.capsule`, `RoundedRectangle`).
  Group adjacent glass elements with `GlassEffectContainer` to merge their
  sampling region and enable morphing transitions.  Button styles
  `.glass` and `.glassProminent` mirror the plain/prominent styles in
  AppKit.  See `SwiftUIGlassWindow.swift` and other SwiftUI examples for
  patterns.

---

## AppKit Bridges

- **SwiftUI → AppKit**: `NSViewRepresentable`, `NSViewControllerRepresentable`.
- **AppKit → SwiftUI**: `NSHostingView`, `NSHostingController` with sizing options.
- **Responder integration.** Ensure hosted views participate in focus and responder chain correctly.

  **Liquid Glass bridging.** To use Liquid Glass across frameworks, embed
  `NSGlassEffectView` in SwiftUI via `NSViewRepresentable` when you need
  AppKit‑level control (e.g. grouping, custom tint).  Conversely, embed
  SwiftUI views that use `.glassEffect` into AppKit using `NSHostingView`
  or `NSHostingController`.  This skill provides bridging examples in
  `examples/hybrid/AppKitGlassInSwiftUI.swift` and
  `examples/hybrid/SwiftUIGlassInAppKit.swift`.

---

## Hybrid Architecture (AppKit + SwiftUI)

- **Strategy.** Keep windowing, menus, and toolbars in **AppKit**; implement content panes in **SwiftUI** for speed and consistency.
- **Data flow.** Use `ObservableObject` and dependency injection for SwiftUI, and delegates/notifications bridging in AppKit.
- **Testing.** Unit test reducers/view models; UI tests for menu validation and toolbar state.

  **Liquid Glass across frameworks.** When combining AppKit and SwiftUI, unify
  glass surfaces by grouping related views in `NSGlassEffectContainerView` or
  `GlassEffectContainer`.  Manage state in a shared model so both
  frameworks update tints and visibility consistently.  Use bridging
  patterns to embed AppKit glass in SwiftUI and vice versa (see
  `examples/hybrid` for details).  Always respect system preferences for
  Clear/Tinted and fall back to solid materials when accessibility
  settings require it.

---

## NavigationSplitView Patterns

- **Two‑ and three‑column** patterns match Mail and Finder.
- Persist selection and column visibility; conditionally hide detail for narrow layouts.
- Use **list styles** that match source lists; prefer leading disclosure triangles and badges.

---

## Settings Scene

- Implement a `Settings` scene to automatically wire the **App menu → Settings…** item.
- Provide categorized tabs or grouped lists; respect system‑wide search if implemented.

---

## MenuBarExtra

- Use `MenuBarExtra` for menu‑only or window‑style extras; provide a **Quit** affordance.
- Avoid Dock icons for utilities unless discoverability requires it; don’t hijack ⌘Q behavior.

---

## macOS HIG 2025 Checklist

- **Menus are complete** and discoverable; labels match system verbs.
- **Unified toolbar** with clear, icon‑first affordances and optional labels.
- **Keyboard**: Every major command has a shortcut; tab order and focus rings verified.
- **Windows**: Restore gracefully; use sheets judiciously; avoid modality unless necessary.
- **Accessibility**: Speakable labels, roles, values; visible focus; full VoiceOver traversal.
- **Materials**: System materials, vibrancy only when helpful; avoid distracting effects.
- **Glass materials**: Use Liquid Glass for toolbars, sidebars, palettes and popovers where it aids separation; avoid glass behind dense text or data tables.
- **Glass grouping**: Group related glass surfaces in an `NSGlassEffectContainerView` or `GlassEffectContainer` so they morph and sample together.
- **System preference**: Respect the Clear/Tinted Liquid Glass preference and do not override it with custom translucency toggles.
- **Concentricity**: Align glass corners with window geometry and adjacent panes for a harmonious look.
- **Performance**: Test glass rendering on older Macs to ensure animations and morphing remain smooth; group panes to reduce passes.
- **Accessibility fallback**: Honor Reduce Transparency and Increase Contrast by replacing glass with solid materials and disabling motion when necessary.

---

## Accessibility

- Adopt **NSAccessibility** roles and labels for custom controls.
- Ensure hit targets, color contrast, dynamic type scaling where applicable.
- Test with **VoiceOver** and keyboard‑only use; avoid pointer‑only affordances.

---

## Best Practices

- Prefer **nil‑target** menu actions and **first responder** routing.
- Treat sidebars and toolbars as **navigation**, not dumping grounds for toggles.
- Persist **window state** and selection across launches.
- Build **hybrid**: AppKit for windowing + SwiftUI for content.

---

## Anti-Patterns

- iOS port with no menu bar or keyboard shortcuts.
- Custom theming that clashes with system materials and vibrancy.
- Overloaded popovers/sheets that block primary workflows.
- Ignoring autosave/restoration, forcing users to rearrange every launch.

---

## Common Gotchas

- **validateMenuItem** not firing because the target is not in the responder chain.
- Focus rings clipped by layer‑backed views — implement **focus ring mask**.
- Window tabbing leaking into apps unintentionally — set `NSWindow.allowsAutomaticWindowTabbing = false` at launch.
- `Settings` scene on newer macOS versions supersedes legacy Preferences wiring.

---

## Troubleshooting

- If menus are disabled, confirm the intended controller is in the **first responder** path.
- If window state doesn’t restore, set a unique **frameAutosaveName** and encode custom state explicitly.
- If status bar extras won’t quit, ensure a **Quit** menu item exists when hiding Dock icon.
- If SwiftUI views don’t size in AppKit, set **NSHostingController.sizingOptions** appropriately.

---

## Tool Reference (scripts/)

- `scripts/scaffold_macos_app.py` — Generate a **hybrid AppKit + SwiftUI** project skeleton with unified toolbar, sidebar, and menus.
- `scripts/menu_generator.py` — Generate Swift **Commands/NSMenu** from JSON/YAML specs.
- `scripts/toolbar_generator.py` — Generate **NSToolbar** implementations from specs.
- `scripts/statusbar_generator.py` — Generate **NSStatusItem** and **MenuBarExtra** templates.
- `scripts/window_manager_generator.py` — Generate multi‑window orchestration and restoration code.

Each tool supports `--out` to pick an output folder; see `--help`.

---

## File Layout

```
apple-macos-ux-full/
  SKILL.md
  scripts/
  examples/
    appkit/
    swiftui/
    hybrid/
  docs/
    visuals/
  templates/
  plist/
```

---

## References

- Apple Human Interface Guidelines (menus, toolbars, split views, accessibility)
- AppKit documentation (NSWindow, NSToolbar, NSMenuItem validation, NSStatusItem)
- SwiftUI documentation (NavigationSplitView, Settings, MenuBarExtra)
- Bridging (NSHostingController, NSViewRepresentable)

This skill encodes production patterns seen in Finder, Settings, and Mail while staying faithful to platform conventions.
