---
name: data-fetching-strategies
description: |
  Reactアプリのデータフェッチ、キャッシュ、エラーハンドリング、楽観的更新を整理するスキル。
  ライブラリ選定から設計・実装・検証までの実務フローを提供する。

  Anchors:
  • Stale-While-Revalidate Pattern / 適用: キャッシュ戦略 / 目的: サーバー状態の一貫性確保
  • React Query vs SWR / 適用: ライブラリ選定 / 目的: 要件に最適な選択
  • MSW / 適用: テスト環境構築 / 目的: API依存の排除

  Trigger:
  Use when implementing data fetching patterns, cache strategies, error handling, optimistic updates, or choosing between SWR and React Query.
  data fetching, cache strategy, swr, react query, optimistic updates, error handling
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# data-fetching-strategies

## 概要

サーバー状態の取得と更新に関する設計・実装・検証の基準を提供し、安定したデータフェッチを実現する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 取得対象・更新頻度・UX要件を整理する。

**アクション**:

1. 取得対象と更新頻度を整理する。
2. エラーハンドリングとローディング要件を整理する。
3. 既存ライブラリの有無を確認する。

**Task**: `agents/analyze-fetching-requirements.md` を参照

### Phase 2: 設計

**目的**: ライブラリ選定とキャッシュ設計を行う。

**アクション**:

1. `references/library-comparison.md` でライブラリを比較する。
2. `references/caching-patterns.md` でキャッシュ方針を設計する。
3. `references/query-key-guidelines.md` でキー設計を決める。

**Task**: `agents/design-fetching-architecture.md` を参照

### Phase 3: 実装

**目的**: データフェッチを実装し、最適化を反映する。

**アクション**:

1. `assets/swr-hook-template.md` と `assets/react-query-hook-template.md` を参照する。
2. `references/optimistic-updates.md` で更新方針を確認する。
3. `scripts/analyze-data-fetching.mjs` で実装の傾向を確認する。

**Task**: `agents/implement-fetching-patterns.md` を参照

### Phase 4: 検証と記録

**目的**: 実装品質を検証し、運用記録を残す。

**アクション**:

1. `references/error-loading-states.md` でUI状態を確認する。
2. `assets/fetching-review-checklist.md` でレビューする。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-fetching-quality.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-fetching-requirements | Phase 1開始時 | 取得対象/制約 | 要件メモ、優先度一覧 |
| design-fetching-architecture | Phase 2開始時 | 要件メモ | 設計方針、キャッシュ方針 |
| implement-fetching-patterns | Phase 3開始時 | 設計方針 | 実装メモ、変更内容 |
| validate-fetching-quality | Phase 4開始時 | 実装メモ | 検証レポート、改善提案 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| ライブラリ選定を明確にする | 運用負荷を減らす |
| キャッシュ方針を決める | UXを安定させる |
| エラーハンドリングを統一する | 回復性を高める |
| 楽観的更新のロールバックを用意する | 失敗時の整合性確保 |
| テスト観点を整理する | 回帰を防ぐ |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| ライブラリの併用 | 保守性が低下する |
| キャッシュ無しの実装 | 遅延と負荷が増える |
| エラーの握りつぶし | 問題検知が遅れる |
| 状態の混在 | 保守性が落ちる |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/analyze-data-fetching.mjs` | データフェッチの分析 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 実装時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 検証時 |
| ライブラリ比較 | [references/library-comparison.md](references/library-comparison.md) | 選定時 |
| キャッシュパターン | [references/caching-patterns.md](references/caching-patterns.md) | キャッシュ設計時 |
| エラー/ローディング | [references/error-loading-states.md](references/error-loading-states.md) | UI設計時 |
| 楽観的更新 | [references/optimistic-updates.md](references/optimistic-updates.md) | 更新設計時 |
| キー設計 | [references/query-key-guidelines.md](references/query-key-guidelines.md) | キー設計時 |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md) | 仕様確認時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/swr-hook-template.md` | SWRフックテンプレート |
| `assets/react-query-hook-template.md` | React Queryフックテンプレート |
| `assets/fetching-requirements-template.md` | 要件整理テンプレート |
| `assets/cache-policy-matrix.md` | キャッシュ方針整理 |
| `assets/fetching-review-checklist.md` | 実装レビュー観点 |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
