---
name: electron-architecture
description: |
  Electronデスクトップアプリケーションのアーキテクチャ設計を専門とするスキル。
  Main/Renderer/Preloadプロセスの責務分離、型安全なIPC通信設計、セキュリティ設定を支援する。

  Anchors:
  • Clean Architecture (Robert C. Martin) / 適用: 依存関係ルール / 目的: プロセス間の責務分離
  • Electron公式ドキュメント / 適用: プロセスモデル / 目的: セキュアな設計パターン
  • TypeScript / 適用: 型安全なIPC設計 / 目的: エンドツーエンドの型安全性

  Trigger:
  Use when designing Electron architecture, implementing IPC communication, configuring security settings, or separating Main/Renderer responsibilities.
  electron, ipc, main process, renderer, preload, contextIsolation, contextBridge
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron Architecture

## 概要

Electronデスクトップアプリケーションのアーキテクチャ設計を専門とするスキル。Main/Renderer/Preloadプロセスの責務分離、型安全なIPC通信設計、セキュリティ設定を支援する。

## ワークフロー

### Phase 1: アーキテクチャ設計

**目的**: プロセス構造と責務分離を設計

**アクション**:

1. アプリケーション要件を分析
2. Main/Renderer/Preloadの責務を決定
3. `references/process-model.md` でプロセスモデルを確認

**Task**: `agents/architecture-designer.md` を参照

### Phase 2: IPC通信設計

**目的**: 型安全なプロセス間通信を設計

**アクション**:

1. IPC通信パターンを選定
2. チャンネルと型を定義
3. `references/ipc-patterns.md` でパターンを確認

**Task**: `agents/ipc-designer.md` を参照

### Phase 3: 実装と検証

**目的**: テンプレートを使用して実装し検証

**アクション**:

1. `assets/main-process.ts` でMainプロセスを実装
2. `assets/preload.ts` でPreloadを実装
3. `scripts/analyze-ipc.mjs` でIPC分析
4. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                  | 起動タイミング | 入力       | 出力                 |
| --------------------- | -------------- | ---------- | -------------------- |
| architecture-designer | Phase 1開始時  | アプリ要件 | アーキテクチャ設計書 |
| ipc-designer          | Phase 2開始時  | 設計書     | IPC設計書            |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                 | 理由                               |
| ------------------------ | ---------------------------------- |
| contextIsolation: true   | XSS攻撃からの保護                  |
| nodeIntegration: false   | Rendererからのシステムアクセス防止 |
| sandbox: true            | プロセス権限の最小化               |
| invoke/handleを使用      | 型安全な双方向通信                 |
| Preloadは最小限のAPI公開 | 攻撃対象面の最小化                 |

### 避けるべきこと

| 禁止事項                  | 問題点                     |
| ------------------------- | -------------------------- |
| RendererでNode.js API使用 | セキュリティリスク         |
| sendSyncの使用            | UIブロッキング             |
| Preloadで複雑ロジック実装 | 責務違反・テスト困難       |
| remote moduleの使用       | 非推奨・セキュリティリスク |

## リソース参照

### scripts/（決定論的処理）

| スクリプト           | 機能               |
| -------------------- | ------------------ |
| `analyze-ipc.mjs`    | IPC使用状況の分析  |
| `log_usage.mjs`      | フィードバック記録 |
| `validate-skill.mjs` | スキル構造の検証   |

### references/（詳細知識）

| リソース       | パス                          | 読込条件             |
| -------------- | ----------------------------- | -------------------- |
| プロセスモデル | `references/process-model.md` | アーキテクチャ設計時 |
| IPCパターン    | `references/ipc-patterns.md`  | IPC通信設計時        |

### assets/（テンプレート）

| アセット          | 用途                          |
| ----------------- | ----------------------------- |
| `main-process.ts` | Mainプロセステンプレート      |
| `preload.ts`      | Preloadスクリプトテンプレート |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠版に再構築 |
| 1.0.0   | 2025-12-24 | 初版作成                           |
