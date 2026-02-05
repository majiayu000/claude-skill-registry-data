---
name: agent-template-patterns
description: |
  Specialist skill for agent templates and design patterns.
  Provides 4 types of agent templates (Analysis, Implementation, Orchestrator, Deploy),
  {{variable}} format abstraction, abstraction balance, and conceptual element design principles.

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: テンプレート設計 / 目的: 手順設計と実践的改善の原則

  Trigger:
  Use when creating new agent templates, generalizing existing agents into reusable patterns, designing standard templates for agent mass production, implementing {{variable}} format abstraction, or optimizing conceptual element design and abstraction balance.
  agent template, template design, orchestrator pattern, variable abstraction, template standardization

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Agent Template Patterns

## 概要

エージェントテンプレートと設計パターンを専門とするスキル。4タイプのエージェントテンプレート（分析、実装、オーケストレーター、デプロイ）、{{variable}}形式による抽象化、抽象度バランス、概念要素設計の原則を提供します。

## ワークフロー

### Phase 1: 要件分析と設計

**目的**: タスク要件を分析し、最適なテンプレートタイプを選定する

**アクション**:

1. エージェントのタイプ（分析、実装、オーケストレーター、デプロイ）を判定
2. 必要な変数化レベルを決定
3. `references/Level1_basics.md` と `references/Level2_intermediate.md` で基礎と実装方法を確認
4. `references/template-reference-guide.md` で該当テンプレートを特定
5. 既存パターンとの互換性を検討

**Task**: `agents/analyze-template-requirements.md` を参照

### Phase 2: テンプレート実装

**目的**: 選定したテンプレートを基にエージェントテンプレートを実装する

**アクション**:

1. `assets/unified-agent-template.md` を参照
2. {{variable}} 形式の変数を定義（`references/template-variable-guide.md` を参照）
3. 抽象度バランスを最適化（`references/Level3_advanced.md` を参照）
4. テンプレート本体を作成・拡張
5. 設計判断を記録

**Task**: `agents/implement-template.md` を参照

### Phase 3: 検証と最適化

**目的**: テンプレートの品質を確保し、実装記録を残す

**アクション**:

1. `scripts/validate-skill.mjs` でテンプレート構造を検証
2. 抽象度とバランスをレビュー（`references/Level4_expert.md` を参照）
3. 概念要素設計が適切かを確認
4. `scripts/log_usage.mjs` を実行して実装記録を残す
5. 成果物を `references/legacy-skill.md` に追記（必要に応じて）

**Task**: `agents/validate-template.md` を参照

## Task仕様ナビ

エージェントテンプレートパターンに関連するタスクと対応するリソース・テンプレートの対応表です。

| タスク               | 対応Phase | 関連リソース                | テンプレート              | 説明                                                    |
| -------------------- | --------- | --------------------------- | ------------------------- | ------------------------------------------------------- |
| **4タイプの選定**    | Phase 1   | Level1_basics.md            | unified-agent-template.md | 分析・実装・オーケストレーター・デプロイの4タイプを判定 |
| **テンプレート設計** | Phase 1   | template-reference-guide.md | unified-agent-template.md | 11個の既存テンプレートから最適を選択                    |
| **変数化設計**       | Phase 2   | template-variable-guide.md  | unified-agent-template.md | {{variable}}形式で抽象化                                |
| **抽象度バランス**   | Phase 2   | Level3_advanced.md          | unified-agent-template.md | 抽象度と具体性のバランスを最適化                        |
| **概念要素設計**     | Phase 2   | Level2_intermediate.md      | unified-agent-template.md | コア概念要素を定義・設計                                |
| **実装パターン**     | Phase 2   | Level2_intermediate.md      | unified-agent-template.md | テンプレートの実装方法を確定                            |
| **テンプレート検証** | Phase 3   | Level4_expert.md            | validate-skill.mjs        | スクリプトで構造検証                                    |
| **品質確保**         | Phase 3   | Level4_expert.md            | validate-skill.mjs        | アンチパターンを回避、品質基準達成                      |
| **実装記録**         | Phase 3   | -                           | log_usage.mjs             | 実装履歴を自動記録                                      |

## ベストプラクティス

### すべきこと

- **4つのタイプを意識する**: エージェントが分析・実装・オーケストレーター・デプロイのいずれかを判定してから設計開始
- **テンプレート参照ガイドを活用**: `template-reference-guide.md` で既存11個のテンプレートから最適を選択
- **{{variable}}形式で抽象化**: 具体値を避け、{{変数名}}形式で再利用可能に設計
- **抽象度バランスを最適化**: 高すぎず低すぎない抽象度で、多様なシナリオに対応可能に
- **概念要素を明確に**: エージェントのコア概念要素を事前に定義・設計
- **検証スクリプトを実行**: `validate-skill.mjs` で構造の正確性を確認
- **実装記録を残す**: `log_usage.mjs` で設計判断と実装履歴を記録
- **リソースレベルを段階的に活用**: Level1→Level2→Level3→Level4で段階的に学習・適用

### 避けるべきこと

- **アンチパターンを無視**: `references/Level3_advanced.md` と `Level4_expert.md` のアンチパターンを確認しないまま実装
- **抽象度のズレ**: 過度に具体的または過度に抽象的なテンプレートを作成
- **変数化を忘れる**: ハードコーディングされた値をテンプレートに含める
- **概念要素を曖昧にする**: エージェントの意図や役割を不明確なまま設計
- **検証をスキップ**: `validate-skill.mjs` で構造検証を行わないまま納品
- **既存パターンを無視**: `template-reference-guide.md` を確認せず、重複したテンプレートを作成
- **ドキュメントをコピペ**: リソースの内容を丸写しせず、プロジェクト固有にカスタマイズ

## リソース参照

### 学習レベル別リソース

| レベル   | ファイル                            | 対象ユーザー       | 目的                                       |
| -------- | ----------------------------------- | ------------------ | ------------------------------------------ |
| **基礎** | `references/Level1_basics.md`       | テンプレート初心者 | 4つのエージェントタイプと基本概念を理解    |
| **実務** | `references/Level2_intermediate.md` | 実装者             | テンプレート設計と概念要素の実装方法を学習 |
| **応用** | `references/Level3_advanced.md`     | 経験者             | 抽象度バランスとアンチパターンを学習       |
| **専門** | `references/Level4_expert.md`       | 専門家             | 高度な最適化と品質基準を学習               |

### ガイドと参考資料

- **`references/template-reference-guide.md`**: 11個の既存テンプレート一覧とPhase別活用法
- **`references/template-variable-guide.md`**: {{variable}}形式の設計と使用法の詳細ガイド
- **`references/legacy-skill.md`**: 旧SKILL.mdの全文（廃止予定の内容も含む）

### テンプレート

- **`assets/unified-agent-template.md`**: 統一エージェントテンプレート（Phase 2で活用）

### スクリプト/ツール

| スクリプト                   | 用途                   | 実行例                                                                   |
| ---------------------------- | ---------------------- | ------------------------------------------------------------------------ |
| `scripts/validate-skill.mjs` | テンプレート構造の検証 | `node .claude/skills/agent-template-patterns/scripts/validate-skill.mjs` |
| `scripts/log_usage.mjs`      | 実装履歴の自動記録     | `node .claude/skills/agent-template-patterns/scripts/log_usage.mjs`      |

## 変更履歴

| Version | Date       | Changes                                                                                                    |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| 3.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加                                                                |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠（Anchors・Triggers・allowed-tools・Task仕様ナビ・詳細なベストプラクティス追加） |
| 1.0.0   | 2025-12-24 | 初期リリース：基本構成とリソース参照の整備                                                                 |
