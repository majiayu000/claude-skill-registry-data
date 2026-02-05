---
name: observability-pillars
description: |
  オブザーバビリティ三本柱（ログ・メトリクス・トレース）の統合設計スキル。
  相関IDによる連携と双方向ナビゲーション（メトリクス→ログ→トレース）を実現。

  Anchors:
  • Observability Engineering (Charity Majors) / 適用: 三本柱統合パターン / 目的: 高カーディナリティObservability
  • Google SRE Book / 適用: メトリクス設計とSLI/SLO / 目的: 信頼性エンジニアリング
  • W3C Trace Context / 適用: 分散トレーシング標準 / 目的: 相互運用可能なトレース伝播

  Trigger:
  Use when integrating logs, metrics, and traces with correlation IDs, designing bi-directional navigation between pillars, implementing OpenTelemetry, or setting up high-cardinality observability.
  observability, three pillars, logs, metrics, traces, correlation ID, OpenTelemetry, tracing, distributed systems
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Observability Pillars

## 概要

オブザーバビリティ三本柱（ログ・メトリクス・トレース）の統合設計スキル。
Charity Majorsの『Observability Engineering』に基づき、相関IDによる連携と双方向ナビゲーションを実現する。

## ワークフロー

### Phase 1: 現状分析

**目的**: 既存のObservability成熟度を評価

**アクション**:

1. 現在のログ・メトリクス・トレース実装状況を調査
2. 相関IDの有無と一貫性を確認
3. ナビゲーション経路（メトリクス→ログ→トレース）を評価

**Task**: `agents/analyze-pillars.md` を参照

### Phase 2: 統合設計

**目的**: 三本柱の統合アーキテクチャを設計

**アクション**:

1. 相関ID体系（Request ID、Trace ID）を設計
2. コンテキスト伝播方式を選定（同期/非同期）
3. 双方向ナビゲーション経路を設計

**Task**: `agents/design-integration.md` を参照

### Phase 3: 実装

**目的**: 統合パターンを実装

**アクション**:

1. ミドルウェアで相関ID生成・伝播を実装
2. ログ・メトリクス・トレースにID埋め込み
3. ダッシュボードでナビゲーションリンクを設定

**Task**: `agents/implement-correlation.md` を参照

## Task仕様（ナビゲーション）

| Task                  | 起動タイミング | 入力         | 出力           |
| --------------------- | -------------- | ------------ | -------------- |
| analyze-pillars       | Phase 1開始時  | 現行システム | 成熟度評価結果 |
| design-integration    | Phase 2開始時  | 評価結果     | 統合設計書     |
| implement-correlation | Phase 3開始時  | 設計書       | 実装済みコード |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## 三本柱の役割

| 柱      | 目的             | 強み               | 弱み               |
| ------- | ---------------- | ------------------ | ------------------ |
| Logs    | イベント詳細記録 | 高カーディナリティ | 検索コスト高       |
| Metrics | 集約数値監視     | 低コスト、長期保持 | 詳細コンテキスト欠 |
| Traces  | リクエストフロー | 分散システム可視化 | サンプリング必要   |

## 相関ID体系

| ID Type    | スコープ           | フォーマット            | 生成タイミング     |
| ---------- | ------------------ | ----------------------- | ------------------ |
| Request ID | 単一HTTPリクエスト | UUID v4                 | リクエスト受信時   |
| Trace ID   | 分散システム全体   | W3C Trace Context (16B) | エントリーポイント |
| Span ID    | 単一操作           | 8バイトHex              | 各スパン開始時     |

## ベストプラクティス

### すべきこと

- 統一相関ID: すべての柱でrequest_id/trace_idを共有
- 双方向ナビゲーション: メトリクス ⇄ ログ ⇄ トレース
- 自動相関: 異常検知時に関連情報を自動収集
- 一貫性: タイムスタンプ・サービス名・環境を統一

### 避けるべきこと

- 三本柱が独立: 相関IDなしで各々が孤立
- メトリクスのみ依存: ログとトレースがない
- 過剰な高カーディナリティ: メトリクスに数百万のラベル
- PIIの無防備な記録: 個人情報をマスキングせず記録

## リソース参照

### references/（詳細知識）

| リソース            | パス                                                                         | 用途                       |
| ------------------- | ---------------------------------------------------------------------------- | -------------------------- |
| 基礎知識            | See [references/basics.md](references/basics.md)                             | 三本柱の基本概念           |
| 統合パターン        | See [references/integration-patterns.md](references/integration-patterns.md) | 相関ID・ナビゲーション設計 |
| OpenTelemetryガイド | See [references/opentelemetry-guide.md](references/opentelemetry-guide.md)   | OTel導入手順               |
| サンプリング戦略    | See [references/sampling-strategies.md](references/sampling-strategies.md)   | トレースサンプリング設計   |

### assets/（テンプレート）

| リソース | パス                           | 用途                              |
| -------- | ------------------------------ | --------------------------------- |
| 統合設定 | `assets/integration-config.ts` | OpenTelemetry統合設定テンプレート |

## 変更履歴

| Version | Date       | Changes                    |
| ------- | ---------- | -------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠 |
| 1.0.0   | 2025-12-24 | 初期実装                   |
