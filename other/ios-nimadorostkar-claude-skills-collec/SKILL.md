---
name: ios
description: Use when building native iOS applications. Covers SwiftUI architecture, state management, navigation, networking, persistence, background behavior, and App Store submission requirements.
metadata:
  category: mobile
  version: 1.0.0
  tags: [ios, swiftui, mvvm, app-store, swift]
---

# iOS

## Purpose

Build iOS applications with a single source of truth for state, correct lifecycle handling, and an architecture that survives the App Review process without surprises.

## When to Use

- Building or reviewing a SwiftUI application.
- Structuring navigation, state, and dependencies.
- Handling background execution, notifications, or deep links.
- Preparing an App Store submission.

## Capabilities

- SwiftUI architecture with `@Observable` and unidirectional data flow.
- Navigation with `NavigationStack` and type-safe routes.
- Networking with async/await, retries, and offline behavior.
- Persistence: SwiftData, Core Data, Keychain.
- Background tasks, push notifications, and app lifecycle.
- App Store requirements: privacy manifest, permissions, review guidelines.

## Inputs

- The feature set and the minimum supported iOS version.
- Data requirements: offline, sync, sensitive.
- Distribution target: App Store, TestFlight, enterprise.

## Outputs

- Views that read state and emit intent; models that own the state.
- A navigation model that supports deep links by construction.
- A submission checklist covering permissions, privacy, and metadata.

## Workflow

1. **Model the state** — One `@Observable` model per screen or feature. The view derives everything it displays from it; it holds no duplicate copies.
2. **Make navigation data-driven** — `NavigationStack(path:)` with an enumerated route type. Deep linking then becomes "append to the path", not a second navigation system.
3. **Handle the lifecycle** — Work started in the foreground is suspended when the app is backgrounded. Anything that must complete needs a background task assertion or a background URL session.
4. **Design for offline** — Assume the network fails. Cache, queue writes, and reconcile. On mobile this is the normal case, not the edge case.
5. **Prepare for review** — Every permission needs a purpose string that says what the app does with it. A privacy manifest is mandatory. Rejections are almost always about permissions, purchases, or metadata.

## Best Practices

- Never do work in a view's `body`. It runs whenever SwiftUI decides it should, which is more often than you expect.
- `@State` for view-local state, `@Observable` models for anything shared. Passing a model down through six views is a sign it should be in the environment.
- Long-running work never blocks the main actor. Mark it `nonisolated` or run it in a detached task and hop back to update state.
- Store tokens in the Keychain, never in `UserDefaults`. `UserDefaults` is a plist, readable from a backup.
- Test on the oldest supported device you claim to support, not the newest simulator. Performance is a feature on a four-year-old phone.
- A permission prompt with no context is a permission denial. Explain why before the system dialog appears.

## Examples

**Type-safe, deep-linkable navigation:**

```swift
enum Route: Hashable {
    case orderList
    case order(id: String)
    case refund(orderID: String)
}

@Observable
final class Router {
    var path: [Route] = []

    func handle(_ url: URL) {
        // myapp://orders/ord_123/refund
        guard url.host == "orders" else { return }
        let parts = url.pathComponents.filter { $0 != "/" }
        guard let orderID = parts.first else { return path = [.orderList] }

        path = parts.contains("refund")
            ? [.orderList, .order(id: orderID), .refund(orderID: orderID)]
            : [.orderList, .order(id: orderID)]
    }
}

struct AppView: View {
    @State private var router = Router()

    var body: some View {
        NavigationStack(path: $router.path) {
            OrderListView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .orderList:            OrderListView()
                    case .order(let id):        OrderDetailView(orderID: id)
                    case .refund(let orderID):  RefundView(orderID: orderID)
                    }
                }
        }
        .environment(router)
        .onOpenURL { router.handle($0) }
    }
}
```

Deep links reconstruct the full back stack, so the user can navigate up naturally — a detail most hand-rolled routers get wrong.

## Notes

- A privacy manifest (`PrivacyInfo.xcprivacy`) is required for apps and for many third-party SDKs. A missing one is an automatic rejection at submission.
- `@Observable` (iOS 17+) invalidates only the views that read the changed property, unlike `ObservableObject`, which invalidates every observer. It is a material performance difference on complex screens.
- Background URL sessions continue after the app is suspended and even after it is terminated. They are the only reliable way to complete a large upload.
