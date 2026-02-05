---
name: swiftui-ssot
description: Single Source of Truth (SSOT) guidelines for SwiftUI state management. Use when designing state architecture, choosing between @State/@Binding/@StateObject/@ObservedObject/@EnvironmentObject, fixing state synchronization issues, refactoring duplicated state, or reviewing state management in PRs. Covers SSOT principles, property wrapper selection, state lifting, and common violations.
---

# SwiftUI SSOT (Single Source of Truth)

SwiftUIにおける状態管理とSSOT原則の包括的ガイド。

## ディレクトリ構成

```
swiftui-ssot/
├── SKILL.md (このファイル)
└── references/
    └── ssot.md
```

## リファレンスファイル

### references/ssot.md
Single Source of Truth（SSOT）の包括的ガイド：
- **SSOTの3つの柱**: 唯一の情報源、導出状態、単方向データフロー
- **Property Wrapper選択フローチャート**: @State/@Binding/@StateObject/@ObservedObject/@EnvironmentObject
- **パターン別ガイド**:
  - 状態重複の解消
  - 導出状態（Computed Property）
  - State Lifting（状態の持ち上げ）
  - 兄弟View間通信
  - EnvironmentObjectの適切な使用
- **違反検出方法**: コードスメル、検索パターン
- **iOS 17+ @ObservableでのSSO実装**
- **レビューチェックリスト**

## 使用方法

### 状態設計時
1. `references/ssot.md`のProperty Wrapper選択フローチャートを参照
2. データの所有者を明確化
3. 導出可能な状態は持たない

### 状態関連の問題発生時
1. `references/ssot.md`の違反パターンを確認
2. 該当するパターンの解決策を適用

### PRレビュー時
1. `references/ssot.md`のレビューチェックリストを使用

## SSOT 3つの柱

1. **唯一の情報源**: 各データは1箇所でのみ管理
2. **導出状態**: 他の状態から計算可能なものは持たない
3. **単方向データフロー**: 親→子へデータを渡し、子→親へはアクション

## Property Wrapper 選択ガイド

| 状況 | 推奨 |
|------|------|
| View内のローカル状態 | `@State` |
| 親から受け取る値（読み書き） | `@Binding` |
| Viewが所有するObservableObject | `@StateObject` |
| 外部から注入されるObservableObject | `@ObservedObject` |
| アプリ全体で共有 | `@EnvironmentObject` |
| iOS 17+ | `@Observable` + `@Bindable` |

## 関連スキル

- **swiftui-coding-guidelines**: 基本的なベストプラクティス
- **swift-ios-migration**: iOS 17 @Observable移行
