---
name: health-check-implementation
description: |
  ヘルスチェックの設計・実装・監視の指針を提供するスキル。マイクロサービスの信頼性と観測性を確立するためのガイダンスを提供。

  Anchors:
  • Observability Engineering (Charity Majors) / 適用: ヘルスチェック設計の観測性原則 / 目的: 効果的なモニタリング指標の選定
  • Site Reliability Engineering (Google) / 適用: ヘルスチェックのレベル分類と段階的実装 / 目的: 運用負荷の最適化
  • Release It! (Michael T. Nygard) / 適用: 障害対応パターン / 目的: 自動回復とフェイルセーフ設計

  Trigger:
  Use when designing microservice health checks, implementing system reliability monitoring, establishing baseline metrics, or configuring alert thresholds.
  health check, liveness probe, readiness probe, monitoring, metrics, observability, kubernetes probes, circuit breaker
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Health Check Implementation

## 概要

ヘルスチェックの設計・実装・監視を通じて、マイクロサービスの信頼性と観測性を確立するためのガイダンス。
Liveness/Readinessプローブ、依存関係チェック、カスケード障害防止を含む包括的なヘルスチェック戦略を提供。

## ワークフロー

### Phase 1: 要件分析と仕様設計

**目的**: ヘルスチェック実装の要件を明確化し、仕様を策定

**アクション**:

1. `references/Level1_basics.md` でヘルスチェックの分類を確認
2. 対象システムのRTO/RPO要件を整理
3. 依存サービスとの関係性をマッピング
4. `assets/health-check-specification-template.md` で仕様を作成

**Task**: `agents/specification-design.md` を参照

### Phase 2: メトリクス定義と実装

**目的**: 有効なヘルスチェック指標を定義し実装

**アクション**:

1. `references/Level2_intermediate.md` で段階的実装パターンを参照
2. `assets/metrics-definition-template.md` でメトリクスを定義
3. Liveness/Readinessプローブを実装
4. 依存関係チェックを組み込み

**Task**: `agents/metrics-definition.md` を参照

### Phase 3: アラート設定と検証

**目的**: アラート閾値を設定し、動作を検証

**アクション**:

1. `assets/alert-configuration-template.md` でアラート設定
2. `scripts/validate-skill.mjs` で構成を検証
3. 非本番環境でテスト実行
4. `scripts/log_usage.mjs` で使用記録

**Task**: `agents/threshold-configuration.md` を参照

## Task仕様ナビ

| Task                    | 起動タイミング | 入力           | 出力               |
| ----------------------- | -------------- | -------------- | ------------------ |
| specification-design    | Phase 1開始時  | システム要件   | ヘルスチェック仕様 |
| metrics-definition      | Phase 2開始時  | 仕様書         | メトリクス定義書   |
| threshold-configuration | Phase 3開始時  | メトリクス定義 | アラート設定       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- Liveness/Readinessプローブを明確に分離
- 依存サービスの状態を段階的にチェック
- タイムアウトと再試行の適切な設定
- メトリクス収集とアラート設定を一体で設計
- 非本番環境での十分な検証
- グレースフルデグラデーションの実装

### 避けるべきこと

- 過度に細粒度なヘルスチェック（運用負荷増加）
- 根拠のないアラート閾値設定
- 依存サービスの障害を即座に自身の障害として報告
- タイムアウトなしの外部依存チェック
- 単純な自動修復の有効化（段階的フェイルセーフを検討）

## リソース参照

### references/（詳細知識）

| リソース   | パス                                                                       | 内容                   |
| ---------- | -------------------------------------------------------------------------- | ---------------------- |
| 基礎知識   | See [references/Level1_basics.md](references/Level1_basics.md)             | 分類と基本パターン     |
| 中級知識   | See [references/Level2_intermediate.md](references/Level2_intermediate.md) | 段階的実装手順         |
| 上級知識   | See [references/Level3_advanced.md](references/Level3_advanced.md)         | 複雑なトポロジー対応   |
| 専門家向け | See [references/Level4_expert.md](references/Level4_expert.md)             | 大規模分散システム展開 |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                        |
| -------------------- | ------------------ | --------------------------------------------- |
| `validate-skill.mjs` | スキル構造検証     | `node scripts/validate-skill.mjs`             |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート                             | 用途                 |
| ---------------------------------------- | -------------------- |
| `health-check-specification-template.md` | ヘルスチェック仕様書 |
| `metrics-definition-template.md`         | メトリクス定義書     |
| `alert-configuration-template.md`        | アラート設定書       |

## 変更履歴

| Version | Date       | Changes                                       |
| ------- | ---------- | --------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md完全準拠、形式統一、Trigger英語化 |
| 1.1.0   | 2025-12-31 | Anchors/Trigger追加、Task仕様ナビ導入         |
| 1.0.0   | 2025-12-24 | 初版                                          |
