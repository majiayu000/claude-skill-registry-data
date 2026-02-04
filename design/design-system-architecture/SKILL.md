---
name: design-system-architecture
description: |
  一貫性と拡張性を両立するデザインシステムの基盤設計を支援するスキル。
  デザイントークン、コンポーネント規約、Figma/コード同期を体系化する。

  Anchors:
  • Atomic Design / 適用: コンポーネント階層設計 / 目的: 構造の一貫性確保
  • Design Tokens / 適用: トークン管理 / 目的: 再利用性の向上
  • Clean Architecture / 適用: 依存関係設計 / 目的: 責務分離

  Trigger:
  Use when designing a design system, defining design tokens, or establishing component and Figma-code synchronization rules.
  design system architecture, design tokens, figma sync, component guidelines
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# design-system-architecture

## 概要

デザインシステムの基盤設計を整理し、トークン・コンポーネント・同期ルールを統合して運用する。

## ワークフロー

### Phase 1: 要件整理

**目的**: デザインシステムのスコープと制約を明確化する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/design-system-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-design-system-requirements.md` を参照

### Phase 2: トークン/構造設計

**目的**: トークン体系とコンポーネント階層を設計する。

**アクション**:

1. `references/design-tokens-guide.md` でトークン設計を確認する。
2. `references/component-hierarchy.md` で階層構造を整理する。
3. `assets/token-audit-checklist.md` で設計観点を揃える。

**Task**: `agents/design-token-architecture.md` を参照

### Phase 3: 規約と同期設計

**目的**: コンポーネント規約と同期ルールを確定する。

**アクション**:

1. `references/naming-conventions.md` で命名規約を確認する。
2. `references/figma-code-sync.md` で同期戦略を整理する。
3. `assets/sync-strategy-template.md` で方針をまとめる。

**Task**: `agents/implement-system-guidelines.md` を参照

### Phase 4: 検証と運用

**目的**: トークンの整合性と運用記録を更新する。

**アクション**:

1. `scripts/validate-tokens.mjs` でトークン検証を実行する。
2. `assets/component-spec-template.md` で仕様を整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-system-consistency.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-design-system-requirements | Phase 1開始時 | 要件/制約 | スコープ整理、制約メモ |
| design-token-architecture | Phase 2開始時 | スコープ整理 | トークン設計、階層方針 |
| implement-system-guidelines | Phase 3開始時 | 設計方針 | 規約/同期方針 |
| validate-system-consistency | Phase 4開始時 | 規約/同期方針 | 検証レポート、改善提案 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| トークンの責務を分離する | 再利用性が高まる |
| 規約と同期ルールを明文化する | 運用の一貫性が保てる |
| 検証結果を記録する | 改善が継続する |
| 要件整合を定期確認する | 不整合を防ぐ |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| 暫定トークンの乱立 | 整合性が崩れる |
| 規約未整備のまま運用 | 同期失敗が増える |
| 検証を省略する | 品質低下につながる |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/validate-tokens.mjs` | トークン検証 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 規約設計時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 改善時 |
| コンポーネント階層 | [references/component-hierarchy.md](references/component-hierarchy.md) | 階層設計時 |
| トークン設計 | [references/design-tokens-guide.md](references/design-tokens-guide.md) | トークン設計時 |
| 同期設計 | [references/figma-code-sync.md](references/figma-code-sync.md) | 同期設計時 |
| 命名規約 | [references/naming-conventions.md](references/naming-conventions.md) | 規約設計時 |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md) | 仕様確認時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/design-system-requirements-template.md` | 要件整理テンプレート |
| `assets/token-audit-checklist.md` | トークン設計チェック |
| `assets/sync-strategy-template.md` | 同期方針テンプレート |
| `assets/component-spec-template.md` | コンポーネント仕様テンプレート |
| `assets/design-tokens-template.json` | トークン定義テンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
