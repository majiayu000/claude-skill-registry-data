---
name: ios-test-design
description: "XCTest/XCUITestを用いたiOSアプリのテスト設計支援スキル。テスト戦略立案、モック/スタブ設計、テストデータ管理、カバレッジ分析を包括的にサポート。Use when: iOSテスト設計、XCTest実装、UITest作成、テストカバレッジ向上、テスト戦略立案、テストダブル設計。"
---

# iOS Test Design（iOSテスト設計支援）

## 概要

XCTestおよびXCUITestを活用したiOSアプリケーションのテスト設計を支援するスキル。
デトロイト学派寄りのアプローチを採用し、実際のコンポーネント連携をテストすることで、信頼性の高いテストスイートを構築する。

### 対象範囲

- **Unit Test**: XCTestによる単体テスト設計
- **Integration Test**: コンポーネント間連携テスト
- **UI Test**: XCUITestによるUIテスト設計
- **テストダブル**: モック/スタブ/フェイク/スパイの設計
- **テストデータ**: フィクスチャ、ファクトリ、シード管理

## 実行条件

以下の状況でこのスキルを起動する：

- iOSアプリのテスト設計・実装を行う時
- 既存テストのリファクタリングを検討する時
- テストカバレッジを向上させたい時
- テストダブル（モック/スタブ）の設計を相談したい時
- テスト戦略を立案したい時
- テストの保守性・可読性を改善したい時

## プロセス

### Phase 1: テスト対象の分析

#### 1.1 対象コードの理解

1. テスト対象のクラス/構造体/関数を特定
2. 依存関係を洗い出す
3. 公開インターフェースを確認
4. 副作用（ネットワーク、永続化、通知等）を特定

#### 1.2 テスト可能性の評価

| 評価項目 | 確認内容 |
|---------|---------|
| 依存性注入 | コンストラクタ/プロパティ経由で差し替え可能か |
| 副作用の分離 | I/O操作がプロトコル経由で抽象化されているか |
| 状態の観測 | 内部状態の変化を外部から検証可能か |
| 決定論性 | 同一入力に対して同一出力が保証されるか |

### Phase 2: テスト戦略の策定

#### 2.1 テストピラミッドの設計

```
        ╱╲
       ╱  ╲     E2E Test（XCUITest）: 主要シナリオのみ
      ╱────╲
     ╱      ╲   Integration Test: コンポーネント間連携
    ╱────────╲
   ╱          ╲ Unit Test: ビジネスロジック中心
  ╱────────────╲
```

#### 2.2 テストレベル別の方針

| レベル | 対象 | テストダブル | 実行頻度 |
|-------|------|------------|---------|
| Unit | ビジネスロジック、ViewModel、Utility | スタブ/モック | 常時 |
| Integration | UseCase + Repository、View + ViewModel | スタブ（外部境界のみ） | PR/CI |
| UI | 主要ユーザーフロー | なし（実環境に近づける） | デイリー/リリース |

### Phase 3: XCTestによるUnitテスト設計

詳細は `references/xctest-patterns.md` を参照。

#### 3.1 テストケースの構造

```swift
final class SampleTests: XCTestCase {
    
    // MARK: - Properties
    private var sut: SystemUnderTest!
    private var mockDependency: MockDependency!
    
    // MARK: - Setup/Teardown
    override func setUp() {
        super.setUp()
        mockDependency = MockDependency()
        sut = SystemUnderTest(dependency: mockDependency)
    }
    
    override func tearDown() {
        sut = nil
        mockDependency = nil
        super.tearDown()
    }
    
    // MARK: - Tests
    func test_methodName_condition_expectedBehavior() {
        // Given（前提条件）
        let input = ...
        
        // When（実行）
        let result = sut.method(input)
        
        // Then（検証）
        XCTAssertEqual(result, expected)
    }
}
```

#### 3.2 命名規則

```
test_<対象メソッド>_<条件>_<期待される振る舞い>

例:
test_login_withValidCredentials_returnsSuccess
test_fetchUser_whenNetworkError_throwsError
test_calculate_withNegativeInput_returnsZero
```

### Phase 4: テストダブルの設計

詳細は `references/test-doubles.md` を参照。

#### 4.1 テストダブルの種類と使い分け

| 種類 | 用途 | 実装例 |
|-----|------|-------|
| Stub | 事前定義した値を返す | `stub.returnValue = expectedData` |
| Mock | 呼び出しを検証する | `XCTAssertTrue(mock.didCallMethod)` |
| Fake | 軽量な実装 | `InMemoryUserRepository` |
| Spy | 呼び出し履歴を記録 | `spy.calledArguments` |

#### 4.2 プロトコルベースのテストダブル

```swift
// 抽象化されたプロトコル
protocol UserRepositoryProtocol {
    func fetch(id: String) async throws -> User
}

// 本番実装
final class UserRepository: UserRepositoryProtocol { ... }

// テストダブル
final class MockUserRepository: UserRepositoryProtocol {
    var fetchResult: Result<User, Error> = .success(User.stub)
    var fetchCallCount = 0
    var lastFetchedId: String?
    
    func fetch(id: String) async throws -> User {
        fetchCallCount += 1
        lastFetchedId = id
        return try fetchResult.get()
    }
}
```

### Phase 5: XCUITestによるUIテスト設計

詳細は `references/xcuitest-patterns.md` を参照。

#### 5.1 Page Objectパターン

```swift
// Page Object
final class LoginPage {
    private let app: XCUIApplication
    
    var emailField: XCUIElement { app.textFields["email"] }
    var passwordField: XCUIElement { app.secureTextFields["password"] }
    var loginButton: XCUIElement { app.buttons["login"] }
    
    init(app: XCUIApplication) {
        self.app = app
    }
    
    func login(email: String, password: String) -> HomePage {
        emailField.tap()
        emailField.typeText(email)
        passwordField.tap()
        passwordField.typeText(password)
        loginButton.tap()
        return HomePage(app: app)
    }
}
```

#### 5.2 Accessibility Identifierの設計

| 要素 | 命名規則 | 例 |
|-----|---------|---|
| 画面 | `<screen>_screen` | `login_screen` |
| ボタン | `<action>_button` | `submit_button` |
| テキストフィールド | `<field>_field` | `email_field` |
| ラベル | `<content>_label` | `error_label` |
| セル | `<item>_cell_<index>` | `user_cell_0` |

### Phase 6: テストデータ管理

詳細は `references/test-data.md` を参照。

#### 6.1 Factoryパターン

```swift
enum UserFactory {
    static func make(
        id: String = UUID().uuidString,
        name: String = "Test User",
        email: String = "test@example.com",
        isActive: Bool = true
    ) -> User {
        User(id: id, name: name, email: email, isActive: isActive)
    }
    
    static var activeUser: User { make(isActive: true) }
    static var inactiveUser: User { make(isActive: false) }
}
```

#### 6.2 フィクスチャファイル

```
Tests/
├── Fixtures/
│   ├── JSON/
│   │   ├── user_response.json
│   │   └── error_response.json
│   └── Stubs/
│       └── UserStub.swift
```

### Phase 7: テストカバレッジ分析

#### 7.1 カバレッジ目標

| レベル | 目標 | 説明 |
|-------|-----|------|
| 行カバレッジ | 80%以上 | 実行された行の割合 |
| 分岐カバレッジ | 70%以上 | if/switch分岐の網羅 |
| 重要パス | 100% | ビジネスクリティカルなパス |

#### 7.2 Xcodeでのカバレッジ確認

1. スキーム設定 → Test → Options → Code Coverage有効化
2. `Cmd + U` でテスト実行
3. Report Navigator → Coverage でレポート確認

#### 7.3 カバレッジ改善の優先順位

1. **ビジネスロジック**: Domain層、UseCase層
2. **状態管理**: ViewModel、Reducer
3. **データ変換**: Mapper、Parser、Formatter
4. **エラーハンドリング**: 例外処理、リトライロジック

## 出力形式

### テスト設計ドキュメント

```markdown
# テスト設計書: <機能名>

## 1. テスト対象
- クラス/構造体: `ClassName`
- 責務: 〇〇を行う

## 2. テスト戦略
- テストレベル: Unit / Integration / UI
- テストダブル: 使用する依存のリスト

## 3. テストケース一覧
| ID | カテゴリ | テスト内容 | 期待結果 |
|----|---------|----------|---------|
| TC-001 | 正常系 | ... | ... |
| TC-002 | 異常系 | ... | ... |

## 4. テストダブル設計
- MockXxx: 〇〇の呼び出しを検証
- StubYyy: 〇〇の値を返す

## 5. テストデータ
- Factory: XxxFactory
- Fixture: xxx_response.json
```

### テストコード

```swift
import XCTest
@testable import TargetModule

final class FeatureTests: XCTestCase {
    // 上記パターンに従ったテストコード
}
```

## ガードレール

### 必須遵守事項

1. **テストの独立性**: 各テストは他のテストに依存しない
2. **テストの決定論性**: 同じ条件で常に同じ結果
3. **テストの高速性**: Unitテストは1秒以内に完了
4. **明確な命名**: テスト名から内容が分かる

### 禁止事項

1. **本番コードのテスト用変更**: テストのために本番コードにテスト用分岐を入れない
2. **ネットワーク依存**: Unitテストで実ネットワークアクセスしない
3. **時間依存**: `Date()` 直接使用ではなく注入する
4. **グローバル状態**: シングルトンの直接参照を避ける

### 警告事項

1. **過度なモック**: 全てをモックすると実装詳細への依存が増す
2. **テストの重複**: 同じ振る舞いを複数箇所でテストしない
3. **実装の検証**: 「どう動くか」ではなく「何をするか」をテスト

## 参照

- `references/xctest-patterns.md`: XCTestパターン集
- `references/xcuitest-patterns.md`: XCUITestパターン集
- `references/test-doubles.md`: テストダブル設計ガイド
- `references/test-data.md`: テストデータ管理ガイド
