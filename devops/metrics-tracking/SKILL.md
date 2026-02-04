---
name: metrics-tracking
description: |
  アジャイル開発におけるメトリクス追跡と分析のためのスキル。
  ベロシティ、リードタイム、DORA 4メトリクスの計測・可視化・改善を支援する。
  データ駆動の意思決定と継続的改善を実現する。

  Anchors:
  • Accelerate (Nicole Forsgren) / 適用: DORA 4メトリクス設計 / 目的: 科学的根拠に基づくメトリクス選定
  • Observability Engineering (Charity Majors) / 適用: 計測システム実装 / 目的: 信頼性の高いデータ収集
  • The Lean Startup (Eric Ries) / 適用: Build-Measure-Learn / 目的: 改善サイクルの確立

  Trigger:
  Use when measuring team performance, tracking velocity, analyzing lead time, implementing DORA metrics, or building metrics dashboards.
  metrics, velocity, burndown, lead time, DORA, deployment frequency, change failure rate, MTTR
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Metrics Tracking

## 概要

アジャイル開発チームのパフォーマンスを可視化し、データ駆動の意思決定と継続的改善を実現するためのスキル。DORA 4メトリクス（デプロイ頻度、リードタイム、変更失敗率、MTTR）を中核に、チーム固有のメトリクス計測システムを構築する。

## ワークフロー

### Phase 1: メトリクス定義

**目的**: ビジネスゴールに紐付いた計測対象メトリクスを定義する

**アクション**:

1. ビジネスゴール（市場投入速度、品質向上等）を特定
2. DORA 4メトリクスとの整合性を確認
3. 計測可能性（データソース、取得コスト）を検証
4. 計測間隔とデータ保持期間を決定
5. チームへの説明計画を策定

**Task**: `agents/define-metrics.md` を参照

### Phase 2: 計測実装

**目的**: メトリクス収集システムを構築し、自動化を確立する

**アクション**:

1. 計測ツール（Jira、GitHub、Grafana等）を設定
2. データパイプラインを構築
3. ダッシュボードを作成
4. 異常検知アラートを設定
5. `scripts/validate-metrics.mjs` で計測の妥当性を検証

**Task**: `agents/implement-collection.md` を参照

### Phase 3: 分析と改善

**目的**: メトリクスデータを分析し、継続的改善を推進する

**アクション**:

1. 週次・月次のメトリクスレビューを実施
2. トレンド分析と根本原因分析を実行
3. 改善施策を立案・実施・効果測定
4. `scripts/log_usage.mjs` で分析結果を記録

**Task**: `agents/analyze-improve.md` を参照

## Task仕様ナビ

| Task                 | 起動タイミング | 入力                         | 出力                         |
| -------------------- | -------------- | ---------------------------- | ---------------------------- |
| define-metrics       | Phase 1開始時  | ビジネスゴール、現状プロセス | メトリクス定義書             |
| implement-collection | Phase 2開始時  | メトリクス定義書             | 計測システム、ダッシュボード |
| analyze-improve      | Phase 3開始時  | 収集データ                   | 分析レポート、改善計画       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                               | 理由                       |
| -------------------------------------- | -------------------------- |
| ビジネスゴールからメトリクスを逆算する | 意味のある指標を選定できる |
| DORA 4メトリクスを基本セットとして採用 | 科学的に検証された指標     |
| チーム単位でメトリクスを公開する       | 心理的安全性を確保         |
| 3-5スプリント分のトレンドで判断する    | 単発の変動に惑わされない   |
| 計測システムを自動化する               | 手動入力の負荷を排除       |

### 避けるべきこと

| 禁止事項                           | 問題点               |
| ---------------------------------- | -------------------- |
| 個人のベロシティを計測・公開する   | 心理的安全性の低下   |
| 計測しやすさだけでメトリクスを選ぶ | ビジネス価値との乖離 |
| 単一メトリクスで意思決定する       | ゲーミングのリスク   |
| 異常値を調査せず無視する           | 改善機会の損失       |
| 時系列データを保持しない           | トレンド分析が不可能 |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                     | 機能                     |
| ------------------------------ | ------------------------ |
| `scripts/log_usage.mjs`        | 分析結果と改善実績の記録 |
| `scripts/validate-metrics.mjs` | メトリクス計測設定の検証 |

### references/（詳細知識）

| リソース           | パス                                                         | 読込条件           |
| ------------------ | ------------------------------------------------------------ | ------------------ |
| 基本概念           | [references/basics.md](references/basics.md)                 | 初回利用時         |
| 実装パターン       | [references/patterns.md](references/patterns.md)             | 計測システム構築時 |
| DORAフレームワーク | [references/dora-framework.md](references/dora-framework.md) | 高度な分析時       |

## 変更履歴

| Version | Date       | Changes                                |
| ------- | ---------- | -------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠版として再構築 |
| 1.2.0   | 2025-12-31 | Triggers、Anchors追加                  |
| 1.1.0   | 2025-12-24 | 初版作成                               |
