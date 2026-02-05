---
name: http-best-practices
description: |
  HTTPプロトコルの仕様に基づき、RESTful APIおよびWebサービス実装における通信設計を提供。ステータスコード、ヘッダー、キャッシュ、冪等性設計を網羅。

  Anchors:
  • HTTP/2 in Action (Barry Pollard) / 適用: プロトコル仕様・パフォーマンス / 目的: 効率的なHTTP通信
  • RESTful Web Services (Richardson, Ruby) / 適用: REST設計原則 / 目的: 一貫したAPI設計
  • Web API Design (Brian Mulloy) / 適用: 実践的なAPI設計パターン / 目的: 使いやすいAPI

  Trigger:
  Use when designing REST APIs, implementing HTTP clients, configuring cache strategies, setting security headers, or ensuring idempotency.
  http, rest api, status codes, cache-control, cors, idempotency, headers, http/2, keep-alive
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# HTTP Best Practices

## 概要

HTTPプロトコルの仕様に基づき、RESTful APIおよびWebサービス実装における正しく効率的な通信設計を提供。
ステータスコード選択、ヘッダー管理、キャッシュ戦略、コネクション最適化、セキュリティヘッダー設定、冪等性設計を網羅。

## ワークフロー

### Phase 1: 要件分析

**目的**: API設計のための通信仕様要件を明確化

**アクション**:

1. `references/Level1_basics.md` でHTTPの基本概念を確認
2. API仕様に基づき適用すべきHTTPパターンを特定
3. セキュリティ要件に基づき必要なヘッダーを洗い出す

**Task**: `agents/requirements-analysis.md` を参照

### Phase 2: 詳細設計

**目的**: HTTPプロトコル仕様に基づいた詳細設計を実施

**アクション**:

1. `references/status-codes.md` でステータスコード選択基準を確認
2. `references/headers-best-practices.md` でヘッダー設計
3. `references/caching-strategies.md` でキャッシュ戦略設計
4. `references/idempotency.md` で冪等性実装パターンを確認

**Task**: `agents/detailed-design.md` を参照

### Phase 3: 実装検証

**目的**: 設計の実装可能性を検証し記録

**アクション**:

1. `scripts/analyze-headers.mjs` でセキュリティヘッダー検証
2. `scripts/validate-http-client.mjs` でHTTPクライアント検証
3. `scripts/log_usage.mjs` で実行記録を保存

**Task**: `agents/implementation-verification.md` を参照

## Task仕様ナビ

| Task                        | 起動タイミング | 入力       | 出力         |
| --------------------------- | -------------- | ---------- | ------------ |
| requirements-analysis       | Phase 1開始時  | API仕様    | 要件定義書   |
| detailed-design             | Phase 2開始時  | 要件定義書 | 設計書       |
| implementation-verification | Phase 3開始時  | 設計書     | 検証レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 各エンドポイントに標準ステータスコードを明示的に定義
- CORS、CSP、HSTSなどセキュリティヘッダーを一元設定
- Cache-Control、ETagをリソース種別ごとに定義
- PUT/DELETE/PATCHはIdempotency-Keyで冪等性を確保
- Keep-Alive、HTTP/2、コネクションプーリングを活用
- エラーレスポンス形式を統一

### 避けるべきこと

- 401/403の意味を誤って使用
- セキュリティヘッダーなしでAPI公開
- キャッシュ無効化戦略なしでキャッシュ有効化
- 冪等性保証なしで外部API連携
- リクエストごとにTCP接続を確立

## リソース参照

### references/（詳細知識）

| リソース         | パス                                                                             | 内容                 |
| ---------------- | -------------------------------------------------------------------------------- | -------------------- |
| 基礎知識         | See [references/Level1_basics.md](references/Level1_basics.md)                   | HTTP基本概念         |
| 中級知識         | See [references/Level2_intermediate.md](references/Level2_intermediate.md)       | 実装パターン         |
| 上級知識         | See [references/Level3_advanced.md](references/Level3_advanced.md)               | HTTP/2最適化         |
| 専門家向け       | See [references/Level4_expert.md](references/Level4_expert.md)                   | 高負荷環境設計       |
| ステータスコード | See [references/status-codes.md](references/status-codes.md)                     | 2xx/3xx/4xx/5xx選択  |
| ヘッダー設計     | See [references/headers-best-practices.md](references/headers-best-practices.md) | セキュリティヘッダー |
| コネクション管理 | See [references/connection-management.md](references/connection-management.md)   | Keep-Alive/HTTP/2    |
| 冪等性設計       | See [references/idempotency.md](references/idempotency.md)                       | Idempotency-Key実装  |

### scripts/（決定論的処理）

| スクリプト                 | 用途                 | 使用例                                             |
| -------------------------- | -------------------- | -------------------------------------------------- |
| `validate-http-client.mjs` | HTTPクライアント検証 | `node scripts/validate-http-client.mjs src/api.ts` |
| `analyze-headers.mjs`      | ヘッダー分析         | `node scripts/analyze-headers.mjs response.json`   |
| `log_usage.mjs`            | フィードバック記録   | `node scripts/log_usage.mjs --result success`      |

### assets/（テンプレート）

| テンプレート                 | 用途                 |
| ---------------------------- | -------------------- |
| `http-client-template.ts`    | HTTPクライアント実装 |
| `api-response-template.json` | APIレスポンス設計    |

## 変更履歴

| Version | Date       | Changes                                 |
| ------- | ---------- | --------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md完全準拠、description簡潔化 |
| 1.1.0   | 2025-12-31 | Phase詳細化、Task仕様ナビ追加           |
| 1.0.0   | 2025-12-24 | 初版                                    |
