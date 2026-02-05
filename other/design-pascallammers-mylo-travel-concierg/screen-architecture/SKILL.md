---
name: screen-architecture
description: iOS画面実装のアーキテクチャ・設計思想スキル。Reduxパターンに基づくSingle Root State、Reducerによるビジネスロジック分離、テスタビリティを重視した実装を支援。使用シーン：(1)「このプロトタイプを本番実装にして」などの本格実装リクエスト (2)「状態管理を整理して」などのアーキテクチャ適用リクエスト (3) 画面の状態管理やテスト可能な設計が必要な場合 (4)「この画面をテストしやすくして」などのリファクタリングリクエスト
---

# Screen Architecture

Reduxパターンによる画面実装の設計指針。

## Reduxパターンとは

JavaScriptエコシステムで生まれた状態管理パターン。3つの原則に基づく:

1. **Single Source of Truth**: アプリ全体の状態は単一のStoreに保持
2. **State is Read-Only**: 状態変更はActionを発行することでのみ行う
3. **Changes with Pure Functions**: Reducerは純粋関数

iOSでは**TCA (The Composable Architecture)** が有名だが、このスキルではTCAを使わずに同じ思想を実現する。

## 設計思想

1. **Single Root State**: 状態はルートで一元管理。子ビューは必要な値を親から受け取る
2. **Reducerでロジック分離**: ビジネスロジックは純粋関数として切り出し、テスト可能に
3. **SwiftUIに任せる**: 画面更新のタイミングやパフォーマンスはSwiftUIの差分更新に委ねる

## 基本構造

```
App/
├── AppState.swift           # ルート状態（Single Source of Truth）
├── AppAction.swift          # 全アクション定義
├── AppStore.swift           # Store（状態保持 + Action dispatch）
├── Features/
│   ├── Order/
│   │   ├── OrderState.swift     # 機能別の状態（AppStateの一部）
│   │   ├── OrderAction.swift    # 機能別のアクション
│   │   ├── OrderReducer.swift   # 純粋関数（テスト対象）
│   │   └── OrderView.swift      # View（パラメータを受け取るだけ）
│   └── Profile/
│       └── ...
└── Services/                # 副作用（API、DB等）
    └── OrderService.swift
```

## State

### AppState（ルート）

```swift
struct AppState {
    var order = OrderState()
    var profile = ProfileState()
    var navigation = NavigationState()
}
```

### Feature State

```swift
struct OrderState {
    var orders: [Order] = []
    var isLoading = false
    var error: Error?
}
```

状態は値型（struct）で定義。AppStateが唯一の真実の源。

## Action

```swift
enum AppAction {
    case order(OrderAction)
    case profile(ProfileAction)
}

enum OrderAction {
    case loadOrders
    case ordersLoaded([Order])
    case ordersFailed(Error)
    case selectOrder(Order)
}
```

## Reducer

ビジネスロジックを純粋関数として定義。**テストの主要対象**。

```swift
enum OrderReducer {
    static func reduce(state: inout OrderState, action: OrderAction) {
        switch action {
        case .loadOrders:
            state.isLoading = true
            state.error = nil

        case .ordersLoaded(let orders):
            state.orders = orders
            state.isLoading = false

        case .ordersFailed(let error):
            state.error = error
            state.isLoading = false

        case .selectOrder(let order):
            // 選択状態の更新など
            break
        }
    }
}
```

### AppReducer（統合）

```swift
enum AppReducer {
    static func reduce(state: inout AppState, action: AppAction) {
        switch action {
        case .order(let action):
            OrderReducer.reduce(state: &state.order, action: action)
        case .profile(let action):
            ProfileReducer.reduce(state: &state.profile, action: action)
        }
    }
}
```

## Store

状態の保持とAction dispatchを担当。副作用（API呼び出し等）もここで処理。

```swift
@MainActor
final class AppStore: ObservableObject {
    @Published private(set) var state = AppState()

    // Dependencies
    private let orderService: OrderServiceProtocol

    init(orderService: OrderServiceProtocol) {
        self.orderService = orderService
    }

    func send(_ action: AppAction) {
        // 1. Reducerで状態更新
        AppReducer.reduce(state: &state, action: action)

        // 2. 副作用の実行
        Task {
            await handleSideEffects(action)
        }
    }

    private func handleSideEffects(_ action: AppAction) async {
        switch action {
        case .order(.loadOrders):
            do {
                let orders = try await orderService.fetchOrders()
                send(.order(.ordersLoaded(orders)))
            } catch {
                send(.order(.ordersFailed(error)))
            }

        default:
            break
        }
    }
}
```

## View

Viewはパラメータを受け取り、表示とアクション送信のみを担当。

### RootView

```swift
@main
struct MyApp: App {
    @StateObject private var store = AppStore(
        orderService: OrderService()
    )

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(store)
        }
    }
}
```

### Feature View

```swift
struct OrderListView: View {
    // 必要な値だけを受け取る
    let orders: [Order]
    let isLoading: Bool
    let onOrderTap: (Order) -> Void
    let onRefresh: () -> Void

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else {
                List(orders) { order in
                    OrderRow(order: order)
                        .onTapGesture { onOrderTap(order) }
                }
                .refreshable { onRefresh() }
            }
        }
    }
}

// 親から呼び出す
struct OrderContainerView: View {
    @EnvironmentObject var store: AppStore

    var body: some View {
        OrderListView(
            orders: store.state.order.orders,
            isLoading: store.state.order.isLoading,
            onOrderTap: { store.send(.order(.selectOrder($0))) },
            onRefresh: { store.send(.order(.loadOrders)) }
        )
    }
}
```

### なぜこの形式か

- **OrderListViewは純粋なView**: 状態を持たず、渡された値を表示するだけ。Preview可能
- **OrderContainerView**: Storeとの橋渡し。状態の購読とアクション送信
- **SwiftUIに任せる**: `store.state.order.orders`が変わればSwiftUIが自動で差分更新

## プロトタイプ→本番実装ワークフロー

### 1. 状態の抽出

プロトタイプ内の`@State`をFeature Stateに移動:

```swift
// Before（プロトタイプ）
struct OrderView: View {
    @State private var orders: [Order] = []
    @State private var isLoading = false
}

// After（Feature State）
struct OrderState {
    var orders: [Order] = []
    var isLoading = false
}
```

### 2. アクションの定義

ユーザー操作とイベントをAction enumに。非同期結果も含める:

```swift
enum OrderAction {
    // ユーザー操作
    case loadOrders
    case selectOrder(Order)

    // 非同期結果
    case ordersLoaded([Order])
    case ordersFailed(Error)
}
```

### 3. Reducerの作成

状態更新ロジックを純粋関数に:

```swift
enum OrderReducer {
    static func reduce(state: inout OrderState, action: OrderAction) {
        // 同期的な状態更新のみ
    }
}
```

### 4. 副作用の実装

Storeで非同期処理を実行:

```swift
private func handleSideEffects(_ action: AppAction) async {
    // API呼び出しなど
}
```

### 5. Viewの簡素化

Viewをパラメータ受け取り形式に変換。

### 6. テストの追加

Reducerのテストを作成（純粋関数なのでテストしやすい）。

## チェックリスト

- [ ] 状態はAppState配下で一元管理されているか
- [ ] 子Viewは`@State`を持たず、パラメータを受け取っているか
- [ ] ビジネスロジックはReducerに切り出されているか
- [ ] Reducerは純粋関数か（副作用なし）
- [ ] 副作用（API等）はStoreで処理されているか
- [ ] Reducerのテストが作成されているか

## リファレンス

| ファイル | 内容 |
|---------|------|
| `references/state-management.md` | 状態設計の詳細パターン |
| `references/testing-guide.md` | Reducerテストの書き方 |
