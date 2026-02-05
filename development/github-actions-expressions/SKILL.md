---
name: github-actions-expressions
description: |
  GitHub Actionsのワークフローで使用できる式構文とコンテキストオブジェクトを専門とするスキル。
  ${{ }}構文、演算子、リテラル、組み込み関数、および利用可能なすべてのコンテキスト（github, env, job, steps, runner, secrets, needs, matrix, inputs）を提供します。

  Anchors:
  • Continuous Delivery (Jez Humble) / 適用: パイプライン設計とCI/CD自動化 / 目的: 信頼性の高いワークフロー式の設計

  Trigger:
  Use when implementing conditional execution (if:), referencing step outputs, generating dynamic values, or utilizing context information (branch names, commit SHA, event types) in GitHub Actions workflows.
  Keywords: github actions, workflow, expressions, context, ${{ }}, if condition, matrix, secrets, steps output
version: 1.0.0
level: 1
last_updated: 2025-12-31
---

# GitHub Actions Expressions

## 概要

GitHub Actionsのワークフローで使用できる式構文とコンテキストオブジェクトを専門とするスキル。
${{ }}構文、演算子、リテラル、組み込み関数、および利用可能なすべてのコンテキスト（github, env, job, steps, runner, secrets, needs, matrix, inputs）を提供します。
**適用範囲**: GitHub Actionsワークフローを使用するすべてのリポジトリ

## ワークフロー

### Phase 1: 要件分析とタスク起動

**目的**: ワークフロー要件を分析し、適切な式設計を行う

**タスク**: Expression Analyzer (`agents/expression-analyzer.md`)

**アクション**:

1. ワークフロー要件を明確化（条件分岐、動的値生成、コンテキスト使用）
2. [references/context-objects.md](references/context-objects.md) でコンテキストを選択
3. Expression Analyzer タスクを起動し、式設計仕様書を作成
   - 使用コンテキストの選択
   - 組み込み関数の選定
   - 適用パターンの特定

**成果物**: 式設計仕様書（使用コンテキスト、関数、パターン、エッジケース含む）

### Phase 2: 式の実装

**目的**: 設計された式を正確なYAML形式で実装する

**タスク**: Expression Implementer (`agents/expression-implementer.md`)

**アクション**:

1. `references/expression-syntax.md` で構文規則を確認
2. Expression Implementer タスクを起動し、式を実装
   - 設計仕様書に基づく実装
   - `assets/expression-examples.yaml` のテンプレート形式に準拠
   - 説明コメントとエッジケース対応を追加

**成果物**: 実装済みワークフロー式（YAML形式、コメント、使用例含む）

### Phase 3: 検証と記録

**目的**: 実装された式の品質を検証し、実行記録を保存する

**タスク**: Expression Validator (`agents/expression-validator.md`)

**アクション**:

1. Expression Validator タスクを起動し、検証を実施
   - `scripts/validate-expressions.mjs` で構文検証
   - `references/conditional-patterns.md` でアンチパターン確認
   - エッジケーステスト実施
2. 検証レポートを確認し、必要に応じて修正
3. `scripts/log_usage.mjs` で実行記録を保存

**成果物**: 検証レポート、修正提案、ログ記録

## Task仕様（実行直前に参照）

### Expression Analyzer

- **パス**: `agents/expression-analyzer.md`
- **役割**: ワークフロー要件を分析し、適切な式設計を行う
- **入力**: ワークフロー要件、既存ワークフローファイル（任意）
- **出力**: 式設計仕様書（コンテキスト、関数、パターン、エッジケース）
- **参照**: `references/context-objects.md`, `references/builtin-functions.md`, `references/conditional-patterns.md`

### Expression Implementer

- **パス**: `agents/expression-implementer.md`
- **役割**: 設計された式を正確なYAML形式で実装する
- **入力**: 式設計仕様書
- **出力**: 実装済みワークフロー式（YAML、コメント、使用例）
- **参照**: `references/expression-syntax.md`, `assets/expression-examples.yaml`

### Expression Validator

- **パス**: `agents/expression-validator.md`
- **役割**: 実装された式の品質を検証する
- **入力**: 実装済みワークフロー式、式設計仕様書（参照用）
- **出力**: 検証レポート（構文、ロジック、セキュリティ、パフォーマンス）
- **参照**: `scripts/validate-expressions.mjs`, `references/conditional-patterns.md`

## ベストプラクティス

### すべきこと

- 必ず `references/context-objects.md` でコンテキストの利用可能性を確認
- `references/builtin-functions.md` から適切な関数を選択
- `references/conditional-patterns.md` の推奨パターンを適用
- セキュリティリスク（secrets の不適切な使用）に注意
- エッジケースを考慮した設計・実装

### 避けるべきこと

- コンテキストや関数の仕様を確認せずに進めること
- `references/conditional-patterns.md` のアンチパターンを使用すること
- 検証なしで本番環境に適用すること
- 複雑すぎる式（可読性・保守性の低下）

## リソース参照

### references/（知識外部化）

| リソース     | パス                                                                     | 内容                                     |
| ------------ | ------------------------------------------------------------------------ | ---------------------------------------- |
| コンテキスト | [references/context-objects.md](references/context-objects.md)           | github, env, job, steps等のコンテキスト  |
| 組み込み関数 | [references/builtin-functions.md](references/builtin-functions.md)       | 文字列関数、配列関数、型変換等           |
| 条件パターン | [references/conditional-patterns.md](references/conditional-patterns.md) | ブランチ/イベント条件、アンチパターン    |
| 式構文       | [references/expression-syntax.md](references/expression-syntax.md)       | ${{ }}構文、演算子、リテラル、エスケープ |

### scripts/（決定論的処理）

| スクリプト                 | 用途               | 使用例                                                  |
| -------------------------- | ------------------ | ------------------------------------------------------- |
| `validate-expressions.mjs` | 式の構文検証       | `node scripts/validate-expressions.mjs <workflow-file>` |
| `log_usage.mjs`            | フィードバック記録 | `node scripts/log_usage.mjs --result success`           |
| `validate-skill.mjs`       | 構造検証           | `node scripts/validate-skill.mjs`                       |

### assets/（テンプレート）

| テンプレート               | 用途                 |
| -------------------------- | -------------------- |
| `expression-examples.yaml` | 標準的な式パターン集 |

## 変更履歴

| Version | Date       | Changes                                                                               |
| ------- | ---------- | ------------------------------------------------------------------------------------- |
| 1.2.0   | 2026-01-05 | CI/CDカバレッジ統合で使用、条件分岐設計（PR or main）の実績追加                       |
| 1.1.0   | 2026-01-02 | references/を整理、Level1-4削除、18-skills.md仕様準拠                                 |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様準拠: agents/追加、EVALS.json/LOGS.md作成、Progressive Disclosure適用 |
