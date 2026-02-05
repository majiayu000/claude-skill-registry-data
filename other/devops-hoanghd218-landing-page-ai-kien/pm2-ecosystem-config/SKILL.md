---
name: pm2-ecosystem-config
description: |
  PM2エコシステム設定の専門スキル。
  Node.jsプロセス管理のためのecosystem.config.js設計、実行モード選択、環境変数管理、パフォーマンス最適化を提供します。

  Anchors:
  • PM2 Documentation (Keymetrics) / 適用: プロセス管理設定 / 目的: 運用自動化
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: DRY原則・保守性 / 目的: 品質向上
  • Node.js Design Patterns (Mario Casciaro, Luciano Mammino) / 適用: スケーリング戦略 / 目的: パフォーマンス最適化

  Trigger:
  Use when configuring PM2 ecosystem.config.js, deploying Node.js applications with PM2, optimizing PM2 cluster mode, managing PM2 environment variables, or troubleshooting PM2 process issues
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# PM2 Ecosystem Configuration スキル

## 概要

PM2エコシステム設定の設計と最適化を専門とするスキル。ecosystem.config.jsの構成、実行モード選択、環境設定、監視設定を体系的に設計し、Node.jsアプリケーションのプロセス管理を最適化します。

このスキルは以下のタスクに対応します：

- ecosystem.config.jsの新規作成と既存設定の最適化
- forkモードとclusterモードの選択と実装
- 環境変数管理と本番環境構築
- プロセス監視とエラーハンドリング設定
- パフォーマンスチューニングとリソース最適化

## ワークフロー

### Phase 1: 要件確認と初期設計

**目的**: アプリケーション特性を分析し、PM2設定の方針を決定

**アクション**:

1. `references/basics.md`でPM2の基本を確認
2. アプリケーション種別（Web API、バッチ、WebSocket等）を特定
3. 負荷特性（I/O bound、CPU bound）を判断
4. 実行モード（fork/cluster）の初期選択

**Task**: `agents/design-config.md`を参照

### Phase 2: 設定ファイル作成

**目的**: ecosystem.config.jsを作成し、基本設定を実装

**アクション**:

1. `assets/ecosystem.config.template.js`をベースに作成
2. `references/config-reference.md`で設定オプションを確認
3. 必須項目（name、script、instances）を設定
4. ログ設定と再起動戦略を実装
5. `scripts/validate-ecosystem.mjs`で検証

**Task**: `agents/design-config.md`を参照

### Phase 3: 最適化と調整

**目的**: パフォーマンスを最適化し、運用要件を満たす

**アクション**:

1. `references/patterns.md`で最適化パターンを確認
2. instances数の調整とクラスタモード最適化
3. メモリ制限と再起動戦略の調整
4. 環境変数の階層設計と機密情報の外部化
5. 負荷テストと監視設定の検証

**Task**: `agents/optimize-performance.md`を参照

## ベストプラクティス

### すべきこと

- PM2でNode.jsアプリケーションを管理する時
- ecosystem.config.jsを新規作成する時
- 既存PM2設定を最適化する時
- 本番環境でのプロセス管理設定を設計する時
- クラスタモードでパフォーマンスを向上させる時

### 避けるべきこと

- 実行モードを検討せずにデフォルト設定を使用する
- CPU数を超えるinstances数を設定する
- 本番環境でwatchモードを有効にする
- 機密情報を設定ファイルに直接記述する
- メモリリーク対策（max_memory_restart）を設定しない

## Task仕様ナビ

| Task                 | 起動タイミング | 入力                         | 出力                |
| -------------------- | -------------- | ---------------------------- | ------------------- |
| design-config        | Phase 1-2      | アプリケーション情報         | ecosystem.config.js |
| optimize-performance | Phase 3        | 既存設定、パフォーマンス要件 | 最適化済み設定      |

**詳細仕様**: 各Taskの詳細は`agents/`ディレクトリの対応ファイルを参照

## リソース参照

### references/（詳細知識）

| リソース         | パス                             | 内容                                       |
| ---------------- | -------------------------------- | ------------------------------------------ |
| 基礎知識         | `references/basics.md`           | PM2基本、ecosystem.config.js構造、基本操作 |
| 設定パターン     | `references/patterns.md`         | 実行モード選択、環境変数、再起動戦略       |
| 設定リファレンス | `references/config-reference.md` | 全オプションの完全リファレンス             |

### scripts/（決定論的処理）

| スクリプト               | 用途                    | 使用例                                                          |
| ------------------------ | ----------------------- | --------------------------------------------------------------- |
| `validate-ecosystem.mjs` | ecosystem.config.js検証 | `node scripts/validate-ecosystem.mjs ecosystem.config.js`       |
| `log_usage.mjs`          | スキル使用記録          | `node scripts/log_usage.mjs --result success --phase "Phase 2"` |

### assets/（テンプレート）

| テンプレート                   | 用途                    |
| ------------------------------ | ----------------------- |
| `ecosystem.config.template.js` | ecosystem.config.js雛形 |

## 変更履歴

| Version | Date       | Changes                                              |
| ------- | ---------- | ---------------------------------------------------- |
| 2.0.0   | 2025-01-02 | 18-skills.md仕様完全準拠。agents統合、references再編 |
| 1.0.0   | 2025-12-31 | 初版リリース                                         |
