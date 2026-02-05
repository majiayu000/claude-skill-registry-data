---
name: prompt-testing-evaluation
description: |
  プロンプトのテスト、評価、反復改善を専門とするスキル。A/Bテスト、評価メトリクス、自動化されたプロンプト品質保証により、本番環境で信頼性の高いプロンプトを実現します。

  Anchors:
  • Test-Driven Development: By Example (Kent Beck) / 適用: Red-Green-Refactorサイクル / 目的: 反復的な品質改善
  • LLM-as-a-Judge pattern / 適用: 自動評価とスコアリング / 目的: スケーラブルな品質評価
  • A/B Testing for AI Systems / 適用: プロンプト比較実験設計 / 目的: データドリブンな改善

  Trigger:
  Use when testing prompts, evaluating prompt quality, running A/B tests on prompts, implementing automated prompt evaluation, or establishing continuous prompt improvement cycles.
  Keywords: prompt testing, A/B testing, evaluation metrics, LLM-as-a-judge, prompt quality, automated evaluation, regression testing
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Prompt Testing & Evaluation

## 概要

プロンプトのテスト、評価、反復改善を専門とするスキル。テスト設計、A/Bテスト、LLM-as-Judge自動評価、評価メトリクス分析を通じて、本番環境で信頼性の高いプロンプトを実現します。

## ワークフロー

### Phase 1: テスト設計

**目的**: プロンプトのテストケースと評価基準を設計

**Task**: `agents/test-design.md`

**入力**:

- プロンプト
- 期待動作の概要
- 評価観点

**出力**:

- テストケース一覧（正常系・異常系・エッジケース）
- 評価ルブリック（スコアリング基準）
- テスト実行計画

**実行タイミング**: 新規プロンプト作成時、プロンプト改善前

### Phase 2: 評価実行

**目的**: 設計に基づきテストを実行し、スコアを算出

**Task**: `agents/evaluation-execution.md`

**入力**:

- Phase 1 のテストケースとルブリック
- プロンプトバージョン（A/Bテスト時は複数）

**出力**:

- スコアリング結果
- A/Bテスト結果（統計的有意性含む）
- 評価ログ

**実行タイミング**: テスト設計完了後、プロンプト比較時

### Phase 3: 分析・改善

**目的**: 評価結果を分析し、改善提案と次イテレーションを計画

**Task**: `agents/analysis-improvement.md`

**入力**:

- Phase 2 のスコアリング結果
- A/Bテスト結果
- 評価ルブリック

**出力**:

- 分析レポート（弱点・傾向）
- 改善アクションプラン
- 次イテレーションのテスト計画

**実行タイミング**: 評価完了後、改善サイクル開始時

## Task仕様

| Task                 | 起動タイミング | 入力                     | 出力                     |
| -------------------- | -------------- | ------------------------ | ------------------------ |
| test-design          | Phase 1開始時  | プロンプト・評価観点     | テストケース・ルブリック |
| evaluation-execution | Phase 2開始時  | テストケース・バージョン | スコアリング・統計結果   |
| analysis-improvement | Phase 3開始時  | スコア結果・ルブリック   | 分析・改善プラン         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

- [agents/test-design.md](agents/test-design.md)
- [agents/evaluation-execution.md](agents/evaluation-execution.md)
- [agents/analysis-improvement.md](agents/analysis-improvement.md)

## ベストプラクティス

### すべきこと

- テスト実行前に期待値と評価基準を定義（テストファースト）
- 正常系・異常系・エッジケースを網羅的に設計
- A/Bテストで統計的有意性を確保（N≥30）
- LLM-as-Judgeを活用したスケーラブルな自動評価
- 継続的改善サイクル（PDCA）を確立
- すべての評価結果をログに残す

### 避けるべきこと

- 評価基準なしのテスト実行
- サンプルサイズ不足のA/Bテスト
- 主観的・非再現的な評価
- 改善せずに同じテストを繰り返す
- 盲検評価を怠る（バイアス混入）

## リソース参照

### references/（詳細知識）

| リソース                   | パス                                                                     | 内容             |
| -------------------------- | ------------------------------------------------------------------------ | ---------------- |
| 基礎知識                   | [references/Level1_basics.md](references/Level1_basics.md)               | 基礎概念と用語   |
| 実務パターン               | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | 実務での適用     |
| 高度な評価手法             | [references/Level3_advanced.md](references/Level3_advanced.md)           | 高度な評価技法   |
| 専門トラブルシューティング | [references/Level4_expert.md](references/Level4_expert.md)               | 専門的な問題解決 |
| A/Bテストガイド            | [references/ab-testing-guide.md](references/ab-testing-guide.md)         | A/Bテスト設計    |
| 自動評価                   | [references/automated-evaluation.md](references/automated-evaluation.md) | LLM-as-Judge     |
| 評価メトリクス             | [references/evaluation-metrics.md](references/evaluation-metrics.md)     | スコアリング基準 |

### scripts/（決定論的処理）

| スクリプト             | 用途           | 使用例                                                                  |
| ---------------------- | -------------- | ----------------------------------------------------------------------- |
| `prompt-evaluator.mjs` | プロンプト評価 | `node scripts/prompt-evaluator.mjs --prompt "..." --rubric rubric.json` |
| `log_usage.mjs`        | 使用履歴記録   | `node scripts/log_usage.mjs --result success --phase design`            |
| `validate-skill.mjs`   | 構造検証       | `node scripts/validate-skill.mjs`                                       |

### assets/（テンプレート）

| テンプレート            | 用途                       |
| ----------------------- | -------------------------- |
| `evaluation-rubric.md`  | 評価ルブリックテンプレート |
| `test-case-template.md` | テストケーステンプレート   |

## 変更履歴

| Version | Date       | Changes                                                   |
| ------- | ---------- | --------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠: 3 Tasks追加、ワークフロー体系化 |
| 2.0.0   | 2026-01-02 | Trigger英語化、Anchors追加                                |
| 1.0.0   | 2025-12-24 | 初版: 基本構造とリソース整備                              |
