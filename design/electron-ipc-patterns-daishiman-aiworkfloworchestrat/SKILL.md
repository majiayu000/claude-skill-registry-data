---
name: electron-ipc-patterns
description: |
  Electronプロセス間通信（IPC）パターンの設計と実装専門知識。
  安全で効率的なMain-Rendererプロセス通信、contextBridge、型安全なAPI設計を提供。

  Anchors:
  • Electron Security / 適用: contextBridge/preload設計 / 目的: セキュアなIPC実装
  • Clean Architecture / 適用: Main/Renderer境界設計 / 目的: 責務分離と保守性
  • Type Safety / 適用: TypeScript型契約 / 目的: IPC通信の型安全性確保

  Trigger:
  Use when implementing IPC communication patterns, setting up contextBridge, designing typed IPC handlers, securing renderer-main communication, or structuring bidirectional messaging flows.
  ipcMain, ipcRenderer, contextBridge, invoke, handle, preload, typed IPC
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron IPC Patterns

## 概要

Electronプロセス間通信（IPC）パターンの設計と実装専門知識を提供。
Main-Rendererプロセス間の双方向通信、型安全なAPI設計、セキュアなcontextBridge実装を支援する。

## ワークフロー

### Phase 1: 要件分析とパターン選択

**目的**: IPC通信要件を整理し適切なパターンを選択

**アクション**:

1. 通信方向（単方向/双方向/イベント駆動）を特定
2. セキュリティ要件（context isolation必須）を確認
3. `references/pattern-catalog.md` から適切なパターンを選択
4. 必要に応じて `agents/analyze-requirements.md` を参照

### Phase 2: 型定義とAPI設計

**目的**: 型安全なIPC契約を設計

**アクション**:

1. `assets/ipc-types-template.ts` を使用してAPI型を定義
2. チャネル命名規則を適用（例: `app:feature:action`）
3. 入力検証スキーマを設計
4. 必要に応じて `agents/design-typed-api.md` を参照

### Phase 3: 実装

**目的**: IPCハンドラとクライアントコードを実装

**アクション**:

1. `assets/preload-template.ts` を使用してcontextBridgeを実装
2. Mainプロセスハンドラを実装
3. Rendererクライアントを実装
4. 複雑な実装は `agents/implement-ipc-layer.md` を参照

### Phase 4: セキュリティ検証

**目的**: セキュリティベストプラクティスを検証

**アクション**:

1. `references/security-checklist.md` でセキュリティ確認
2. 必要に応じて `agents/security-review.md` を参照
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                 | 起動タイミング     | 入力       | 出力             |
| -------------------- | ------------------ | ---------- | ---------------- |
| analyze-requirements | IPC要件分析時      | 通信要件   | パターン推奨     |
| design-typed-api     | API設計時          | 機能要件   | 型定義・契約     |
| implement-ipc-layer  | 実装時             | API設計    | 実装コード       |
| security-review      | セキュリティ検証時 | 実装コード | セキュリティ報告 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **context isolation有効化**: contextBridgeを必ず使用
- **型定義**: TypeScriptでIPC契約を型定義
- **命名規則**: チャネル名に一貫した規則（`app:feature:action`）
- **invoke/handle**: Promise-basedパターンを優先
- **入力検証**: Mainプロセス側で必ず検証
- **エラーハンドリング**: 適切なタイムアウトと例外処理

### 避けるべきこと

- **nodeIntegration有効化**: セキュリティリスク
- **ipcRenderer直接公開**: Rendererからの直接アクセスを禁止
- **any型使用**: 型安全性を無視しない
- **sendSync使用**: 同期IPCは避ける
- **入力信頼**: 外部入力は常にバリデーション

## リソース参照

### references/（詳細知識）

| リソース                   | パス                                                                     | 用途               |
| -------------------------- | ------------------------------------------------------------------------ | ------------------ |
| IPCパターンカタログ        | See [references/pattern-catalog.md](references/pattern-catalog.md)       | パターン選択・比較 |
| セキュリティチェックリスト | See [references/security-checklist.md](references/security-checklist.md) | セキュリティ検証   |

### scripts/（決定論的処理）

| スクリプト      | 用途               | 使用例                                                          |
| --------------- | ------------------ | --------------------------------------------------------------- |
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 4"` |

### assets/（テンプレート）

| テンプレート            | 用途                          |
| ----------------------- | ----------------------------- |
| `ipc-types-template.ts` | IPC型定義テンプレート         |
| `preload-template.ts`   | Preloadスクリプトテンプレート |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、構造最適化 |
| 1.0.0   | 2025-12-31 | 初版作成                             |
