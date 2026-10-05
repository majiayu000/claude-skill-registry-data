---
name: swiftui-interaction-footguns
description: 'Checklist of SwiftUI interaction bugs that pass code review but break at runtime: tap-target shrink under `.buttonStyle(.plain)`, inert sidebar `Label`s, `horizontalSizeClass` on Mac, `.task` re-fire, blank `fullScreenCover(isPresented:)` race, stale `dynamicTypeSize` in modals, `.tint` not propagating, `NSHostingView` environment. Use when reviewing a SwiftUI View for runtime interaction bugs (taps, navigation, lifecycle re-fire, presentation races) — a PR adding Button / NavigationLink / TabView / Form / NavigationSplitView, or after a smoke test surfaces a tap or navigation bug. Navigation shape itself → swiftui-navigation-architecture; general SwiftUI style / API-modernity review → swiftui-pro:swiftui-pro or swiftui-expert:swiftui-expert-skill.'
---

# SwiftUI Interaction Footguns

A class of bugs that look fine in code but break at runtime. These have shipped to production from real projects (see Sightings section). Sweep this checklist on every SwiftUI View review.

## When to invoke

- Reviewing any new or modified SwiftUI View
- Reviewing `Button` / `NavigationLink` / `TabView` / `Form` / `Menu`
- Reviewing Mac variants (`NavigationSplitView` / sidebar)
- After a macOS or iPad smoke test surfaces a tap or navigation bug
- Before declaring a Phase complete that ships new View code

## Checklist

### Tap target & hit-test

- `Button { } label: { LayoutWithSpacer }` `.buttonStyle(.plain)` → hit-test shrinks to drawn content; the Spacer-expanded area is **not** tappable. **Fix:** `.contentShape(Rectangle())` on the label's outermost container.
- Same trap for `NavigationLink`, `Menu`, and any custom interactive view with `.onTapGesture` + Spacer / `frame(maxWidth: .infinity)` / padding.
- Padding and `frame(maxWidth: .infinity)` enlarge the visual frame but do **not** automatically enlarge the hit region under `.plain`. When in doubt, add `.contentShape`.

### Accessibility identifiers (XCUITest anchors)

- An `.accessibilityIdentifier` on a **container** can cascade down and clobber its accessibility-element descendants' own identifiers — in XCUITest the children then report the container's id, and a query for the child's id finds nothing ("No matches found"). **Fix:** put the container-level id on a leaf (a title `Text`), or attach it to a zero-size `Color.clear` marker in a `.background(...)` — a *sibling* layer rather than an ancestor.
- The cascade is **conditional on the accessibility-element shape, not universal**: an id on a `ScrollView` above tappable cards can work fine. So don't reason from the view hierarchy — drive the actual XCUITest query and see which element answers.
- Conditional ids (`.accessibilityIdentifier(flag ? "x" : "")`) are fine, but if several siblings can carry the same id simultaneously, queries must use `.matching(identifier:).firstMatch` or the tap is ambiguous.

### NavigationSplitView (Mac / iPad)

- Sidebar items must be `NavigationLink(value:)` or `Button` — a bare `Label` is non-interactive even if it visually looks like a row.
- iPhone compact size class should fall back to `NavigationStack`, not split. Snapshot tests for iPhone fixtures must force `.compact` (see next item).
- Selection binding pitfall: sidebar selection and detail's path must share the same source of truth, or selection won't navigate.

### `horizontalSizeClass` on Mac

- `@Environment(\.horizontalSizeClass)` returns `.regular` for every macOS-hosted SwiftUI view — even iPhone-shaped fixtures inside `NSHostingView`. iPhone snapshot tests must inject `.compact` explicitly via `.environment(\.horizontalSizeClass, .compact)`.

### Async state load timing

- `.task { await viewModel.bootstrap() }` re-fires on every view mount / identity change. If a test pre-seeds VM state, the task overwrites it back to `.loading`. **Fix:** `hasBootstrapped` latch in the VM + a separate `retry()` method for user-driven retry.
- `.task(id:)` cancels and restarts when `id` changes — confirm that's the intent.

### Dynamic Type / AX3–AX5

- **Do NOT gate layout on `@Environment(\.dynamicTypeSize)` inside a `fullScreenCover` / `sheet` modal.** The env value can read a **stale `.large`** there even while the Text views actually scale via UIFont metrics — so a `dynamicTypeSize.isAccessibilitySize ? VStack : HStack` reflow **never fires** and labels still clip off-screen (negative-x frame). (Proved in a real project: a game board presented in a modal; cells/labels enlarged but the gate read `.large`.) Use a **geometry-driven** layout instead — `ViewThatFits(in: .horizontal) { HStack; VStack }` picks the row/column from the *actual offered width*, no env read.
- **`minimumScaleFactor` is WIDTH-driven** — it shrinks text too WIDE for its frame. It does **not** rescue a glyph that overflows **vertically**. A single digit "5" at AX5 is ~50–60pt tall in a 44pt pill → clipped top/bottom to a **blank** pill; `minimumScaleFactor` never engages and `.frame(maxHeight:)` alone just clips it.
- **Fix for compact fixed-size controls** (numeric pads, headers) that must stay legible without honoring full AX scaling: **cap the Dynamic Type** — `.dynamicTypeSize(...DynamicTypeSize.xLarge)`. The cap clamps only sizes ABOVE `.xLarge`, so default `.large` rendering — and committed snapshot baselines — stay **byte-identical**; surrounding content keeps scaling. Standard compact-numeric-control approach; geometry/UIFont-driven, so a modal's stale env can't defeat it.
- **Snapshot tests do NOT prove a Dynamic Type fix.** A snapshot that injects `DynamicTypeSize.accessibility3` into an `NSHostingView` bypasses the modal env-propagation path and gives a **false pass** (real example: three rounds passed snapshots, all failed on device). Verify AX4 and AX5 on a booted simulator instead (drive loop → `interactive-simulator-ux-audit`), eyeball the screenshot — don't trust the injected-env snapshot.
- Keep fixed-metric grids and critical regions (e.g. a fixed-metric grid) stable; let body/label text scale.

### Theme propagation to SwiftUI system controls

- `Picker`, `Button(.borderedProminent)`, `ProgressView`, `Toggle`, `Stepper` etc. follow `.tint` / `.accentColor`. A custom theme color does **not** auto-propagate — apply `.tint(<your accent Color>)` on each system control or at a high-enough ancestor.

### `NSHostingView` snapshot environment

- `colorScheme` override needs `host.appearance = NSAppearance(named: ...)` on macOS — SwiftUI's `.preferredColorScheme` does not propagate through `NSHostingView`.
- `locale` and `horizontalSizeClass` overrides must be set on the View **before** wrapping in `NSHostingView`; mutating after host creation is unreliable.

### Button / Picker styling

- `.labelsHidden()` on `Picker` when the label is provided externally (avoids duplicated label rendering on Mac).
- `.buttonStyle(.borderedProminent)` honours `.tint` from **iOS 15+ / macOS 12+**; both APIs were introduced together in SwiftUI 3.
- `.foregroundStyle(...)` chained **after** `.buttonStyle(.borderedProminent)` on the `Button` itself is silently ignored — the prominent style keeps its own default label color, even though the code compiles and unit tests pass. **Fix:** apply `.foregroundStyle` to the label content **inside** the `Button { } label: { … }` closure, not chained on the `Button` call. Only a rendered screenshot exposes the ignored-placement variant.

### `.onAppear` does not re-fire on `fullScreenCover` dismiss

- When a `fullScreenCover` dismisses back to its presenting view, that view's `.onAppear` does **not** re-fire — an `.onAppear { refresh() }` wired for "refresh when the user returns from the modal" silently never runs. (Verified on-device across repeated open/dismiss cycles; the only fresh `.onAppear` fire in that round-trip is a transient re-mount at *open*, not at dismiss.)
- **Fix:** drive post-dismiss refresh off an explicit teardown signal instead — a counter or flag the dismiss path sets, observed via `.onChange`, never `.onAppear`. Unit tests and code review both pass the wrong wiring; only an instrumented on-device or simulator run (a log probe in the refresh call, driving open→dismiss) exposes it.

### Touch target minimums

- Apple HIG (Accessibility): iOS / iPadOS default control size 44×44pt, minimum 28×28pt (macOS 28×28 / 20×20; visionOS 60×60 / 28×28); this catalog targets 44 on iOS. Buttons that look smaller due to compact text + tight padding fail accessibility audit even if visually balanced.

### View identity & `if/else`

- Branching between `if A { ViewA } else { ViewB }` gives the two branches distinct identities; state (`@State`, `.task` latches, focus) resets on switch. Use a single view with conditional modifiers when identity preservation matters.

### Sheet / fullScreenCover presentation vs data race

- `fullScreenCover(isPresented: $bool)` / `sheet(isPresented:)` driven by a **separate** optional `@State` for the content, set back-to-back (`data = x; isPresented = true`), races: the cover presents from the Bool before the optional propagates into the content closure, so `if let data { … }` renders the **empty branch** → a **blank cover**. Looks correct in code; only a runtime drive (not snapshots, not unit tests) catches it. **Fix:** make the payload `Identifiable` and use `fullScreenCover(item: $data) { data in … }` — presentation and data are then atomic. (`@MainActor` payload → mark `id` `nonisolated`.)

### `@Observable` + `@Bindable`

- Reading an `@Observable` model via `let vm = …` does not establish a binding scope; passing `vm` into a child that needs `@Bindable var vm` requires the child to redeclare with `@Bindable`. Forgetting this silently breaks two-way bindings (TextField, Toggle).
- **Swift 6 mode without the Xcode 26 template defaults** (MainActor default isolation / Approachable Concurrency): calling a nonisolated `async` method on a non-isolated view-model from `.task` (`.task { await vm.load() }`) fails with "sending 'self.vm' risks causing data races"; reading or writing the model's properties in `body` does not. **Fix:** annotate the view-model class with `@MainActor` (implicit under the Xcode 26 template defaults).

### View-model built inside a `navigationDestination` / factory closure

- **Symptom:** a screen stuck on its spinner even though the view-model actually reached `.loaded`. Confirm by logging `ObjectIdentifier(self)` in `bootstrap()` vs `ObjectIdentifier(viewModel)` in `body` — a mismatch means the VM instance `body` reads is not the one that finished loading (an orphaned VM).
- **Why:** a view-model constructed **inline inside the `.navigationDestination(for:)` closure** (or a `RouteFactory.view(for:)` that the destination calls) and stored as `@Bindable` is **re-minted on every destination re-render**. Any parent re-render gives the view a **fresh `.idle` instance**, and because the view keeps the same SwiftUI identity its `.task { bootstrap() }` does **NOT re-fire** — so it's stuck loading forever while the original (already-`.loaded`) instance is orphaned. This is a runtime-only bug: only a live drive of the app catches it; offline (no re-render trigger) it stays hidden.
- **Fix:** the destination view must **own** the VM via `@State` (first-value-wins: `_viewModel = State(wrappedValue: viewModel)`), so SwiftUI retains the first instance across destination re-invocations. Never `@Bindable` for a factory-built destination VM.

## How to apply

1. Before approving any PR touching SwiftUI Views, sweep the checklist mentally.
2. For each item that *could* apply, grep / re-read the diff for the trigger pattern.
3. If a footgun is present, flag it with a concrete fix (cite the bullet).

## Sightings (real bugs that shipped past review)

- **Tap-target shrink** — A home screen mode card used `Button { } label: { card-with-Spacer }` with `.buttonStyle(.plain)`, shrinking the tap target to drawn content only. Caught by macOS smoke test, **not** by Code Reviewer. Fix: `.contentShape(Rectangle())`.
- **Inert sidebar Labels** — Mac `NavigationSplitView` sidebar items were bare `Label`s with no `NavigationLink` / `Button`, so clicking did nothing. Same review-blind-spot path.
- **Accessibility-id cascade** — An empty-state block carried its id on the enclosing `VStack`; the two buttons inside it, each with their own ids, both reported the *container's* id and could not be tapped. Passed code review and unit tests; only a failing XCUITest surfaced it. Fix: id moved to the leaf `Text`; a later container-level anchor used a zero-size `.background` marker (sibling, not ancestor) instead.
- **Blank `fullScreenCover`** — A near-win hook presented a **blank** `fullScreenCover`: `fullScreenCover(isPresented: $bool)` + a separate optional `@State` for content, set back-to-back, raced → content closure's `if let` rendered the empty branch (a11y tree = 1 element vs 99 for a real board). Dual-model CR + unit tests passed; only the idb interactive audit caught it. Fix: `fullScreenCover(item:)` with an `Identifiable` payload.
- **Orphaned destination view-model** — a factory-built `@Bindable` view-model re-minted on every `navigationDestination` re-render; an ad banner WebView finishing its load was enough of a parent re-render to trigger it, so the screen sat on its spinner forever. Same class of bug has appeared as "transient VM loses state" in other forms. Caught only by an interactive drive with network/ads active, not by unit tests. Fix: destination view owns the VM via `@State` (see the "View-model built inside a `navigationDestination` / factory closure" checklist entry).

## Related skills

- `swiftui-navigation-architecture` — the shape these components are wired into; go there for push/sheet/cover choice, not here.
- `collaboration-skills:subagent-review-cycles` — Code Reviewer dispatch brief should explicitly name this skill when reviewing SwiftUI Views.
- `swiftui-expert:swiftui-expert-skill` (aggregated external) — broader domain skill (Instruments traces, hang/hitch profiling); different scope.
- `swiftui-pro:swiftui-pro` (aggregated external) — a broad "SwiftUI mistakes LLMs make" catalog (navigation/layout/animation/state/deprecated-API). This skill is the narrower complement: runtime-only bugs that shipped **past code review** in one project, each with a reproduction note (vmid logging, blank-`fullScreenCover` race, stale-modal Dynamic Type, idb-verify-not-snapshot). Use both.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
