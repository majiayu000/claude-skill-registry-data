---
name: react-server-components
description: |
  React Server Components（RSC）の実装パターンとNext.js App Routerにおけるベストプラクティスを提供する専門スキル。
  サーバーコンポーネントとクライアントコンポーネントの責務分離、データフェッチの最適化、
  Suspenseとストリーミングの活用を支援します。

  Anchors:
  • 『Learning React Server Components』（Tejas Kumar）/ 適用: RSCアーキテクチャ / 目的: サーバーとクライアント間の責務分離
  • Next.js App Router公式ドキュメント / 適用: RSC実装パターン / 目的: Next.js固有の最適化手法
  • Dan Abramovのブログ / 適用: RSC設計思想 / 目的: 第一原理からの理解

  Trigger:
  Use when implementing Next.js App Router, designing Server Components, defining Client Component boundaries, optimizing data fetching, integrating Suspense, or implementing streaming SSR.
  rsc, server components, client components, next.js app router, use client, suspense, streaming, data fetching

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Server Components

## 概要

React Server Components（RSC）の実装パターンとNext.js App Routerにおけるベストプラクティスを提供する専門スキル。サーバーコンポーネントとクライアントコンポーネントの責務分離、データフェッチの最適化、Suspenseとストリーミングの活用を支援します。

## ワークフロー

### Phase 1: アーキテクチャ分析

**目的**: RSCアーキテクチャの適用範囲と境界を定義する

**アクション**:

1. `references/basics.md` でRSCの基本概念を確認
2. `references/server-client-boundaries.md` でコンポーネント境界を理解
3. プロジェクトの要件とRSCの適合性を評価

**Task**: `agents/analyze-architecture.md` を参照

### Phase 2: コンポーネント設計

**目的**: Server ComponentsとClient Componentsの適切な分離を設計する

**アクション**:

1. `references/server-client-boundaries.md` で境界設計パターンを確認
2. `references/composition-patterns.md` でコンポーネント構成を検討
3. テンプレートをベースに実装

**Task**: `agents/design-components.md` を参照

### Phase 3: データフェッチ最適化

**目的**: RSCの並列データフェッチとストリーミングを最適化する

**アクション**:

1. `references/data-fetching-patterns.md` で最適なパターンを選択
2. キャッシュ戦略を検討
3. Suspense境界を適切に配置

**Task**: `agents/optimize-data-fetching.md` を参照

### Phase 4: 検証と記録

**目的**: 実装の検証と実行記録の保存

**アクション**:

1. バンドルサイズを検証
2. コンポーネント境界の妥当性を確認
3. `scripts/log_usage.mjs` を実行して記録を残す

**Task**: `agents/validate-implementation.md` を参照

## Task仕様ナビ

| Task                    | 起動タイミング | 入力               | 出力               |
| ----------------------- | -------------- | ------------------ | ------------------ |
| analyze-architecture    | Phase 1開始時  | プロジェクト要件   | アーキテクチャ方針 |
| design-components       | Phase 2開始時  | アーキテクチャ方針 | コンポーネント設計 |
| optimize-data-fetching  | Phase 3開始時  | コンポーネント設計 | データフェッチ実装 |
| validate-implementation | Phase 4開始時  | 実装コード         | 検証済み実装       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

- Server Componentsをデフォルトとし、必要な場合のみClient Components（`'use client'`）を使用する
- データフェッチはできるだけサーバー側で行い、並列フェッチを活用する
- Suspense境界を適切に配置し、ユーザー体験を最適化する
- `async/await` を直接Server Components内で使用する（useEffect不要）
- クライアント側のJavaScriptを最小化し、バンドルサイズを削減する
- `references/composition-patterns.md` のパターンに従って、props drilling を回避する
- キャッシュ戦略（`cache()`, `revalidate`）を適切に設定する
- `references/server-client-boundaries.md` で境界設計の原則を確認する

### 避けるべきこと

- Server Components内でクライアント専用API（useState, useEffect等）を使用する
- Client Components内で直接データベース接続やAPIキーを扱う
- 不要にClient Componentsを使用し、クライアントバンドルを肥大化させる
- Suspense境界なしで非同期処理を行い、ウォーターフォールを引き起こす
- Server Componentsをprops経由でClient Componentsに渡す（children経由で渡すべき）
- `'use client'` ディレクティブを親コンポーネントに配置し、子までクライアント化する
- fetch結果を適切にキャッシュせず、同じリクエストを重複実行する
- エラーハンドリングを省略し、エラー時のUXを悪化させる
- テスト戦略を立てずに実装を進める
- 既存のPages Router パターンをそのまま適用する

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                             | 読込条件             |
| -------------- | -------------------------------------------------------------------------------- | -------------------- |
| 基礎           | [references/basics.md](references/basics.md)                                     | RSC初学者、基本理解  |
| 境界定義       | [references/server-client-boundaries.md](references/server-client-boundaries.md) | 境界設計時           |
| 構成パターン   | [references/composition-patterns.md](references/composition-patterns.md)         | コンポーネント構成時 |
| データフェッチ | [references/data-fetching-patterns.md](references/data-fetching-patterns.md)     | データ取得設計時     |

### scripts/（決定論的処理）

| スクリプト              | 機能                 |
| ----------------------- | -------------------- |
| `scripts/log_usage.mjs` | スキル使用履歴の記録 |

### assets/（テンプレート）

| アセット                              | 用途                         |
| ------------------------------------- | ---------------------------- |
| `assets/server-component-template.md` | Server Componentテンプレート |

## 変更履歴

| Version | Date       | Changes                               |
| ------- | ---------- | ------------------------------------- |
| 3.1.0   | 2026-01-02 | references/整理、18-skills.md仕様準拠 |
| 3.0.0   | 2026-01-02 | agents/追加（4エージェント体制確立）  |
| 1.0.0   | 2025-12-31 | 初版                                  |
