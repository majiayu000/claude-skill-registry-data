---
name: ios-development
description: iOS native development expertise with Swift, SwiftUI, UIKit, and modern Apple platform patterns. Use when building iOS applications, designing UI with.
---

# iOS Development

Structured guidance for building native iOS applications with Swift, SwiftUI, UIKit, and modern Apple platform patterns. Covers project setup, declarative UI, navigation, UIKit interop, architecture, data persistence, networking, Apple framework integration, and testing strategies for production iOS applications.

## When to Use This Skill

Use this skill for:

- Setting up a new iOS project with proper Xcode configuration and Swift Package Manager dependencies
- Building declarative user interfaces with SwiftUI views, modifiers, and state management
- Implementing navigation with NavigationStack, sheets, alerts, and deep linking
- Working with UIKit view controllers, table views, collection views, and Auto Layout
- Designing MVVM architecture with @Observable, coordinators, and dependency injection
- Persisting data with SwiftData, Core Data, UserDefaults, or Keychain
- Building async/await networking layers with URLSession and Codable serialization
- Integrating Apple frameworks such as HealthKit, MapKit, StoreKit 2, or App Intents
- Writing unit tests, UI tests, and snapshot tests for iOS applications

**Trigger phrases**: "iOS app", "SwiftUI", "UIKit", "Swift Package Manager", "MVVM iOS", "SwiftData", "Core Data", "HealthKit", "MapKit", "StoreKit", "App Intents", "XCTest", "XCUITest", "NavigationStack", "async await networking", "Codable", "@Observable", "@State", "@Binding", "UICollectionView", "diffable data source", "Keychain", "push notification", "background task"

## What This Skill Does

Provides iOS development patterns including:

- **Project Setup**: Xcode project configuration, Swift Package Manager, module organization, build settings, Info.plist
- **SwiftUI Fundamentals**: Views, modifiers, property wrappers, @State/@Binding/@Observable, previews
- **Layouts and Navigation**: VStack/HStack/ZStack, LazyStacks, NavigationStack, sheets, alerts, deep linking
- **UIKit Patterns**: View controller lifecycle, diffable data sources, Auto Layout, UIKit-SwiftUI interop
- **Architecture**: MVVM with @Observable, Coordinator pattern, dependency injection, Repository pattern
- **Data and Networking**: SwiftData, Core Data, Keychain, URLSession async/await, Codable
- **Apple Frameworks**: Notifications, background tasks, HealthKit, MapKit, StoreKit 2, App Intents
- **Testing**: XCTest, Swift Testing, XCUITest, snapshot testing, async test patterns, protocol-based mocking

## Instructions

### Step 1: Project Structure and Configuration

A well-organized iOS project separates features into modules, configures build settings for each environment, and manages dependencies through Swift Package Manager.

**Recommended Project Structure**:

```
MyApp/
  MyApp.xcodeproj
  MyApp/
    App/
      MyAppApp.swift              -- @main entry point
      AppDelegate.swift           -- UIKit lifecycle hooks (if needed)
      Info.plist
    Features/
      Home/
        HomeView.swift
        HomeViewModel.swift
      Settings/
        SettingsView.swift
        SettingsViewModel.swift
    Core/
      Networking/
        APIClient.swift
        Endpoint.swift
      Persistence/
        DataStore.swift
      Models/
        User.swift
        Transaction.swift
    SharedUI/
      Components/
        PrimaryButton.swift
        LoadingOverlay.swift
      Modifiers/
        ShimmerModifier.swift
    Resources/
      Assets.xcassets
      Localizable.xcstrings
  MyAppTests/
    Features/
      HomeViewModelTests.swift
    Core/
      APIClientTests.swift
    Helpers/
      TestFixtures.swift
  MyAppUITests/
    HomeFlowTests.swift
    SettingsFlowTests.swift
  Packages/
    MyAppKit/                     -- local Swift package for shared logic
      Package.swift
      Sources/MyAppKit/
      Tests/MyAppKitTests/
```

**App Entry Point** (SwiftUI lifecycle):

```swift
import SwiftUI
import SwiftData

@main
struct MyAppApp: App {
    private let container: ModelContainer

    init() {
        do {
            let schema = Schema([User.self, Transaction.self])
            let configuration = ModelConfiguration(
                "MyApp",
                schema: schema,
                isStoredInMemoryOnly: false
            )
            container = try ModelContainer(for: schema, configurations: [configuration])
        } catch {
            fatalError("Failed to create ModelContainer: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .modelContainer(container)
        }
    }
}
```

**Swift Package Manager Configuration** (local package):

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyAppKit",
    platforms: [.iOS(.v17)],
    products: [
        .library(name: "MyAppKit", targets: ["MyAppKit"]),
    ],
    dependencies: [
        .package(url: "https://github.com/pointfreeco/swift-dependencies", from: "1.0.0"),
        .package(url: "https://github.com/apple/swift-algorithms", from: "1.2.0"),
    ],
    targets: [
        .target(
            name: "MyAppKit",
            dependencies: [
                .product(name: "Dependencies", package: "swift-dependencies"),
                .product(name: "Algorithms", package: "swift-algorithms"),
            ]
        ),
        .testTarget(
            name: "MyAppKitTests",
            dependencies: ["MyAppKit"]
        ),
    ]
)
```

**Build Configuration with xcconfig Files**:

```
// Shared.xcconfig
IPHONEOS_DEPLOYMENT_TARGET = 17.0
SWIFT_VERSION = 6.0
SWIFT_STRICT_CONCURRENCY = complete
ENABLE_USER_SCRIPT_SANDBOXING = YES

// Debug.xcconfig
#include "Shared.xcconfig"
SWIFT_OPTIMIZATION_LEVEL = -Onone
SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG
OTHER_SWIFT_FLAGS = -warn-concurrency

// Release.xcconfig
#include "Shared.xcconfig"
SWIFT_OPTIMIZATION_LEVEL = -O
SWIFT_COMPILATION_MODE = wholemodule
ENABLE_TESTABILITY = NO
```

**Info.plist Essentials**:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
</dict>
<key>NSCameraUsageDescription</key>
<string>We need camera access to scan documents.</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>We use your location to show nearby results.</string>
<key>UIBackgroundModes</key>
<array>
    <string>fetch</string>
    <string>remote-notification</string>
</array>
```

**Key Project Setup Principles**:

- Set the deployment target to iOS 17+ to use @Observable and SwiftData without backward-compatibility shims
- Enable Swift 6 strict concurrency checking (`SWIFT_STRICT_CONCURRENCY = complete`) from day one to catch data races at compile time
- Use local Swift packages to extract shared logic into testable modules with explicit dependency boundaries
- Keep the main app target thin: it should wire together feature modules but contain minimal logic itself
- Configure separate xcconfig files for Debug and Release to avoid conditional compilation scattered through code

### Step 2: SwiftUI Fundamentals

SwiftUI uses a declarative syntax where views are lightweight value types that describe the desired UI state. The framework diffs the view hierarchy and updates only what changed.

**View Composition and Modifiers**:

```swift
import SwiftUI

struct TransactionRow: View {
    let transaction: Transaction
    @Environment(\.dynamicTypeSize) private var typeSize

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: transaction.category.iconName)
                .font(.title2)
                .foregroundStyle(transaction.category.color)
                .frame(width: 40, height: 40)
                .background(transaction.category.color.opacity(0.12))
                .clipShape(Circle())

            VStack(alignment: .leading, spacing: 2) {
                Text(transaction.merchantName)
                    .font(.body)
                    .fontWeight(.medium)
                    .lineLimit(1)

                Text(transaction.date.formatted(date: .abbreviated, time: .shortened))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Text(transaction.amount, format: .currency(code: transaction.currencyCode))
                .font(.body.monospacedDigit())
                .foregroundStyle(transaction.amount < 0 ? .primary : .green)
        }
        .padding(.vertical, 4)
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(transaction.merchantName), \(transaction.amount.formatted(.currency(code: transaction.currencyCode))), \(transaction.date.formatted(date: .abbreviated, time: .shortened))")
    }
}
```

**State Management with @State, @Binding, and @Observable**:

```swift
import SwiftUI
import Observation

@Observable
final class AuthViewModel {
    var email = ""
    var password = ""
    var isLoading = false
    var errorMessage: String?

    private let authService: AuthServiceProtocol

    init(authService: AuthServiceProtocol) {
        self.authService = authService
    }

    func signIn() async {
        guard !email.isEmpty, !password.isEmpty else {
            errorMessage = "Email and password are required."
            return
        }

        isLoading = true
        errorMessage = nil

        do {
            try await authService.signIn(email: email, password: password)
        } catch let error as AuthError {
            errorMessage = error.userFacingMessage
        } catch {
            errorMessage = "An unexpected error occurred. Please try again."
        }

        isLoading = false
    }
}

struct SignInView: View {
    @State private var viewModel: AuthViewModel

    init(authService: AuthServiceProtocol) {
        _viewModel = State(initialValue: AuthViewModel(authService: authService))
    }

    var body: some View {
        Form {
            Section {
                TextField("Email", text: $viewModel.email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocorrectionDisabled()
                    .textInputAutocapitalization(.never)

                SecureField("Password", text: $viewModel.password)
                    .textContentType(.password)
            }

            if let errorMessage = viewModel.errorMessage {
                Section {
                    Label(errorMessage, systemImage: "exclamationmark.triangle")
                        .foregroundStyle(.red)
                }
            }

            Section {
                Button {
                    Task { await viewModel.signIn() }
                } label: {
                    if viewModel.isLoading {
                        ProgressView()
                            .frame(maxWidth: .infinity)
                    } else {
                        Text("Sign In")
                            .frame(maxWidth: .infinity)
                    }
                }
                .disabled(viewModel.isLoading)
            }
        }
        .navigationTitle("Sign In")
    }
}
```

**Custom Property Wrapper for UserDefaults**:

```swift
import SwiftUI

@propertyWrapper
struct AppStorage<Value: Codable> {
    private let key: String
    private let defaultValue: Value
    private let store: UserDefaults

    init(wrappedValue: Value, _ key: String, store: UserDefaults = .standard) {
        self.key = key
        self.defaultValue = wrappedValue
        self.store = store
    }

    var wrappedValue: Value {
        get {
            guard let data = store.data(forKey: key),
                  let decoded = try? JSONDecoder().decode(Value.self, from: data) else {
                return defaultValue
            }
            return decoded
        }
        set {
            if let data = try? JSONEncoder().encode(newValue) {
                store.set(data, forKey: key)
            }
        }
    }
}
```

**SwiftUI Previews with Sample Data**:

```swift
#Preview("Transaction Row - Expense") {
    List {
        TransactionRow(transaction: .preview(
            merchantName: "Whole Foods Market",
            amount: -87.32,
            category: .groceries
        ))
        TransactionRow(transaction: .preview(
            merchantName: "Monthly Salary",
            amount: 5200.00,
            category: .income
        ))
    }
}

extension Transaction {
    static func preview(
        merchantName: String = "Preview Merchant",
        amount: Double = -25.00,
        category: TransactionCategory = .general,
        currencyCode: String = "USD"
    ) -> Transaction {
        Transaction(
            id: UUID(),
            merchantName: merchantName,
            amount: Decimal(amount),
            currencyCode: currencyCode,
            category: category,
            date: .now
        )
    }
}
```

**Key SwiftUI Principles**:

- Use `@Observable` (iOS 17+) instead of `ObservableObject`/`@Published` for simpler, more efficient observation with fine-grained tracking
- Keep views small and composable. Extract subviews when a view exceeds 40 lines or when a section is reused
- Always provide accessibility labels for non-text elements and use `.accessibilityElement(children: .combine)` for composite rows
- Use `@State` for view-local state, `@Binding` for child-to-parent communication, and `@Environment` for shared values
- Prefer the `format:` parameter on `Text` for locale-aware formatting of numbers, dates, and currencies

### Step 3: SwiftUI Layouts and Navigation

SwiftUI provides stack-based layouts for composition, lazy containers for performance with large data sets, and NavigationStack for type-safe, path-based navigation.

**Stack-Based Layouts**:

```swift
import SwiftUI

struct DashboardView: View {
    let accounts: [Account]
    let recentTransactions: [Transaction]

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Horizontal scrolling account cards
                ScrollView(.horizontal, showsIndicators: false) {
                    LazyHStack(spacing: 16) {
                        ForEach(accounts) { account in
                            AccountCard(account: account)
                                .containerRelativeFrame(
                                    .horizontal,
                                    count: 1,
                                    spacing: 16
                                )
                        }
                    }
                    .scrollTargetLayout()
                }
                .scrollTargetBehavior(.viewAligned)
                .contentMargins(.horizontal, 20)

                // Recent transactions list
                LazyVStack(alignment: .leading, spacing: 0) {
                    Section {
                        ForEach(recentTransactions) { transaction in
                            TransactionRow(transaction: transaction)
                            if transaction.id != recentTransactions.last?.id {
                                Divider()
                                    .padding(.leading, 52)
                            }
                        }
                    } header: {
                        Text("Recent Transactions")
                            .font(.headline)
                            .padding(.horizontal, 20)
                            .padding(.bottom, 8)
                    }
                }
            }
            .padding(.vertical)
        }
    }
}

struct AccountCard: View {
    let account: Account

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(account.name)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                Spacer()
                Image(systemName: account.type.iconName)
                    .foregroundStyle(.secondary)
            }

            Text(account.balance, format: .currency(code: account.currencyCode))
                .font(.title.bold().monospacedDigit())

            Text("Updated \(account.lastUpdated, format: .relative(presentation: .named))")
                .font(.caption2)
                .foregroundStyle(.tertiary)
        }
        .padding()
        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 16))
    }
}
```

**NavigationStack with Type-Safe Path-Based Routing**:

```swift
import SwiftUI

enum AppRoute: Hashable {
    case transactionDetail(Transaction.ID)
    case accountDetail(Account.ID)
    case settings
    case profile
}

@Observable
final class Router {
    var path = NavigationPath()

    func navigate(to route: AppRoute) {
        path.append(route)
    }

    func popToRoot() {
        path = NavigationPath()
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }
}

struct ContentView: View {
    @State private var router = Router()
    @State private var selectedTab: Tab = .home

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack(path: $router.path) {
                HomeView()
                    .navigationDestination(for: AppRoute.self) { route in
                        switch route {
                        case .transactionDetail(let id):
                            TransactionDetailView(transactionID: id)
                        case .accountDetail(let id):
                            AccountDetailView(accountID: id)
                        case .settings:
                            SettingsView()
                        case .profile:
                            ProfileView()
                        }
                    }
            }
            .tabItem { Label("Home", systemImage: "house") }
            .tag(Tab.home)

            NavigationStack {
                SearchView()
            }
            .tabItem { Label("Search", systemImage: "magnifyingglass") }
            .tag(Tab.search)
        }
        .environment(router)
    }
}
```

**Sheets, Alerts, and Confirmations**:

```swift
import SwiftUI

struct TransactionDetailView: View {
    let transactionID: Transaction.ID
    @State private var showDeleteConfirmation = false
    @State private var showEditSheet = false
    @State private var alertItem: AlertItem?

    var body: some View {
        List {
            // Transaction detail sections...
        }
        .navigationTitle("Transaction")
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Menu {
                    Button("Edit", systemImage: "pencil") {
                        showEditSheet = true
                    }
                    Button("Delete", systemImage: "trash", role: .destructive) {
                        showDeleteConfirmation = true
                    }
                } label: {
                    Image(systemName: "ellipsis.circle")
                }
            }
        }
        .sheet(isPresented: $showEditSheet) {
            EditTransactionView(transactionID: transactionID)
                .presentationDetents([.medium, .large])
                .presentationDragIndicator(.visible)
        }
        .confirmationDialog(
            "Delete Transaction",
            isPresented: $showDeleteConfirmation,
            titleVisibility: .visible
        ) {
            Button("Delete", role: .destructive) {
                Task { await deleteTransaction() }
            }
        } message: {
            Text("This action cannot be undone.")
        }
        .alert(item: $alertItem) { item in
            Alert(
                title: Text(item.title),
                message: Text(item.message),
                dismissButton: .default(Text("OK"))
            )
        }
    }

    private func deleteTransaction() async {
        // deletion logic
    }
}

struct AlertItem: Identifiable {
    let id = UUID()
    let title: String
    let message: String
}
```

**Key Layout and Navigation Principles**:

- Use `LazyVStack` and `LazyHStack` for lists with more than a few dozen items. Lazy stacks create views on demand as they scroll into the viewport
- Use `NavigationStack` with `NavigationPath` for programmatic, type-safe navigation. Avoid the deprecated `NavigationView`
- Centralize routing logic in a `Router` object injected via `@Environment` so that any view can trigger navigation without passing closures through the hierarchy
- Use `.presentationDetents` on sheets to control their height. Half-height sheets (`.medium`) work well for quick forms
- Prefer `confirmationDialog` over `alert` for destructive actions because it presents as an action sheet on iPhone

### Step 4: UIKit Patterns

UIKit remains essential for complex custom layouts, advanced collection view compositions, and brownfield projects. Understanding view controller lifecycle, modern diffable data sources, and UIKit-SwiftUI interop is critical.

**View Controller Lifecycle**:

```swift
import UIKit

final class TransactionsViewController: UIViewController {
    private let viewModel: TransactionsViewModel
    private var collectionView: UICollectionView!
    private var dataSource: UICollectionViewDiffableDataSource<Section, Transaction.ID>!

    enum Section: Int, CaseIterable {
        case pending
        case completed
    }

    init(viewModel: TransactionsViewModel) {
        self.viewModel = viewModel
        super.init(nibName: nil, bundle: nil)
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("init(coder:) is not supported")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Transactions"
        configureCollectionView()
        configureDataSource()
        bindViewModel()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        Task { await viewModel.loadTransactions() }
    }

    // MARK: - Collection View Setup

    private func configureCollectionView() {
        var configuration = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
        configuration.headerMode = .supplementary
        configuration.trailingSwipeActionsConfigurationProvider = { [weak self] indexPath in
            self?.trailingSwipeActions(for: indexPath)
        }

        let layout = UICollectionViewCompositionalLayout.list(using: configuration)
        collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
        collectionView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(collectionView)

        NSLayoutConstraint.activate([
            collectionView.topAnchor.constraint(equalTo: view.topAnchor),
            collectionView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            collectionView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            collectionView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ])
    }

    private func trailingSwipeActions(for indexPath: IndexPath) -> UISwipeActionsConfiguration? {
        guard let transactionID = dataSource.itemIdentifier(for: indexPath) else {
            return nil
        }
        let deleteAction = UIContextualAction(style: .destructive, title: "Delete") { [weak self] _, _, completion in
            Task {
                await self?.viewModel.deleteTransaction(id: transactionID)
                completion(true)
            }
        }
        return UISwipeActionsConfiguration(actions: [deleteAction])
    }
}
```

**Diffable Data Source with Cell Registration**:

```swift
extension TransactionsViewController {
    private func configureDataSource() {
        let cellRegistration = UICollectionView.CellRegistration<UICollectionViewListCell, Transaction.ID> {
            [weak self] cell, indexPath, transactionID in

            guard let transaction = self?.viewModel.transaction(for: transactionID) else { return }

            var content = cell.defaultContentConfiguration()
            content.text = transaction.merchantName
            content.secondaryText = transaction.amount.formatted(
                .currency(code: transaction.currencyCode)
            )
            content.image = UIImage(systemName: transaction.category.iconName)
            content.imageProperties.tintColor = UIColor(transaction.category.color)
            cell.contentConfiguration = content

            cell.accessories = [.disclosureIndicator()]
        }

        let headerRegistration = UICollectionView.SupplementaryRegistration<UICollectionViewListCell>(
            elementKind: UICollectionView.elementKindSectionHeader
        ) { [weak self] headerView, _, indexPath in
            guard let section = Section(rawValue: indexPath.section) else { return }
            var content = headerView.defaultContentConfiguration()
            content.text = section == .pending ? "Pending" : "Completed"
            headerView.contentConfiguration = content
        }

        dataSource = UICollectionViewDiffableDataSource(collectionView: collectionView) {
            collectionView, indexPath, transactionID in
            collectionView.dequeueConfiguredReusableCell(
                using: cellRegistration, for: indexPath, item: transactionID
            )
        }

        dataSource.supplementaryViewProvider = { collectionView, kind, indexPath in
            collectionView.dequeueConfiguredReusableSupplementary(
                using: headerRegistration, for: indexPath
            )
        }
    }

    private func bindViewModel() {
        viewModel.onTransactionsChanged = { [weak self] pending, completed in
            guard let self else { return }
            var snapshot = NSDiffableDataSourceSnapshot<Section, Transaction.ID>()
            snapshot.appendSections(Section.allCases)
            snapshot.appendItems(pending.map(\.id), toSection: .pending)
            snapshot.appendItems(completed.map(\.id), toSection: .completed)
            self.dataSource.apply(snapshot, animatingDifferences: true)
        }
    }
}
```

**UIKit-SwiftUI Interop with UIHostingController**:

```swift
import SwiftUI
import UIKit

// Embedding SwiftUI in UIKit
final class SettingsHostingController: UIHostingController<SettingsView> {
    init(viewModel: SettingsViewModel) {
        let settingsView = SettingsView(viewModel: viewModel)
        super.init(rootView: settingsView)
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("init(coder:) is not supported")
    }
}

// Embedding UIKit in SwiftUI
struct MapViewRepresentable: UIViewRepresentable {
    let region: MKCoordinateRegion
    let annotations: [MKAnnotation]

    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        return mapView
    }

    func updateUIView(_ mapView: MKMapView, context: Context) {
        mapView.setRegion(region, animated: true)
        mapView.removeAnnotations(mapView.annotations)
        mapView.addAnnotations(annotations)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    final class Coordinator: NSObject, MKMapViewDelegate {
        func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            let identifier = "CustomPin"
            let view = mapView.dequeueReusableAnnotationView(withIdentifier: identifier)
                ?? MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
            view.annotation = annotation
            return view
        }
    }
}
```

**Key UIKit Principles**:

- Mark `init(coder:)` as `@available(*, unavailable)` on programmatic view controllers to prevent accidental storyboard instantiation
- Use `UICollectionViewDiffableDataSource` instead of the older `UITableViewDataSource` delegate pattern. Diffable data sources eliminate index-out-of-bounds crashes and provide smooth animations
- Use compositional layout (`UICollectionViewCompositionalLayout`) for all new collection views. It handles complex grid, list, and waterfall layouts without custom `UICollectionViewFlowLayout` subclasses
- Bridge UIKit views into SwiftUI with `UIViewRepresentable` and SwiftUI views into UIKit with `UIHostingController`. Always implement the coordinator pattern for delegate callbacks

### Step 5: Architecture Patterns

A clean architecture separates UI, business logic, and data access into distinct layers. On iOS, MVVM with @Observable provides the best balance of testability and SwiftUI integration.

**MVVM with @Observable**:

```swift
import Foundation
import Observation

// MARK: - Protocol for dependency injection and testing

protocol TransactionRepositoryProtocol: Sendable {
    func fetchTransactions(for accountID: Account.ID) async throws -> [Transaction]
    func deleteTransaction(id: Transaction.ID) async throws
}

// MARK: - ViewModel

@Observable
@MainActor
final class TransactionListViewModel {
    private(set) var transactions: [Transaction] = []
    private(set) var isLoading = false
    private(set) var error: AppError?

    private let repository: TransactionRepositoryProtocol
    private let accountID: Account.ID

    init(accountID: Account.ID, repository: TransactionRepositoryProtocol) {
        self.accountID = accountID
        self.repository = repository
    }

    func loadTransactions() async {
        isLoading = true
        error = nil

        do {
            transactions = try await repository.fetchTransactions(for: accountID)
        } catch {
            self.error = AppError(underlying: error)
        }

        isLoading = false
    }

    func deleteTransaction(at offsets: IndexSet) async {
        let idsToDelete = offsets.map { transactions[$0].id }

        // Optimistic UI update
        var removedTransactions: [(Int, Transaction)] = []
        for offset in offsets.sorted().reversed() {
            removedTransactions.append((offset, transactions[offset]))
            transactions.remove(at: offset)
        }

        do {
            for id in idsToDelete {
                try await repository.deleteTransaction(id: id)
            }
        } catch {
            // Rollback on failure
            for (index, transaction) in removedTransactions.reversed() {
                transactions.insert(transaction, at: index)
            }
            self.error = AppError(underlying: error)
        }
    }
}

// MARK: - View

struct TransactionListView: View {
    @State private var viewModel: TransactionListViewModel

    init(accountID: Account.ID, repository: TransactionRepositoryProtocol) {
        _viewModel = State(initialValue: TransactionListViewModel(
            accountID: accountID,
            repository: repository
        ))
    }

    var body: some View {
        Group {
            if viewModel.isLoading && viewModel.transactions.isEmpty {
                ProgressView("Loading transactions...")
            } else if let error = viewModel.error, viewModel.transactions.isEmpty {
                ContentUnavailableView {
                    Label("Unable to Load", systemImage: "exclamationmark.triangle")
                } description: {
                    Text(error.userMessage)
                } actions: {
                    Button("Retry") {
                        Task { await viewModel.loadTransactions() }
                    }
                }
            } else {
                List {
                    ForEach(viewModel.transactions) { transaction in
                        TransactionRow(transaction: transaction)
                    }
                    .onDelete { offsets in
                        Task { await viewModel.deleteTransaction(at: offsets) }
                    }
                }
                .refreshable {
                    await viewModel.loadTransactions()
                }
            }
        }
        .task { await viewModel.loadTransactions() }
        .navigationTitle("Transactions")
    }
}
```

**Coordinator Pattern for Navigation**:

```swift
import UIKit

protocol Coordinator: AnyObject {
    var childCoordinators: [any Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

final class AppCoordinator: Coordinator {
    var childCoordinators: [any Coordinator] = []
    let navigationController: UINavigationController
    private let dependencyContainer: DependencyContainer

    init(navigationController: UINavigationController, dependencyContainer: DependencyContainer) {
        self.navigationController = navigationController
        self.dependencyContainer = dependencyContainer
    }

    func start() {
        let homeCoordinator = HomeCoordinator(
            navigationController: navigationController,
            dependencyContainer: dependencyContainer
        )
        homeCoordinator.delegate = self
        childCoordinators.append(homeCoordinator)
        homeCoordinator.start()
    }
}

extension AppCoordinator: HomeCoordinatorDelegate {
    func homeCoordinatorDidRequestTransactionDetail(_ coordinator: HomeCoordinator, transactionID: Transaction.ID) {
        let detailCoordinator = TransactionDetailCoordinator(
            navigationController: navigationController,
            transactionID: transactionID,
            dependencyContainer: dependencyContainer
        )
        childCoordinators.append(detailCoordinator)
        detailCoordinator.start()
    }
}
```

**Dependency Container**:

```swift
import Foundation

@MainActor
final class DependencyContainer: Sendable {
    private let apiClient: APIClient
    private let modelContainer: ModelContainer

    init(apiClient: APIClient, modelContainer: ModelContainer) {
        self.apiClient = apiClient
        self.modelContainer = modelContainer
    }

    func makeTransactionRepository() -> TransactionRepositoryProtocol {
        TransactionRepository(apiClient: apiClient, modelContainer: modelContainer)
    }

    func makeAuthService() -> AuthServiceProtocol {
        AuthService(apiClient: apiClient)
    }

    func makeTransactionListViewModel(accountID: Account.ID) -> TransactionListViewModel {
        TransactionListViewModel(
            accountID: accountID,
            repository: makeTransactionRepository()
        )
    }
}
```

**Key Architecture Principles**:

- Define protocols for all services and repositories. View models depend on protocols, not concrete types, enabling test doubles
- Mark view models `@MainActor` and `@Observable`. The `@MainActor` annotation guarantees all property updates happen on the main thread, which SwiftUI requires
- Use optimistic UI updates for delete and toggle operations, rolling back if the server call fails
- Use the `.task` modifier to kick off async work when a view appears. SwiftUI cancels the task automatically when the view disappears
- The Coordinator pattern is most valuable in UIKit-heavy apps. In pure SwiftUI apps, the Router pattern from Step 3 serves the same purpose with less boilerplate

### Step 6: Data Persistence and Networking

iOS apps typically need local persistence for offline support and caching, secure storage for credentials, and a networking layer for API communication.

**SwiftData Model and CRUD Operations**:

```swift
import Foundation
import SwiftData

@Model
final class Transaction {
    @Attribute(.unique) var id: UUID
    var merchantName: String
    var amount: Decimal
    var currencyCode: String
    var category: TransactionCategory
    var date: Date
    var note: String?

    @Relationship(deleteRule: .nullify, inverse: \Account.transactions)
    var account: Account?

    init(
        id: UUID = UUID(),
        merchantName: String,
        amount: Decimal,
        currencyCode: String,
        category: TransactionCategory,
        date: Date,
        note: String? = nil
    ) {
        self.id = id
        self.merchantName = merchantName
        self.amount = amount
        self.currencyCode = currencyCode
        self.category = category
        self.date = date
        self.note = note
    }
}

@Model
final class Account {
    @Attribute(.unique) var id: UUID
    var name: String
    var balance: Decimal
    var currencyCode: String
    var lastUpdated: Date

    @Relationship(deleteRule: .cascade)
    var transactions: [Transaction] = []

    init(id: UUID = UUID(), name: String, balance: Decimal, currencyCode: String) {
        self.id = id
        self.name = name
        self.balance = balance
        self.currencyCode = currencyCode
        self.lastUpdated = .now
    }
}

// SwiftData queries in SwiftUI
struct TransactionListSwiftDataView: View {
    @Query(
        filter: #Predicate<Transaction> { $0.amount < 0 },
        sort: \Transaction.date,
        order: .reverse
    )
    private var expenses: [Transaction]

    @Environment(\.modelContext) private var modelContext

    var body: some View {
        List {
            ForEach(expenses) { transaction in
                TransactionRow(transaction: transaction)
            }
            .onDelete(perform: deleteTransactions)
        }
    }

    private func deleteTransactions(at offsets: IndexSet) {
        for index in offsets {
            modelContext.delete(expenses[index])
        }
    }
}
```

**Keychain Wrapper for Secure Storage**:

```swift
import Foundation
import Security

enum KeychainError: Error {
    case duplicateItem
    case itemNotFound
    case unexpectedStatus(OSStatus)
    case invalidData
}

struct KeychainManager {
    static func save(_ data: Data, for key: String, accessGroup: String? = nil) throws {
        var query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrAccount: key,
            kSecValueData: data,
            kSecAttrAccessible: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
        ]
        if let accessGroup {
            query[kSecAttrAccessGroup] = accessGroup
        }

        let status = SecItemAdd(query as CFDictionary, nil)
        if status == errSecDuplicateItem {
            let updateQuery: [CFString: Any] = [
                kSecClass: kSecClassGenericPassword,
                kSecAttrAccount: key,
            ]
            let updateAttributes: [CFString: Any] = [kSecValueData: data]
            let updateStatus = SecItemUpdate(updateQuery as CFDictionary, updateAttributes as CFDictionary)
            guard updateStatus == errSecSuccess else {
                throw KeychainError.unexpectedStatus(updateStatus)
            }
        } else if status != errSecSuccess {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    static func load(for key: String) throws -> Data {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrAccount: key,
            kSecReturnData: true,
            kSecMatchLimit: kSecMatchLimitOne,
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess else {
            if status == errSecItemNotFound {
                throw KeychainError.itemNotFound
            }
            throw KeychainError.unexpectedStatus(status)
        }
        guard let data = result as? Data else {
            throw KeychainError.invalidData
        }
        return data
    }

    static func delete(for key: String) throws {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrAccount: key,
        ]
        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unexpectedStatus(status)
        }
    }
}
```

**Async/Await Networking Layer**:

```swift
import Foundation

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
}

struct Endpoint {
    let path: String
    let method: HTTPMethod
    let queryItems: [URLQueryItem]?
    let body: (any Encodable)?
    let headers: [String: String]

    init(
        path: String,
        method: HTTPMethod = .get,
        queryItems: [URLQueryItem]? = nil,
        body: (any Encodable)? = nil,
        headers: [String: String] = [:]
    ) {
        self.path = path
        self.method = method
        self.queryItems = queryItems
        self.body = body
        self.headers = headers
    }
}

enum APIError: Error, LocalizedError {
    case invalidURL
    case httpError(statusCode: Int, data: Data)
    case decodingError(DecodingError)
    case networkError(URLError)
    case unauthorized
    case serverError(statusCode: Int)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid request URL."
        case .httpError(let code, _):
            return "Server returned status \(code)."
        case .decodingError:
            return "Failed to parse server response."
        case .networkError(let urlError):
            return urlError.localizedDescription
        case .unauthorized:
            return "Your session has expired. Please sign in again."
        case .serverError(let code):
            return "Server error (\(code)). Please try again later."
        }
    }
}

actor APIClient {
    private let baseURL: URL
    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder
    private let tokenProvider: TokenProviderProtocol

    init(
        baseURL: URL,
        session: URLSession = .shared,
        tokenProvider: TokenProviderProtocol
    ) {
        self.baseURL = baseURL
        self.session = session
        self.tokenProvider = tokenProvider

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder = decoder

        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.keyEncodingStrategy = .convertToSnakeCase
        self.encoder = encoder
    }

    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        var components = URLComponents(url: baseURL.appending(path: endpoint.path), resolvingAgainstBaseURL: false)
        components?.queryItems = endpoint.queryItems

        guard let url = components?.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let token = try await tokenProvider.currentToken()
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")

        for (key, value) in endpoint.headers {
            request.setValue(value, forHTTPHeaderField: key)
        }

        if let body = endpoint.body {
            request.httpBody = try encoder.encode(body)
        }

        let (data, response): (Data, URLResponse)
        do {
            (data, response) = try await session.data(for: request)
        } catch let error as URLError {
            throw APIError.networkError(error)
        }

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidURL
        }

        switch httpResponse.statusCode {
        case 200..<300:
            break
        case 401:
            throw APIError.unauthorized
        case 500..<600:
            throw APIError.serverError(statusCode: httpResponse.statusCode)
        default:
            throw APIError.httpError(statusCode: httpResponse.statusCode, data: data)
        }

        do {
            return try decoder.decode(T.self, from: data)
        } catch let error as DecodingError {
            throw APIError.decodingError(error)
        }
    }
}
```

**Repository Pattern Combining Remote and Local Data**:

```swift
import Foundation
import SwiftData

struct TransactionRepository: TransactionRepositoryProtocol {
    private let apiClient: APIClient
    private let modelContainer: ModelContainer

    init(apiClient: APIClient, modelContainer: ModelContainer) {
        self.apiClient = apiClient
        self.modelContainer = modelContainer
    }

    func fetchTransactions(for accountID: Account.ID) async throws -> [Transaction] {
        // Try network first, fall back to cache
        do {
            let response: TransactionsResponse = try await apiClient.request(
                Endpoint(path: "/accounts/\(accountID)/transactions")
            )
            try await cacheTransactions(response.transactions, for: accountID)
            return response.transactions
        } catch is APIError {
            return try await loadCachedTransactions(for: accountID)
        }
    }

    @ModelActor
    private actor DataStoreActor {
        func cacheTransactions(_ transactions: [Transaction], for accountID: Account.ID) throws {
            for transaction in transactions {
                modelContext.insert(transaction)
            }
            try modelContext.save()
        }

        func loadCachedTransactions(for accountID: Account.ID) throws -> [Transaction] {
            let descriptor = FetchDescriptor<Transaction>(
                predicate: #Predicate { $0.account?.id == accountID },
                sortBy: [SortDescriptor(\.date, order: .reverse)]
            )
            return try modelContext.fetch(descriptor)
        }
    }

    private func cacheTransactions(_ transactions: [Transaction], for accountID: Account.ID) async throws {
        let actor = DataStoreActor(modelContainer: modelContainer)
        try await actor.cacheTransactions(transactions, for: accountID)
    }

    private func loadCachedTransactions(for accountID: Account.ID) async throws -> [Transaction] {
        let actor = DataStoreActor(modelContainer: modelContainer)
        return try await actor.loadCachedTransactions(for: accountID)
    }
}
```

**Key Persistence and Networking Principles**:

- Use SwiftData for structured local persistence. It integrates with SwiftUI via `@Query` and `@Model`, providing automatic change tracking
- Store authentication tokens and sensitive credentials in the Keychain, never in UserDefaults or plain files
- Make the `APIClient` an actor to ensure thread-safe access to mutable state such as token refresh logic
- Use the Repository pattern to abstract whether data comes from the network or local cache. Views and view models never call the API client directly
- Configure `JSONDecoder` with `.convertFromSnakeCase` and `JSONEncoder` with `.convertToSnakeCase` once at the client level to avoid per-endpoint boilerplate

### Step 7: Apple Frameworks Integration

iOS provides specialized frameworks that require careful integration. Each framework has its own permission model, lifecycle requirements, and best practices.

**Push Notifications**:

```swift
import UserNotifications
import UIKit

final class NotificationManager: NSObject, UNUserNotificationCenterDelegate, Sendable {
    static let shared = NotificationManager()

    func requestAuthorization() async throws -> Bool {
        let center = UNUserNotificationCenter.current()
        center.delegate = self
        let granted = try await center.requestAuthorization(options: [.alert, .badge, .sound])
        if granted {
            await MainActor.run {
                UIApplication.shared.registerForRemoteNotifications()
            }
        }
        return granted
    }

    func scheduleLocalNotification(
        title: String,
        body: String,
        triggerDate: Date,
        identifier: String
    ) async throws {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let components = Calendar.current.dateComponents(
            [.year, .month, .day, .hour, .minute],
            from: triggerDate
        )
        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)
        let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)

        try await UNUserNotificationCenter.current().add(request)
    }

    // Handle notification when app is in foreground
    nonisolated func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        [.banner, .badge, .sound]
    }

    // Handle notification tap
    nonisolated func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        let userInfo = response.notification.request.content.userInfo
        // Route to appropriate screen based on notification payload
        if let transactionID = userInfo["transaction_id"] as? String {
            await MainActor.run {
                NotificationCenter.default.post(
                    name: .didTapTransactionNotification,
                    object: nil,
                    userInfo: ["transactionID": transactionID]
                )
            }
        }
    }
}
```

**Background Tasks with BGTaskScheduler**:

```swift
import BackgroundTasks

enum BackgroundTaskIdentifier {
    static let refresh = "com.myapp.refresh"
    static let sync = "com.myapp.datasync"
}

final class BackgroundTaskManager {
    static func registerTasks() {
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: BackgroundTaskIdentifier.refresh,
            using: nil
        ) { task in
            guard let appRefreshTask = task as? BGAppRefreshTask else { return }
            handleAppRefresh(task: appRefreshTask)
        }

        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: BackgroundTaskIdentifier.sync,
            using: nil
        ) { task in
            guard let processingTask = task as? BGProcessingTask else { return }
            handleDataSync(task: processingTask)
        }
    }

    static func scheduleAppRefresh() {
        let request = BGAppRefreshTaskRequest(identifier: BackgroundTaskIdentifier.refresh)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // 15 minutes
        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            // Log scheduling failure; do not crash
        }
    }

    private static func handleAppRefresh(task: BGAppRefreshTask) {
        scheduleAppRefresh() // Schedule the next refresh

        let refreshTask = Task {
            do {
                let repository = DependencyContainer.shared.makeTransactionRepository()
                _ = try await repository.fetchTransactions(for: .currentUser)
                task.setTaskCompleted(success: true)
            } catch {
                task.setTaskCompleted(success: false)
            }
        }

        task.expirationHandler = {
            refreshTask.cancel()
        }
    }

    private static func handleDataSync(task: BGProcessingTask) {
        let syncTask = Task {
            do {
                let syncService = DependencyContainer.shared.makeSyncService()
                try await syncService.performFullSync()
                task.setTaskCompleted(success: true)
            } catch {
                task.setTaskCompleted(success: false)
            }
        }

        task.expirationHandler = {
            syncTask.cancel()
        }
    }
}
```

**StoreKit 2 In-App Purchases**:

```swift
import StoreKit

@Observable
@MainActor
final class StoreManager {
    private(set) var products: [Product] = []
    private(set) var purchasedProductIDs: Set<String> = []
    private var transactionListener: Task<Void, Never>?

    private let productIDs: Set<String> = [
        "com.myapp.premium.monthly",
        "com.myapp.premium.yearly",
    ]

    init() {
        transactionListener = listenForTransactions()
    }

    deinit {
        transactionListener?.cancel()
    }

    func loadProducts() async {
        do {
            products = try await Product.products(for: productIDs)
                .sorted { $0.price < $1.price }
        } catch {
            products = []
        }
    }

    func purchase(_ product: Product) async throws -> StoreKit.Transaction? {
        let result = try await product.purchase()

        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            purchasedProductIDs.insert(transaction.productID)
            await transaction.finish()
            return transaction

        case .userCancelled:
            return nil

        case .pending:
            return nil

        @unknown default:
            return nil
        }
    }

    func restorePurchases() async {
        for await result in Transaction.currentEntitlements {
            if let transaction = try? checkVerified(result) {
                purchasedProductIDs.insert(transaction.productID)
            }
        }
    }

    var isPremium: Bool {
        !purchasedProductIDs.isEmpty
    }

    private func listenForTransactions() -> Task<Void, Never> {
        Task.detached { [weak self] in
            for await result in Transaction.updates {
                if let transaction = try? self?.checkVerified(result) {
                    await MainActor.run {
                        self?.purchasedProductIDs.insert(transaction.productID)
                    }
                    await transaction.finish()
                }
            }
        }
    }

    private func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
        switch result {
        case .unverified:
            throw StoreError.failedVerification
        case .verified(let value):
            return value
        }
    }
}

enum StoreError: Error {
    case failedVerification
}
```

**App Intents for Shortcuts**:

```swift
import AppIntents

struct ViewBalanceIntent: AppIntent {
    static let title: LocalizedStringResource = "View Account Balance"
    static let description = IntentDescription("Shows the current balance of a selected account.")

    @Parameter(title: "Account")
    var account: AccountEntity

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let repository = DependencyContainer.shared.makeAccountRepository()
        let balance = try await repository.fetchBalance(for: account.id)
        let formatted = balance.formatted(.currency(code: account.currencyCode))
        return .result(dialog: "Your \(account.name) balance is \(formatted).")
    }
}

struct AccountEntity: AppEntity {
    static let typeDisplayRepresentation = TypeDisplayRepresentation(name: "Account")
    static let defaultQuery = AccountQuery()

    let id: UUID
    let name: String
    let currencyCode: String

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(name)")
    }
}

struct AccountQuery: EntityQuery {
    func entities(for identifiers: [UUID]) async throws -> [AccountEntity] {
        let repository = DependencyContainer.shared.makeAccountRepository()
        let accounts = try await repository.fetchAccounts()
        return accounts
            .filter { identifiers.contains($0.id) }
            .map { AccountEntity(id: $0.id, name: $0.name, currencyCode: $0.currencyCode) }
    }

    func suggestedEntities() async throws -> [AccountEntity] {
        let repository = DependencyContainer.shared.makeAccountRepository()
        let accounts = try await repository.fetchAccounts()
        return accounts.map { AccountEntity(id: $0.id, name: $0.name, currencyCode: $0.currencyCode) }
    }
}

struct MyAppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: ViewBalanceIntent(),
            phrases: [
                "Show my balance in \(.applicationName)",
                "Check \(\.$account) balance in \(.applicationName)",
            ],
            shortTitle: "View Balance",
            systemImageName: "dollarsign.circle"
        )
    }
}
```

**Key Framework Integration Principles**:

- Always request permissions at the moment of use, not at app launch. Explain why the permission is needed before showing the system prompt
- Register background tasks in `application(_:didFinishLaunchingWithOptions:)` or early in the app lifecycle. Always reschedule the next occurrence inside the handler
- Use StoreKit 2 (the async/await API) for all new in-app purchase implementations. StoreKit 2 handles receipt validation server-side via `VerificationResult`
- App Intents enable Siri Shortcuts and Spotlight integration. Define intents for the three to five most common actions users perform in your app
- Always listen for `Transaction.updates` on app launch to handle purchases that completed while the app was not running

### Step 8: Testing

Comprehensive testing on iOS combines unit tests with XCTest or Swift Testing, UI tests with XCUITest, and protocol-based mocking for dependency isolation.

**Unit Tests with Swift Testing Framework**:

```swift
import Testing
@testable import MyApp

@Suite("TransactionListViewModel")
struct TransactionListViewModelTests {
    let mockRepository: MockTransactionRepository

    init() {
        mockRepository = MockTransactionRepository()
    }

    @Test("loads transactions on initial fetch")
    @MainActor
    func loadTransactions() async {
        let expected = [
            Transaction.preview(merchantName: "Coffee Shop", amount: -4.50),
            Transaction.preview(merchantName: "Salary", amount: 5000.00),
        ]
        mockRepository.stubbedTransactions = expected

        let viewModel = TransactionListViewModel(
            accountID: UUID(),
            repository: mockRepository
        )

        await viewModel.loadTransactions()

        #expect(viewModel.transactions.count == 2)
        #expect(viewModel.transactions[0].merchantName == "Coffee Shop")
        #expect(viewModel.isLoading == false)
        #expect(viewModel.error == nil)
    }

    @Test("sets error state when fetch fails")
    @MainActor
    func loadTransactionsFailure() async {
        mockRepository.stubbedError = APIError.networkError(URLError(.notConnectedToInternet))

        let viewModel = TransactionListViewModel(
            accountID: UUID(),
            repository: mockRepository
        )

        await viewModel.loadTransactions()

        #expect(viewModel.transactions.isEmpty)
        #expect(viewModel.error != nil)
        #expect(viewModel.isLoading == false)
    }

    @Test("deletes transaction with optimistic update")
    @MainActor
    func deleteTransaction() async {
        let transactions = [
            Transaction.preview(merchantName: "Item 1"),
            Transaction.preview(merchantName: "Item 2"),
            Transaction.preview(merchantName: "Item 3"),
        ]
        mockRepository.stubbedTransactions = transactions

        let viewModel = TransactionListViewModel(
            accountID: UUID(),
            repository: mockRepository
        )
        await viewModel.loadTransactions()

        await viewModel.deleteTransaction(at: IndexSet(integer: 1))

        #expect(viewModel.transactions.count == 2)
        #expect(viewModel.transactions.contains(where: { $0.merchantName == "Item 2" }) == false)
    }

    @Test("rolls back optimistic delete on failure")
    @MainActor
    func deleteTransactionRollback() async {
        let transactions = [
            Transaction.preview(merchantName: "Item 1"),
            Transaction.preview(merchantName: "Item 2"),
        ]
        mockRepository.stubbedTransactions = transactions
        mockRepository.stubbedDeleteError = APIError.serverError(statusCode: 500)

        let viewModel = TransactionListViewModel(
            accountID: UUID(),
            repository: mockRepository
        )
        await viewModel.loadTransactions()

        await viewModel.deleteTransaction(at: IndexSet(integer: 0))

        #expect(viewModel.transactions.count == 2, "Transaction should be restored after failed delete")
        #expect(viewModel.error != nil)
    }
}
```

**Protocol-Based Mocking**:

```swift
@testable import MyApp

final class MockTransactionRepository: TransactionRepositoryProtocol, @unchecked Sendable {
    var stubbedTransactions: [Transaction] = []
    var stubbedError: Error?
    var stubbedDeleteError: Error?
    var fetchCallCount = 0
    var deletedIDs: [Transaction.ID] = []

    func fetchTransactions(for accountID: Account.ID) async throws -> [Transaction] {
        fetchCallCount += 1
        if let error = stubbedError {
            throw error
        }
        return stubbedTransactions
    }

    func deleteTransaction(id: Transaction.ID) async throws {
        if let error = stubbedDeleteError {
            throw error
        }
        deletedIDs.append(id)
    }
}

final class MockAPIClient: APIClientProtocol, @unchecked Sendable {
    var stubbedResponses: [String: Any] = [:]
    var stubbedErrors: [String: Error] = [:]
    var requestLog: [(path: String, method: HTTPMethod)] = []

    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        requestLog.append((path: endpoint.path, method: endpoint.method))

        if let error = stubbedErrors[endpoint.path] {
            throw error
        }
        guard let response = stubbedResponses[endpoint.path] as? T else {
            throw APIError.decodingError(
                DecodingError.dataCorrupted(.init(codingPath: [], debugDescription: "No stub"))
            )
        }
        return response
    }
}
```

**XCTest Unit Tests** (for projects not yet on Swift Testing):

```swift
import XCTest
@testable import MyApp

final class APIClientTests: XCTestCase {
    private var sut: APIClient!
    private var mockSession: URLSession!
    private var mockTokenProvider: MockTokenProvider!

    override func setUp() {
        super.setUp()
        let configuration = URLSessionConfiguration.ephemeral
        configuration.protocolClasses = [MockURLProtocol.self]
        mockSession = URLSession(configuration: configuration)
        mockTokenProvider = MockTokenProvider(token: "test-token")
        sut = APIClient(
            baseURL: URL(string: "https://api.example.com")!,
            session: mockSession,
            tokenProvider: mockTokenProvider
        )
    }

    override func tearDown() {
        MockURLProtocol.requestHandler = nil
        sut = nil
        super.tearDown()
    }

    func testSuccessfulRequest() async throws {
        let expectedUser = UserDTO(id: "user-1", name: "Alice", email: "alice@example.com")
        let data = try JSONEncoder().encode(expectedUser)

        MockURLProtocol.requestHandler = { request in
            XCTAssertEqual(request.value(forHTTPHeaderField: "Authorization"), "Bearer test-token")
            let response = HTTPURLResponse(
                url: request.url!,
                statusCode: 200,
                httpVersion: nil,
                headerFields: nil
            )!
            return (response, data)
        }

        let result: UserDTO = try await sut.request(Endpoint(path: "/users/user-1"))
        XCTAssertEqual(result.id, "user-1")
        XCTAssertEqual(result.name, "Alice")
    }

    func testUnauthorizedThrowsError() async {
        MockURLProtocol.requestHandler = { request in
            let response = HTTPURLResponse(
                url: request.url!,
                statusCode: 401,
                httpVersion: nil,
                headerFields: nil
            )!
            return (response, Data())
        }

        do {
            let _: UserDTO = try await sut.request(Endpoint(path: "/me"))
            XCTFail("Expected APIError.unauthorized")
        } catch {
            XCTAssertTrue(error is APIError)
            if case APIError.unauthorized = error { } else {
                XCTFail("Expected .unauthorized, got \(error)")
            }
        }
    }
}

final class MockURLProtocol: URLProtocol {
    nonisolated(unsafe) static var requestHandler: ((URLRequest) throws -> (HTTPURLResponse, Data))?

    override class func canInit(with request: URLRequest) -> Bool { true }
    override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }

    override func startLoading() {
        guard let handler = Self.requestHandler else {
            client?.urlProtocol(self, didFailWithError: URLError(.unknown))
            return
        }
        do {
            let (response, data) = try handler(request)
            client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
            client?.urlProtocol(self, didLoad: data)
            client?.urlProtocolDidFinishLoading(self)
        } catch {
            client?.urlProtocol(self, didFailWithError: error)
        }
    }

    override func stopLoading() {}
}
```

**UI Testing with XCUITest**:

```swift
import XCTest

final class TransactionFlowUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--uitesting"]
        app.launchEnvironment = ["API_BASE_URL": "http://localhost:8080"]
        app.launch()
    }

    func testViewTransactionDetail() {
        // Navigate to transactions tab
        let transactionsTab = app.tabBars.buttons["Transactions"]
        XCTAssertTrue(transactionsTab.waitForExistence(timeout: 5))
        transactionsTab.tap()

        // Wait for list to load
        let firstTransaction = app.cells.firstMatch
        XCTAssertTrue(firstTransaction.waitForExistence(timeout: 10))

        // Tap to view detail
        firstTransaction.tap()

        // Verify detail screen
        let merchantLabel = app.staticTexts["merchantName"]
        XCTAssertTrue(merchantLabel.waitForExistence(timeout: 5))

        let amountLabel = app.staticTexts["amount"]
        XCTAssertTrue(amountLabel.exists)
    }

    func testDeleteTransaction() {
        let transactionsTab = app.tabBars.buttons["Transactions"]
        XCTAssertTrue(transactionsTab.waitForExistence(timeout: 5))
        transactionsTab.tap()

        let firstCell = app.cells.firstMatch
        XCTAssertTrue(firstCell.waitForExistence(timeout: 10))

        let initialCount = app.cells.count

        // Swipe to delete
        firstCell.swipeLeft()
        let deleteButton = app.buttons["Delete"]
        XCTAssertTrue(deleteButton.waitForExistence(timeout: 3))
        deleteButton.tap()

        // Confirm deletion dialog
        let confirmButton = app.buttons["Delete"].firstMatch
        if confirmButton.waitForExistence(timeout: 3) {
            confirmButton.tap()
        }

        // Verify count decreased
        let expectation = XCTNSPredicateExpectation(
            predicate: NSPredicate(format: "count < %d", initialCount),
            object: app.cells
        )
        wait(for: [expectation], timeout: 5)
    }

    func testPullToRefresh() {
        let transactionsTab = app.tabBars.buttons["Transactions"]
        XCTAssertTrue(transactionsTab.waitForExistence(timeout: 5))
        transactionsTab.tap()

        let firstCell = app.cells.firstMatch
        XCTAssertTrue(firstCell.waitForExistence(timeout: 10))

        // Pull to refresh
        firstCell.swipeDown()

        // Verify refresh indicator appeared and data reloaded
        let refreshedCell = app.cells.firstMatch
        XCTAssertTrue(refreshedCell.waitForExistence(timeout: 10))
    }
}
```

**Async Test Patterns**:

```swift
import Testing
@testable import MyApp

@Suite("APIClient Async Patterns")
struct APIClientAsyncTests {
    @Test("cancels in-flight request when task is cancelled")
    func cancellation() async {
        let client = APIClient(
            baseURL: URL(string: "https://api.example.com")!,
            session: .shared,
            tokenProvider: MockTokenProvider(token: "token")
        )

        let task = Task {
            let _: UserDTO = try await client.request(
                Endpoint(path: "/slow-endpoint")
            )
        }

        // Cancel immediately
        task.cancel()

        let result = await task.result
        switch result {
        case .success:
            Issue.record("Expected cancellation error")
        case .failure(let error):
            #expect(error is CancellationError || (error as? URLError)?.code == .cancelled)
        }
    }

    @Test("retries request up to max attempts on transient failure")
    func retryLogic() async throws {
        var attemptCount = 0
        let mockSession = MockRetryURLSession { _ in
            attemptCount += 1
            if attemptCount < 3 {
                throw URLError(.networkConnectionLost)
            }
            return (
                HTTPURLResponse(
                    url: URL(string: "https://api.example.com/data")!,
                    statusCode: 200,
                    httpVersion: nil,
                    headerFields: nil
                )!,
                try JSONEncoder().encode(["status": "ok"])
            )
        }

        // Test with retry-enabled client
        #expect(attemptCount == 0)
        // After performing request with retry logic...
        #expect(attemptCount == 3)
    }
}
```

**Key Testing Principles**:

- Use Swift Testing (`@Test`, `#expect`, `@Suite`) for all new tests. It provides clearer syntax, parameterized tests, and better diagnostics than XCTest
- Mock at the protocol boundary. Define protocols for all external dependencies (network, persistence, system services) and inject mock implementations in tests
- Use `MockURLProtocol` to intercept `URLSession` requests without a real server. This avoids flaky tests caused by network conditions
- Mark tests that mutate `@MainActor`-isolated view models with `@MainActor` to satisfy Swift 6 concurrency requirements
- Keep UI tests focused on critical user flows (three to five scenarios). UI tests are slow and brittle, so cover edge cases with unit tests instead
- Use launch arguments (`--uitesting`) to configure the app for UI testing: stub network responses, seed test data, and disable animations

## Best Practices

- **Start with SwiftUI, bridge to UIKit when needed**: Use SwiftUI for all new screens. Drop into UIKit only for complex custom layouts, map annotations, or camera integration where UIKit provides capabilities SwiftUI lacks
- **Adopt @Observable over ObservableObject**: The @Observable macro (iOS 17+) provides fine-grained observation without `@Published` wrappers and eliminates unnecessary view re-renders
- **Use Swift concurrency everywhere**: Replace completion handlers, Combine pipelines, and GCD with async/await and structured concurrency. Enable strict concurrency checking to catch data races at compile time
- **Design for offline first**: Cache API responses locally with SwiftData. Show cached data immediately and refresh in the background. Display clear indicators when data is stale
- **Follow the principle of least privilege for permissions**: Request camera, location, notification, and health data permissions at the moment of use with a pre-prompt explaining why the permission is needed
- **Invest in accessibility from day one**: Use semantic SwiftUI modifiers (`.accessibilityLabel`, `.accessibilityHint`, `.accessibilityValue`). Test with VoiceOver enabled during development
- **Keep the main thread free**: Move all I/O, parsing, and heavy computation off the main actor. Use `Task.detached` or custom actors for CPU-intensive work
- **Pin deployment targets explicitly**: Set the minimum iOS version in xcconfig files, not in Xcode project settings, to prevent accidental changes from UI clicks
- **Use SwiftData for new projects, Core Data only for existing ones**: SwiftData is the modern replacement for Core Data with simpler syntax and SwiftUI integration
- **Automate with Xcode Cloud or CI**: Run tests, linting (SwiftLint), and archive builds on every pull request. Catch regressions before they reach the main branch

## Quality Checklist

- [ ] Deployment target set to iOS 17+ with Swift 6 strict concurrency enabled
- [ ] Project organized with feature modules and local Swift packages for shared logic
- [ ] All views use @Observable for state management, not ObservableObject
- [ ] Navigation uses NavigationStack with type-safe routes
- [ ] All external dependencies defined as protocols for testability
- [ ] View models marked @MainActor with async methods for data loading
- [ ] Sensitive data stored in Keychain, not UserDefaults
- [ ] Networking layer uses async/await with proper error handling and Codable
- [ ] SwiftData models configured with proper relationships and constraints
- [ ] Accessibility labels provided for all interactive elements
- [ ] Unit tests cover view model logic with protocol-based mocks
- [ ] UI tests cover critical user flows (sign in, main action, purchase)
- [ ] Privacy usage descriptions set in Info.plist for all requested permissions
- [ ] Background tasks registered and scheduled correctly
- [ ] StoreKit 2 transaction listener active on app launch

## Related Skills

- `architecture-design` - System decomposition and trade-off analysis for complex apps
- `security-review` - Security assessment for authentication and data protection
- `testing-review` - Test coverage and strategy evaluation
- `code-quality` - Code quality metrics and maintainability assessment
- `typescript-expert` - Cross-platform comparison when evaluating React Native alternatives

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
