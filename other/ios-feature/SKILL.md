---
name: ios-feature
description: Use when adding or changing an iOS screen or feature in a Polyforms SwiftUI app (screen, page, organism, ViewModel, client, API, fixtures, previews, tests), or taking its screenshot. The long form of stack rule 10-ios.
---

# Add an iOS feature

`Features/Settings/` is the reference: copy its shape.

## Files

```
Features/<Domain>/
  <Feature>Screen.swift       connected: ViewModel, tasks, change notices, navigation, sheets
  <Feature>ViewModel.swift    @MainActor @Observable, init(client:), state private(set)
  <Domain>Client.swift        struct of @Sendable closures, .live and .preview
  <Domain>API.swift           the only file that sees <App>GraphQL types; returns app models
  <Domain>Models.swift        Sendable app models
  <Domain>Fixtures.swift      static let preview data, shared by previews and tests
  GraphQL/<Domain>.graphql    operations
  components/organisms/       sections, rows, cards: may take a model, map to primitives
  components/pages/           whole screens, pure, one onAction over an enum
```

## The page and its screen

```swift
enum OrdersAction { case open(Order.ID); case delete(Order.ID); case refresh }

struct OrdersPage: View {
    let orders: [Order]
    let isLoading: Bool
    let errorMessage: String?
    let onAction: (OrdersAction) async -> Void
    var body: some View { /* list, EmptyState, EmptyState.failure, .refreshable */ }
}

struct OrdersScreen: View {
    @State private var viewModel = OrdersViewModel(client: .live)
    @State private var opened: Order.ID?
    var body: some View {
        OrdersPage(orders: viewModel.orders, isLoading: viewModel.isLoading,
                   errorMessage: viewModel.errorMessage) { action in
            switch action {
            case let .open(id): opened = id
            case let .delete(id): await viewModel.delete(id)
            case .refresh: await viewModel.load()
            }
        }
        .task { await viewModel.load() }
        .onReceive(NotificationCenter.default.publisher(for: .dataDidChange)) { _ in
            Task { await viewModel.load() }
        }
    }
}
```

## Loading rules in code

- Nothing yet: `ProgressView()` in the body. Failure over nothing: `EmptyState.failure`.
  Failure over rows: keep the rows, `reportError` only.
- Every mutation through `GraphQLHelpers.perform` (it posts `.dataDidChange`); a mutation
  that changes nothing a list shows passes `changesData: false`.
- A button that waits: `AsyncButton` / `AsyncToolbarButton`.
- Lists: `CursorPage`, a `LoadMoreRow`-style closer, a generation token in the ViewModel.

## Patterns

A list row, a detail page (fiche), a tab's main screen, a form: as described in rule 10-ios,
"Screen patterns". The toolbar of a detail page: `xmark` left; on the right the one repeated
action as an icon, then a `…` menu, edit first, delete last and red.

## Strings

Written in French in the code. After the build: `bun run ios:strings -- --write`, fill the
English of each new key in `Localizable.xcstrings`, rerun without `--write` until it reports
every string translated, commit the catalogue with the code.

## Tests

`<App>Tests/<Domain>/<Feature>ViewModelTests.swift` with Swift Testing: the client built
inline from `.preview` with one closure overridden; `Boom`, `Flag`, `Calls` from
`Support/TestDoubles.swift`. Never a test of a `body`.

## Screenshot

1. A temporary launch argument in `App.swift` that shows the page with its fixtures
   (`if CommandLine.arguments.contains("-shot-orders") { OrdersPage(orders: Order.previews, ...) }`).
2. Build into `/tmp/<app>-shot-<topic>` with `SWIFT_ENABLE_EXPLICIT_MODULES=NO`, install on
   the reference simulator, launch with the argument, `xcrun simctl io <udid> screenshot`.
3. Revert the harness before the commit; keep fixtures and previews.
4. Check the design conventions, send the screenshot, wait for approval.

Then `bun run ios:components` (pure and previewed) and `bun run ios:test`.
