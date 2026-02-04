---
name: monitoring-alerting
description: |
  アプリケーションとインフラの監視・アラート設計を専門とするスキル。
  ゴールデンシグナル（レイテンシー・トラフィック・エラー・飽和度）に基づくメトリクス戦略、
  構造化ログ設計、SLI/SLO定義、アラート閾値設定、ダッシュボード構成を統合的に提供する。

  Anchors:
  • Observability Engineering (Charity Majors) / 適用: ログ設計とメトリクス戦略 / 目的: 高カーディナリティ観測の実現
  • Site Reliability Engineering (Google) / 適用: SLI/SLO設計 / 目的: ビジネス価値に基づく監視体系
  • Golden Signals / 適用: 4指標（Latency・Traffic・Errors・Saturation） / 目的: 効果的な監視指標の選定

  Trigger:
  Use when designing monitoring strategy, defining SLI/SLO, configuring alerts, implementing structured logging, or building observability dashboards.
  monitoring, alerting, observability, metrics, logging, SLI, SLO, golden signals, dashboard, Grafana, Prometheus, Discord webhook
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Monitoring & Alerting

## 概要

システム可観測性を実現するためのスキル。ゴールデンシグナルに基づくメトリクス戦略、
構造化ログ設計、SLI/SLO定義、アラート閾値設定を統合的に提供する。

## ワークフロー

### Phase 1: 監視戦略の立案

**目的**: ビジネス要件からSLI/SLOを定義し、監視対象を決定

**参照エージェント**: `agents/define-sli-slo.md`

**アクション**:

1. ビジネス目標からSLI（Service Level Indicator）を特定
2. ゴールデンシグナルの4軸を適用範囲内で選択
3. SLO（Service Level Objective）の目標値を設定
4. `references/golden-signals.md` でメトリクス設計パターンを確認

### Phase 2: 監視実装

**目的**: SLI/SLOに基づいてメトリクス、ログ、アラートを実装

**参照エージェント**: `agents/implement-monitoring.md`

**アクション**:

1. ログ設計：`references/logging-design.md` で構造化ログ仕様を確認
2. メトリクス収集：`scripts/check-metrics.mjs` で死活監視を実装
3. アラートルール定義：`references/alerting-rules.md` で閾値設定
4. 通知連携：`references/discord-notifications.md` でWebhook統合

### Phase 3: ダッシュボードと検証

**目的**: 可観測性の可視化と動作確認

**参照エージェント**: `agents/validate-observability.md`

**アクション**:

1. `assets/dashboard-template.json` でGrafanaダッシュボード構成
2. `scripts/check-metrics.mjs` でメトリクス出力を検証
3. `scripts/log_usage.mjs` で実行記録と成功/失敗を記録

## リソース参照

### 参照ドキュメント

| ドキュメント                                                               | 内容                              |
| -------------------------------------------------------------------------- | --------------------------------- |
| [references/basics.md](references/basics.md)                               | 監視基本概念、メトリクス/ログ分類 |
| [references/patterns.md](references/patterns.md)                           | 実装パターン、設計原則            |
| [references/golden-signals.md](references/golden-signals.md)               | ゴールデンシグナル4指標詳細       |
| [references/logging-design.md](references/logging-design.md)               | 構造化ログ仕様、相関ID設計        |
| [references/alerting-rules.md](references/alerting-rules.md)               | 閾値決定、エスカレーション        |
| [references/discord-notifications.md](references/discord-notifications.md) | Discord Webhook連携               |

### スクリプト

| スクリプト                   | 用途                                   |
| ---------------------------- | -------------------------------------- |
| `scripts/check-metrics.mjs`  | メトリクスエンドポイント確認、死活監視 |
| `scripts/log_usage.mjs`      | 使用記録・評価スクリプト               |
| `scripts/validate-skill.mjs` | スキル構造検証                         |

### テンプレート

| テンプレート                           | 用途                              |
| -------------------------------------- | --------------------------------- |
| `assets/alert-rules-template.yml`      | Prometheus/Alertmanagerルール定義 |
| `assets/dashboard-template.json`       | Grafanaダッシュボード設定         |
| `assets/incident-report-template.md`   | インシデント記録                  |
| `assets/structured-logger-template.ts` | 構造化ロガー実装例                |

## ベストプラクティス

### すべきこと

- ゴールデンシグナル優先でメトリクス選定
- 構造化ログ（JSON形式）で相関ID付与
- SLI/SLO駆動でアラート閾値決定
- 段階的監視実装（最初は3〜5メトリクス）
- アラート抑制ルールでノイズ防止

### 避けるべきこと

- 無差別なメトリクス収集（コスト増・ノイズ増）
- 固定閾値のみ（ビジネス目標との乖離）
- ログレベルの不統一（解析困難）
- アラート疲れを招く過剰通知
