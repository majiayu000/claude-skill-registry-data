---
name: nodejs-stream-processing
description: |
  Node.jsにおけるストリーム処理とバックプレッシャー管理の専門知識。
  大容量ファイルの効率的処理、メモリ使用量の最適化、
  Readable/Writable/Transform/Duplexストリームの適切な活用方法を提供。

  Anchors:
  • Node.js Streams API Documentation / 適用: ストリームAPI全般 / 目的: 公式APIの正確な使用
  • Backpressuring in Streams (Node.js official) / 適用: バックプレッシャー管理 / 目的: メモリ効率最適化
  • The Pragmatic Programmer (Hunt and Thomas) / 適用: 実装品質 / 目的: 保守性とテスタビリティ

  Trigger:
  Use when implementing stream processing in Node.js, handling large files, managing backpressure, or building data transformation pipelines.
  nodejs stream, stream processing, backpressure, readable stream, writable stream, transform stream, duplex stream, pipeline, large file
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Node.js Stream Processing

## 概要

Node.jsにおけるストリーム処理とバックプレッシャー管理の専門知識を提供する。
大容量ファイル（>10MB）の効率的処理、メモリ使用量の一定維持、データ変換パイプラインの構築を支援。

## ワークフロー

### Phase 1: 要件分析

**目的**: ストリーム処理の要件を明確化し、適切なストリームタイプを選定

**アクション**:

1. データソースとシンクを特定（ファイル、ネットワーク、メモリ等）
2. データフロー方向を決定（読み取り専用、書き込み専用、双方向）
3. 変換処理の有無を確認
4. バックプレッシャー要件を評価
5. エラーハンドリング戦略を決定

**Task**: `agents/analyze-stream-requirements.md` を参照

### Phase 2: 実装

**目的**: ストリームパイプラインの実装

**アクション**:

1. 適切なストリームタイプを選択
2. `pipeline()` を使用した安全なチェーン構築
3. エラーハンドリングの実装
4. バックプレッシャー対応の確認
5. リソースクリーンアップの実装

**Task**: `agents/implement-stream-pipeline.md` を参照

### Phase 3: 検証

**目的**: 実装の品質と性能を検証

**アクション**:

1. メモリ使用量の監視
2. バックプレッシャー動作の確認
3. エラーケースのテスト
4. 大容量データでの負荷テスト
5. `scripts/log_usage.mjs` で記録

## Task仕様（ナビゲーション）

| Task                        | 起動タイミング | 入力             | 出力                 |
| --------------------------- | -------------- | ---------------- | -------------------- |
| analyze-stream-requirements | Phase 1開始時  | データフロー要件 | ストリームタイプ選定 |
| implement-stream-pipeline   | Phase 2開始時  | ストリームタイプ | パイプライン実装     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- `pipeline()` を使用してストリームをチェーンする（エラー伝播とクリーンアップ自動化）
- `highWaterMark` を適切に設定してメモリ使用量を制御
- 必ずエラーイベントをハンドリング
- `destroy()` でリソースを明示的にクリーンアップ
- Transform ストリームで `async` ジェネレータを活用

### 避けるべきこと

- `pipe()` の直接使用（エラーハンドリングが困難）
- 同期的な大容量データ読み込み
- `pause()`/`resume()` の手動管理（バグの温床）
- エラーイベントの無視
- `_read()`/`_write()` 内での例外スロー

## リソース参照

### references/（詳細知識）

| リソース           | パス                                                                     | 用途                       |
| ------------------ | ------------------------------------------------------------------------ | -------------------------- |
| 基礎知識           | See [references/basics.md](references/basics.md)                         | ストリーム基本概念         |
| パターン集         | See [references/patterns.md](references/patterns.md)                     | 実装パターンとユースケース |
| バックプレッシャー | See [references/backpressure-guide.md](references/backpressure-guide.md) | メモリ効率の最適化         |

### scripts/（決定論的処理）

| スクリプト      | 用途               | 使用例                                                          |
| --------------- | ------------------ | --------------------------------------------------------------- |
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート      | 用途                                                 |
| ----------------- | ---------------------------------------------------- |
| `stream-utils.ts` | Readable/Writable/Transform/Duplexの実装テンプレート |

## 変更履歴

| Version | Date       | Changes                    |
| ------- | ---------- | -------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠 |
| 1.0.0   | 2025-12-24 | 初期バージョン             |
