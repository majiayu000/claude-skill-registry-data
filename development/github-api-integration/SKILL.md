---
name: github-api-integration
description: |
  GitHub APIをGitHub Actions内で活用するための統合スキル。REST APIとGraphQL APIの両方を使用して、Issue、Pull Request、リリース、ワークフローなどの自動化を実現。

  Anchors:
  • GitHub REST API / 適用: Issue、PR、リポジトリ操作 / 目的: 標準的なCRUD操作
  • GitHub GraphQL API / 適用: 複雑なデータ取得 / 目的: 効率的なバッチ処理
  • RESTful Web APIs (Leonard Richardson) / 適用: API設計原則 / 目的: 適切なリソース設計

  Trigger:
  Use when integrating GitHub API calls in GitHub Actions, automating Issue and PR operations, generating release notes, managing repositories programmatically, or handling API authentication and rate limiting.
  github api, rest api, graphql, gh cli, automation, issue, pull request, release
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# GitHub API Integration

## 概要

GitHub APIをGitHub Actionsワークフロー内で効果的に活用するための実装ガイド。REST API、GraphQL API、gh CLIを使用した自動化パターンを提供。

## ワークフロー

### Phase 1: API設計

**目的**: API操作の要件と認証方式を決定

**アクション**:

1. 操作対象（Issue/PR/Release等）を特定
2. REST API vs GraphQL APIの選択
3. 認証方式（GITHUB_TOKEN/PAT）を決定

**Task**: `agents/design-api-integration.md` を参照

### Phase 2: 実装

**目的**: API呼び出しを実装

**アクション**:

1. `assets/api-workflow.yaml` をベースに作成
2. 認証とパーミッションを設定
3. API呼び出しとエラーハンドリングを実装

**Task**: `agents/implement-api-calls.md` を参照

### Phase 3: 検証

**目的**: API操作の動作を検証

**アクション**:

1. ドライランでAPI呼び出しをテスト
2. レート制限とエラー処理を確認
3. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-api-integration.md` を参照

## Task仕様ナビ

| Task                     | 起動タイミング | 入力   | 出力             |
| ------------------------ | -------------- | ------ | ---------------- |
| design-api-integration   | Phase 1開始時  | 要件   | API設計書        |
| implement-api-calls      | Phase 2開始時  | 設計書 | ワークフローYAML |
| validate-api-integration | Phase 3開始時  | YAML   | 検証レポート     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- GITHUB_TOKENはsecretsとして管理する
- 必要最小限のパーミッションを設定する
- GraphQL APIで効率的にデータを取得する
- レート制限を監視しリトライロジックを実装する
- エラーレスポンスを適切にハンドリングする

### 避けるべきこと

- トークンをワークフローファイルに直接記載しない
- 不必要に高い権限スコープを設定しない
- ループ内で複数回APIを呼び出さない（バッチ処理を使用）
- APIレスポンスの機密情報をログに出力しない
- レート制限を無視してリトライしない

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                                 | 内容              |
| ------------ | -------------------------------------------------------------------- | ----------------- |
| 基礎知識     | See [references/basics.md](references/basics.md)                     | API概念と認証     |
| RESTパターン | See [references/rest-patterns.md](references/rest-patterns.md)       | REST API実装例    |
| GraphQL      | See [references/graphql-patterns.md](references/graphql-patterns.md) | GraphQL API実装例 |

### scripts/（決定論的処理）

| スクリプト       | 用途               | 使用例                                        |
| ---------------- | ------------------ | --------------------------------------------- |
| `api-helper.mjs` | API操作ヘルパー    | `node scripts/api-helper.mjs --action list`   |
| `log_usage.mjs`  | フィードバック記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート        | 用途                |
| ------------------- | ------------------- |
| `api-workflow.yaml` | API操作ワークフロー |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、構造再編成 |
| 1.0.0   | 2025-12-31 | 初版                                 |
