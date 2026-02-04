---
name: domain-event-patterns
description: |
  ドメインイベントパターンを使用して、ビジネスドメイン内で発生した重要な出来事をモデル化・永続化・伝播するスキル。
  イベントソーシング、CQRS、イベント駆動アーキテクチャの実装をサポートする。

  Anchors:
  • Domain-Driven Design (Eric Evans) / 適用: ドメインイベント設計 / 目的: ビジネス上の重要な出来事の捕捉
  • Implementing DDD (Vaughn Vernon) / 適用: イベントストア実装 / 目的: イベント永続化パターン
  • CQRS/Event Sourcing (Greg Young) / 適用: 状態再構築 / 目的: イベントストリームからの状態復元

  Trigger:
  Use when designing domain events, implementing event sourcing, building event-driven architecture, modeling state changes as events, implementing CQRS patterns, creating event stores.
  domain event, event sourcing, CQRS, event-driven, event store, event handler
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Domain Event Patterns

## 概要

ドメインイベントパターンを使用して、ビジネスドメイン内で発生した重要な出来事をモデル化・永続化・伝播するスキル。イベントソーシング、CQRS、イベント駆動アーキテクチャの実装をサポートする。

## ワークフロー

### Phase 1: イベント設計

**目的**: ドメインイベントの識別と設計

**アクション**:

1. ビジネスイベントを識別
2. イベント名を過去形で命名
3. イベント構造を設計

**Task**: `agents/event-designer.md` を参照

### Phase 2: イベントストア実装

**目的**: イベントの永続化機構を構築

**アクション**:

1. イベントストアインターフェースを設計
2. 永続化ロジックを実装
3. スナップショット機構を検討

**Task**: `agents/event-store-implementer.md` を参照

### Phase 3: イベントハンドリング

**目的**: イベント発行・購読・処理の実装

**アクション**:

1. イベントパブリッシャーを実装
2. イベントハンドラーを作成
3. べき等性を確保

**Task**: `agents/event-handler-builder.md` を参照

### Phase 4: イベントソーシング

**目的**: イベントストリームからの状態再構築

**アクション**:

1. イベント適用ロジックを実装
2. 状態再構築機構を構築
3. `scripts/log_usage.mjs` で記録

**Task**: `agents/event-sourcing-architect.md` を参照

## Task仕様ナビ

| Task                     | 起動タイミング | 入力         | 出力           |
| ------------------------ | -------------- | ------------ | -------------- |
| event-designer           | Phase 1開始時  | ユースケース | イベント定義   |
| event-store-implementer  | Phase 2開始時  | イベント定義 | イベントストア |
| event-handler-builder    | Phase 3開始時  | イベント定義 | ハンドラー実装 |
| event-sourcing-architect | Phase 4開始時  | 集約定義     | ES実装         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項               | 理由                  |
| ---------------------- | --------------------- |
| イベント名は過去形     | 過去の事実を表現      |
| イベントは不変         | データ整合性の保証    |
| タイムスタンプを含める | 時系列での追跡が可能  |
| 小さなイベントを設計   | Single Responsibility |
| べき等なハンドラー     | 再実行時の安全性確保  |

### 避けるべきこと

| 禁止事項             | 問題点             |
| -------------------- | ------------------ |
| イベントの変更・削除 | 不変性違反         |
| 現在形のイベント名   | セマンティクス混乱 |
| 大きすぎるペイロード | パフォーマンス低下 |
| バージョニング無視   | 互換性問題         |

## リソース参照

### scripts/（決定論的処理）

| スクリプト      | 機能               |
| --------------- | ------------------ |
| `log_usage.mjs` | フィードバック記録 |

### references/（詳細知識）

| リソース           | パス                                                                     | 読込条件         |
| ------------------ | ------------------------------------------------------------------------ | ---------------- |
| イベント基礎       | [references/event-fundamentals.md](references/event-fundamentals.md)     | 設計時に参照     |
| イベントストア     | [references/event-store-patterns.md](references/event-store-patterns.md) | ストア実装時     |
| ハンドリング       | [references/event-handling.md](references/event-handling.md)             | ハンドラー実装時 |
| イベントソーシング | [references/event-sourcing.md](references/event-sourcing.md)             | ES実装時         |

### assets/（テンプレート）

| アセット                    | 用途                     |
| --------------------------- | ------------------------ |
| `domain-event-template.ts`  | ドメインイベントテンプレ |
| `event-handler-template.ts` | ハンドラーテンプレート   |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠版に再構築 |
| 1.0.0   | 2025-12-31 | 初版作成                           |
