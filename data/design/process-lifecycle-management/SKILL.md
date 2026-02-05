---
name: process-lifecycle-management
description: |
  Node.jsプロセスのライフサイクル管理を専門とするスキル。
  Linuxカーネルのプロセス管理思想に基づき、プロセスの生成、実行、
  監視、終了までの完全な制御と、シグナル処理、ゾンビプロセス回避を設計します。

  Anchors:
  • The Pragmatic Programmer（Andrew Hunt, David Thomas）/ 適用: プロセス管理 / 目的: 実践的改善と品質維持

  Trigger:
  process lifecycle management, application startup and shutdown control, graceful shutdown implementation, signal handler design, PM2 process management configuration
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# プロセスライフサイクル管理

## 概要

Node.jsプロセスのライフサイクル管理を専門とするスキル。Linuxカーネルのプロセス管理思想に基づき、プロセスの生成、実行、監視、終了までの完全な制御と、シグナル処理、ゾンビプロセス回避を設計します。

## ワークフロー

### Phase 1: ライフサイクル分析

**目的**: プロセスの要件と状態遷移を分析

**アクション**:

1. アプリケーションの起動・終了要件を特定
2. 管理対象プロセス（親・子）を洗い出し
3. 必要なシグナル処理を決定
4. 状態遷移図を設計

**Task**: `agents/analyze-lifecycle.md` を参照

### Phase 2: シグナルハンドラ実装

**目的**: Graceful Shutdownとシグナル処理を実装

**アクション**:

1. `assets/signal-handler.template.ts` を基にハンドラーを実装
2. SIGTERM、SIGINT、SIGHUPの処理を定義
3. クリーンアップ関数を登録
4. タイムアウト処理を設定

**Task**: `agents/implement-handlers.md` を参照

### Phase 3: シャットダウン検証

**目的**: 実装したシグナルハンドラの動作を検証

**アクション**:

1. `scripts/check-process-health.mjs` で動作確認
2. シグナル送信テストを実施
3. リソースリークを検証
4. PM2との連携を確認

**Task**: `agents/validate-shutdown.md` を参照

## Task仕様ナビ

| Task               | 起動タイミング | 入力                     | 出力                 |
| ------------------ | -------------- | ------------------------ | -------------------- |
| analyze-lifecycle  | Phase 1開始時  | アプリケーション要件情報 | ライフサイクル設計書 |
| implement-handlers | Phase 2開始時  | ライフサイクル設計       | シグナルハンドラ実装 |
| validate-shutdown  | Phase 3開始時  | 実装済みハンドラ         | 検証結果レポート     |

## ベストプラクティス

### すべきこと

- Node.jsプロセスの起動・終了フローを設計する時
- シグナルハンドラーを実装する時
- 子プロセスの管理戦略を決定する時
- PM2でプロセスを管理する設定を行う時
- Graceful Shutdownの実装時にタイムアウトを設定する
- クリーンアップ関数を逆順（後入れ先出し）で実行する

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける
- graceful shutdownの実装なしに本番環境へ展開することを避ける
- シグナルハンドラーなしのプロセス管理を避ける
- 子プロセスの終了確認なしの設計を避ける
- SIGKILLへのハンドラー登録（不可能）を試みることを避ける

## リソース参照

### references/

| リソース           | パス                                   | 用途                           |
| ------------------ | -------------------------------------- | ------------------------------ |
| 基本概念           | `references/basics.md`                 | プロセス管理の基本理論         |
| 実装パターン       | `references/patterns.md`               | パターンのナビゲーション       |
| シグナル処理       | `references/signal-handling.md`        | シグナルハンドリング詳細ガイド |
| プロセス状態       | `references/process-states.md`         | 状態遷移とライフサイクル管理   |
| 子プロセスパターン | `references/child-process-patterns.md` | 子プロセス管理の実装パターン集 |

### scripts/

| スクリプト                 | 用途                   | 使用例                                  |
| -------------------------- | ---------------------- | --------------------------------------- |
| `check-process-health.mjs` | プロセスヘルスチェック | `node scripts/check-process-health.mjs` |
| `validate-skill.mjs`       | スキル構造検証         | `node scripts/validate-skill.mjs`       |
| `log_usage.mjs`            | 使用記録と自動評価     | `node scripts/log_usage.mjs`            |

### assets/

| テンプレート                 | 用途                           |
| ---------------------------- | ------------------------------ |
| `signal-handler.template.ts` | Signal Handler実装テンプレート |

## 変更履歴

| Version | Date       | Changes                                                                                      |
| ------- | ---------- | -------------------------------------------------------------------------------------------- |
| 2.1.0   | 2026-01-02 | 18-skills.md完全準拠: references/構造変更（Level1-4→basics/patterns）、validate-shutdown追加 |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠版に再構築: agents/Task仕様書追加、references統合                        |
| 1.1.0   | 2025-12-31 | Anchors/Trigger追加、Task仕様ナビ（テーブル形式）追加                                        |
| 1.0.0   | 2025-12-24 | 初版作成                                                                                     |
