---
name: websocket-patterns
description: |
  WebSocketによる双方向リアルタイム通信パターン専門スキル。
  接続ライフサイクル管理、メッセージキューイング、ハートビート戦略、エラーリカバリーを提供する。

  Anchors:
  • RFC 6455 (WebSocket Protocol) / 適用: プロトコル仕様 / 目的: 標準準拠の実装
  • 『Designing Data-Intensive Applications』(Martin Kleppmann) / 適用: メッセージング設計 / 目的: 信頼性確保
  • Circuit Breaker Pattern / 適用: エラーリカバリー / 目的: 障害伝播防止

  Trigger:
  Use when implementing WebSocket connections, real-time bidirectional communication, connection lifecycle management, message queueing, or heartbeat monitoring.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
  - Task
---

# WebSocket Patterns

## 概要

WebSocketによる双方向リアルタイム通信パターンを専門とするスキル。
接続ライフサイクル管理、メッセージキューイング、ハートビート戦略、エラーリカバリーを通じて、信頼性の高いリアルタイム通信を実現する。

## ワークフロー

### Phase 1: 接続設計

**目的**: WebSocket接続の要件を整理し設計方針を決定

**アクション**:

1. 接続要件の確認（URL、プロトコル、認証方式）
2. 再接続戦略の決定（Exponential Backoff設定）
3. メッセージフォーマットの定義（JSON/Binary）
4. 信頼性要件の確認（ACK必要性、順序保証）

**Task**: `agents/connection-manager.md` を参照

### Phase 2: 実装

**目的**: 各エージェントに基づいて機能を実装

**アクション（要件に応じて選択）**:

| 機能               | エージェント       | 主な実装内容                       |
| ------------------ | ------------------ | ---------------------------------- |
| 接続管理           | connection-manager | 状態マシン、再接続、クリーンアップ |
| メッセージ送受信   | message-handler    | キューイング、ACK、順序保証        |
| ヘルスモニタリング | health-monitor     | Ping/Pong、レイテンシ測定          |
| エラー処理         | error-recoverer    | 分類、リカバリー、フォールバック   |

**Task**: 機能に応じたエージェントを参照

### Phase 3: 検証と記録

**目的**: 実装の検証と知見の記録

**アクション**:

1. 接続・切断・再接続のテスト
2. メッセージ送受信の信頼性テスト
3. エッジケース（ネットワーク断など）の確認
4. `scripts/log_usage.mjs` で実行記録を保存

## Task仕様ナビ

| Task               | 説明                                       | 参照                           |
| ------------------ | ------------------------------------------ | ------------------------------ |
| 接続ライフサイクル | 接続確立、状態管理、再接続、クリーンアップ | `agents/connection-manager.md` |
| メッセージング     | キューイング、ACK/NACK、順序保証           | `agents/message-handler.md`    |
| ヘルスチェック     | ハートビート、レイテンシ測定、接続監視     | `agents/health-monitor.md`     |
| エラーリカバリー   | 分類、自動復旧、Circuit Breaker            | `agents/error-recoverer.md`    |

## ベストプラクティス

### すべきこと

- 接続状態を明示的な状態マシンで管理する
- 再接続にはExponential Backoffを使用する
- 重要なメッセージにはACK確認を実装する
- ハートビートで接続の健全性を監視する
- エラーを種別ごとに分類して適切に対処する
- Circuit Breakerで障害の伝播を防止する

### 避けるべきこと

- ハートビートなしに長時間接続を保持する
- ACKなしに重要なメッセージを送信する
- エラーハンドリングなしにプロダクション運用する
- 再接続の上限なしに無限リトライする
- 接続状態を確認せずにメッセージを送信する

## リソース参照

### agents/（Task仕様書）

| エージェント       | パス                           | 用途               |
| ------------------ | ------------------------------ | ------------------ |
| connection-manager | `agents/connection-manager.md` | 接続ライフサイクル |
| message-handler    | `agents/message-handler.md`    | メッセージング     |
| health-monitor     | `agents/health-monitor.md`     | ヘルスチェック     |
| error-recoverer    | `agents/error-recoverer.md`    | エラーリカバリー   |

### references/（詳細知識）

| リソース           | パス                                 | 用途             |
| ------------------ | ------------------------------------ | ---------------- |
| 接続ライフサイクル | `references/connection-lifecycle.md` | 状態遷移パターン |
| メッセージキュー   | `references/message-queueing.md`     | キューイング設計 |
| ハートビート戦略   | `references/heartbeat-strategies.md` | 接続監視パターン |

### scripts/（自動化処理）

| スクリプト                   | 用途     | 使用例                                        |
| ---------------------------- | -------- | --------------------------------------------- |
| analyze-websocket-config.mjs | 設定分析 | `node scripts/analyze-websocket-config.mjs`   |
| log_usage.mjs                | 使用記録 | `node scripts/log_usage.mjs --result success` |
| validate-skill.mjs           | 構造検証 | `node scripts/validate-skill.mjs -v`          |

### assets/（テンプレート）

| テンプレート          | パス                                  | 用途                 |
| --------------------- | ------------------------------------- | -------------------- |
| WebSocketクライアント | `assets/websocket-client-template.ts` | クライアント実装基盤 |

## 変更履歴

| Version | Date       | Changes                                       |
| ------- | ---------- | --------------------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様準拠。4エージェント体制に拡張 |
| 1.1.0   | 2025-12-31 | Task仕様ナビ追加、ワークフロー詳細化          |
| 1.0.0   | 2025-12-24 | 初版作成                                      |
