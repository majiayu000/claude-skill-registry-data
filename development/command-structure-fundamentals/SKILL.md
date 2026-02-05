---
name: command-structure-fundamentals
description: |
  Claude Code スラッシュコマンドの基本構造（YAML frontmatter/本文パターン/ファイル構造）を整理し、最小構成と設計判断を支援するスキル。
  frontmatter設計、本文パターン、配置ルールを一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 構造設計の実務 / 目的: コマンド構造の再現性確保
  • 18-skills.md 仕様 / 適用: スキル構造の整合 / 目的: frontmatter規約の統一

  Trigger:
  Use when designing slash command structure, defining YAML frontmatter fields, or establishing consistent command composition patterns.
  command structure, YAML frontmatter, command composition, minimal command template
---
# command-structure-fundamentals

## 概要

Claude Code スラッシュコマンドの基本構造（YAML frontmatter/本文パターン/ファイル構造）を整理し、最小構成と設計判断を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 必須フィールドと目的を明確化する。

**アクション**:

1. 目的と対象コマンドを整理する。
2. 必須 frontmatter と本文要素を整理する。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-structure-requirements.md` を参照

### Phase 2: 構造設計

**目的**: frontmatter/本文/配置ルールを具体化する。

**アクション**:

1. frontmatter 仕様と本文パターンを定義する。
2. ファイル構造と配置ルールを整理する。
3. テンプレートで表現を統一する。

**Task**: `agents/design-command-structure.md` を参照

### Phase 3: 検証と記録

**目的**: コマンド構造を検証し、記録を残す。

**アクション**:

1. 検証スクリプトで構造整合を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-command-structure.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-structure-requirements | Phase 1開始時 | 目的/対象 | 要件整理メモ、必須項目 |
| design-command-structure | Phase 2開始時 | 要件整理メモ | 構造設計、配置ルール |
| validate-command-structure | Phase 3開始時 | 構造設計 | 検証レポート、改善方針 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| 必須フィールドを先に整理する | 実装漏れを防ぐため |
| テンプレートで構造を統一する | 読みやすさが保てるため |
| 検証と記録を実施する | 改善が継続できるため |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| frontmatter を曖昧にする | 実行要件が不明確になる |
| 本文パターンを混在させる | 構造が崩れる |
| 記録を残さない | 改善が続かない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/validate-command.mjs` | コマンド構造検証 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 初回整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 構造設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 詳細設計時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 改善ループ時 |
| frontmatter参照 | [references/yaml-frontmatter-reference.md](references/yaml-frontmatter-reference.md) | 仕様確認時 |
| 仕様: description | [references/specification-18.3.4-description.md](references/specification-18.3.4-description.md) | description整理時 |
| 仕様: 本文セクション | [references/specification-18.3.6-body-sections.md](references/specification-18.3.6-body-sections.md) | 本文設計時 |
| 仕様: エージェント起動 | [references/specification-18.3.7-agent-launch-flow.md](references/specification-18.3.7-agent-launch-flow.md) | エージェント起動設計時 |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md) | 要件参照時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/minimal-command.md` | 最小構成コマンドテンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
