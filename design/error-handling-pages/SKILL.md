---
name: error-handling-pages
description: |
  Next.js App Routerのエラーハンドリングを専門とするスキル。
  error.tsx、not-found.tsx、global-error.tsxを使用したエラー境界とリカバリーを実現。

  Anchors:
  - The Pragmatic Programmer / 適用: エラーハンドリング原則 / 目的: 品質維持と堅牢性
  - Next.js Error Handling / 適用: error.tsx・not-found.tsx / 目的: エラーページ設計

  Trigger:
  Use when implementing error handling pages, designing error.tsx/not-found.tsx/global-error.tsx,
  or building error boundaries and recovery mechanisms in Next.js App Router.
  error.tsx, not-found.tsx, global-error.tsx, error boundary, recovery
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Error Handling Pages

## 概要

Next.js App Routerのエラーハンドリングを専門とするスキル。
error.tsx、not-found.tsx、global-error.tsxを使用したエラー境界とリカバリーを実現する。

## ワークフロー

### Phase 1: エラーページ要件の整理

**目的**: 必要なエラーページタイプを特定

**アクション**:

1. 対象ルートのエラーハンドリング要件を確認
2. `references/error-tsx-guide.md` でerror.tsxの実装パターンを確認
3. `references/not-found-guide.md` で404ページパターンを確認

**Task**: `agents/analyze-error-requirements.md` を参照

### Phase 2: エラーページ実装

**目的**: エラーハンドリングページを実装

**アクション**:

1. `assets/error-page-template.md` をベースにerror.tsxを実装
2. `assets/not-found-template.md` をベースにnot-found.tsxを実装
3. 必要に応じて`references/global-error-guide.md`でグローバルエラーを設定

**Task**: `agents/implement-error-pages.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/check-error-handling.mjs` でエラーハンドリングを検証
2. エラーページの動作確認
3. `scripts/log_usage.mjs` を実行して記録

## Task仕様（ナビゲーション）

| Task | 起動タイミング | 入力 | 出力 |
|------|----------------|------|------|
| analyze-error-requirements | 要件分析時 | ルート構造 | エラーページ要件書 |
| implement-error-pages | 実装時 | エラーページ要件書 | エラーページファイル群 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **ルート別エラーページ**: 各ルートセグメントにerror.tsxを配置
- **ユーザーフレンドリーメッセージ**: 技術的詳細を隠し、行動可能な情報を提供
- **リカバリーボタン**: reset()関数でエラーからの回復を提供
- **ローディング状態**: loading.tsxで読み込み中のUXを改善
- **global-error.tsx**: ルートレイアウトのエラーをキャッチ

### 避けるべきこと

- **生のエラーメッセージ表示**: ユーザーに技術的スタックトレースを見せない
- **リカバリー手段なし**: ユーザーが先に進める方法を提供する
- **階層の無視**: 親error.tsxが子のエラーをキャッチすることを忘れない

## リソース参照

### agents/（Task仕様書）

| Task | パス | 用途 |
|------|------|------|
| 要件分析 | See [agents/analyze-error-requirements.md](agents/analyze-error-requirements.md) | エラーページ要件整理 |
| 実装 | See [agents/implement-error-pages.md](agents/implement-error-pages.md) | エラーページ実装 |

### references/（詳細知識）

| リソース | パス | 用途 |
|----------|------|------|
| error.tsxガイド | See [references/error-tsx-guide.md](references/error-tsx-guide.md) | error.tsx実装パターン |
| not-foundガイド | See [references/not-found-guide.md](references/not-found-guide.md) | not-found.tsx実装パターン |
| global-errorガイド | See [references/global-error-guide.md](references/global-error-guide.md) | global-error.tsx実装 |
| loading.tsxガイド | See [references/loading-tsx-guide.md](references/loading-tsx-guide.md) | loading.tsx実装パターン |

### scripts/（決定論的処理）

| スクリプト | 用途 | 使用例 |
|------------|------|--------|
| `check-error-handling.mjs` | エラーハンドリング検証 | `node scripts/check-error-handling.mjs --help` |
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート | 用途 |
|--------------|------|
| `error-page-template.md` | error.tsxテンプレート |
| `not-found-template.md` | not-found.tsxテンプレート |

## 変更履歴

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-01 | agents追加、18-skills.md仕様完全準拠 |
| 2.0.0 | 2026-01-01 | 18-skills.md仕様完全準拠、Level1-4削除 |
| 1.0.0 | 2025-12-24 | 初版作成 |
