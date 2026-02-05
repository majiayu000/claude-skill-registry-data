---
name: agent-quality-standards
description: |
  エージェント品質基準と検証プロセスを専門とするスキル。エージェント設計、品質メトリクス、検証戦略、エラーハンドリング、品質スコアリングに対応。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: エージェント品質設計 / 目的: 実践的な品質基準の構築
  • Code Complete (Steve McConnell) / 適用: エラーハンドリング戦略 / 目的: 堅牢なエージェント実装

  Trigger:
  Use when evaluating agent quality, designing completion criteria, defining quality metrics, or planning error handling strategies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
version: 1.0.0
level: 1
last_updated: 2025-12-31
references:
  - book: "The Pragmatic Programmer"
    author: "Andrew Hunt, David Thomas"
    concepts:
      - "手順設計"
      - "実践的改善"
---

# Agent Quality Standards

## 概要

エージェント品質基準と検証プロセスを専門とするスキル。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要な references/scripts/templates を特定

**Task**: `agents/analyze-quality-context.md` を参照

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 品質スコアを算出し改善提案を作成

**Task**: `agents/apply-quality-standards.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す

**Task**: `agents/validate-quality.md` を参照

---

## Task仕様ナビ

| Task                    | 起動タイミング | 入力             | 出力             |
| ----------------------- | -------------- | ---------------- | ---------------- |
| analyze-quality-context | Phase 1開始時  | タスク仕様       | コンテキスト分析 |
| apply-quality-standards | Phase 2開始時  | コンテキスト分析 | 品質評価レポート |
| validate-quality        | Phase 3開始時  | 品質評価レポート | 検証結果レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

- エージェントの完了条件を設計する時
- 品質メトリクスを定義する時
- エラーハンドリング戦略を設計する時
- 品質評価とスコアリングを行う時

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける

## リソース参照

### 学習リソース（段階別）

| レベル | ファイル                            | 対象                         |
| ------ | ----------------------------------- | ---------------------------- |
| 基礎   | `references/Level1_basics.md`       | スキルの基本概念と初期設定   |
| 実務   | `references/Level2_intermediate.md` | 実装パターンと実務ガイド     |
| 応用   | `references/Level3_advanced.md`     | 高度な設計と最適化           |
| 専門   | `references/Level4_expert.md`       | 専門的なアプローチと事例研究 |

### スキル固有リソース

| リソース                           | 用途                                          |
| ---------------------------------- | --------------------------------------------- |
| `references/quality-metrics.md`    | 品質メトリクス定義と計算                      |
| `references/requirements-index.md` | 要求仕様の索引（docs/00-requirements と同期） |
| `references/legacy-skill.md`       | 旧SKILL.mdの全文（互換性確認用）              |

### テンプレート

| テンプレート                           | 用途               |
| -------------------------------------- | ------------------ |
| `assets/quality-checklist-template.md` | 品質チェックリスト |

### スクリプト（自動化）

| スクリプト                            | 機能               |
| ------------------------------------- | ------------------ |
| `scripts/calculate-quality-score.mjs` | 品質スコア計算     |
| `scripts/log_usage.mjs`               | 使用記録・自動評価 |
| `scripts/validate-skill.mjs`          | スキル構造検証     |

## 変更履歴

| Version | Date       | Changes                                                  |
| ------- | ---------- | -------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | agents/追加、Task仕様ナビ改善                            |
| 1.0.1   | 2025-12-31 | 18-skills.md仕様対応: frontmatter、Trigger、Task仕様ナビ |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added              |
