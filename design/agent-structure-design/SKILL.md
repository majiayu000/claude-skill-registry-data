---
name: agent-structure-design
description: |
  Claude Codeエージェントの構造設計を専門とするスキル。エージェント定義、YAML Frontmatter設計、依存スキル形式、ワークフロー設計を担当する。

  Anchors:
  • 『The Pragmatic Programmer』（Andrew Hunt, David Thomas） / 適用: 手順設計と実装原則 / 目的: エージェント設計に実践的改善パターンを適用
  • 18-skills.md 仕様書 / 適用: Skill構造、YAML frontmatter、Task仕様書設計 / 目的: Skillメタデータと本文構造を標準化
  • docs/00-requirements 要求仕様 / 適用: エージェント割り当てと責務定義 / 目的: システム要求からエージェント設計へのマッピング

  Trigger:
  エージェント構造の設計・検証が必要な場合に使用。新規エージェント作成時、既存エージェントのYAML frontmatterやタスク分割の見直し、スキル依存関係の最適化などが対象。

allowed-tools:
  - read_file
  - write_file
  - bash
  - grep
---

# Agent Structure Design

## 概要

Claude Codeエージェントの構造設計を専門とするスキル。エージェント定義書のYAML Frontmatter、概要、ワークフロー、Task仕様書、ベストプラクティスなどの構成を統一された仕様に基づいて設計・検証する。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要な references/scripts/templates を特定

**Task**: `agents/analyze-structure-context.md` を参照

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す

**Task**: `agents/design-structure.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す

**Task**: `agents/validate-structure.md` を参照

## Task仕様ナビ

このスキルで設計・検証するドキュメントと実行フェーズを以下に示します。

| Task                   | 実行フェーズ | 入力                   | 出力                            | 関連リソース                                |
| ---------------------- | ------------ | ---------------------- | ------------------------------- | ------------------------------------------- |
| YAML Frontmatter設計   | Phase 1      | エージェント要件・目的 | 仕様準拠のYAML frontmatter      | references/yaml-frontmatter-guide.md        |
| エージェント概要作成   | Phase 2      | 責務・専門領域         | エージェント概要（1-2文）       | references/Level2_intermediate.md           |
| ワークフロー設計       | Phase 2      | タスク分解結果         | Phase 1/2/3 構成                | references/workflow-patterns.md             |
| Task仕様書作成         | Phase 2      | Task詳細・入出力       | agents/\*.md ファイル           | 18-skills.md仕様の3.3節                     |
| 依存関係設計           | Phase 2      | スキル参照・順序       | dependencies フィールド         | references/dependency-skill-format-guide.md |
| ベストプラクティス定義 | Phase 2      | 設計原則・注意点       | すべきこと/避けるべきことリスト | references/Level3_advanced.md               |
| 構造検証               | Phase 3      | 成果物                 | 検証レポート                    | scripts/validate-structure.mjs              |

## ベストプラクティス

### すべきこと

- エージェント設計時は、18-skills.md仕様の3.2節に従いYAML frontmatterを構成する（name、description、allowed-tools、dependencies）
- description フィールドにはAnchorsとTriggerを日本語で記載し、Markdown禁止規則（箇条書き不可）に従う
- ワークフローをPhase 1（準備）→ Phase 2（実装）→ Phase 3（検証）の3段階で明確に分割する
- Task仕様書は agents/\*.md として独立させ、役割・入力・出力・制約・参照を含める
- 知識本文は references/ に外部化し、SKILL.md本文は500行以内に保つ
- スクリプトは冪等性を持たせ、エラー出力（stderr）と終了コード規則に従う
- 検証スクリプト（validate-structure.mjs）で自動検証し、YAML構文と必須フィールドを確認する

### 避けるべきこと

- YAML frontmatterにreferences フィールドを含める（description内のAnchorsに統合済み）
- Task仕様書に長い知識本文をベタ書きする（references/.へ移動）
- description内でMarkdown箇条書き（`-` や `*`）を使用する（行区切りで表現）
- スキルに README.md や補助ドキュメントを含める（不要）
- スクリプトの引数検証やヘルプ機能を省略する
- 相対パス参照で `../` を使用する（SKILL.mdから1レベルに保つ）

## リソース参照

### 段階的学習リソース（レベル別）

- **references/Level1_basics.md**: エージェント構造設計の基礎概念
- **references/Level2_intermediate.md**: YAML frontmatter実装、ワークフロー設計パターン
- **references/Level3_advanced.md**: 複雑なTask仕様書設計、依存関係管理の応用
- **references/Level4_expert.md**: パフォーマンス最適化、スキルメタデータの詳細設計

### 仕様・ガイドリソース

- **references/yaml-frontmatter-guide.md**: name、description、allowed-tools、dependencies フィールドの詳細ルール
- **references/dependency-skill-format-guide.md**: スキル依存関係の表記と検証方法
- **references/yaml-description-rules.md**: Anchors と Trigger の記述形式とベストプラクティス
- **references/skill-dependency-format-examples.md**: 実例に基づく依存関係表記の例
- **references/legacy-skill.md**: 旧仕様との比較と移行ガイド
- **references/requirements-index.md**: 要求仕様との対応インデックス

### スクリプト・テンプレート

**構造検証スクリプト**:

- `scripts/validate-structure.mjs`: YAML Frontmatter構文、必須フィールド、ファイル構造の4項目を自動検証
- `scripts/validate-skill.mjs`: スキル全体の一貫性を検証
- `scripts/validate-structure.sh`: シェルベースの構造検証

**フィードバックログ**:

- `scripts/log_usage.mjs`: スキル使用記録と自動評価（--result success|failure オプション）

**テンプレート**:

- `assets/agent-template.md`: エージェント定義書の基本テンプレート

## 変更履歴

| Version | Date       | Changes                                                                                                                                                                              |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加                                                                                                                                          |
| 1.2.0   | 2025-12-31 | 18-skills.md仕様に準拠。YAML frontmatterをAnchors/Trigger形式に統一、allowed-toolsフィールド追加、Task仕様ナビを表形式で追加、ベストプラクティスを18-skills.md仕様の詳細ルールに対応 |
| 1.1.0   | 2025-12-24 | Spec alignment and required artifacts added                                                                                                                                          |
