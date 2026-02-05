---
name: network-resilience
description: |
  ネットワーク障害に対する耐性設計を専門とするスキル。
  部分障害からの自動復旧、オフラインキュー、データ同期を統合的に提供し、
  ネットワーク不安定環境でも堅牢に動作するアプリケーションを構築する。

  Anchors:
  • Distributed Systems (Andrew Tanenbaum) / 適用: 部分障害への対応設計 / 目的: 障害耐性のあるシステム構築
  • The Pragmatic Programmer / 適用: 実践的なエラーハンドリング / 目的: 保守性の高いコード設計
  • Release It! (Michael Nygard) / 適用: サーキットブレーカー・リトライパターン / 目的: プロダクション品質の実現

  Trigger:
  Use when implementing network-aware applications, designing offline-first features, implementing automatic reconnection, building offline queues, or ensuring data synchronization between local and remote states.
  network resilience, offline, reconnection, retry, circuit breaker, state sync, offline queue, connection management
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Network Resilience

## 概要

ネットワーク障害に対する耐性設計を専門とするスキル。
部分障害からの自動復旧、オフラインキュー、データ同期を統合的に提供し、
ネットワーク不安定環境でも堅牢に動作するアプリケーションを構築する。

## ワークフロー

### Phase 1: 要件分析と耐性設計

**目的**: ネットワーク耐性要件を分析し、設計方針を決定

**参照エージェント**: `agents/requirements-analysis.md`

**アクション**:

1. `references/basics.md` でネットワーク耐性の基本概念を理解
2. オフライン要件（完全オフライン/一時オフライン）を確認
3. `references/reconnection-strategies.md` で再接続戦略を選定
4. `scripts/analyze-network-config.mjs` で設定の妥当性を検証

### Phase 2: 実装

**目的**: 接続管理、オフラインキュー、状態同期を実装

**参照エージェント**: `agents/implementation.md`

**アクション**:

1. `references/patterns.md` で実装パターンを確認
2. `assets/connection-manager-template.ts` をベースに接続管理を実装
3. `references/offline-queue-patterns.md` でオフラインキューを実装
4. `references/state-synchronization.md` でデータ同期を実装

### Phase 3: 検証

**目的**: ネットワーク障害シナリオでの動作検証

**参照エージェント**: `agents/validation.md`

**アクション**:

1. ネットワーク切断/復旧シミュレーション
2. オフラインキューの永続性確認
3. 競合解決の動作確認
4. `scripts/log_usage.mjs` で実行記録を保存

## リソース参照

### 参照ドキュメント

| ドキュメント                                                                   | 内容                     |
| ------------------------------------------------------------------------------ | ------------------------ |
| [references/basics.md](references/basics.md)                                   | ネットワーク耐性基礎     |
| [references/patterns.md](references/patterns.md)                               | 実装パターン             |
| [references/reconnection-strategies.md](references/reconnection-strategies.md) | 再接続戦略               |
| [references/offline-queue-patterns.md](references/offline-queue-patterns.md)   | オフラインキューパターン |
| [references/state-synchronization.md](references/state-synchronization.md)     | 状態同期戦略             |

### エージェント

| エージェント                      | 役割                   |
| --------------------------------- | ---------------------- |
| `agents/requirements-analysis.md` | 要件分析、設計方針決定 |
| `agents/implementation.md`        | 実装ガイド             |
| `agents/validation.md`            | 検証、品質確認         |

### スクリプト

| スクリプト                           | 用途                 |
| ------------------------------------ | -------------------- |
| `scripts/analyze-network-config.mjs` | 設定検証、推奨値算出 |
| `scripts/validate-skill.mjs`         | スキル構造検証       |
| `scripts/log_usage.mjs`              | 使用記録             |

### テンプレート

| テンプレート                            | 用途             |
| --------------------------------------- | ---------------- |
| `assets/connection-manager-template.ts` | 接続状態管理     |
| `assets/offline-queue-template.ts`      | オフラインキュー |

## ベストプラクティス

### すべきこと

- オフライン時のタスク蓄積（キュー実装）
- ネットワーク復旧後の自動再同期
- 接続状態に応じた動的な動作切り替え
- 指数バックオフによる再接続
- べき等性を考慮したキュー設計

### 避けるべきこと

- リトライなしのネットワーク呼び出し
- オフライン状態の無視
- 競合解決戦略の未定義
- 永続化なしのキュー（ブラウザリロードで消失）
- タイムアウトなしの接続待機
