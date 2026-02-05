---
name: swift-ios-migration
description: Migration guide for Swift and iOS. Use when migrating ObservableObject to @Observable (iOS 17), enabling Swift 6/6.2 Strict Concurrency, fixing @MainActor/Sendable warnings, adopting Approachable Concurrency (Swift 6.2), or handling iPadOS 26 windowing system changes (UIRequiresFullScreen deprecation). Covers breaking changes and version upgrade tasks.
---

# Swift/iOS マイグレーションガイド

既存コードの移行作業やバージョンアップに伴う破壊的変更への対応ガイド。

## ディレクトリ構成

```
swift-ios-migration/
├── SKILL.md (このファイル)
└── references/
    ├── ios17-observable.md   # @Observable移行パターン
    ├── swift6-concurrency.md # Swift 6並行処理対応
    ├── swift62-changes.md    # Swift 6.2 / Xcode 26
    └── ipados26-windowing.md # iPadOS 26ウィンドウシステム
```

## リファレンスファイル

### references/ios17-observable.md
iOS 17+ @Observableマクロへの移行ガイド：
- **移行パターン**: ObservableObject → @Observable
- **@Bindable**: @Published/@Bindingの代替
- **@Environment変更**: 環境値の新しい渡し方
- **パフォーマンス向上**: プロパティ単位の監視
- **注意点**: 互換性、既存コードとの共存

### references/swift6-concurrency.md
Swift 6並行処理対応ガイド：
- **@MainActor**: ViewModel全体への適用、UI保護
- **Sendable**: データモデル設計、アクター境界
- **移行チェックリスト**: Strict Concurrency Checking有効化
- **よくある警告と解決策**:
  - "Non-sendable type captured"
  - "Actor-isolated property cannot be mutated"
- **Actor**: カスタムActorでスレッドセーフ保証

### references/swift62-changes.md
Swift 6.2 / Xcode 26 移行ガイド：
- **Approachable Concurrency**: より使いやすい並行処理
- **Default Actor Isolation**: MainActorをデフォルトに
- **@concurrent**: 明示的なバックグラウンド実行
- **Xcode 26新機能**: AI Coding Tools、Playground強化
- **デバッグ改善**: LLDB強化、並行処理デバッグ

### references/ipados26-windowing.md
iPadOS 26 ウィンドウシステム移行ガイド：
- **UIRequiresFullScreen廃止**: Info.plistからの削除、Auto Layout対応
- **シーンジオメトリ**: UIWindowScene.Geometry、effectiveGeometry、リサイズ検知
- **サイズ制限**: UISceneSizeRestrictions、minimumSize/maximumSize設定
- **方向ロック**: prefersInterfaceOrientationLocked、方向変更監視
- **メニューバー対応**: SwiftUI Commands、UIMenuBuilder、キーボードショートカット
- **マルチウィンドウ**: UIApplicationSupportsMultipleScenes、新規ウィンドウ作成
- **Trait Collection**: サイズクラス対応、自動トラッキング

## 使用方法

### iOS 17 @Observable移行時
1. `references/ios17-observable.md`で移行パターン確認
2. 新規コードから`@Observable`を使用開始
3. 既存の小さなViewModelから段階的に移行
4. 大きなViewModelは慎重に移行

### Swift 6移行時
1. `references/swift6-concurrency.md`でチェックリスト確認
2. Strict Concurrency Checkingを有効化
3. ViewModelに`@MainActor`を追加
4. データモデルを`Sendable`に対応
5. 警告を順次解消

### Swift 6.2移行時
1. `references/swift62-changes.md`で新機能確認
2. Xcode 26にアップデート
3. Approachable Concurrencyを有効化
4. Default Actor IsolationをMainActorに設定
5. 必要な箇所に`@concurrent`を追加
6. 既存のSwift 6コードを簡略化

### iPadOS 26ウィンドウシステム対応時
1. `references/ipados26-windowing.md`で移行チェックリスト確認
2. `UIRequiresFullScreen`をInfo.plistから削除
3. Auto Layoutでサイズ適応レイアウトを実装
4. `UISceneSizeRestrictions`で最小サイズを設定
5. メニューバー対応（外部キーボード使用時）

## 移行優先順位

### Swift 6.2（推奨順）
1. Build SettingsでApproachable Concurrencyを有効化
2. Default Actor IsolationをMainActorに設定
3. 必要な箇所に`@concurrent`を追加
4. 既存のSwift 6コードを簡略化

### Swift 6（推奨順）
1. ViewModelに`@MainActor`を追加
2. データモデルを`Sendable`に対応
3. 非同期処理を`async/await`に統一

### iOS 17 @Observable（推奨順）
1. 新規コードから`@Observable`を使用
2. 既存の小さなViewModelから移行
3. 大きなViewModelは慎重に移行

### iPadOS 26（推奨順）
1. Xcode 26でビルド・テスト
2. UIRequiresFullScreenを削除
3. Auto Layout対応を確認
4. メニューバー実装

## バージョン対応表

| 機能 | Swift 5.9 | Swift 6 | Swift 6.2 |
|------|-----------|---------|-----------|
| Strict Concurrency | Opt-in | Default | Default |
| @MainActor | ✅ | ✅ | ✅ |
| Default Actor Isolation | - | - | ✅ |
| @concurrent | - | - | ✅ |
| Approachable Concurrency | - | - | ✅ |

| 機能 | iOS 16 | iOS 17 | iOS 18 | iOS 26 |
|------|--------|--------|--------|--------|
| @Observable | - | ✅ | ✅ | ✅ |
| iPadOS新ウィンドウシステム | - | - | - | ✅ |

## 関連スキル

- **swiftui-components**: UIコンポーネントカタログ
- **swiftui-coding-guidelines**: 基本的なベストプラクティス
- **swiftui-ssot**: 状態管理の設計
- **swiftui-accessibility**: アクセシビリティ実装

