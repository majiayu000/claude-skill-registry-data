---
name: native-platform-first
description: Use before building any custom UI component, animation, gesture, modal, dropdown, or interaction. The rule is exhaust the native platform APIs first — built-in iOS/tvOS/web/Android/macOS APIs before custom code. Maintenance cost of custom compounds every OS update; the platform's primitives are designed for the affordances users already understand. Triggers on custom widget, build a [dropdown/modal/menu], "I'll write a", reaching for a custom implementation.
---

# Native Platform First

## The principle

**Every interaction = built-in platform API before custom code.**

`.searchable` before custom search bars. `<dialog>` before custom modal overlays. `.navigationTransition(.zoom)` before custom modal animation. Popover API before hand-rolled dropdowns + click-outside listeners.

If the platform doesn't provide it, accept the platform's adjacent pattern instead of building custom. **The maintenance cost of custom compounds every OS update.**

## When to invoke

Before reaching for ANY of:

- Custom dropdown / menu / popover
- Custom modal / dialog / overlay
- Custom navigation transition
- Custom drawer / sheet
- Custom focus management
- Custom click-outside detection
- Custom keyboard handling
- Custom scroll-edge effects
- Custom toolbar / nav bar / tab bar
- Custom search box

Stop. Ask: is there a native API that does 80% of this?

## Why this principle is load-bearing

Custom UI is a debt that compounds:

1. **Every OS update** can break your custom interaction in ways the platform's own components handle automatically. Custom focus traps break in iOS 17's keyboard rework. Custom click-outside listeners conflict with iOS 18's `presentationCompactAdaptation`. Custom drawer animations fight Liquid Glass compositor in iOS 26.

2. **Users have muscle memory** for native interactions. A custom dropdown that almost-but-not-quite behaves like the native one is uncanny-valley. iOS users expect ESC to dismiss, swipe-down to dismiss sheets, two-finger pan to drag-the-object — every deviation is friction.

3. **Accessibility is harder than it looks.** Native `<dialog>` ships with focus trap, ESC handling, screen-reader announcement, and `::backdrop` styling. A custom `<div>` modal ships with none of those and quietly fails WCAG.

4. **Performance**: iOS native components hand off compositing to the system in ways custom components can't. A `position: fixed` overlay on iOS Safari competes with Dynamic Island's compositor and bleeds content; the native flex-column body doesn't.

## The 80% rule

Before reaching for custom, ask: **is there a native API that does 80% of this?**

If yes → use it, accept the 20% gap as platform-native behavior the user expects.

If no → consider whether the feature can be reframed to fit a native pattern. Often the answer is yes.

If genuinely no → propose the custom build, but document WHY no native API fits, AND commit to maintaining it as the platform evolves.

## Specific examples — iOS

| Custom temptation | Native primitive |
|---|---|
| Custom search bar with text field + filter button | `Tab(role: .search)` or `.searchable(text:tokens:placement:)` |
| Custom dropdown for picking one of N | `Picker` (segmented if N ≤ 4, menu if more) |
| Custom modal overlay | `.sheet(item:)` w/ `presentationDetents` OR `.fullScreenCover(item:)` |
| Custom animation when opening detail | `.matchedTransitionSource` + `.navigationTransition(.zoom(...))` |
| Custom click-outside handling | Native dismiss (sheets auto-dismiss; popovers auto-dismiss) |
| Custom focus trap | `.focused($field)` + `FocusState` |
| Custom keyboard shortcuts | `.keyboardShortcut(_:modifiers:)` |
| Custom toolbar | `.toolbar { ToolbarItem(placement: ...) }` |
| Custom inline picker row in settings | `Picker(_:selection:)` inline (NOT a NavigationLink) |
| Custom scroll-edge fade gradient overlay | `.scrollEdgeEffectStyle(.soft\|.hard, for: .top)` (iOS 26) |
| Custom haptic feedback | `Haptic.feedback(_:)` or `.sensoryFeedback(_:trigger:)` |

## Specific examples — Web

| Custom temptation | Native primitive |
|---|---|
| Custom modal overlay div | `<dialog>` + `showModal()` (native focus trap + ESC + `::backdrop` + top layer) |
| Custom search input | `<input type="search">` with built-in clear button |
| Custom dropdown with click-outside | Popover API (`popover="auto"`) — auto-dismiss + focus + ESC + top-layer all native |
| Custom collapsible section | `<details>` / `<summary>` |
| Custom form validation | Native HTML validation (`required`, `pattern`, `:invalid`, `:valid`) |
| Custom scroll-snap behavior | CSS `scroll-snap-type` + `scroll-snap-align` |
| Custom share button | Web Share API (`navigator.share()`) with copy-link fallback |
| Custom focus visualization | `:focus-visible` (NOT `:focus` — `:focus-visible` fires for keyboard only) |
| Custom responsive component | Container queries (`@container`) — adapts to container, not viewport |
| Custom view transition | View Transitions API (`document.startViewTransition()`) |

## Specific examples — tvOS

| Custom temptation | Native primitive |
|---|---|
| Custom focus halo / glow on cards | `.hoverEffect(.highlight)` for art, `.lift` for buttons — or `.focusEffectDisabled()` + `@Environment(\.isFocused)` if truly custom; never both |
| Custom grid keyboard for search | `.searchable` — directional keyboard + free Siri dictation; custom keyboards test worse |
| Custom sidebar with manual expand logic | `TabView(.sidebarAdaptable)` (tvOS 18+/26) |
| Custom focus routing between panes | `.focusSection()` per container + `.defaultFocus` |
| Custom video transport controls | `AVPlayerViewController` — scrubber, Info panel, captions, Now Playing all free |
| Custom "press play to start" handling | `.onPlayPauseCommand` on the focused card |
| Custom Back-button behavior | Don't. Back is system-owned outside player/modal (review-rejection risk) |

## Specific examples — Android

| Custom temptation | Native primitive |
|---|---|
| Custom search bar | M3 `SearchBar` / `DockedSearchBar` |
| Custom bottom sheet | `ModalBottomSheet` |
| Custom nav-rail/drawer width switching | `NavigationSuiteScaffold` + `currentWindowAdaptiveInfo()` |
| Custom hero zoom transition | `SharedTransitionLayout` + `sharedBounds` |
| Custom pull-to-refresh | `PullToRefreshBox` |
| Custom back animation handling | Predictive back — let M3 components animate the drag |
| Custom media notification | Media3 `MediaSession` — lock-screen + media keys free |

## The failure-mode reflex

When a custom UI choice produces a bug at every iteration, that's a signal the foundation is wrong — not that the implementation needs more polish. The fix is usually to discard the custom approach and adopt the native one, not to refine the custom one further.

Real-world examples from this codebase:

- **v2.038 custom Decks drawer**: 12+ iterations of "drawer flash" bugs. Each iteration produced a new artifact. Fix was `.fullScreenCover` with native `.matchedTransitionSource` + `.zoom` — drawer abandoned entirely.

- **v2.054–v2.061 "forehead bug"**: 10+ iterations of custom hero-zoom transition logic. Each iteration produced a different layout artifact. Fix was making sure `.matchedTransitionSource` was the OUTERMOST modifier and using `.navigationTransition(.zoom(...))` exactly as documented.

- **Hero Shot sparkle overlay**: 5+ iterations of a custom CustomMaterial overlay plane producing dots (black, then colored, then differently colored). Fix was dropping the overlay entirely — there's no foundation in stock RealityKit for "a per-fragment sparkle overlay on a thin plane" that doesn't fight the alpha/blending pipeline.

## Decision tree for "do I need to build custom?"

1. **Is the user request describable in native-platform vocabulary?**

   ✓ "Show a settings sheet with a list of toggles" → `.sheet` + `Form` + `Toggle`. Done.

   ✗ "Show a settings sheet that hovers above the content with a custom blur and shrinks the underlying view" → Stop. The "shrinks the underlying view" detail isn't a native pattern. Either reframe (drop the shrink, the native sheet's elevation is enough) or commit to custom (accept the maintenance cost).

2. **Are there 2+ native components that compose?**

   Often a "custom" request is actually two natives composed. "A search bar with filter chips below" = `.searchable` + `searchScopes`. "A picker that shows a preview" = `Menu` content + `ScrollView` inside. Compose first; custom second.

3. **Will the platform release a primitive for this within ~2 years?**

   iOS 26 added native scroll-edge effects (custom blur overlays no longer needed). iOS 26 added native popover-attachment-style sheets (custom drawers redundant). If the platform is trending toward providing the primitive, building custom now is throw-away work. Use a thin native equivalent until the proper primitive ships.

## When you DO build custom

Sometimes there genuinely is no native fit. When that happens:

- **Document WHY** in DECISIONS.md ("no native API for X because Y; custom implementation here lives in Z")
- **Keep the custom layer thin** — wrap as much native behavior as possible inside, only customize the gap
- **Plan for platform updates** — flag the custom code with a TODO that re-evaluates on each major OS release
- **Test on the broadest input space** — accessibility tools, reduced-motion, increased-contrast, dynamic type, RTL layout, all OS-level toggles

## Anti-patterns

### ❌ Reaching for "I'll write a quick custom version"

The phrase "quick custom" is a tell. Custom is rarely quick. Even a 30-line custom dropdown ships with focus, click-outside, ESC, keyboard navigation, accessibility, animation, mobile-touch, and OS-update fragility issues that the native equivalent handles. The "quick" mostly comes from skipping those.

### ❌ Adding custom on top of native instead of inside it

Wrapping a native `Picker` in custom chrome ("I'll show the native menu but with my own padding and background") often fights the native component's own padding/background. Trust the native shape; customize via documented hooks (`.tint`, `.controlSize`, `.menuStyle`).

### ❌ "The native version doesn't look quite right" leading to a custom rebuild

The native version usually doesn't look "quite right" because it doesn't yet match your visual brand. The right path is making your brand fit the native pattern, not replacing the native pattern. Native sheets, menus, search bars, etc. carry user expectations that custom design alternatives violate.

### ❌ Ignoring native APIs that ship in the upcoming OS version

If your work happens during a beta cycle of the next OS, ship native-API-aware code with availability gating (`if #available`) rather than custom alternatives. The platform's beta APIs become stable quickly.

## See also

- [[binding-design-doc-discipline]] — the design doc usually has a "native first" rule encoded — quote it when proposing
- [[universal-feature-states]] — native components handle most of the loading/empty/error states for you
