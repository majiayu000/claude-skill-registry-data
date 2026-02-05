---
name: swift-code-review
description: Swiftコードの品質レビュー。Swift 6のStrict Concurrency対応、プロトコル指向設計、値型/参照型の使用、エラーハンドリングをチェック。「Swiftコードをレビューして」「Swift 6対応を確認して」で使用。
---

# Swift Code Review

Swiftコードの品質レビューを行い、Swift 6時代のベストプラクティスに基づく改善提案を行う。

## 概要

Swiftコードベースに対して以下の観点でレビューを実施：

- Swift 6 Strict Concurrency対応
- プロトコル指向設計の評価
- 値型 vs 参照型の適切な使用
- エラーハンドリングのベストプラクティス
- Swiftイディオムの適用

## 実行条件

- Swiftファイル（.swift）が対象
- コードレビュー依頼時
- Swift 6移行準備時
- プルリクエストレビュー時

## プロセス

### Step 1: コード取得

対象のSwiftコードを取得：
- ファイルパス指定
- ディレクトリ全体
- git diff
- PR差分

### Step 2: Swift 6 Strict Concurrency チェック

```markdown
## Strict Concurrency 観点

### Sendable適合
- [ ] 共有される型にSendable適合があるか
- [ ] @unchecked Sendableの使用は適切か
- [ ] 暗黙的Sendable推論に依存していないか

### Actor分離
- [ ] 適切なActor境界が設定されているか
- [ ] @MainActorの過剰使用がないか
- [ ] nonisolatedの使用は適切か

### データ競合防止
- [ ] 可変状態の共有がないか
- [ ] Task間のデータ受け渡しは安全か
- [ ] クロージャのキャプチャは適切か
```

### Step 3: プロトコル指向設計の評価

```markdown
## プロトコル設計観点

### 適切な抽象化
- [ ] プロトコルが単一責任を持っているか
- [ ] 過度な抽象化になっていないか
- [ ] Protocol Extensionを活用しているか

### 関連型の設計
- [ ] Associated Typeの制約は適切か
- [ ] Primary Associated Typeを活用しているか（Swift 5.7+）
- [ ] where句による制約は明確か

### 依存性注入
- [ ] プロトコルによる依存性注入が可能か
- [ ] テスタビリティが確保されているか
```

### Step 4: 値型 vs 参照型の評価

```markdown
## 型の選択観点

### 値型（struct, enum）
- [ ] 不変性が活かされているか
- [ ] CoWの意識があるか
- [ ] 値の意味論が適切か

### 参照型（class）
- [ ] 参照型が本当に必要か
- [ ] 継承は適切に使用されているか
- [ ] finalキーワードが適切に付与されているか

### 型の選択基準
- [ ] 同一性（identity）vs 同等性（equality）
- [ ] 可変性の要件
- [ ] パフォーマンス要件
```

### Step 5: エラーハンドリング評価

```markdown
## エラーハンドリング観点

### Swift Error Handling
- [ ] throws/try/catchが適切に使用されているか
- [ ] Result型の使用は適切か
- [ ] エラー型は具体的か（Error vs 具体的なError型）

### Optional処理
- [ ] 強制アンラップ（!）の使用は安全か
- [ ] guard letの活用
- [ ] nil合体演算子（??）のデフォルト値は適切か

### 失敗ケース
- [ ] fatalError/preconditionの使用は適切か
- [ ] 回復可能なエラーと回復不能なエラーの区別
```

### Step 6: Swiftイディオム評価

```markdown
## イディオム観点

### モダンSwift構文
- [ ] if/switch式の活用（Swift 5.9+）
- [ ] 末尾クロージャの適切な使用
- [ ] キーパス（\.）の活用

### コレクション処理
- [ ] map/filter/reduceの適切な使用
- [ ] lazy評価の検討
- [ ] Sequenceプロトコルの活用

### 型安全性
- [ ] タグ付き型（Newtypes）の活用
- [ ] Phantom Typesの検討
- [ ] @frozen/@usableFromInlineの適切な使用
```

## 出力形式

```markdown
# Swift Code Review Report

## 対象
- ファイル: `path/to/file.swift`
- Swift Version: 6.x

## サマリー
| カテゴリ | 問題数 | 重要度 |
|---------|--------|--------|
| Concurrency | 2 | 🔴 High |
| Protocol Design | 1 | 🟡 Medium |
| Type Choice | 0 | 🟢 OK |
| Error Handling | 1 | 🟡 Medium |

## 詳細

### 🔴 [Concurrency] データ競合リスク
**Location**: `UserManager.swift:45`

**Issue**:
クラスプロパティ`users`が複数のTaskからアクセス可能だが、Sendable適合がない。

**現状コード**:
```swift
class UserManager {
    var users: [User] = []  // 危険: 複数Taskからアクセス可能

    func addUser(_ user: User) {
        users.append(user)
    }
}
```

**推奨修正**:
```swift
actor UserManager {
    private var users: [User] = []

    func addUser(_ user: User) {
        users.append(user)
    }
}
```

**理由**:
Swift 6のStrict Concurrencyでは、共有可変状態へのアクセスはコンパイルエラーになる。
Actorを使用することで、データ競合を防止できる。

---

### 🟡 [Protocol] 過度な抽象化
...
```

## ガードレール

### 必須チェック項目
- Swift 6コンパイラ警告の確認
- Sendable適合の検証
- 強制アンラップの使用箇所確認

### 自動修正の制限
- Actor導入は手動確認必須
- プロトコル設計変更は影響範囲を確認
- エラーハンドリング変更はテスト必須

### レビュー対象外
- 生成コード（SwiftGen等）
- 外部ライブラリ
- テストコード（別スキルで対応）

## 関連スキル

- `swift-concurrency`: 並行処理の詳細レビュー
- `swift-protocol`: プロトコル設計の詳細支援
- `swiftui-component`: SwiftUI固有のレビュー
