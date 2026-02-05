---
name: swiftui-coding-guidelines
description: Core coding guidelines for iOS, iPadOS, macOS, watchOS, tvOS, and visionOS app development using SwiftUI and Swift. Use when implementing Views, working with @State/@Binding/@Observable/@StateObject, using NavigationStack/List/LazyVStack, designing components, or asking about SwiftUI patterns (infinite scroll, pull-to-refresh, search). Covers best practices, implementation patterns, and anti-patterns to avoid.
---

# SwiftUI Coding Guidelines

SwiftUIの日常的な開発で参照するコアガイドライン。

## ディレクトリ構成

```
swiftui-coding-guidelines/
├── SKILL.md (このファイル)
└── references/
    ├── best-practices.md      # ベストプラクティス
    ├── patterns-list.md       # 1-x: リスト・データ表示系
    ├── patterns-navigation.md # 2-x: ナビゲーション・画面遷移系
    ├── patterns-forms.md      # 3-x: フォーム・入力系
    ├── patterns-views.md      # 4-x: View構築・レイアウト系
    └── anti-patterns.md       # アンチパターン
```

## リファレンスファイル

### references/best-practices.md
SwiftUIのベストプラクティス集：
- **状態管理**: プロパティラッパー（@State、@Binding、@StateObject等）
- **パフォーマンス最適化**: View構造、LazyスタックとGrid、Equatable
- **コンポーネント設計**: 責務分離、Root Views vs Content Views、ViewModifier
- **非同期処理**: .taskモディファイア、async/await、@MainActor
- **ナビゲーション**: NavigationStack（iOS 16+）、型安全ルーティング
- **Layoutプロトコル**: GeometryReaderの代替（iOS 16+）
- **Preview駆動開発**: 複数状態プレビュー

### references/patterns-list.md（1-x: リスト・データ表示系）
| 番号 | パターン |
|------|---------|
| 1-1 | 無限スクロール（Pagination） |
| 1-2 | プルトゥリフレッシュ |
| 1-3 | フィルタリング・ソート |
| 1-4 | スワイプアクション |
| 1-5 | コンテキストメニュー |

### references/patterns-navigation.md（2-x: ナビゲーション・画面遷移系）
| 番号 | パターン |
|------|---------|
| 2-1 | タブビュー |
| 2-2 | ナビゲーション（NavigationStack） |
| 2-3 | モーダル表示（Sheet / FullScreenCover） |
| 2-4 | アラート・ダイアログ |

### references/patterns-forms.md（3-x: フォーム・入力系）
| 番号 | パターン |
|------|---------|
| 3-1 | 検索機能（デバウンス付き） |
| 3-2 | フォーム入力（バリデーション付き） |
| 3-3 | 認証画面（ログイン / 新規登録 / OTP） |

### references/patterns-views.md（4-x: View構築・レイアウト系）
| 番号 | パターン |
|------|---------|
| 4-1 | AsyncImage（キャッシュ付き） |
| 4-2 | 空状態・エラー状態 |
| 4-3 | アニメーション |
| 4-4 | View重なり（ZStack / overlay / background） |
| 4-5 | ContentUnavailableView（iOS 17+） |

### references/anti-patterns.md
アンチパターンと解決策：
- 状態管理、パフォーマンス、ビジネスロジック
- 非同期処理、ナビゲーション、メモリ管理
- ViewのIdentity: 不安定なID、ForEachでのインデックス使用
- AnyView: 型消去によるパフォーマンス低下
- コンポーネント設計: スペーシング管理、opacity vs if文

## 使用方法

### 新規実装時
1. 該当する`patterns-*.md`で実装パターン確認
2. `best-practices.md`で関連ベストプラクティス確認
3. `anti-patterns.md`で避けるべきパターン確認

### 問題解決時
1. `anti-patterns.md`で該当パターン検索
2. `best-practices.md`で推奨実装確認

## 重要な原則

1. **状態の最小化**: 導出可能な状態は持たない
2. **責務の分離**: Root Views（ロジック）とContent Views（UI）を分離
3. **パフォーマンス**: Lazy、Equatable、非同期処理の適切な使用
4. **ViewのIdentity**: 安定したIDを使用、ForEachでインデックス禁止
5. **スペーシングは親が管理**: 子コンポーネントはpaddingでスペースを作らない

## 関連スキル

- **swiftui-ssot**: 状態管理（SSOT）の詳細設計
- **swiftui-code-review-checklist**: PRレビュー用チェックリスト
- **swift-ios-migration**: iOS 17/18、Swift 6移行
- **swiftui-accessibility**: アクセシビリティ対応
