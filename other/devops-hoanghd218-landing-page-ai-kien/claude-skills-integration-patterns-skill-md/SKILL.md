---
name: .claude/skills/integration-patterns/SKILL.md
description: |
  MCPサーバーと外部システム間の統合パターンに関する専門知識。
  同期・非同期通信、イベント駆動アーキテクチャ、データ同期パターンの設計指針を提供します。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/integration-patterns/resources/async-patterns.md`: Message Queue/Pub-Sub/Sagaパターンの詳細と実装ガイド
  - `.claude/skills/integration-patterns/resources/event-driven-guide.md`: Event Sourcing/CQRS/Webhookによるイベント駆動設計
  - `.claude/skills/integration-patterns/resources/sync-patterns.md`: Request-Response/Aggregator/Gatewayパターンの詳細
  - `.claude/skills/integration-patterns/scripts/review-integration-design.mjs`: 統合設計のアーキテクチャレビューと改善提案
  - `.claude/skills/integration-patterns/scripts/validate-message-schema.mjs`: メッセージスキーマ定義の検証とバージョン互換性チェック
  - `.claude/skills/integration-patterns/templates/integration-design-template.md`: 統合パターン選択と設計ドキュメントテンプレート
  - `.claude/skills/integration-patterns/templates/message-schema-template.json`: イベント/メッセージスキーマ定義テンプレート

  使用タイミング:
  - MCPサーバーと外部システムの連携設計時
  - 非同期処理パターンの設計時
  - イベント駆動統合の設計時
  - マルチサービス連携の設計時

version: 1.0.1
tags: [mcp, integration, async, event-driven, synchronization]
related_skills:
  - .claude/skills/mcp-protocol/SKILL.md
  - .claude/skills/api-connector-design/SKILL.md
  - .claude/skills/resource-oriented-api/SKILL.md
---

# Integration Patterns スキル

## 概要

MCP サーバーと外部システム間の統合パターンを提供します。同期・非同期通信、イベント駆動アーキテクチャ、データ同期など、様々な統合シナリオに対応した設計パターンを網羅します。

## 統合アーキテクチャ概要

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP クライアント                       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                    MCP プロトコル (JSON-RPC)
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                      MCP サーバー                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Tools     │  │  Resources  │  │   Prompts   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                    統合レイヤー                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ 同期通信   │  │ 非同期通信  │  │ イベント   │            │
│  │ (REST等)   │  │ (Queue等)  │  │ (Webhook等)│            │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘            │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                    外部システム                             │
│     REST API    |    Message Queue    |    Webhooks         │
│     Database    |    File System      |    Cloud Services   │
└─────────────────────────────────────────────────────────────┘
```

## 1. 同期統合パターン

### Request-Response

```
クライアント → MCPサーバー → 外部API → レスポンス → クライアント

特徴:
- シンプルで直感的
- 即座に結果を取得
- 外部APIの遅延が全体に影響

用途:
- 単純なデータ取得
- CRUD操作
- リアルタイム要件が低い操作
```

### Aggregator

```
                    ┌──► API A ──┐
クライアント → MCP ─┼──► API B ──┼──► 集約 → クライアント
                    └──► API C ──┘

特徴:
- 複数ソースからのデータ統合
- 並列実行で効率化
- 単一レスポンスに集約

用途:
- ダッシュボードデータ
- 複合検索
- レポート生成
```

### Gateway

```
クライアント → MCP Gateway → ルーティング → 適切なサービス

特徴:
- 単一エントリーポイント
- 認証・認可の一元化
- プロトコル変換

用途:
- マイクロサービス統合
- レガシーシステムラッピング
- APIバージョン管理
```

## 2. 非同期統合パターン

### Message Queue

```
プロデューサー → キュー → コンシューマー

┌─────────┐     ┌─────────┐     ┌─────────┐
│ MCP     │ ──► │  Queue  │ ──► │ Worker  │
│ Server  │     │ (Redis/ │     │ Process │
└─────────┘     │ RabbitMQ)     └─────────┘
                └─────────┘

特徴:
- 疎結合
- スケーラビリティ
- 信頼性（再試行可能）

用途:
- 長時間実行タスク
- バッチ処理
- 負荷分散
```

### Pub/Sub

```
パブリッシャー → トピック → 複数サブスクライバー

┌─────────┐     ┌─────────┐     ┌─────────┐
│ MCP     │ ──► │  Topic  │ ──► │ Service │
│ Server  │     │         │ ──► │ Service │
└─────────┘     └─────────┘ ──► │ Service │
                                └─────────┘

特徴:
- 1対多の通信
- 動的なサブスクリプション
- イベントブロードキャスト

用途:
- リアルタイム通知
- ログ/監査
- システム間同期
```

### Saga Pattern

```
トランザクション全体を補償可能なステップに分割

Step 1 → Step 2 → Step 3 → 完了
    ↓ 失敗     ↓ 失敗     ↓ 失敗
Compensate ← Compensate ← Compensate

特徴:
- 分散トランザクション
- 各ステップが独立
- 補償アクションで整合性維持

用途:
- オーダー処理
- 予約システム
- 複数サービス連携
```

## 3. イベント駆動パターン

### Event Sourcing

```
イベント1 → イベント2 → イベント3 → 現在の状態

すべての状態変更をイベントとして保存

特徴:
- 完全な監査証跡
- 時間旅行（状態復元）
- デバッグ容易性

用途:
- 金融システム
- コンプライアンス要件
- 複雑なビジネスロジック
```

### CQRS (Command Query Responsibility Segregation)

```
┌─────────────────┐
│    Commands     │ ──► Write Model ──► Event Store
└─────────────────┘
┌─────────────────┐
│     Queries     │ ──► Read Model  ──► 最適化されたビュー
└─────────────────┘

特徴:
- 読み書きの最適化
- スケーラビリティ
- 複雑さの分離

用途:
- 高負荷システム
- 複雑なクエリ要件
- イベントソーシングとの組み合わせ
```

### Webhook

```
外部イベント → Webhook → MCP サーバー → 処理

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  External   │ ──► │  Webhook    │ ──► │    MCP      │
│  Service    │     │  Endpoint   │     │   Server    │
└─────────────┘     └─────────────┘     └─────────────┘

特徴:
- プッシュ型通知
- リアルタイム
- ポーリング不要

用途:
- GitHub イベント
- 支払い完了通知
- サードパーティ統合
```

## 4. データ同期パターン

### Change Data Capture (CDC)

```
データベース変更 → キャプチャ → 伝播

┌─────────┐     ┌─────────┐     ┌─────────┐
│   DB    │ ──► │   CDC   │ ──► │ Target  │
│ Source  │     │ (Debezium)    │ System  │
└─────────┘     └─────────┘     └─────────┘

特徴:
- リアルタイム同期
- 低オーバーヘッド
- 完全性保証

用途:
- データレプリケーション
- キャッシュ無効化
- 検索インデックス更新
```

### Two-Phase Commit

```
Phase 1: Prepare
  Coordinator → 全参加者に準備要求
  参加者 → 準備完了または拒否

Phase 2: Commit/Rollback
  Coordinator → 全員準備完了なら Commit
            → 1つでも失敗なら Rollback

特徴:
- 強い一貫性
- 分散トランザクション
- ブロッキング

用途:
- 銀行振込
- 在庫管理
- 厳密な整合性要件
```

### Eventual Consistency

```
更新 → 伝播（非同期）→ 最終的に一貫

特徴:
- 高可用性
- パーティション耐性
- 一時的な不整合を許容

用途:
- SNSフィード
- 分散キャッシュ
- グローバルシステム
```

## 5. 統合パターン選択ガイド

### 要件別推奨パターン

| 要件               | 推奨パターン               |
| ------------------ | -------------------------- |
| 即時レスポンス必要 | Request-Response           |
| 長時間処理         | Message Queue + Async      |
| 複数サービス連携   | Aggregator / Saga          |
| リアルタイム通知   | Pub/Sub / Webhook          |
| 監査要件           | Event Sourcing             |
| 高スケーラビリティ | CQRS                       |
| データ同期         | CDC / Eventual Consistency |

### 判断フローチャート

```
同期が必要？
├── Yes → レスポンス時間 < 3秒？
│         ├── Yes → Request-Response
│         └── No  → Polling / Long-polling
└── No  → 順序保証必要？
          ├── Yes → Message Queue (FIFO)
          └── No  → Pub/Sub
```

## 6. 実装チェックリスト

### 同期統合

- [ ] タイムアウト設定は適切？
- [ ] リトライロジックは実装？
- [ ] サーキットブレーカーは導入？
- [ ] エラーハンドリングは網羅？

### 非同期統合

- [ ] メッセージの永続化？
- [ ] 重複処理対策（冪等性）？
- [ ] Dead Letter Queue？
- [ ] 監視・アラート設定？

### イベント駆動

- [ ] イベントスキーマはバージョン管理？
- [ ] 順序保証は必要？実装済み？
- [ ] イベント再生機能？
- [ ] 失敗イベントのリカバリー？

## リソース参照

詳細なパターンとガイドについては以下を参照:

- **同期統合パターン詳細**: `cat .claude/skills/integration-patterns/resources/sync-patterns.md`
- **非同期統合パターン詳細**: `cat .claude/skills/integration-patterns/resources/async-patterns.md`
- **イベント駆動設計ガイド**: `cat .claude/skills/integration-patterns/resources/event-driven-guide.md`

## テンプレート参照

- **統合設計テンプレート**: `cat .claude/skills/integration-patterns/templates/integration-design-template.md`
- **メッセージスキーマテンプレート**: `cat .claude/skills/integration-patterns/templates/message-schema-template.json`

## スクリプト実行

```bash
# 統合設計のレビュー
node .claude/skills/integration-patterns/scripts/review-integration-design.mjs <design.md>

# メッセージスキーマ検証
node .claude/skills/integration-patterns/scripts/validate-message-schema.mjs <schema.json>
```

## 関連スキル

| スキル                                          | 用途               |
| ----------------------------------------------- | ------------------ |
| `.claude/skills/mcp-protocol/SKILL.md`          | MCP プロトコル基盤 |
| `.claude/skills/api-connector-design/SKILL.md`  | API 設計パターン   |
| `.claude/skills/resource-oriented-api/SKILL.md` | リソース設計       |
