---
name: swift-architecture
description: "Select, implement, or migrate between app architecture patterns for Apple platform apps. Use when choosing between MV (Model-View with @Observable), MVVM, MVI, TCA (The Composable Architecture), Clean Architecture, VIPER, or Coordinator patterns; when evaluating architecture fit for a feature's complexity; when migrating from one pattern to another; or when reviewing whether an app's current architecture is appropriate. Scoped to Apple-platform patterns using Swift 6.3, SwiftUI, and UIKit."
---

# Swift Architecture

Select and implement the right architecture pattern for Apple platform apps
built with Swift 6.3 and SwiftUI or UIKit.

## Contents

- [Architecture Selection](#architecture-selection)
- [MV Pattern (Model-View with @Observable)](#mv-pattern)
- [MVVM](#mvvm)
- [MVI (Model-View-Intent)](#mvi)
- [TCA (The Composable Architecture)](#tca)
- [Clean Architecture](#clean-architecture)
- [Coordinator Pattern](#coordinator-pattern)
- [Migration Between Patterns](#migration-between-patterns)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)

## Architecture Selection

Choose based on feature complexity, team size, and testing requirements.

| Pattern | Best For | Complexity | Testability |
|---------|----------|-----------|-------------|
| **MV** | Small-to-medium SwiftUI apps, rapid iteration | Low | Moderate |
| **MVVM** | Medium apps, teams familiar with reactive patterns | Medium | High |
| **MVI** | Complex state machines, predictable state flow | Medium-High | High |
| **TCA** | Large apps needing composable features, strong testing | High | Very High |
| **Clean Architecture** | Enterprise apps, strict separation of concerns | High | Very High |
| **Coordinator** | Apps with complex navigation flows (UIKit or hybrid) | Medium | High |

**Default recommendation for new SwiftUI apps:** Start with MV (Model-View
with `@Observable`). Escalate to MVVM or TCA only when the feature's complexity
demands it.

### Decision Framework

1. **Is the feature a simple CRUD screen?** → MV pattern
2. **Does the screen have complex business logic separate from the view?** → MVVM
3. **Do you need deterministic state transitions and side-effect management?** → MVI or TCA
4. **Is the app large with many independent feature modules?** → TCA or Clean Architecture
5. **Is navigation complex with deep linking and conditional flows?** → Add Coordinator pattern

## MV Pattern

The simplest SwiftUI architecture. The view observes `@Observable` models
directly. No intermediate view model layer.

Docs: [@Observable](https://sosumi.ai/documentation/observation/observable())

```swift
import Observation
import SwiftUI

@Observable
class TripStore {
    var trips: [Trip] = []
    var isLoading = false
    var error: Error?

    private let service: TripService

    init(service: TripService) {
        self.service = service
    }

    func loadTrips() async {
        isLoading = true
        defer { isLoading = false }
        do {
            trips = try await service.fetchTrips()
        } catch {
            self.error = error
        }
    }

    func deleteTrip(_ trip: Trip) async throws {
        try await service.delete(trip)
        trips.removeAll { $0.id == trip.id }
    }
}

struct TripsView: View {
    @State private var store = TripStore(service: .live)

    var body: some View {
        List(store.trips) { trip in
            TripRow(trip: trip)
        }
        .task { await store.loadTrips() }
    }
}
```

**When MV is enough:** Single-screen features, prototype/MVP, small teams,
straightforward data flow.

**When to upgrade:** Business logic grows complex, unit testing the view's
behavior becomes difficult, multiple views need to share and transform the
same state differently.

## MVVM

Separates view logic into a `ViewModel` that the view observes. The view model
transforms model data for display and handles user actions.

```swift
@Observable
class TripListViewModel {
    private(set) var trips: [TripRowItem] = []
    private(set) var isLoading = false
    var searchText = ""

    var filteredTrips: [TripRowItem] {
        guard !searchText.isEmpty else { return trips }
        return trips.filter { $0.name.localizedStandardContains(searchText) }
    }

    private let repository: TripRepository

    init(repository: TripRepository) {
        self.repository = repository
    }

    func loadTrips() async {
        isLoading = true
        defer { isLoading = false }
        let models = (try? await repository.fetchAll()) ?? []
        trips = models.map { TripRowItem(from: $0) }
    }

    func delete(at offsets: IndexSet) async {
        let toDelete = offsets.map { filteredTrips[$0] }
        for item in toDelete {
            try? await repository.delete(id: item.id)
        }
        await loadTrips()
    }
}

struct TripRowItem: Identifiable {
    let id: UUID
    let name: String
    let dateRange: String

    init(from trip: Trip) {
        self.id = trip.id
        self.name = trip.name
        self.dateRange = trip.startDate.formatted(.dateTime.month().day())
            + " – " + trip.endDate.formatted(.dateTime.month().day())
    }
}

struct TripListView: View {
    @State private var viewModel: TripListViewModel

    init(repository: TripRepository) {
        _viewModel = State(initialValue: TripListViewModel(repository: repository))
    }

    var body: some View {
        List {
            ForEach(viewModel.filteredTrips) { item in
                Text(item.name)
            }
            .onDelete { offsets in
                Task { await viewModel.delete(at: offsets) }
            }
        }
        .searchable(text: $viewModel.searchText)
        .task { await viewModel.loadTrips() }
    }
}
```

**Testing a ViewModel:**

```swift
@Test func filteredTripsMatchesSearch() async {
    let repo = MockTripRepository(trips: [
        Trip(name: "Paris"), Trip(name: "Tokyo"), Trip(name: "Paris TX")
    ])
    let vm = TripListViewModel(repository: repo)
    await vm.loadTrips()
    vm.searchText = "Paris"
    #expect(vm.filteredTrips.count == 2)
}
```

## MVI

Unidirectional data flow: views dispatch **intents**, a **reducer** produces
new **state**, and **side effects** are handled explicitly.

```swift
@Observable
class TripListStore {
    private(set) var state = State()

    struct State {
        var trips: [Trip] = []
        var isLoading = false
        var error: String?
    }

    enum Intent {
        case loadTrips
        case deleteTrip(Trip)
        case clearError
    }

    private let service: TripService

    init(service: TripService) {
        self.service = service
    }

    func send(_ intent: Intent) {
        Task { await handle(intent) }
    }

    @MainActor
    private func handle(_ intent: Intent) async {
        switch intent {
        case .loadTrips:
            state.isLoading = true
            do {
                state.trips = try await service.fetchTrips()
            } catch {
                state.error = error.localizedDescription
            }
            state.isLoading = false

        case .deleteTrip(let trip):
            try? await service.delete(trip)
            state.trips.removeAll { $0.id == trip.id }

        case .clearError:
            state.error = nil
        }
    }
}
```

**Advantages:** Predictable state transitions, easy to log/replay intents,
clear separation of "what happened" from "what changed."

## TCA

The Composable Architecture (Point-Free) provides composable reducers,
dependency injection, exhaustive testing, and structured side effects.

Docs: [TCA](https://sosumi.ai/external/https://swiftpackageindex.com/pointfreeco/swift-composable-architecture/main/documentation/composablearchitecture)

```swift
import ComposableArchitecture

@Reducer
struct TripList {
    @ObservableState
    struct State: Equatable {
        var trips: IdentifiedArrayOf<Trip> = []
        var isLoading = false
    }

    enum Action {
        case onAppear
        case tripsLoaded([Trip])
        case deleteTrip(Trip.ID)
    }

    @Dependency(\.tripClient) var tripClient

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .onAppear:
                state.isLoading = true
                return .run { send in
                    let trips = try await tripClient.fetchAll()
                    await send(.tripsLoaded(trips))
                }
            case .tripsLoaded(let trips):
                state.trips = IdentifiedArray(uniqueElements: trips)
                state.isLoading = false
                return .none
            case .deleteTrip(let id):
                state.trips.remove(id: id)
                return .run { _ in try await tripClient.delete(id) }
            }
        }
    }
}
```

**Use TCA when:** Large team needs consistent patterns, exhaustive test
coverage is a priority, features compose from smaller features, you need
structured dependency injection across the app.

## Clean Architecture

Layers: **Domain** (entities, use cases, repository protocols) → **Data**
(repository implementations, network, persistence) → **Presentation** (views,
view models). Dependencies point inward.

```swift
// Domain layer
protocol TripRepository: Sendable {
    func fetchAll() async throws -> [Trip]
    func save(_ trip: Trip) async throws
    func delete(id: UUID) async throws
}

struct FetchUpcomingTripsUseCase: Sendable {
    private let repository: TripRepository

    init(repository: TripRepository) {
        self.repository = repository
    }

    func execute() async throws -> [Trip] {
        try await repository.fetchAll()
            .filter { $0.startDate > .now }
            .sorted { $0.startDate < $1.startDate }
    }
}

// Data layer
struct RemoteTripRepository: TripRepository {
    private let client: APIClient

    func fetchAll() async throws -> [Trip] {
        try await client.request(.get, "/trips")
    }
    // ...
}

// Presentation layer
@Observable
class UpcomingTripsViewModel {
    private(set) var trips: [Trip] = []
    private let useCase: FetchUpcomingTripsUseCase

    init(useCase: FetchUpcomingTripsUseCase) {
        self.useCase = useCase
    }

    func load() async {
        trips = (try? await useCase.execute()) ?? []
    }
}
```

**Use Clean Architecture when:** Strict separation is required (enterprise,
regulated domains), the domain layer must be testable without any framework
dependencies, or multiple presentation targets share the same business logic.

## Coordinator Pattern

Separates navigation logic from views. Especially useful in UIKit or hybrid
apps with complex navigation flows.

```swift
@MainActor
protocol Coordinator: AnyObject {
    var navigationController: UINavigationController { get }
    func start()
}

@MainActor
final class TripCoordinator: Coordinator {
    let navigationController: UINavigationController
    private let repository: TripRepository

    init(navigationController: UINavigationController, repository: TripRepository) {
        self.navigationController = navigationController
        self.repository = repository
    }

    func start() {
        let vm = TripListViewModel(repository: repository)
        vm.onSelectTrip = { [weak self] trip in
            self?.showDetail(for: trip)
        }
        let vc = TripListViewController(viewModel: vm)
        navigationController.pushViewController(vc, animated: false)
    }

    private func showDetail(for trip: Trip) {
        let vm = TripDetailViewModel(trip: trip, repository: repository)
        vm.onEdit = { [weak self] trip in self?.showEditor(for: trip) }
        let vc = TripDetailViewController(viewModel: vm)
        navigationController.pushViewController(vc, animated: true)
    }

    private func showEditor(for trip: Trip) {
        // ...
    }
}
```

In pure SwiftUI apps, `NavigationStack` with path-based routing often
replaces the Coordinator pattern. Use Coordinators when you need UIKit
integration or shared navigation logic across platforms.

## Migration Between Patterns

### ObservableObject → @Observable

```swift
// Before (iOS 16)
class TripStore: ObservableObject {
    @Published var trips: [Trip] = []
}
// View uses @ObservedObject or @StateObject

// After (iOS 17+)
@Observable
class TripStore {
    var trips: [Trip] = []
}
// View uses @State for owned, plain property for injected
```

### MVVM → MV (simplifying)

If a view model only passes through model data without transforming it,
remove the view model and let the view observe the model directly.

### MV → MVVM (scaling up)

Extract business logic and data transformation into a view model when:
- The view's `body` contains conditional logic for data formatting
- Multiple views need different projections of the same model
- You need to test logic without instantiating views

### Any → TCA

TCA adoption is typically incremental: wrap one feature's state and actions
in a `Reducer`, migrate its dependencies to `@Dependency`, and test.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `ObservableObject` in new iOS 17+ code | Use `@Observable` instead |
| View model that only forwards model properties | Remove the view model; use MV pattern |
| Massive view model with navigation, networking, and formatting | Split into focused collaborators (coordinator, service, formatter) |
| Choosing TCA for a two-screen app | Start with MV; adopt TCA when composition and testing demands justify it |
| Protocol-heavy Clean Architecture for a simple feature | Match architecture complexity to feature complexity |
| Coordinator pattern in pure SwiftUI without UIKit needs | Use `NavigationStack` path-based routing instead |
| Mixing architecture patterns inconsistently within a module | One pattern per feature module; different modules can use different patterns |

## Review Checklist

- [ ] Architecture choice is justified by feature complexity and team needs
- [ ] `@Observable` used instead of `ObservableObject` for iOS 17+ targets
- [ ] Dependencies are injected, not created internally (testability)
- [ ] Navigation logic is separated from business logic
- [ ] State mutations happen in a clear, auditable location
- [ ] View models (if present) are testable without views
- [ ] No god objects — responsibilities are distributed appropriately
- [ ] Pattern is consistent within each feature module

## References

- Apple docs: [Observation](https://sosumi.ai/documentation/observation) | [Observable](https://sosumi.ai/documentation/observation/observable())
