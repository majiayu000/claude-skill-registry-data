---
name: conditional-execution-gha
description: |
  GitHub Actions の条件付き実行を設計し、if 条件とイベントフィルタの運用を支援するスキル。
  条件式の整理、イベント別の分岐、検証と記録の流れを体系化する。

  Anchors:
  • The Pragmatic Programmer（Andrew Hunt, David Thomas）/ 適用: 条件分岐による品質管理 / 目的: 実践的な流れ制御パターンを参照
  • Continuous Delivery（Jez Humble）/ 適用: パイプラインの段階的実行制御 / 目的: 効率的な実行制御
  • GitHub Actions / 適用: if 条件・event filters・status functions / 目的: 標準構文の準拠

  Trigger:
  Use when designing conditional execution in GitHub Actions workflows, handling if expressions, or applying event filters and status functions.
  conditional execution, github actions, if conditions, event filters, status functions
---
# conditional-execution-gha

## 概要

GitHub Actions の条件付き実行を設計し、if 条件とイベントフィルタを運用する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 目的・条件・制約を明確化する。

**アクション**:

1. 目的と実行条件を整理する。
2. 失敗時の挙動と制約を整理する。
3. 条件式の影響範囲を整理する。

**Task**: `agents/analyze-conditional-requirements.md` を参照

### Phase 2: 条件設計

**目的**: if 条件とイベントフィルタの構成を設計する。

**アクション**:

1. if 条件とイベントフィルタの構成を決める。
2. 条件の優先順位と例外を整理する。
3. 検証手順と監視項目を整理する。

**Task**: `agents/design-conditional-logic.md` を参照

### Phase 3: 検証と記録

**目的**: 条件式と構造を検証し記録を更新する。

**アクション**:

1. `scripts/validate-skill.mjs` で構造を検証する。
2. `scripts/analyze-conditions.mjs` で条件式を分析する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-conditional-setup.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-conditional-requirements | Phase 1開始時 | 目的/条件 | 要件整理メモ、成功条件一覧 |
| design-conditional-logic | Phase 2開始時 | 要件整理メモ | 条件実行設計書、検証ガイド |
| validate-conditional-setup | Phase 3開始時 | 条件実行設計書 | 検証レポート、ログ更新内容 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| 条件式の意図を明文化する | 影響範囲を把握するため |
| イベントフィルタを整理する | 無駄な実行を防ぐため |
| 失敗時の挙動を定義する | 運用の再現性を保つため |
| テンプレートを参照する | 構文ミスを防ぐため |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| 条件式を過度に複雑化する | メンテナンスが難しくなる |
| 影響範囲を確認しない | 意図しない実行が起きる |
| 検証なしで運用する | 失敗の検知が遅れる |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/analyze-conditions.mjs` | 条件式の分析 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 初回整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 詳細設計時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 改善ループ時 |
| event filtering | [references/event-filtering.md](references/event-filtering.md) | イベント条件整理時 |
| if 条件 | [references/if-conditions.md](references/if-conditions.md) | 条件式設計時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/conditional-workflow.yaml` | 条件付き実行テンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
