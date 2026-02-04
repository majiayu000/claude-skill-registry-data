---
name: github-actions-syntax
description: |
  GitHub Actionsワークフローの構文とイベントトリガー、ジョブ定義、ステップ実行、パーミッション管理、環境変数設定について実装指針を提供する。CI/CDパイプラインの構築と管理を支援。

  Anchors:
  • GitHub Actions Workflow Syntax / 適用: ワークフロー構造設計 / 目的: 公式構文に準拠した実装
  • YAML 1.2 Specification / 適用: 構文検証・パース / 目的: 正確なYAML記述
  • 12-Factor App (Config) / 適用: 環境変数設計 / 目的: 環境非依存の設定管理

  Trigger:
  Use when creating or editing GitHub Actions workflow files, troubleshooting syntax errors, configuring event triggers, setting up job dependencies and matrix strategies, or managing permissions and environment variables.
  github actions, workflow syntax, yaml, event trigger, jobs, steps, permissions, environment variables
allowed-tools:
  - Glob
  - Grep
  - Read
  - Edit
  - Write
  - Bash
---

# GitHub Actions Syntax

## 概要

GitHub Actionsワークフロー構文の実装ガイド。ワークフローファイルの基本構造、イベントトリガー、ジョブ定義、ステップ実行、パーミッション管理、環境変数設定をカバー。

## ワークフロー

### Phase 1: 構文設計

**目的**: ワークフローの目的と構造を設計

**アクション**:

1. ワークフローの目的（CI/CD/自動化）を明確化
2. 必要なイベントトリガーを特定
3. ジョブの依存関係と実行順序を設計

**Task**: `agents/design-workflow.md` を参照

### Phase 2: 実装

**目的**: ワークフローYAMLを実装

**アクション**:

1. `assets/workflow-template.yaml` をベースに作成
2. イベントトリガー、ジョブ、ステップを実装
3. パーミッションと環境変数を設定

**Task**: `agents/implement-workflow.md` を参照

### Phase 3: 検証

**目的**: ワークフロー構文を検証

**アクション**:

1. `scripts/validate-workflow.mjs` で構文検証
2. ローカルまたはテストブランチで動作確認
3. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-workflow.md` を参照

## Task仕様ナビ

| Task               | 起動タイミング | 入力       | 出力               |
| ------------------ | -------------- | ---------- | ------------------ |
| design-workflow    | Phase 1開始時  | 要件・目的 | ワークフロー設計書 |
| implement-workflow | Phase 2開始時  | 設計書     | ワークフローYAML   |
| validate-workflow  | Phase 3開始時  | YAML       | 検証レポート       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- ワークフローファイルを作成する前に構文仕様を確認する
- イベントトリガーを適切に設定して不要な実行を防ぐ
- ジョブに明示的なpermissionsを設定する
- シークレットはsecretsコンテキスト経由で参照する
- マトリックス戦略で複数環境テストを効率化する
- キャッシュを活用して実行時間を短縮する

### 避けるべきこと

- シークレットをワークフロー定義やログに露出しない
- 過度に複雑なワークフロー設計で保守性を損なわない
- 不必要なジョブの並列実行でリソースを浪費しない
- キャッシュキーの設計が不適切でキャッシュミスを多発させない
- パーミッションを最小限の原則に従わずに設定しない

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                                 | 内容                 |
| ------------ | -------------------------------------------------------------------- | -------------------- |
| 基礎知識     | See [references/basics.md](references/basics.md)                     | ワークフロー基本構造 |
| 構文パターン | See [references/patterns.md](references/patterns.md)                 | 実装パターン集       |
| 構文一覧     | See [references/syntax-reference.md](references/syntax-reference.md) | 完全構文リファレンス |

### scripts/（決定論的処理）

| スクリプト              | 用途               | 使用例                                            |
| ----------------------- | ------------------ | ------------------------------------------------- |
| `validate-workflow.mjs` | ワークフロー検証   | `node scripts/validate-workflow.mjs workflow.yml` |
| `log_usage.mjs`         | フィードバック記録 | `node scripts/log_usage.mjs --result success`     |

### assets/（テンプレート）

| テンプレート             | 用途                         |
| ------------------------ | ---------------------------- |
| `workflow-template.yaml` | ワークフロー基本テンプレート |

## 変更履歴

| Version | Date       | Changes                                                    |
| ------- | ---------- | ---------------------------------------------------------- |
| 2.1.0   | 2026-01-05 | Codecov統合パターン追加（patterns.md）、CI/CD統合実績追加  |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、構造再編成                       |
| 1.1.0   | 2025-12-31 | Anchor/Trigger形式に改善                                   |
| 1.0.0   | 2025-12-24 | 初版                                                       |
