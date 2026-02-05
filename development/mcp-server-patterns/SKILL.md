---
name: mcp-server-patterns
description: |
  MCPサーバー設計パターンとアーキテクチャベストプラクティス。ツール組織化、エラーハンドリング、状態管理、サーバーライフサイクル管理の実証済みパターンを提供。

  Anchors:
  • Clean Architecture / 適用: サーバー構造と依存関係管理 / 目的: テスト可能で保守性の高いコード
  • Domain-Driven Design / 適用: ツールドメインモデリングと境界付きコンテキスト / 目的: 機能別ツール組織化
  • Pragmatic Programmer / 適用: エラーハンドリングと回復性パターン / 目的: 堅牢なサーバー構築

  Trigger:
  Use when designing MCP server architecture, organizing tool definitions, implementing error handling patterns, managing server state, structuring MCP server projects, or refactoring existing MCP servers.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# MCP Server Patterns

> **相対パス**: `SKILL.md`
> **読込条件**: スキル使用時（自動）

---

## 概要

MCP サーバー設計パターンとアーキテクチャベストプラクティス。

**対象領域**:

| 領域               | 説明                                   |
| ------------------ | -------------------------------------- |
| サーバー構造       | 3 層アーキテクチャ、プロジェクト構成   |
| ツール組織化       | ドメイン別、規模別組織化パターン       |
| エラーハンドリング | 分類、中央集権化、リトライ             |
| 状態管理           | セッション、キャッシュ、ライフサイクル |

---

## ワークフロー

### Phase 1: アーキテクチャ設計

**Task**: `agents/architecture-designer.md`

| 入力         | 出力             |
| ------------ | ---------------- |
| 要件・ツール | 設計ドキュメント |

**参照**: `references/basics.md`

### Phase 2: 実装構造

**Task**: `agents/implementation-guide.md`

| 入力     | 出力             |
| -------- | ---------------- |
| 設計仕様 | 実装済みサーバー |

**参照**: `references/patterns.md`, `assets/`

### Phase 3: ライフサイクル管理

**Task**: `agents/lifecycle-manager.md`

| 入力     | 出力         |
| -------- | ------------ |
| サーバー | 状態管理実装 |

**参照**: `references/patterns.md`

---

## ベストプラクティス

| すべきこと                                        | 避けるべきこと                   |
| ------------------------------------------------- | -------------------------------- |
| ドメイン/機能別にツールを整理                     | モノリシックなツール定義         |
| 適切な MCP エラーコードで包括的エラー処理         | 汎用エラーメッセージ             |
| テスタビリティのための DI 使用                    | 密結合実装                       |
| 関心の分離: トランスポート/ロジック/データ        | ビジネスロジックとプロトコル混在 |
| 適切なライフサイクル管理（初期化/クリーンアップ） | 適切な状態管理なしの可変状態保持 |
| TypeScript で型安全なツールスキーマ               | any 型の使用                     |

---

## Task ナビゲーション

| Task                       | 目的               | 参照リソース  |
| -------------------------- | ------------------ | ------------- |
| `architecture-designer.md` | サーバー設計       | `basics.md`   |
| `implementation-guide.md`  | 実装ガイダンス     | `patterns.md` |
| `lifecycle-manager.md`     | ライフサイクル実装 | `patterns.md` |

---

## リソース参照

### References

| ファイル      | 内容                                   | 読込条件   |
| ------------- | -------------------------------------- | ---------- |
| `basics.md`   | サーバー構造、ツール定義、基本パターン | 初回使用時 |
| `patterns.md` | 高度なアーキテクチャ、状態管理、回復性 | 設計時     |

### Assets

| ファイル           | 内容                       |
| ------------------ | -------------------------- |
| `tool-template.ts` | ツール定義テンプレート     |
| `error-handler.ts` | エラーハンドラテンプレート |

### Scripts

| スクリプト           | 用途       |
| -------------------- | ---------- |
| `validate-skill.mjs` | スキル検証 |
| `log_usage.mjs`      | 使用記録   |

---

## 関連スキル

- `mcp-protocol` - MCP プロトコル仕様とツールスキーマ定義
- `clean-architecture-principles` - 全体的なアーキテクチャ設計
- `error-handling-patterns` - エラー処理パターン
