---
name: command-performance-optimization
description: |
  コマンドのパフォーマンス最適化（トークン効率化/並列実行/モデル選択/速度改善）を整理し、性能改善の判断と適用を支援するスキル。
  計測観点、最適化手順、テンプレート運用を一貫して整理する。

  Anchors:
  • High Performance Browser Networking (Ilya Grigorik) / 適用: パフォーマンス測定 / 目的: レイテンシー削減
  • Design of Computer Programs (Peter Norvig) / 適用: 最適化設計 / 目的: 実行速度向上
  • Programming Pearls (Jon Bentley) / 適用: トークン効率化 / 目的: リソース削減

  Trigger:
  Use when optimizing command performance, reducing token usage, or designing parallel execution flows and model selection.
  command performance, token optimization, parallel execution, model selection
---
# command-performance-optimization

## 概要

コマンドのパフォーマンス最適化（トークン効率化/並列実行/モデル選択/速度改善）を整理し、性能改善の判断と適用を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: パフォーマンス課題と目標を明確化する。

**アクション**:

1. 対象コマンドとボトルネックを整理する。
2. 目標（時間/コスト/トークン）を定義する。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-performance-requirements.md` を参照

### Phase 2: 最適化設計

**目的**: 最適化手法と適用方針を具体化する。

**アクション**:

1. トークン/並列/モデル選択の方針を定義する。
2. 実行速度改善と計測手順を整理する。
3. テンプレートで表現を統一する。

**Task**: `agents/design-performance-optimization.md` を参照

### Phase 3: 検証と記録

**目的**: 改善効果を検証し、記録を残す。

**アクション**:

1. 分析スクリプトで改善効果を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-performance-optimization.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-performance-requirements | Phase 1開始時 | 対象/課題 | 要件整理メモ、目標一覧 |
| design-performance-optimization | Phase 2開始時 | 要件整理メモ | 最適化方針、計測手順 |
| validate-performance-optimization | Phase 3開始時 | 最適化方針 | 検証レポート、改善方針 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| 目標と計測指標を明確にする | 改善の評価が容易になるため |
| 低コストな改善から着手する | 効果が早く出るため |
| 検証と記録を実施する | 改善が継続できるため |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| 目標不在で最適化する | 効果が不明確になる |
| 並列化を乱用する | 複雑度が増える |
| 記録を残さない | 改善が続かない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/analyze-performance.mjs` | パフォーマンス分析 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 初回整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 詳細設計時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 改善ループ時 |
| トークン最適化 | [references/token-optimization.md](references/token-optimization.md) | 圧縮検討時 |
| 並列実行 | [references/parallel-execution.md](references/parallel-execution.md) | 並列設計時 |
| モデル選択 | [references/model-selection.md](references/model-selection.md) | モデル選定時 |
| 実行速度 | [references/execution-speed.md](references/execution-speed.md) | 速度改善時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/optimized-command-template.md` | 最適化コマンドテンプレート |
| `assets/parallel-execution-template.md` | 並列実行テンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
