---
name: agent-persona-design
description: |
  実在する専門家の思想をエージェントに移植し、その専門性と思考パターンを再現するスキル。

  Anchors:
  • 『心の社会』（Marvin Minsky） / 適用: 複雑系とエージェントシステム / 目的: 小規模エージェントの集合知実現
  • 『ファスト&スロー』（Daniel Kahneman） / 適用: 意思決定と思考パターン / 目的: 専門家の直感と論理の統合

  Trigger:
  Use when designing or improving agent personas, modeling expert thinking patterns, upgrading existing personas, or building multi-persona systems.
  persona design, expert modeling, thinking patterns, agent architecture, multi-agent systems

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# エージェントペルソナ設計

## 概要

実在する専門家の思想と思考パターンをエージェントに移植し、その専門性を再現するスキルです。心理学（Kahneman）と認知科学（Minsky）の理論に基づき、複雑な意思決定や領域専門知識をエージェント化します。

このスキルは以下を実現します：

- **専門家思考の再現**: 異なる分野の専門家の思考フローをモデル化
- **ペルソナの段階的成長**: Level 1（基礎）から Level 4（専門）への段階的なペルソナ構築
- **マルチペルソナシステムの設計**: 複数の専門家エージェントの相互作用設計

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: ペルソナ設計の背景・目的・制約条件を明確化

**アクション**:

1. `references/Level1_basics.md` で基礎概念（専門家モデルの要素）を確認
2. 対象となる専門分野・専門家のプロファイルを整理
3. ペルソナが解決すべきタスク領域を定義
4. `references/expert-modeling-guide.md` で専門家の思考パターン抽出方法を学習

**Task**: `agents/analyze-persona-context.md` を参照

### Phase 2: ペルソナ設計と実装

**目的**: リソースとテンプレートに基づいて、ペルソナ構造を具体化

**アクション**:

1. `references/Level2_intermediate.md` で実務的な設計手順を確認
2. `assets/persona-template.md` を使用してペルソナの骨子を作成
3. 専門家の特性（思考スピード・深さ・判断基準）をペルソナに組み込み
4. `scripts/analyze-persona.mjs` でペルソナの構造を分析・改善
5. Level 3/4 の応用ガイドで特殊なケース・統合パターンを検討

**Task**: `agents/design-persona.md` を参照

### Phase 3: 検証と定着

**目的**: 設計されたペルソナの妥当性を検証し、実装準備を完了

**アクション**:

1. `scripts/validate-skill.mjs` でペルソナ定義の構造的妥当性を確認
2. ペルソナが目的のタスク領域で機能するか試行検証
3. `scripts/log_usage.mjs` を実行してペルソナ設計の記録を保存
4. 必要に応じて `references/Level3_advanced.md` で統合パターンを適用

**Task**: `agents/validate-persona.md` を参照

---

## Task仕様ナビ

| Task                    | 起動タイミング | 入力                 | 出力                 |
| ----------------------- | -------------- | -------------------- | -------------------- |
| analyze-persona-context | Phase 1開始時  | タスク仕様           | ペルソナ設計ブリーフ |
| design-persona          | Phase 2開始時  | ペルソナ設計ブリーフ | ペルソナ定義書       |
| validate-persona        | Phase 3開始時  | ペルソナ定義書       | 検証結果レポート     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

- **段階的にリソースを活用する**: Level 1 → Level 2 → Level 3/4 の順序で深掘りする
- **実在の専門家から学ぶ**: 著書・論文・インタビューから思考パターンを直接抽出する
- **System 1/2 の思考を区別する**: 直感的判断（System 1）と論理的分析（System 2）を明示的に分離
- **テンプレートで構造化する**: `persona-template.md` を基に、漏れなく属性を定義する
- **検証スクリプトで品質確保**: `validate-skill.mjs` で構造的妥当性を定期的に確認
- **変化に対応する**: 実装フェーズで新たな発見が出たら ペルソナ定義を反復改善する

### 避けるべきこと

- **仮説のみで設計する**: 必ず実在の専門家・事例・データベースで検証する
- **思考パターンを曖昧なまま使用する**: 「合理的」「慎重」など抽象的な表現のみで済ませない
- **Level をスキップする**: 基礎（Level 1）を理解せずに応用（Level 3/4）に進まない
- **単一の思考パターンに依存する**: 異なるシナリオで柔軟に判断基準を切り替えられるようにする
- **変更履歴を記録しない**: `log_usage.mjs` を実行し、試行錯誤の過程を記録に残す

## リソース参照

### references/（詳細知識）

| リソース         | パス                                                                       | 読込条件     |
| ---------------- | -------------------------------------------------------------------------- | ------------ |
| 基礎概念         | [references/Level1_basics.md](references/Level1_basics.md)                 | 初回利用時   |
| 実務パターン     | [references/Level2_intermediate.md](references/Level2_intermediate.md)     | 実務適用時   |
| 応用ガイド       | [references/Level3_advanced.md](references/Level3_advanced.md)             | 複雑系対応時 |
| 専門解説         | [references/Level4_expert.md](references/Level4_expert.md)                 | 高度な課題時 |
| 専門家モデリング | [references/expert-modeling-guide.md](references/expert-modeling-guide.md) | 思考抽出時   |

### scripts/（決定論的処理）

| スクリプト                    | 機能               |
| ----------------------------- | ------------------ |
| `scripts/analyze-persona.mjs` | ペルソナ構造分析   |
| `scripts/validate-skill.mjs`  | スキル構造検証     |
| `scripts/log_usage.mjs`       | フィードバック記録 |

### assets/（テンプレート）

| アセット                     | 用途                     |
| ---------------------------- | ------------------------ |
| `assets/persona-template.md` | ペルソナ設計テンプレート |

## 変更履歴

| Version | Date       | Changes                                                      |
| ------- | ---------- | ------------------------------------------------------------ |
| 4.0.0   | 2025-12-31 | agents/追加、テーブル形式統一、Task仕様ナビ改善              |
| 3.0.0   | 2025-12-31 | 18-skills.md仕様に準拠（Task仕様ナビ、詳細ワークフロー追加） |
| 2.0.0   | 2025-12-24 | Spec alignment and required artifacts added                  |
