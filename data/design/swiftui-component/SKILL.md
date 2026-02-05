---
name: swiftui-component
description: SwiftUIコンポーネント設計支援。View構造化、状態管理（@State/@Binding/@Observable）、Previewマクロ活用、アクセシビリティ対応。「SwiftUIコンポーネントを設計して」「Viewを構造化して」で使用。
---

# SwiftUI Component

SwiftUIコンポーネントの設計・実装を支援し、保守性とアクセシビリティを備えたUIを構築する。

## 概要

SwiftUIコンポーネントに対して以下の観点で設計支援を実施：

- View構造化のベストプラクティス
- 状態管理（@State, @Binding, @Observable等）
- Preview/Previewマクロの効果的な活用
- アクセシビリティ対応
- パフォーマンス最適化

## 実行条件

- SwiftUIを使用したプロジェクト
- 新規コンポーネント設計時
- 既存View構造のリファクタリング時
- アクセシビリティ対応が必要な時

## プロセス

### Step 1: 要件の整理

コンポーネントの目的と要件を明確化：

```markdown
## コンポーネント要件

### 機能要件
- [ ] 表示するデータの種類
- [ ] ユーザーインタラクション
- [ ] 状態の種類（ローカル/共有）

### 非機能要件
- [ ] 再利用性の範囲
- [ ] パフォーマンス要件
- [ ] アクセシビリティ要件
```

### Step 2: View構造の設計

#### 単一責任の原則
```swift
// Bad: 1つのViewに多くの責任
struct UserProfileView: View {
    var body: some View {
        VStack {
            // アバター表示ロジック
            // ユーザー情報表示ロジック
            // アクション部分のロジック
            // 設定部分のロジック
        }
    }
}

// Good: 責任を分離
struct UserProfileView: View {
    var body: some View {
        VStack {
            UserAvatarSection()
            UserInfoSection()
            UserActionsSection()
        }
    }
}
```

#### ViewBuilderの活用
```swift
struct CardView<Content: View>: View {
    @ViewBuilder let content: () -> Content

    var body: some View {
        VStack {
            content()
        }
        .padding()
        .background(.background)
        .cornerRadius(12)
        .shadow(radius: 4)
    }
}
```

### Step 3: 状態管理の設計

#### 状態の種類と選択基準

```markdown
## 状態管理ガイド

| 状態の種類 | 使用場面 | Property Wrapper |
|-----------|---------|------------------|
| Viewローカル | アニメーション、一時的なUI状態 | @State |
| 親からの参照 | 親子間の双方向バインディング | @Binding |
| 観測可能オブジェクト | 複雑なロジック、複数View共有 | @Observable (iOS 17+) |
| 環境値 | アプリ全体で共有 | @Environment |
| フォーカス | フォーカス状態管理 | @FocusState |
```

#### @Observable（iOS 17+）
```swift
@Observable
class UserSettings {
    var username: String = ""
    var notifications: Bool = true
    var theme: Theme = .system

    // 計算プロパティも自動追跡
    var isValid: Bool {
        !username.isEmpty
    }
}

struct SettingsView: View {
    @State private var settings = UserSettings()

    var body: some View {
        Form {
            TextField("Username", text: $settings.username)
            Toggle("Notifications", isOn: $settings.notifications)
        }
    }
}
```

#### @State と @Binding
```swift
struct ParentView: View {
    @State private var isPresented = false

    var body: some View {
        Button("Show Sheet") {
            isPresented = true
        }
        .sheet(isPresented: $isPresented) {
            ChildView(isPresented: $isPresented)
        }
    }
}

struct ChildView: View {
    @Binding var isPresented: Bool

    var body: some View {
        Button("Dismiss") {
            isPresented = false
        }
    }
}
```

### Step 4: Previewの設計

#### #Previewマクロ（Swift 5.9+）
```swift
#Preview {
    UserCardView(user: .preview)
}

#Preview("Dark Mode") {
    UserCardView(user: .preview)
        .preferredColorScheme(.dark)
}

#Preview("Large Text") {
    UserCardView(user: .preview)
        .environment(\.sizeCategory, .accessibilityExtraLarge)
}

#Preview(traits: .sizeThatFitsLayout) {
    UserCardView(user: .preview)
}
```

#### Previewデータの準備
```swift
extension User {
    static var preview: User {
        User(
            id: UUID(),
            name: "Preview User",
            email: "preview@example.com"
        )
    }

    static var previewList: [User] {
        [
            User(id: UUID(), name: "Alice", email: "alice@example.com"),
            User(id: UUID(), name: "Bob", email: "bob@example.com"),
        ]
    }
}
```

### Step 5: アクセシビリティ対応

#### 基本的なアクセシビリティ
```swift
struct ProductCardView: View {
    let product: Product

    var body: some View {
        VStack(alignment: .leading) {
            Image(product.imageName)
                .accessibilityLabel(product.imageDescription)

            Text(product.name)
                .font(.headline)

            Text(product.price.formatted(.currency(code: "JPY")))
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(product.name)、\(product.price.formatted(.currency(code: "JPY")))")
        .accessibilityHint("ダブルタップで詳細を表示")
        .accessibilityAddTraits(.isButton)
    }
}
```

#### Dynamic Type対応
```swift
struct AdaptiveTextView: View {
    @Environment(\.sizeCategory) var sizeCategory

    var body: some View {
        if sizeCategory.isAccessibilityCategory {
            // 大きいテキストサイズ用のレイアウト
            VStack(alignment: .leading) {
                titleView
                subtitleView
            }
        } else {
            // 通常サイズ用のレイアウト
            HStack {
                titleView
                Spacer()
                subtitleView
            }
        }
    }
}
```

### Step 6: パフォーマンス最適化

```swift
// Identifiableを活用した効率的なリスト
struct ItemListView: View {
    let items: [Item]

    var body: some View {
        List(items) { item in
            ItemRowView(item: item)
        }
    }
}

// 遅延読み込み
struct LargeGridView: View {
    let items: [Item]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: [GridItem(.adaptive(minimum: 100))]) {
                ForEach(items) { item in
                    ItemCellView(item: item)
                }
            }
        }
    }
}

// 不要な再描画の防止
struct OptimizedView: View {
    let data: ComplexData

    var body: some View {
        // EquatableViewで再描画を最適化
        ExpensiveChildView(data: data)
            .equatable()
    }
}
```

## 出力形式

```markdown
# SwiftUI Component Design

## コンポーネント概要
- 名前: `UserProfileCard`
- 目的: ユーザープロフィール情報の表示
- 再利用性: 高（アプリ全体で使用）

## View構造

```
UserProfileCard
├── AvatarView
│   └── AsyncImage
├── UserInfoSection
│   ├── Text (name)
│   └── Text (email)
└── ActionButtons
    ├── EditButton
    └── SettingsButton
```

## 状態管理

| Property | Type | Wrapper | 理由 |
|----------|------|---------|------|
| user | User | - | 親から受け取るデータ |
| isEditing | Bool | @State | ローカルUI状態 |
| avatarImage | Image? | @State | 非同期読み込み結果 |

## 実装コード

```swift
struct UserProfileCard: View {
    let user: User
    @State private var isEditing = false

    var body: some View {
        // 実装...
    }
}
```

## アクセシビリティ

- [ ] VoiceOver対応
- [ ] Dynamic Type対応
- [ ] カラーコントラスト確認

## Preview設定

```swift
#Preview {
    UserProfileCard(user: .preview)
}
```
```

## ガードレール

### 設計原則
- Single Responsibility: 1つのViewは1つの責任
- Composition over Inheritance: 継承よりコンポジション
- State Minimization: 状態は最小限に

### 避けるべきパターン
- ViewModelの過剰使用（シンプルな状態は@Stateで十分）
- 深いネスト（3階層以上は分割を検討）
- 巨大なbodyプロパティ

### 必須チェック項目
- [ ] Previewが正常に表示される
- [ ] VoiceOverで操作可能
- [ ] Dynamic Typeで崩れない
- [ ] ダークモードで視認できる

## 関連スキル

- `swift-code-review`: 全体的なコードレビュー
- `swift-concurrency`: 非同期処理の設計
