---
name: swiftui-patterns
description: SwiftUI開発パターン・ベストプラクティス。状態管理、ナビゲーション、レイアウト、アニメーション、パフォーマンス最適化など、モダンなSwiftUIアプリケーション開発の実践的なガイド。
---

# SwiftUI Patterns Skill

## 📋 目次

1. [概要](#概要)
2. [状態管理パターン](#状態管理パターン)
3. [ナビゲーション](#ナビゲーション)
4. [レイアウトシステム](#レイアウトシステム)
5. [データフロー](#データフロー)
6. [パフォーマンス最適化](#パフォーマンス最適化)
7. [アニメーション](#アニメーション)
8. [再利用可能なコンポーネント](#再利用可能なコンポーネント)
9. [テスト戦略](#テスト戦略)
10. [よくある問題と解決策](#よくある問題と解決策)

## 概要

SwiftUIアプリケーション開発における実践的なパターンとベストプラクティスを提供します。

**対象:**
- SwiftUIアプリケーション開発者
- iOSエンジニア
- モバイルアプリアーキテクト

**このSkillでできること:**
- 適切な状態管理パターンの選択と実装
- スケーラブルなナビゲーション設計
- パフォーマンスの高いUIの構築
- 保守性の高いコードベースの維持

## 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: SwiftUI状態管理、ナビゲーション設計、レイアウトシステム、パフォーマンス最適化
**公式で確認すべきこと**: 最新のSwiftUIアップデート、新しいAPIとモディファイア、iOS新機能

### 主要な公式ドキュメント

- **[SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)** - Apple公式SwiftUIドキュメント
  - [Tutorials](https://developer.apple.com/tutorials/swiftui)
  - [Views and Controls](https://developer.apple.com/documentation/swiftui/views-and-controls)
  - [State and Data Flow](https://developer.apple.com/documentation/swiftui/state-and-data-flow)

- **[SwiftUI by Example](https://www.hackingwithswift.com/quick-start/swiftui)** - 実践的なSwiftUI学習リソース

- **[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)** - iOSデザインガイドライン
  - [iOS Design](https://developer.apple.com/design/human-interface-guidelines/)

- **[Combine Framework](https://developer.apple.com/documentation/combine)** - リアクティブプログラミング

### 関連リソース

- **[Swift by Sundell](https://www.swiftbysundell.com/)** - Swift/SwiftUIベストプラクティス
- **[Point-Free](https://www.pointfree.co/)** - 高度なSwiftUI技法
- **[SwiftUI Lab](https://swiftui-lab.com/)** - SwiftUI深掘り記事

---

## 状態管理パターン

### @State - ローカル状態

**使用場面:**
- 単一Viewに閉じた状態
- シンプルな値型の管理

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}
```

**ベストプラクティス:**
- private修飾子を付ける
- 値型（struct, enum, Int, String等）に使用
- View階層外に公開しない

### @Binding - 状態の共有

**使用場面:**
- 親Viewから状態を受け取る
- 双方向データバインディング

```swift
struct ToggleView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Setting", isOn: $isOn)
    }
}

struct ParentView: View {
    @State private var setting = false

    var body: some View {
        ToggleView(isOn: $setting)
    }
}
```

**ベストプラクティス:**
- 状態の所有権を明確にする
- データの流れを一方向に保つ
- プレビューでは.constant()を使用

### @StateObject - 参照型の状態管理

**使用場面:**
- ObservableObjectのライフサイクル管理
- View所有の複雑な状態

```swift
class TimerManager: ObservableObject {
    @Published var seconds = 0
    private var timer: Timer?

    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.seconds += 1
        }
    }

    func stop() {
        timer?.invalidate()
    }
}

struct TimerView: View {
    @StateObject private var timerManager = TimerManager()

    var body: some View {
        VStack {
            Text("\(timerManager.seconds)")
            Button("Start") { timerManager.start() }
            Button("Stop") { timerManager.stop() }
        }
    }
}
```

**ベストプラクティス:**
- View所有のオブジェクトに使用
- 初期化は@StateObjectで行う
- 親から受け取る場合は@ObservedObject使用

### @ObservedObject - 外部所有の状態

**使用場面:**
- 親から受け取ったObservableObject
- 複数Viewで共有される状態

```swift
struct SettingsView: View {
    @ObservedObject var settings: AppSettings

    var body: some View {
        Form {
            Toggle("Notifications", isOn: $settings.notificationsEnabled)
            Toggle("Dark Mode", isOn: $settings.darkModeEnabled)
        }
    }
}
```

### @EnvironmentObject - グローバル状態

**使用場面:**
- アプリ全体で共有される状態
- 深い階層への状態の伝播

```swift
class UserSession: ObservableObject {
    @Published var isLoggedIn = false
    @Published var username = ""
}

@main
struct MyApp: App {
    @StateObject private var session = UserSession()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(session)
        }
    }
}

struct ProfileView: View {
    @EnvironmentObject var session: UserSession

    var body: some View {
        Text("Hello, \(session.username)")
    }
}
```

**ベストプラクティス:**
- 本当に必要な場合のみ使用
- プレビューでの注入を忘れない
- 依存関係を明示的にする

## ナビゲーション

### NavigationStack（iOS 16+）

**基本パターン:**

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink("Settings", value: Route.settings)
                NavigationLink("Profile", value: Route.profile)
            }
            .navigationDestination(for: Route.self) { route in
                switch route {
                case .settings:
                    SettingsView()
                case .profile:
                    ProfileView()
                }
            }
        }
    }
}

enum Route: Hashable {
    case settings
    case profile
}
```

**プログラマティックナビゲーション:**

```swift
struct MainView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack {
                Button("Go to Detail") {
                    path.append(DetailRoute.detail(id: 1))
                }
                Button("Go Deep") {
                    path.append(DetailRoute.detail(id: 1))
                    path.append(DetailRoute.subDetail(id: 2))
                }
                Button("Pop to Root") {
                    path.removeLast(path.count)
                }
            }
            .navigationDestination(for: DetailRoute.self) { route in
                DetailView(route: route)
            }
        }
    }
}
```

### Modal Presentation

**Sheet:**

```swift
struct ContentView: View {
    @State private var showingSheet = false

    var body: some View {
        Button("Show Sheet") {
            showingSheet = true
        }
        .sheet(isPresented: $showingSheet) {
            SheetView()
        }
    }
}
```

**FullScreenCover:**

```swift
struct ContentView: View {
    @State private var showingFullScreen = false

    var body: some View {
        Button("Show Full Screen") {
            showingFullScreen = true
        }
        .fullScreenCover(isPresented: $showingFullScreen) {
            FullScreenView()
        }
    }
}
```

## レイアウトシステム

### Stack Layouts

**VStack - 垂直配置:**

```swift
VStack(alignment: .leading, spacing: 16) {
    Text("Title")
        .font(.headline)
    Text("Subtitle")
        .font(.subheadline)
    Text("Body")
        .font(.body)
}
```

**HStack - 水平配置:**

```swift
HStack(alignment: .center, spacing: 8) {
    Image(systemName: "star.fill")
    Text("Favorite")
    Spacer()
    Text("100")
}
```

**ZStack - 重ね配置:**

```swift
ZStack(alignment: .bottomTrailing) {
    Image("background")
        .resizable()
        .aspectRatio(contentMode: .fill)

    Text("Overlay")
        .padding()
        .background(.ultraThinMaterial)
}
```

### Custom Layout（iOS 16+）

```swift
struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let rows = computeRows(proposal: proposal, subviews: subviews)
        let height = rows.reduce(0) { $0 + $1.height } + CGFloat(rows.count - 1) * spacing
        return CGSize(width: proposal.width ?? 0, height: height)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let rows = computeRows(proposal: proposal, subviews: subviews)
        var y = bounds.minY

        for row in rows {
            var x = bounds.minX
            for index in row.indices {
                subviews[index].place(at: CGPoint(x: x, y: y), proposal: .unspecified)
                x += subviews[index].sizeThatFits(.unspecified).width + spacing
            }
            y += row.height + spacing
        }
    }

    private func computeRows(proposal: ProposedViewSize, subviews: Subviews) -> [[Int]] {
        // Flow layout implementation
        []
    }
}
```

### GeometryReader

**適切な使用例:**

```swift
struct AdaptiveView: View {
    var body: some View {
        GeometryReader { geometry in
            if geometry.size.width > 600 {
                HStack {
                    Sidebar()
                    Content()
                }
            } else {
                VStack {
                    Content()
                }
            }
        }
    }
}
```

**避けるべきパターン:**

```swift
// ❌ 不必要なGeometryReader
GeometryReader { geometry in
    Text("Hello")
        .frame(width: geometry.size.width) // .frame(maxWidth: .infinity)で十分
}

// ✅ より良い方法
Text("Hello")
    .frame(maxWidth: .infinity)
```

## データフロー

### MVVM パターン

```swift
// Model
struct User: Identifiable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModel
class UserListViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: Error?

    private let repository: UserRepository

    init(repository: UserRepository = .shared) {
        self.repository = repository
    }

    @MainActor
    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await repository.fetchUsers()
        } catch {
            self.error = error
        }
    }
}

// View
struct UserListView: View {
    @StateObject private var viewModel = UserListViewModel()

    var body: some View {
        List(viewModel.users) { user in
            UserRow(user: user)
        }
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
        .task {
            await viewModel.loadUsers()
        }
        .alert(error: $viewModel.error)
    }
}
```

### Unidirectional Data Flow

```swift
// State
struct AppState {
    var users: [User] = []
    var isLoading = false
}

// Action
enum AppAction {
    case loadUsers
    case usersLoaded([User])
    case usersFailed(Error)
}

// Reducer
func appReducer(state: inout AppState, action: AppAction) {
    switch action {
    case .loadUsers:
        state.isLoading = true
    case .usersLoaded(let users):
        state.users = users
        state.isLoading = false
    case .usersFailed:
        state.isLoading = false
    }
}

// Store
class Store: ObservableObject {
    @Published private(set) var state = AppState()

    func send(_ action: AppAction) {
        appReducer(state: &state, action: action)
    }
}
```

## パフォーマンス最適化

### 不要な再描画を避ける

**EquatableView:**

```swift
struct ExpensiveView: View, Equatable {
    let data: ComplexData

    var body: some View {
        // 重い描画処理
        ComplexRenderingView(data: data)
    }

    static func == (lhs: ExpensiveView, rhs: ExpensiveView) -> Bool {
        lhs.data.id == rhs.data.id
    }
}

struct ParentView: View {
    @State private var counter = 0
    let data: ComplexData

    var body: some View {
        VStack {
            Text("Counter: \(counter)")
            Button("Increment") { counter += 1 }

            // dataが変わらない限り再描画されない
            EquatableView(data: data)
                .equatable()
        }
    }
}
```

### LazyStack の活用

```swift
// ✅ 大量のアイテムにはLazyVStack
ScrollView {
    LazyVStack {
        ForEach(0..<1000) { index in
            RowView(index: index)
        }
    }
}

// ❌ 全て一度に描画される
ScrollView {
    VStack {
        ForEach(0..<1000) { index in
            RowView(index: index)
        }
    }
}
```

### @Published の最適化

```swift
class ViewModel: ObservableObject {
    // ✅ 必要なプロパティのみPublished
    @Published var displayText: String = ""

    // ❌ 頻繁に変わる内部状態をPublishedにしない
    private var internalCounter = 0

    func updateDisplay() {
        internalCounter += 1
        // 10回に1回だけUIを更新
        if internalCounter % 10 == 0 {
            displayText = "Count: \(internalCounter)"
        }
    }
}
```

## アニメーション

### 基本アニメーション

```swift
struct AnimatedView: View {
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 100, height: 100)
            .scaleEffect(scale)
            .onTapGesture {
                withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                    scale = scale == 1.0 ? 1.5 : 1.0
                }
            }
    }
}
```

### カスタムトランジション

```swift
extension AnyTransition {
    static var slideAndFade: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .trailing).combined(with: .opacity),
            removal: .move(edge: .leading).combined(with: .opacity)
        )
    }
}

struct ContentView: View {
    @State private var showDetail = false

    var body: some View {
        VStack {
            if showDetail {
                DetailView()
                    .transition(.slideAndFade)
            }
        }
        .animation(.easeInOut, value: showDetail)
    }
}
```

### Matched Geometry Effect

```swift
struct MatchedView: View {
    @State private var isExpanded = false
    @Namespace private var animation

    var body: some View {
        if isExpanded {
            VStack {
                Circle()
                    .fill(.blue)
                    .matchedGeometryEffect(id: "circle", in: animation)
                    .frame(width: 200, height: 200)
                Text("Expanded")
            }
        } else {
            Circle()
                .fill(.blue)
                .matchedGeometryEffect(id: "circle", in: animation)
                .frame(width: 50, height: 50)
        }
    }
}
```

## 再利用可能なコンポーネント

### View Modifiers

```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.white)
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
}

// 使用例
Text("Card Content")
    .cardStyle()
```

### Custom Containers

```swift
struct Section<Content: View, Header: View>: View {
    let header: Header
    let content: Content

    init(@ViewBuilder content: () -> Content, @ViewBuilder header: () -> Header) {
        self.content = content()
        self.header = header()
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            header
                .font(.headline)
            content
        }
        .padding()
        .cardStyle()
    }
}

// 使用例
Section {
    Text("Content here")
} header: {
    Text("Title")
}
```

## テスト戦略

### ViewInspector でのテスト

```swift
import XCTest
import ViewInspector
@testable import MyApp

final class CounterViewTests: XCTestCase {
    func testInitialState() throws {
        let view = CounterView()
        let text = try view.inspect().find(text: "Count: 0")
        XCTAssertNotNil(text)
    }

    func testIncrement() throws {
        let view = CounterView()
        try view.inspect().find(button: "Increment").tap()
        let text = try view.inspect().find(text: "Count: 1")
        XCTAssertNotNil(text)
    }
}
```

### Snapshot Testing

```swift
import SnapshotTesting
import XCTest

final class SnapshotTests: XCTestCase {
    func testUserCard() {
        let view = UserCard(user: .mock)
        assertSnapshot(matching: view, as: .image(layout: .device(config: .iPhone13)))
    }
}
```

## よくある問題と解決策

### 問題1: Viewが予期せず再描画される

**原因:** 親Viewの状態変更

**解決策:**
```swift
// ❌ 問題のあるコード
struct ParentView: View {
    @State private var counter = 0

    var body: some View {
        VStack {
            Text("\(counter)")
            ExpensiveChildView() // 毎回再作成される
        }
    }
}

// ✅ 改善したコード
struct ParentView: View {
    @State private var counter = 0

    var body: some View {
        VStack {
            Text("\(counter)")
            ExpensiveChildView()
                .equatable() // Equatableに準拠させる
        }
    }
}
```

### 問題2: リストのパフォーマンスが悪い

**解決策:**
```swift
// ✅ LazyVStackとonAppear活用
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            RowView(item: item)
                .onAppear {
                    if item == items.last {
                        loadMore()
                    }
                }
        }
    }
}
```

### 問題3: NavigationStackでメモリリークする

**解決策:**
```swift
// ✅ pathを明示的に管理
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            // ...
        }
        .onDisappear {
            // 必要に応じてクリーンアップ
            path = NavigationPath()
        }
    }
}
```

---

**関連Skills:**
- [ios-development](../ios-development/SKILL.md) - iOS開発全般
- [ios-project-setup](../ios-project-setup/SKILL.md) - プロジェクト初期設定
- [testing-strategy](../testing-strategy/SKILL.md) - テスト戦略
- [frontend-performance](../frontend-performance/SKILL.md) - パフォーマンス最適化の考え方

**更新履歴:**
- 2025-12-24: 初版作成
