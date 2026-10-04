---
name: swiftui-patterns
category: architecture
description: Use when building native iOS with SwiftUI - small composable views, observable state models, atomic components, Swift 6.2+ concurrency, and system styling over hardcoded values
tech_stack: Swift
source: twostraws/SwiftUI-Agent-Skill (MIT), AvdLee/SwiftUI-Agent-Skill (MIT), adapted
---
# SwiftUI Patterns

## Overview

Native iOS (SwiftUI) is chosen when a task needs deep Apple-platform integration or the app is already native (see native-vs-flutter-decision). Same discipline as Flutter: small composed views, state out of the view, reusable atomic components.

**Core principle:** Views are a function of state. Data and business logic live in an observable model, not in the `View`.

## Rules

- **Small views, composed.** Extract subviews as their own `View` types (not `@ViewBuilder` funcs) so each has its own body and preview.
- **State ownership is explicit:** `@State` for local ephemeral UI only (and it is always `private`); app/business state in an `@MainActor @Observable` model injected via `init`/`@Environment`. Views send intents to the model; the model owns the logic and the networking.
- **Atomic components:** a shared component library (atoms → molecules → organisms) of reusable views. Reuse before building; grep before adding.
- **System styling over hardcoded values:** colors from the asset catalog / `Color` semantic roles, spacing/typography from a tokens file (see `mobile-design-system-foundation`) — not scattered magic numbers. Support Dynamic Type and dark mode.
- **`#Preview`** every reusable view in its key states (loading/data/error), and in the matrix: Dynamic Type `.accessibility3`, dark, `traits: .landscapeLeft`.
- **Value types** (`struct`) for models and view state; reference types only where identity is needed.
- **Never name a domain type `Task`** — it shadows `_Concurrency.Task`, which every `async`/`.task {}` call site needs; a rename (`BoardItem`, `WorkItem`, …) is a five-minute fix versus a confusing compile error later.

## Concurrency

- Follow the target's default actor isolation: a new Xcode 26 project defaults to `@MainActor` isolation, so a view model that touches UI state should be `@MainActor @Observable` explicitly rather than relying on inference holding across Swift versions.
- No GCD (`DispatchQueue.main.async`, etc.) in new code — `async`/`await`, `Task { }`, `Task.sleep(for:)`.
- Kick off async work from `.task { }` on the view, not `onAppear` + a detached `Task`.

## Worked Example

```swift
struct BoardItem: Identifiable, Sendable { let id: Int; let title: String }   // never name a model `Task`
enum LoadState<T> { case loading, empty, data(T), failed(String) }

@MainActor @Observable final class ItemListModel {
    private(set) var state: LoadState<[BoardItem]> = .loading
    private let repo: any BoardItemRepository
    init(repo: any BoardItemRepository) { self.repo = repo }
    func load() async {
        state = .loading
        do { let items = try await repo.list(); state = items.isEmpty ? .empty : .data(items) }
        catch { state = .failed(error.localizedDescription) }
    }
}

struct ItemListScreen: View {
    @State private var model: ItemListModel
    init(model: ItemListModel) { _model = State(initialValue: model) }
    var body: some View {
        Group {
            switch model.state {
            case .loading: AppSpinner()
            case .empty: ContentUnavailableView("No items yet", systemImage: "tray")
            case .failed(let message):
                ContentUnavailableView {
                    Label("Couldn't load items", systemImage: "exclamationmark.triangle")
                } description: { Text(message) } actions: {
                    Button("Try again") { Task { await model.load() } }
                }
            case .data(let items): ItemList(items: items)
            }
        }
        .task { await model.load() }
    }
}
```

Typechecks with `swiftc -swift-version 6` (verified). The original example's domain `struct Task` shadowed `_Concurrency.Task`, giving `error: missing argument for parameter 'title' in call` at every `Task { }` call site — renamed to `BoardItem` here. Note the explicit `.empty` case rendered with `ContentUnavailableView` and a retry action on `.failed`, and the `init` that seeds `State(initialValue:)` so the model can be injected.

Previews at the matrix (typechecked against the iOS 18 simulator SDK):

```swift
#Preview("Phone, AX3, dark") { ItemListScreen(model: .preview).environment(\.dynamicTypeSize, .accessibility3).preferredColorScheme(.dark) }
#Preview("Landscape", traits: .landscapeLeft) { ItemListScreen(model: .preview) }
```

For a layout that must switch at large accessibility sizes: `typeSize.isAccessibilitySize ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())`. For an icon-only control: `Button("Add to cart", systemImage: "cart.badge.plus", action:)` with `.labelStyle(.iconOnly)` and `.frame(minWidth: 44, minHeight: 44)` (see `mobile-accessibility`).

## Rules for testing

- Unit-test the `@Observable` model with a mocked repository (no UI).
- New tests in **Swift Testing** (`import Testing`, `@Test`, `#expect`) where the target already uses Xcode 16+; XCTest stays for existing UI tests and `app.performAccessibilityAudit()`. Test-first.

## Modern API

- `foregroundStyle` (not `foregroundColor`), `.clipShape(.rect(cornerRadius:))` (not `.cornerRadius`), the `Tab` API for tab bars, the two-parameter `onChange(of:) { old, new in }`, `.topBarTrailing` placement, `containerRelativeFrame` instead of `GeometryReader` when it covers the case, never `UIScreen.main.bounds`.
- `Color.withValues` is not a thing in SwiftUI (that's the Flutter equivalent) — use asset-catalog colours or `Color(.sRGB, ...)`/`.opacity()` as the repo already does.

## Liquid Glass (iOS 26+)

- Standard bars, tab views and sheets adopt Liquid Glass automatically when built with Xcode 26+. Don't paint an opaque custom background over a toolbar/tab bar to "fix" this.
- Use `.glassEffect` only on custom floating controls, and only when the task asks for it.
- `UIDesignRequiresCompatibility` is ignored when building with the iOS 27 SDK — don't rely on it to opt back out of the new look.

## Common Mistakes

- Networking or business rules inside `body` / `View`.
- `@ViewBuilder` helper funcs instead of real subviews.
- Hardcoded colors/sizes instead of asset-catalog + tokens.
- No previews, so every change needs a full build to see.
- A domain model named `Task`.
- GCD calls in new code instead of `async`/`await`.

## Red Flags

- A `View` with a URLSession call in it.
- Magic `Color(red:...)` and paddings sprinkled across views.
- A 200-line `body`.
- A type named `Task` anywhere in the diff.
