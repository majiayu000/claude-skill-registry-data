---
name: swift-protocol
description: プロトコル指向設計の支援。Protocol拡張、Associated Types設計、依存性注入パターンを提案。「プロトコルを設計して」「依存性注入を実装して」で使用。
---

# Swift Protocol

Swiftのプロトコル指向プログラミングを活用した設計を支援する。

## 概要

プロトコル指向設計に対して以下の観点で支援を実施：

- Protocol定義とExtensionの活用
- Associated Types（関連型）の設計
- Primary Associated Typesの活用（Swift 5.7+）
- プロトコルによる依存性注入
- テスタビリティの確保

## 実行条件

- 抽象化が必要な設計時
- テスト容易性の向上が必要な時
- 依存性注入パターンの実装時
- 既存クラス継承の見直し時

## プロセス

### Step 1: 要件分析

```markdown
## 抽象化の目的

### 動機
- [ ] テスタビリティ向上
- [ ] 実装の交換可能性
- [ ] 共通インターフェースの提供
- [ ] ポリモーフィズムの実現

### 制約
- [ ] パフォーマンス要件
- [ ] ABI安定性要件
- [ ] 後方互換性要件
```

### Step 2: Protocol設計

#### 単一責任の原則
```swift
// Bad: 責任が多すぎる
protocol DataManager {
    func fetch() async throws -> Data
    func save(_ data: Data) async throws
    func cache(_ data: Data)
    func validate(_ data: Data) -> Bool
    func transform(_ data: Data) -> ProcessedData
}

// Good: 責任を分離
protocol DataFetching {
    func fetch() async throws -> Data
}

protocol DataPersisting {
    func save(_ data: Data) async throws
}

protocol DataCaching {
    func cache(_ data: Data)
    func cached() -> Data?
}
```

#### プロトコル合成
```swift
// 必要に応じて合成
typealias DataRepository = DataFetching & DataPersisting

// または具体的な要件として定義
protocol DataRepository: DataFetching, DataPersisting {
    // 追加のメソッドがあれば定義
}
```

### Step 3: Protocol Extension活用

#### デフォルト実装
```swift
protocol Identifiable {
    var id: UUID { get }
}

extension Identifiable {
    // デフォルト実装
    var id: UUID { UUID() }
}

protocol Timestamped {
    var createdAt: Date { get }
    var updatedAt: Date { get }
}

extension Timestamped {
    var isRecent: Bool {
        updatedAt.timeIntervalSinceNow > -86400  // 24時間以内
    }
}
```

#### 条件付きExtension
```swift
// Collectionに対する拡張（要素がEquatableの場合のみ）
extension Collection where Element: Equatable {
    func removingDuplicates() -> [Element] {
        var seen: [Element] = []
        return filter { element in
            if seen.contains(element) {
                return false
            }
            seen.append(element)
            return true
        }
    }
}

// 特定の型に対する拡張
extension Array where Element == Int {
    var sum: Int {
        reduce(0, +)
    }
}
```

### Step 4: Associated Types設計

#### 基本的なAssociated Type
```swift
protocol Repository {
    associatedtype Entity
    associatedtype ID: Hashable

    func find(id: ID) async throws -> Entity?
    func save(_ entity: Entity) async throws
    func delete(id: ID) async throws
}

// 具体的な実装
struct UserRepository: Repository {
    typealias Entity = User
    typealias ID = UUID

    func find(id: UUID) async throws -> User? {
        // 実装
    }

    func save(_ entity: User) async throws {
        // 実装
    }

    func delete(id: UUID) async throws {
        // 実装
    }
}
```

#### Primary Associated Types (Swift 5.7+)
```swift
// Primary Associated Typeを指定
protocol Repository<Entity> {
    associatedtype Entity
    associatedtype ID: Hashable = UUID

    func find(id: ID) async throws -> Entity?
    func save(_ entity: Entity) async throws
}

// 使用側で型を明示できる
func processUsers(repository: some Repository<User>) async throws {
    if let user = try await repository.find(id: UUID()) {
        // userはUser型
    }
}

// 存在型としても使用可能
let repositories: [any Repository<User>] = [
    InMemoryUserRepository(),
    RemoteUserRepository()
]
```

### Step 5: 依存性注入パターン

#### コンストラクタ注入
```swift
protocol NetworkClient: Sendable {
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T
}

final class UserService {
    private let networkClient: NetworkClient
    private let cache: UserCache

    init(networkClient: NetworkClient, cache: UserCache) {
        self.networkClient = networkClient
        self.cache = cache
    }

    func fetchUser(id: UUID) async throws -> User {
        if let cached = cache.get(id: id) {
            return cached
        }
        let user: User = try await networkClient.request(.user(id: id))
        cache.set(user, for: id)
        return user
    }
}
```

#### 環境による注入（SwiftUI）
```swift
// プロトコル定義
protocol AnalyticsTracking: Sendable {
    func track(event: AnalyticsEvent)
}

// 環境キー
struct AnalyticsKey: EnvironmentKey {
    static let defaultValue: AnalyticsTracking = NoOpAnalytics()
}

extension EnvironmentValues {
    var analytics: AnalyticsTracking {
        get { self[AnalyticsKey.self] }
        set { self[AnalyticsKey.self] = newValue }
    }
}

// 使用
struct MyView: View {
    @Environment(\.analytics) var analytics

    var body: some View {
        Button("Tap") {
            analytics.track(event: .buttonTapped("MyButton"))
        }
    }
}
```

### Step 6: テスタビリティ確保

#### モック可能な設計
```swift
// プロダクションコード
protocol UserRepositoryProtocol {
    func fetchUser(id: UUID) async throws -> User
    func saveUser(_ user: User) async throws
}

final class UserRepository: UserRepositoryProtocol {
    private let networkClient: NetworkClient

    init(networkClient: NetworkClient) {
        self.networkClient = networkClient
    }

    func fetchUser(id: UUID) async throws -> User {
        try await networkClient.request(.user(id: id))
    }

    func saveUser(_ user: User) async throws {
        try await networkClient.request(.saveUser(user))
    }
}

// テストコード
final class MockUserRepository: UserRepositoryProtocol {
    var fetchUserResult: Result<User, Error> = .success(.mock)
    var savedUsers: [User] = []

    func fetchUser(id: UUID) async throws -> User {
        try fetchUserResult.get()
    }

    func saveUser(_ user: User) async throws {
        savedUsers.append(user)
    }
}

// テスト
@Test
func testUserService() async throws {
    let mockRepository = MockUserRepository()
    mockRepository.fetchUserResult = .success(User(name: "Test"))

    let service = UserService(repository: mockRepository)
    let user = try await service.getUser(id: UUID())

    #expect(user.name == "Test")
}
```

## 出力形式

```markdown
# Protocol Design Document

## 概要
- 目的: ユーザーデータアクセスの抽象化
- スコープ: データ層

## プロトコル定義

### UserRepositoryProtocol
```swift
protocol UserRepositoryProtocol: Sendable {
    func find(id: UUID) async throws -> User?
    func save(_ user: User) async throws
    func delete(id: UUID) async throws
    func findAll() async throws -> [User]
}
```

### 設計判断

| 項目 | 判断 | 理由 |
|------|------|------|
| Associated Type使用 | No | 単一のEntity型のみ使用 |
| Sendable要件 | Yes | 非同期コンテキストで使用 |
| Extension | Yes | findAllのデフォルト実装 |

### 依存関係図

```
UserService
    └── UserRepositoryProtocol
            ├── CoreDataUserRepository
            ├── InMemoryUserRepository (テスト用)
            └── RemoteUserRepository
```

## 実装例

### プロダクション実装
```swift
final class CoreDataUserRepository: UserRepositoryProtocol {
    // ...
}
```

### テスト用モック
```swift
final class MockUserRepository: UserRepositoryProtocol {
    // ...
}
```
```

## ガードレール

### 設計原則
- Interface Segregation: クライアントが使わないメソッドに依存させない
- Dependency Inversion: 具体ではなく抽象に依存する
- Protocol Composition: 大きなプロトコルより小さなプロトコルの合成

### 避けるべきパターン
- 過度な抽象化（1つの実装しかないプロトコル）
- Fat Protocol（メソッドが多すぎる）
- Protocol Witnessテーブルのオーバーヘッドを無視した設計

### 注意点
- プロトコルは値型で使う場合はexistentialのオーバーヘッドに注意
- `some Protocol`（opaque type）と`any Protocol`（existential）の使い分け
- Swift 6のStrict Concurrency対応（Sendable要件）

## 関連スキル

- `swift-code-review`: コードレビュー
- `swift-concurrency`: 並行処理対応
