---
name: role-prompting
description: |
  AIエージェント・システムロール・ペルソナのための役割プロンプト設計スキル。
  責務分離、専門家思考様式の適用、効果的なプロンプト構造化の指針を提供する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: DRY原則・責務分離 / 目的: ロール設計の品質向上
  • Domain-Driven Design (Eric Evans) / 適用: ユビキタス言語・境界づけられたコンテキスト / 目的: 責務境界の明確化
  • Thinking, Fast and Slow (Daniel Kahneman) / 適用: 専門家思考様式の理解 / 目的: 適切な思考モード設計

  Trigger:
  Use when designing AI agent roles, system prompts, persona definitions, or separating responsibilities between agents.
  role prompting, persona design, agent role, system prompt, responsibility separation, ロール設計, ペルソナ

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Role Prompting

## 概要

AIエージェント・システムロール・ペルソナのための役割プロンプト設計スキル。
単一責務原則に基づく責務分離、専門家思考様式の効果的な適用、構造化されたプロンプト設計を支援する。

## ワークフロー

```
analyze-purpose → design-role → generate-prompt → validate-role
```

### Task 1: 目的分析（analyze-purpose）

**目的**: ロールが必要な理由と達成すべきゴールを明確化する

**アクション**:

1. ロールが担う責務を特定
2. 対象ドメインと専門領域を定義
3. 成功基準と制約条件を設定

**Task**: `agents/analyze-purpose.md` を参照

### Task 2: ロール設計（design-role）

**目的**: 責務・専門領域・思考様式を体系的に定義する

**アクション**:

1. 参照すべき専門家/思考様式を選定
2. 責務と成果物のマッピングを作成
3. 知識ベースと参考文献を特定

**Task**: `agents/design-role.md` を参照

### Task 3: プロンプト生成（generate-prompt）

**目的**: 設計に基づいて構造化されたロールプロンプトを生成する

**アクション**:

1. メタ情報（名前・専門領域）を記述
2. プロフィール（背景・目的・責務）を構成
3. 実行仕様（思考プロセス・チェックリスト）を定義

**Task**: `agents/generate-prompt.md` を参照

### Task 4: 検証（validate-role）

**目的**: 設計したロールの一貫性と効果を検証する

**アクション**:

1. 責務の重複・欠落をチェック
2. 思考様式の適切性を評価
3. 実際のユースケースでテスト

**Task**: `agents/validate-role.md` を参照

## Task仕様ナビ

| Task            | 起動タイミング       | 入力               | 出力             |
| --------------- | -------------------- | ------------------ | ---------------- |
| analyze-purpose | ロール設計開始時     | 要件・コンテキスト | 目的定義書       |
| design-role     | 目的分析完了後       | 目的定義書         | ロール設計書     |
| generate-prompt | ロール設計完了後     | ロール設計書       | ロールプロンプト |
| validate-role   | プロンプト生成完了後 | ロールプロンプト   | 検証レポート     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                         |
| ---------------------------------- | ---------------------------- |
| 単一責務原則を適用する             | ロールの明確性と保守性を確保 |
| 実在の専門家を参照ラベルとして使用 | 思考様式の一貫性を担保       |
| 責務と成果物を明示的にマッピング   | 期待される出力が明確になる   |
| 入出力インターフェースを定義       | 他ロールとの連携が容易になる |
| 検証チェックリストを設ける         | 品質基準を客観的に確認できる |

### 避けるべきこと

| 禁止事項                           | 問題点                       |
| ---------------------------------- | ---------------------------- |
| 複数責務を1ロールに集中させる      | 責務の肥大化と保守困難       |
| 専門家本人を名乗る・発言を捏造     | 倫理的問題                   |
| 曖昧な条件記述（「必要に応じて」） | 再現性と予測可能性の低下     |
| 思考様式なしで役割を定義           | 行動パターンが不明確         |
| 入出力仕様を省略                   | 連携時のエラーとデバッグ困難 |

## リソース参照

### agents/（Task仕様書）

| Task仕様書                  | 責務                       |
| --------------------------- | -------------------------- |
| `agents/analyze-purpose.md` | 目的・責務・制約条件の分析 |
| `agents/design-role.md`     | ロール構造と思考様式の設計 |
| `agents/generate-prompt.md` | 構造化プロンプトの生成     |
| `agents/validate-role.md`   | 設計の検証と改善提案       |

### references/（詳細知識）

| リソース           | パス                                                                               | 読込条件               |
| ------------------ | ---------------------------------------------------------------------------------- | ---------------------- |
| ロール設計パターン | [references/role-patterns.md](references/role-patterns.md)                         | ロール設計時に参照     |
| 責務分離原則       | [references/responsibility-separation.md](references/responsibility-separation.md) | 複数ロール設計時に参照 |
| プロンプト構造     | [references/prompt-structures.md](references/prompt-structures.md)                 | プロンプト生成時に参照 |

### scripts/（決定論的処理）

| スクリプト              | 機能                         |
| ----------------------- | ---------------------------- |
| `scripts/log_usage.mjs` | 使用記録とフィードバック保存 |

### assets/（テンプレート）

| アセット                         | 用途                               |
| -------------------------------- | ---------------------------------- |
| `assets/role-prompt-template.md` | ロールプロンプト作成用テンプレート |

## 変更履歴

| Version | Date       | Changes                                         |
| ------- | ---------- | ----------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠・責務ベースagents/追加 |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様に準拠、YAML frontmatter整備    |
| 1.0.0   | 2025-12-24 | 初版作成                                        |
