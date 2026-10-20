---
name: fespalier-layouts
description: "Layouts and shells in fespalier — layout.dart (a ShellRoute around a folder and everything below it), (group) layouts, tab layouts on a StatefulNavigationShell with tabs, tabOptions and a custom container, nested tabs, transition.dart and how a layout's shell animates, dialogs and sheets as routes, state restoration ids, scroll restoration on the browser's back and forward, and adaptive layouts (since 0.9.0 the package fespalier_adaptive draws the nav.dart menu as a navigation bar, a rail or a drawer by window width, AdaptiveNavScaffold and AdaptiveNavBuilder; by hand before that), and, since 0.8.1, menus and breadcrumbs generated from nav.dart files (a drawer, a tab bar, a breadcrumb row that respects guards). Load before adding or changing a layout.dart, a tab bar, a menu, a nav.dart, a transition.dart or restoration, or when a layout wraps the wrong pages, a tab loses its state, a phone shows no bottom bar, or a ListTile asserts about its Material."
---

# fespalier-layouts

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

## `layout.dart`

A `layout.dart` wraps **its folder and everything below it**: it becomes a go_router
`ShellRoute` and mounts the pages as `child`.

```dart
// lib/app/layout.dart
import 'package:flutter/material.dart';

class AppLayout extends StatelessWidget {
  const AppLayout({super.key, required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) => Scaffold(body: SafeArea(child: child));
}
```

- It asks for **`Widget child`** (a shell), or for a **`StatefulNavigationShell`**
  (`navigationShell` or `shell`: a tab layout). **Both is an error.** It may also
  ask for the segments at or above its folder, query parameters, the **section
  data** it wraps or sits inside (`fespalier-data`), and a nullable `extra`. A
  view **function** form exists too (`Widget layout({required Widget child})`).
- **A `(group)` folder's layout applies only to the routes inside it**, without
  touching their URLs: `(shop)/cart` and `(account)/profile` can have different
  shells and still be `/cart` and `/profile`. Layouts nest, outermost first;
  `RouteInfo.layouts` lists them for a route (`''` is the app folder's own).
- **`not_found.dart` renders without any layout**, and so does every route
  **outside** the layout's folder: they bring their own `Scaffold`.
- A page-less folder with a `layout.dart` and a `data.dart` is a **section**: the
  layout waits for the data (`fespalier-data`).
- **A layout is never deferred** (since 0.7.0, `const deferred = true;` in a `route.dart` defers
  `page.dart` only): it wraps a `Navigator` (a `StatefulNavigationShell` for tabs), and a
  placeholder in its place would unmount them and their state. A tab layout's own page is deferred
  like any page, inside its branch (see `const deferred` in the `route.dart` reference of [`fespalier-routing`](../fespalier-routing/)).
- A group's routes stay together in one `ShellRoute`, so a group holding a dynamic
  route cannot be sorted around a dynamic sibling outside it: that is the usual
  "unreachable" error (`fespalier-routing`).

### The `ListTile` ink assertion

Pages render **below** their layout's `Scaffold`, so during page transitions the
layout's `Scaffold` is **not** their nearest `Material`: a `ListTile` (or `InkWell`)
trips `ListTile background color or ink splashes may be invisible ... wrapped in a
ColoredBox`. Give the page a surface of its own:

```dart
Material(type: MaterialType.transparency, child: ListView(children: [...]))
```

This is a documented gotcha of the project (`docs/troubleshooting.md`, "Things to know"); the
wrapper is what `examples/shop`'s `products/page.dart` uses.

## Tabs

A tab layout keeps **each tab's own navigation stack and state**. `tabs` orders
them, `tabOptions` sets `preload` and `initialLocation` per tab, and an exported
`container` function arranges the tabs' navigators (cross-fade, slide). Nested tab
layouts work. The rules go_router imposes (a tab's first route cannot have a
`:segment`, a root-navigator route cannot be a direct child of the shell) and every
error message are in [`references/tab-layouts.md`](references/tab-layouts.md).

```dart
const tabs = ['.', 'search', 'profile'];          // '.' is the layout folder's own page.dart
const tabOptions = {'search': TabOptions(preload: true)};

onDestinationSelected: (i) => navigationShell.goBranch(
  i,
  initialLocation: i == navigationShell.currentIndex,   // tapping the current tab pops to its root
),
```

## Transitions, dialogs, restoration

`transition.dart` is `Page<void> transition(LocalKey key, Widget child)` (plus
optional `GoRouterState state` and `bool shell`); it covers its folder and below,
nearest wins, **layout shells included** since 0.3.0 (the shell's key is
`ValueKey<String>('layout:<folder>/')`, so only entering or leaving the shell
animates it). `Transitions` has `fade`, `slide`, `none`, `material`, `cupertino`,
`sharedAxis`, `fadeThrough` (since 0.19.0), `dialog`, `sheet` and `fullscreenDialog`. A dialog or sheet route must sit **below
a page** or it opens over an empty screen. Restoration needs
`restorationScopeId` on both `MaterialApp` and `AppRoutes.router(...)`; a `Page` you
build yourself must pass `restorationId: Transitions.restorationIdOf(key)` (since 0.19.0). Since 0.8.1 a shared element is
`Route(...).hero('name', child: ...)` on each side (a `RouteHero`, which stays out of
flights in a hidden tab), and `heroes: const Heroes(onBackGesture: true)` on a `Transitions.*`
call sets how they fly; nothing flies into a dialog or sheet. `Transitions.sharedAxis` and `Transitions.fadeThrough` (since 0.19.0) are Material 3's motion over widgets alone, with a `fill:` or a `MotionFill` behind the pages. Since 0.19.0 every page and `RouteHero` honours the system's reduced motion by default (`slide` cross-fades, `dialog` and `sheet` open unanimated, heroes stop flying; `custom`'s builder is yours to guard; no opt-out). A hero that holds a network image uses
`route.imageHero(...)` (since 0.9.0, `fespalier_image`: [`fespalier-images`](../fespalier-images/SKILL.md)). All in
[`references/transitions-and-restoration.md`](references/transitions-and-restoration.md).

## Menus and breadcrumbs (`nav.dart`, since 0.8.1)

A `nav.dart` (`const nav = Nav(label: 'Products', order: 1);` and an optional
`String label(BuildContext context, {...segments})`) in a folder makes it a menu entry, and `fsp gen`
writes `AppMenu` in `app.g.dart`: `AppMenu.watch(ref, under: '(tabs)')` for drawers and tab bars
(each item has `tab`), `AppMenu.breadcrumbs(ref)` for the path to the page. Entries follow the guards
that would run for them: a sync answer is in the first frame, a `Future` shows the entry pending, a
`Ref` guard is followed. Call them in a layout or a page, never above the router. Rules, guards, traps
and the app-without-nav.dart guarantee are in
[`references/menus-and-breadcrumbs.md`](references/menus-and-breadcrumbs.md).

**Scroll restoration** (since 0.8.1): `scroll_restoration: true` in the pubspec's `fespalier:` section
wraps each page in `RouteScrollMemory`; the browser's back and forward then give a scrollable its
offset back, **only if it has a `PageStorageKey`**, and a `go` starts at the top. Same page.

## Adaptive (`fespalier_adaptive`, since 0.9.0)

The core has no adaptive API; the package `fespalier_adaptive` (a repository dependency at fespalier's tag,
no third-party dependency, generated code unchanged) draws `AppMenu.watch(ref, under: '(tabs)')` as a
`NavigationBar` under 600 logical pixels, a `NavigationRail` from 600 and a permanent `NavigationDrawer` from
1200, around the same body, so a tab keeps its state when the window is resized:

```dart
AdaptiveNavScaffold(
  shell: navigationShell,                       // or child: child, for a plain layout
  menu: (ref) => AppMenu.watch(ref, under: '(tabs)'),   // under: gives each entry its tab
  breakpoints: const NavBreakpoints(rail: 840), // optional; null means never
)
```

- **A phone's bar is hidden on a page no menu entry covers**: a `NavigationBar` cannot show "nothing
  selected". A debug build says `fespalier_adaptive: no menu entry is the current tab (3) of the tab
layout, so the navigation bar is hidden. ...` once; give the tab's folder a `nav.dart`, or render the
  menu with `AdaptiveNavBuilder`. A rail and a drawer show none selected.
- A tab folder with no `page.dart` (a heading) is a bar destination because it is a tab; in the drawer it is
  a section title over its children. Guards hide an entry or, with `NavRefused.disable`, turn it off.
- `package:fespalier_adaptive/fespalier_adaptive.dart` is the model (`AdaptiveNav`, `NavBreakpoints`,
  `AdaptiveNavBuilder`) with **no Material import**, for Cupertino or `material_ui`; `material.dart` is the
  scaffold. In a test, Flutter's default 800 x 600 window is a **rail** with the default breakpoints.

All of it, with compiled samples, is in [`references/adaptive-layouts.md`](references/adaptive-layouts.md).
Without the package, or on 0.8.x, [`references/adaptive-by-hand.md`](references/adaptive-by-hand.md) has a
bar-versus-rail tab layout whose tab state survives a resize, and a drawer-versus-side-list plain layout
that highlights the current route through `AppManifest.of(GoRouterState.of(context))`.

## Examples

- `examples/tabs`: the tab layout (`(tabs)/layout.dart`, a Library tab that is a tab layout of its own), six `nav.dart` files
  drawn by `fespalier_adaptive`, and the restoration and resize tests.
- `examples/features`: a root `layout.dart` and `nav.dart`, the `teams/$teamId` section layout, and the menu and scroll
  restoration tests.

The `fespalier` skill lists every example.

## Quick diagnosis

| Symptom                                           | Likely cause                                                                                   |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Routes do not animate (go_router 18)              | No root `transition.dart`; with Flutter's `MaterialApp` go_router 18 animates nothing          |
| Every layout shell now animates after upgrading   | 0.3.0: a `transition.dart` at or above a layout animates its shell too                         |
| A tab lost its state on switching                 | A custom `container` that does not keep every child in the tree (use `Offstage`/`Stack`)       |
| `tabs` error on a `(group)` or `$folder` tab      | The tab's first route has a `:segment`; add `tabOptions` `initialLocation` or restructure      |
| A full-screen page shows the tab bar              | It is inside the layout's folder without `navigator.dart` (or outside it, to avoid tabs)       |
| Dialog opens over a blank screen on a deep link   | The dialog route has no parent page above it in the tree                                       |
| A menu entry is missing                           | Its folder needs segments the location lacks, `inMenu: false`, or a guard refuses it           |
| No bottom bar on a phone, a rail in a test        | No menu entry is the current tab, or the test window is 800 wide (0.9.0, `fespalier_adaptive`) |
| Restored app forgets a page's local state         | Custom `Page` without `restorationId: Transitions.restorationIdOf(key)`, or renamed folders    |
| A list starts at the top after the browser's back | `scroll_restoration` is off, or the scrollable has no `PageStorageKey` (since 0.8.1)           |

For an `fsp` error message, see
[`fespalier-troubleshooting`](../fespalier-troubleshooting/).
