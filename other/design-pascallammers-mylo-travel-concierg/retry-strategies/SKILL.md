---
name: retry-strategies
description: |
  外部APIや分散システムの一時的障害に対して、リトライ・タイムアウト・サーキットブレーカーを組み合わせた回復戦略を設計し、実装まで導くスキル。
  失敗特性の分類、指数バックオフとジッター、隔離（Bulkhead）などの適用判断を整理し、過剰リトライや雪崩障害を避ける。

  Anchors:
  • Designing Data-Intensive Applications / 適用: 分散システムの障害特性と復旧設計 / 目的: 失敗モードに合わせた戦略選定
  • Release It! (Michael T. Nygard) / 適用: Circuit Breaker・Bulkhead・Timeout / 目的: 耐障害パターンの適切な適用
  • AWS Architecture Blog - Exponential Backoff and Jitter / 適用: リトライ待機とジッター / 目的: 負荷集中の回避

  Trigger:
  Use when designing retry policies, tuning timeouts, introducing circuit breakers or bulkheads, or validating resilience for external API calls.
  retry, backoff, jitter, circuit breaker, bulkhead, timeout, transient failure, resilience
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Retry Strategies

## 概要

外部APIや分散システムの一時的障害に対して、再試行の方針と耐障害パターンを設計し、実装・検証・運用設計までの判断材料を整理するスキルです。

## ワークフロー

### Phase 1: 障害特性アセスメント

**目的**: 依存関係と失敗モードを整理し、リトライ対象と制約を明確化する

**アクション**:

1. 依存先、SLA、過去障害の情報を収集
2. エラーを恒久/一時/部分失敗に分類
3. 再試行可能性（べき等性、予算、上限）を整理
4. 監視指標と制約条件を定義

**Task**: `agents/assess-failure-profile.md` を参照

### Phase 2: リトライ/耐障害ポリシー設計

**目的**: 失敗特性に適合するリトライと保護パターンを設計する

**アクション**:

1. バックオフ曲線とジッター方式を選定
2. Circuit Breaker/Bulkhead/Timeoutの組み合わせを決定
3. しきい値、リトライ予算、上限値を設計
4. 設定パラメータと適用範囲を文書化

**Task**: `agents/design-retry-policy.md` を参照

### Phase 3: 実装検証と運用設計

**目的**: 実装の妥当性を検証し、運用監視の設計を固める

**アクション**:

1. `scripts/analyze-retry-config.mjs` で設定を分析
2. テストシナリオと失敗注入条件を整理
3. 監視指標、アラート、ロールバック手順を定義

**Task**: `agents/validate-rollout.md` を参照

## Task仕様ナビ

| Task                   | 起動タイミング | 入力                         | 出力                               |
| ---------------------- | -------------- | ---------------------------- | ---------------------------------- |
| assess-failure-profile | Phase 1開始時  | 依存関係と障害情報           | 障害特性プロファイル               |
| design-retry-policy    | Phase 2開始時  | 障害特性プロファイル         | リトライ/耐障害ポリシー設計書       |
| validate-rollout       | Phase 3開始時  | 実装コードと設定             | 検証レポート・運用設計ドラフト     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                                       |
| ---------------------------------- | ------------------------------------------ |
| 失敗モードを恒久/一時で分類する    | 不要な再試行を避け、成功率を上げる         |
| リトライ予算と上限を明示する       | 雪崩障害と過剰負荷を防ぐ                   |
| 指数バックオフにジッターを入れる   | 同時リトライによる負荷集中を避ける         |
| しきい値は計測値に基づいて設計する | 障害の検知精度と復旧速度を両立する         |
| タイムアウトをSLAに合わせて設計する | 失敗検知の遅延と待ち過ぎを防ぐ             |

### 避けるべきこと

| 禁止事項                             | 問題点                                   |
| ------------------------------------ | ---------------------------------------- |
| 無限リトライや過度な再試行            | 依存先の障害を拡大させる                 |
| 固定間隔リトライのみの設計            | サンダリングハードを誘発する             |
| エラー種別を区別しない一律リトライ    | 永続障害で無駄な負荷をかける             |
| タイムアウトを未設定のまま運用        | 障害検知が遅れ、回復判断ができない       |
| Circuit Breakerを導入せず外部依存を増やす | 障害の連鎖と復旧遅延を招く           |

## リソース参照

### references/（詳細知識）

| リソース                     | パス                                                                     | 読込条件                     |
| ---------------------------- | ------------------------------------------------------------------------ | ---------------------------- |
| 基礎知識                     | [references/Level1_basics.md](references/Level1_basics.md)               | Phase 1の整理時              |
| 実務判断の整理               | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | Phase 2の設計時              |
| 応用パターン                 | [references/Level3_advanced.md](references/Level3_advanced.md)           | 複雑なケース検討時           |
| エッジケース                 | [references/Level4_expert.md](references/Level4_expert.md)               | 例外条件の調整時             |
| Exponential Backoff          | [references/exponential-backoff.md](references/exponential-backoff.md)   | バックオフ設計時             |
| Circuit Breaker              | [references/circuit-breaker.md](references/circuit-breaker.md)           | しきい値設計時               |
| Bulkhead Pattern             | [references/bulkhead-pattern.md](references/bulkhead-pattern.md)         | 隔離戦略検討時               |
| Timeout Strategies           | [references/timeout-strategies.md](references/timeout-strategies.md)     | タイムアウト設計時           |

### scripts/（決定論的処理）

| スクリプト                           | 機能                                     |
| ------------------------------------ | ---------------------------------------- |
| `scripts/analyze-retry-config.mjs`   | リトライ/CB/タイムアウト設定の静的分析   |
| `scripts/validate-skill.mjs`         | スキル構造と参照リンクの検証             |
| `scripts/log_usage.mjs`              | スキル使用ログの記録                     |

### assets/（テンプレート）

| アセット                               | 用途                                 |
| -------------------------------------- | ------------------------------------ |
| `assets/circuit-breaker-template.ts`   | Circuit Breaker実装の雛形            |
| `assets/retry-wrapper-template.ts`     | リトライラッパーの再利用テンプレート  |

## 変更履歴

| Version | Date       | Changes                                                           |
| ------- | ---------- | ----------------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に合わせて再設計、Task仕様書追加、構成を整理       |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様に合わせてagents/とEVALSを追加                    |
| 1.0.0   | 2025-12-24 | 仕様整合と必要成果物の追加                                        |
