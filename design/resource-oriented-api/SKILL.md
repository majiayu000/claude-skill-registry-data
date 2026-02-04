---
name: resource-oriented-api
description: |
  MCPのリソース指向API設計パターンを提供。URIスキーム設計、リソースモデル定義、
  プロバイダー実装、キャッシュ戦略、リソース変換パターンを網羅する。

  Anchors:
  • RESTful Web APIs (Leonard Richardson) / 適用: リソース設計・URI設計 / 目的: REST原則の適用
  • MCP Resource Protocol / 適用: リソースプロバイダー実装 / 目的: MCP仕様準拠

  Trigger:
  Use when designing MCP resources, implementing resource providers, or defining URI schemes.
  MCP resource, resource provider, URI scheme, リソース定義, リソースモデル, API設計
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Resource Oriented API

## 概要

MCPのリソース指向API設計パターンを提供するスキル。URIスキーム設計からリソースプロバイダー実装まで、リソース指向APIの設計・実装を支援する。

## ワークフロー

### Phase 1: リソースモデル設計

**目的**: ドメインに適したリソースモデルを設計する

**アクション**:

1. リソースとして公開すべきエンティティを特定
2. リソース間の階層・関連を定義
3. URIスキームを設計（`references/uri-scheme-guide.md`参照）
4. MIME-typeとコンテンツ形式を決定

**Task**: `agents/design-resource-model.md` を参照

### Phase 2: リソースプロバイダー実装

**目的**: 設計したリソースモデルをMCPプロバイダーとして実装

**アクション**:

1. リソース定義JSONを作成（`assets/resource-definition-template.json`参照）
2. プロバイダークラスを実装（`assets/resource-provider-template.ts`参照）
3. `scripts/validate-resource-definition.mjs`で定義を検証
4. `scripts/validate-uri.mjs`でURI設計を検証

**Task**: `agents/implement-provider.md` を参照

### Phase 3: 最適化と検証

**目的**: パフォーマンスとセキュリティを最適化

**アクション**:

1. キャッシュ戦略を適用（`references/caching-strategies.md`参照）
2. リソース変換パターンを適用（`references/resource-transformation.md`参照）
3. セキュリティチェック（パストラバーサル、スキーム制限）
4. 最終検証と記録（`scripts/log_usage.mjs`）

## Task仕様（ナビゲーション）

| Task                  | 起動タイミング | 入力                 | 出力                 |
| --------------------- | -------------- | -------------------- | -------------------- |
| design-resource-model | Phase 1開始時  | ドメイン要件         | リソースモデル設計書 |
| implement-provider    | Phase 2開始時  | リソースモデル設計書 | プロバイダー実装     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- URIは階層的で直感的な構造にする（例: `/users/123/posts/456`）
- リソース名は複数形・ケバブケースを使用（例: `my-resources`）
- パス深度は最大4レベルに制限
- 特殊文字は適切にパーセントエンコード
- キャッシュ戦略を必ず検討する

### 避けるべきこと

- 動詞をURIに含めない（例: `/getUser` は不可、`/users/123` を使用）
- パストラバーサル脆弱性を放置しない
- 無制限のスキーム許可（許可リストで制限する）
- キャッシュ無効化戦略なしでの運用

## リソース参照

### references/（詳細知識）

| リソース              | パス                                                                               | 用途                         |
| --------------------- | ---------------------------------------------------------------------------------- | ---------------------------- |
| URIスキーム設計ガイド | See [references/uri-scheme-guide.md](references/uri-scheme-guide.md)               | URI構造・命名規則・正規化    |
| キャッシュ戦略ガイド  | See [references/caching-strategies.md](references/caching-strategies.md)           | 多層キャッシュ・無効化戦略   |
| リソース変換パターン  | See [references/resource-transformation.md](references/resource-transformation.md) | パイプライン・フィルタリング |

### scripts/（決定論的処理）

| スクリプト                         | 用途               | 使用例                                                          |
| ---------------------------------- | ------------------ | --------------------------------------------------------------- |
| `validate-resource-definition.mjs` | リソース定義検証   | `node scripts/validate-resource-definition.mjs definition.json` |
| `validate-uri.mjs`                 | URI形式検証        | `node scripts/validate-uri.mjs "db://sqlite/users/123"`         |
| `log_usage.mjs`                    | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート                        | 用途                         |
| ----------------------------------- | ---------------------------- |
| `resource-definition-template.json` | リソース定義JSONテンプレート |
| `resource-provider-template.ts`     | TypeScriptプロバイダー雛形   |

## 変更履歴

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に準拠、agents追加、構造改善 |
| 1.0.1   | 2025-12-24 | Spec alignment and required artifacts added  |
