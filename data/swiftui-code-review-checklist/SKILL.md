---
name: swiftui-code-review-checklist
description: Code review checklist for SwiftUI and Swift PRs. Use when reviewing pull requests, checking code quality, verifying Swift/SwiftUI implementations, or conducting PR reviews. Provides prioritized checklist covering state management, performance, component design, data flow, async handling, UI/UX, accessibility, security, and testing.
---

# SwiftUI Code Review Checklist

SwiftUI PRレビュー用の包括的チェックリスト。

## ディレクトリ構成

```
swiftui-code-review-checklist/
├── SKILL.md (このファイル)
└── references/
    └── code-review-checklist.md
```

## リファレンスファイル

### references/code-review-checklist.md
コードレビュー用チェックリスト（優先度別）：

**🔴 Critical（必須）**
- 状態管理: SSOT違反、不適切なProperty Wrapper
- パフォーマンス: 不要な再描画、メモリリーク
- セキュリティ: 機密情報の露出

**🟡 Important（重要）**
- コンポーネント設計: 責務分離、再利用性
- データフロー: Binding、環境値の使用
- 非同期処理: Task管理、エラーハンドリング

**🟢 Nice to Have（推奨）**
- UI/UX: アニメーション、レイアウト
- アクセシビリティ: VoiceOver、Dynamic Type
- テスト: プレビュー、ユニットテスト

## 使用方法

### PRレビュー時
1. `references/code-review-checklist.md`を開く
2. 優先度順（🔴→🟡→🟢）でチェック
3. 問題があれば具体的な改善案を提示

### セルフレビュー時
1. PR作成前にチェックリストを確認
2. 自分のコードを検証

## クイックチェック項目

### 状態管理
- [ ] @Stateは適切に使われているか
- [ ] 状態の重複はないか
- [ ] Bindingの向きは正しいか

### パフォーマンス
- [ ] 不要な再描画が発生していないか
- [ ] LazyStack/Gridを適切に使っているか
- [ ] 重い処理はバックグラウンドで実行されているか

### コンポーネント設計
- [ ] Viewの責務は単一か
- [ ] 再利用可能な設計か
- [ ] モディファイアの順序は正しいか

## 関連スキル

- **swiftui-coding-guidelines**: ベストプラクティス・アンチパターン
- **swiftui-ssot**: 状態管理の詳細
- **swiftui-accessibility**: アクセシビリティチェック
