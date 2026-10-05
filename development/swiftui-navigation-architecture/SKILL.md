---
name: swiftui-navigation-architecture
description: 'Wire SwiftUI navigation as data on the iOS 26 / macOS 26, Swift 6 baseline: one `@Observable @MainActor` Router in `.environment`, `NavigationStack(path:)` over a typed `Route` enum, `navigationDestination(for:)` at the stack root, `item:`-driven sheets and covers, `.onOpenURL` deep links, `NavigationSplitView`, per-tab paths, `Codable` restoration. Use when wiring an App''s navigation, choosing push vs sheet vs `fullScreenCover`, adding deep links or restoration, migrating off `NavigationView`, or asked for a router / coordinator in SwiftUI. Runtime bugs → swiftui-interaction-footguns.'
---

# SwiftUI Navigation Architecture

The default navigation shape for Apps on this catalog's baseline (`apple-platform-targets`: iOS 26 / macOS 26, Swift 6 language mode): navigation state is **data** — a typed route enum in one observable router — so flows are unit-testable (assert on `[Route]`), deep-linkable (URL → routes is a pure function), and restorable (routes are `Codable`).

## When to invoke

- Wiring navigation in a new App target, or adding a second entry point (deep link, widget tap, notification, tab)
- Adding deep links / universal links or state restoration to an existing App
- Migrating off `NavigationView` or view-payload `NavigationLink(destination:)`
- Asked "how do I do a router / coordinator in SwiftUI?"

## Scope

Owns container choice (Stack / SplitView / Tab), route modeling, the router object, deep-link funneling, and restoration. Does NOT own: known interaction bugs in nav components → `swiftui-interaction-footguns`; injecting the services destination views need → `swift-dependency-injection`; nav-chrome accessibility → `ios-accessibility-engineering`.

## Pick the container

| App shape | Container |
|---|---|
| Single drill-down flow (iPhone-first) | `NavigationStack(path:)` |
| 2–5 top-level peer sections | `TabView` + one `NavigationStack` per tab, each with its own path |
| Source list → detail (iPad / Mac) | `NavigationSplitView`; sidebar selection is router state, the detail column hosts its own `NavigationStack` |

Never `NavigationView` in new code — superseded by `NavigationStack` / `NavigationSplitView` since iOS 16, deprecated in the iOS 27 SDK (Xcode 27 warns; the Xcode 26 SDK does not).

## The default shape

```swift
enum Route: Hashable, Codable {
    case board(id: UUID)      // payloads are IDs, not model objects
    case settings
}

enum Modal: String, Identifiable {  // presentation is NOT navigation
    case paywall, onboarding
    var id: String { rawValue }
}

@Observable @MainActor
final class Router {
    var path: [Route] = []
    var modal: Modal?

    // One pure mapping: URL → navigation state. Unit-test without UI.
    func open(_ url: URL) {
        guard url.scheme == "myapp" else { return }
        switch url.host {
        case "board": path = [.board(id: UUID(uuidString: url.lastPathComponent) ?? UUID())]
        case "settings": path = [.settings]
        default: break
        }
    }
}

@main struct MyApp: App {
    @State private var router = Router()

    var body: some Scene {
        WindowGroup {
            NavigationStack(path: $router.path) {
                HomeView()
                    .navigationDestination(for: Route.self) { route in
                        switch route {                 // exhaustive — compiler catches new routes
                        case .board(let id): BoardView(id: id)
                        case .settings: SettingsView()
                        }
                    }
            }
            .environment(router)
            .sheet(item: $router.modal) { ModalHost($0) }
            .onOpenURL { router.open($0) }
        }
    }
}
```

Rules the shape encodes:

- **Push with values** — `NavigationLink(value:)` or `router.path.append(...)`; never `NavigationLink(destination:)` in a path-managed stack (those pushes bypass `path`, desyncing back-stack, deep links, and restoration).
- **`navigationDestination(for:)` on the stack's root content, outside lazy containers.** Apple's docs ([navigationDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(for:destination:))): "Do not put a navigation destination modifier inside a 'lazy' container, like `List` or `LazyVStack`. … Add the navigation destination modifier outside these containers so that the navigation stack can always see the destination."
- **Typed `[Route]` over `NavigationPath`** — pattern-matchable, exhaustively switched, `Codable` for free.
- **Modal ≠ push** — presented flows hang off router optionals (`item:`-driven; one optional per presentation kind — sheet, cover, alert. Parallel `isPresented:` Bools race and can present blank); a presented flow is never a `Route` case. *Which* kind → next section.
- **Router is `@MainActor`** (it is UI state; Swift 6 enforces it), routes are `Hashable + Codable` value types. On Xcode 26's default MainActor isolation (SE-0466) this is implicit for a new project's modules — keep the explicit annotation anyway so the class stays correct if the module later turns default isolation off.

## Presentation semantics (decide per transition — iOS and macOS)

"Where does the user land when this closes?" is decided by the semantic you pick, not by the destination view. Pick the tag first; the API and its back/dismiss behavior follow.

| Semantic | API | Dismissal | iOS / iPadOS | macOS |
|---|---|---|---|---|
| **push** | `NavigationStack` + `navigationDestination` | back pops one level; edge-swipe on by default | — | same model, toolbar back |
| **sheet** | `.sheet(item:)` (+ `.presentationDetents`) | swipe-to-dismiss on by default; `interactiveDismissDisabled(true)` to force completion | detents resize; >1 detent shows the grabber | window-styled sheet — detents don't drive sizing, size the content itself |
| **full-screen cover** | `.fullScreenCover(item:)` | no interactive dismiss; exit only via explicit close | opaque, covers everything | **unavailable on native macOS** (Mac Catalyst only) — fall back to push/sheet, see below |
| **popover** | `.popover` | tap outside | collapses to a sheet in compact width unless `.presentationCompactAdaptation(.popover)` | always a true anchored popover |
| **alert** | `.alert(_:isPresented:presenting:)` | button tap only — no scrim tap, no swipe | data-drive off one optional | same |
| **dialog** | `.confirmationDialog` | Cancel **or** tap outside | bottom action sheet | rendered alert-style |
| **root-swap** | conditional root content on `@Observable` state | none — the outgoing tree is destroyed | auth gates, onboarding-done | same |

Two contract rules the table enforces:

- **"Closes on outside tap" is a semantic, not a style** — if that's the requirement, it's a `confirmationDialog` or popover, never an `.alert`, regardless of visual intent.
- **Login/logout is root-swap, not a modal.** Conditionally render `LoginView` vs `AppView` at the root off auth state: success flips the flag and the login tree is destroyed; logout flips it back and tears down the entire app stack (paths, sheets, all of it). Presenting the app *over* login couples app lifetime to a presentation and turns logout into "dismiss a modal" with login still alive underneath.

### macOS fallback for full-screen flows

A flow covered by `fullScreenCover` on iOS ships as a push (or sheet) on macOS — and Close must land on the same screen on both platforms. The trap: `dismiss()` closes the whole cover, but the pushed variant's naive `path.removeLast()` pops one level and strands the user mid-flow.

```swift
extension Router {
    // One flow, two containers: cover on iOS, push on macOS.
    func startGame(id: UUID) {
        #if os(macOS)
        path.append(.board(id: id))
        #else
        cover = .board(id: id)     // .fullScreenCover(item: $router.cover)
        #endif
    }
    func closeGame() {             // lands on the hub on BOTH platforms
        #if os(macOS)
        path.removeAll()           // pop the whole flow — pop-one strands mid-flow
        #else
        cover = nil
        #endif
    }
}
```

Route both entry and exit through router methods (as above) so no view ever encodes the platform branch.

## Deep links & restoration

- Every URL entry point (`onOpenURL`, universal links, `NSUserActivity`, notification taps) funnels into `router.open(_:)` at the scene root — one handler, one mapping function, unit tests assert `URL → [Route]` directly.
- Restoration: on `scenePhase == .background`, `JSONEncoder` the `[Route]` into `@SceneStorage`(a `String` slot); on launch, decode and assign. Routes that reference store objects carry IDs — resolve at display time and drop routes that no longer resolve instead of crashing.

## Multi-column & tabs

- `NavigationSplitView`: sidebar selection lives in the router; only the detail column hosts a `NavigationStack`. Don't nest stacks in the sidebar.
- `TabView`: the router owns `selectedTab` *and* one path per tab — paths kept in per-view `@State` reset whenever tab identity churns. Selecting the already-active tab popping to root becomes a 2-line router method.
- iPad / Mac footguns in these containers (sizeClass on Mac, inert sidebar Labels) → `swiftui-interaction-footguns`.

## Rationale

- **Navigation state as data**: view-payload links hide "where is the user" inside the view tree; a typed path makes it assertable, loggable, and reproducible from a URL or a saved session.
- **One router in `.environment`**: a single owner instead of bindings threaded through N view layers; `@Observable` keeps invalidation scoped to views that actually read `path`.
- **Typed enum over `NavigationPath`**: exhaustive `switch` in `navigationDestination` means the compiler flags every unhandled route; `NavigationPath` trades that away for type erasure most single-module apps don't need.

## Deviation considerations

- **Heterogeneous route types across feature packages** that genuinely can't share one enum → `NavigationPath` + its `CodableRepresentation` for restoration; you give up exhaustive matching.
- **A 2-screen utility** → a bare `NavigationStack` without router or path is fine; adopt the shape when the second entry point appears, not speculatively.
- **UIKit-hosted hybrids** (heavy `UIViewController` interop) → keep coordination at the UIKit layer; don't force a SwiftUI router across the hosting bridge.
- **iOS 18 / macOS 15 floor** (the catalog's `apple-platform-targets` drop-down default) → the shape works unchanged (`@Observable`, `NavigationStack` both available; only Liquid Glass presentation chrome is unavailable).
- **iOS 17 / macOS 14 floor** → still works unchanged; `@Observable` requires iOS 17.0 / macOS 14.0 as its own floor, so this is the lowest target the shape needs no changes on.
- **Below iOS 17 / macOS 14** → `ObservableObject` replaces `@Observable` for the router.
- **Mac Catalyst** → `fullScreenCover` *is* available there; the push/sheet fallback is for native (AppKit-based) macOS targets.

## Common Mistakes

1. **`NavigationView` in new code** — superseded since iOS 16, deprecated in the iOS 27 SDK (Xcode 27 warns), unpredictable column behavior. Use `NavigationStack` / `NavigationSplitView`.
2. **`navigationDestination(for:)` inside `List` / `LazyVStack`** — the lazy container may not have created the registering view yet, so pushes silently fail (runtime console warning). Register at the stack root.
3. **Mixing `NavigationLink(destination:)` into a path-based stack** — pushes invisible to `path`; back-stack count, deep links, and restoration all desync.
4. **Sheets modeled as pushed routes** — back-button vs dismiss semantics conflict; keep a separate `Modal` enum.
5. **Per-tab paths in view `@State`** — switching tabs (or any identity churn) resets the stack; paths belong to the router.
6. **`onOpenURL` sprinkled across views** — multiple competing handlers; one scene-root handler feeding one mapping function.
7. **Router not `@MainActor`** — Swift 6 isolation errors the first time a `Task` mutates `path`; annotate the class, not call sites. (Implicit under Xcode 26's default MainActor isolation — SE-0466 — but not every module opts into that default, so annotate explicitly.)
8. **Model objects as route payloads** — bloats `Hashable`/`Codable`, goes stale after edits; carry IDs and resolve at display.
9. **`@Environment(\.dismiss)` read in the presenter** — the action applies to the environment where it's declared, never to the content the presenter presented: it pops the presenter itself, closes the sheet the presenter lives in, or (macOS / iPadOS, presenter is a window's root) closes the window; only when the presenter isn't itself presented is it a no-op. Presenter-side closing = nil out the router optional.
10. **Shared Close across an iOS cover / macOS push split that pops one level** — on macOS the user lands mid-flow instead of on the hub; branch close to pop-to-landing (see the macOS fallback).
11. **Relying on automatic dismiss cascades** across stacked presentations — model `dismiss()` vs `dismissAll()` as distinct router methods; chain a follow-up presentation in the prior one's `onDismiss`, never present-while-presenting.

## Review Checklist

- [ ] No `NavigationView`; no `NavigationLink(destination:)` inside path-managed stacks
- [ ] One `Route` enum, `Hashable + Codable`; payloads are IDs, not model objects
- [ ] `navigationDestination(for:)` registered at the stack root, outside lazy containers
- [ ] Single `@Observable @MainActor` router in `.environment`; all paths (incl. per-tab) live on it
- [ ] Sheets / covers driven by `item:` off router optionals (one per presentation kind), never a `Route` case or parallel Bools
- [ ] Every transition names its presentation semantic and where close/back lands
- [ ] Full-screen flows branch per platform; Close lands identically on iOS and macOS (pop-to-landing, not pop-one)
- [ ] Auth / onboarding gates are root-swap, not modals over the app
- [ ] One `.onOpenURL` at the scene root; `URL → [Route]` mapping has unit tests
- [ ] Restoration decodes saved routes and drops unresolvable IDs gracefully
- [ ] SplitView: sidebar selection in router, stack only in detail; footguns checklist run

## Related skills

- `swiftui-interaction-footguns` — known bugs in the nav components this skill wires together
- `swift-dependency-injection` — how destination views get their services
- `apple-platform-targets` — the iOS 26 / macOS 26 baseline this shape assumes
- `ios-accessibility-engineering` — accessibility of the navigation chrome
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
