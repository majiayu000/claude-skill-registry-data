---
name: server-components-patterns
description: |
  React Server Componentsの実装パターン専門スキル。
  データフェッチ最適化、Suspenseストリーミング、サーバーアクション実装を提供する。

  Anchors:
  • Next.js Documentation / 適用: Server Components / 目的: パフォーマンス向上
  • React Server Components RFC / 適用: RSCアーキテクチャ / 目的: フェッチ最適化
  • Next.js Data Fetching / 適用: キャッシング戦略 / 目的: 効率的なデータ管理

  Trigger:
  Use when implementing React Server Components, designing RSC patterns, optimizing data fetching, planning Suspense boundaries, or implementing Server Actions.
  RSC, Server Components, data fetching, Suspense, streaming, Server Actions, cache, revalidate
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Server Components Patterns

## 概要

React Server Componentsのデータフェッチ最適化とSuspense活用を専門とするスキル。サーバーコンポーネントアーキテクチャ、データフェッチ戦略、キャッシング、サーバーアクションをカバーする。

## ワークフロー

```
analyze-requirements → design-pattern → implement-components → validate-performance
```

### Phase 1: 要件分析

**目的**: RSCパターンの要件を分析する

**Task**: `agents/analyze-requirements.md` を参照

**アクション**:

1. クライアント/サーバーコンポーネントの分離要件を確認
2. データフェッチのタイミング要件を確認
3. キャッシング戦略を検討

### Phase 2: パターン設計・実装

**目的**: 最適なRSCパターンを選定し実装する

**Task**: `agents/implement-pattern.md` を参照

**アクション**:

1. データフェッチパターンを選定
2. Suspense境界を設計
3. キャッシング戦略を適用
4. Server Actionsを実装

### Phase 3: 検証と最適化

**目的**: パフォーマンスを検証し最適化する

**アクション**:

1. データフェッチパターンを分析
2. パフォーマンスを測定
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                 | 責務         | 入力               | 出力                   |
| -------------------- | ------------ | ------------------ | ---------------------- |
| analyze-requirements | 要件分析     | コンポーネント情報 | RSC要件定義            |
| implement-pattern    | パターン実装 | RSC要件            | 実装済みコンポーネント |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                   |
| ---------------------------------- | ---------------------- |
| 可能な限りServer Componentを使用   | バンドルサイズ削減     |
| 並列フェッチにPromise.allを使用    | ウォーターフォール防止 |
| cache関数で重複排除する            | 不要なフェッチの削減   |
| 細かい粒度のSuspense境界を設計     | UXの向上               |
| revalidateタグで効率的にキャッシュ | オンデマンド再検証     |

### 避けるべきこと

| 禁止事項                           | 問題点               |
| ---------------------------------- | -------------------- |
| 過度なClient Component使用         | バンドルサイズ増加   |
| 逐次フェッチ（ウォーターフォール） | パフォーマンス低下   |
| 粗粒度のSuspense境界               | UX低下               |
| N+1クエリ                          | データベース負荷増大 |
| サーバー検証の省略                 | セキュリティリスク   |

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                         | 読込条件         |
| -------------- | ---------------------------------------------------------------------------- | ---------------- |
| データフェッチ | [references/data-fetching-patterns.md](references/data-fetching-patterns.md) | フェッチ実装時   |
| キャッシング   | [references/caching-strategies.md](references/caching-strategies.md)         | キャッシュ設定時 |
| Suspense       | [references/suspense-streaming.md](references/suspense-streaming.md)         | ストリーミング時 |
| Server Actions | [references/server-actions.md](references/server-actions.md)                 | アクション実装時 |

### scripts/（決定論的処理）

| スクリプト                          | 機能               |
| ----------------------------------- | ------------------ |
| `scripts/log_usage.mjs`             | 使用記録と自動評価 |
| `scripts/analyze-data-fetching.mjs` | データフェッチ分析 |

### assets/（テンプレート）

| アセット                           | 用途                       |
| ---------------------------------- | -------------------------- |
| `assets/data-fetch-template.md`    | データフェッチテンプレート |
| `assets/server-action-template.md` | Server Actionテンプレート  |

## 変更履歴

| Version | Date       | Changes                                            |
| ------- | ---------- | -------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills仕様完全準拠、agents/を責務ベースに再構成 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に基づきリファクタリング           |
| 1.0.0   | 2025-12-24 | 初版                                               |
