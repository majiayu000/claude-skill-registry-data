---
name: electron-auto-updater
description: |
  Electron自動更新機能の実装とデプロイメント専門スキル。electron-updaterライブラリを使用した安全で信頼性の高い自動更新システムの構築を支援します。

  Anchors:
  • electron-updater library / 適用: 自動更新実装全般 / 目的: セキュアな更新配信と署名検証
  • electron-builder / 適用: ビルドと署名設定 / 目的: プラットフォーム固有のパッケージング
  • Code Signing Guide / 適用: 証明書管理 / 目的: macOS/Windows署名の信頼性確保

  Trigger:
  Use when implementing auto-update functionality, configuring electron-updater, setting up update servers, managing code signing certificates, or deploying staged rollouts.
  Keywords: electron-updater, auto-update, autoUpdater, update server, code signing, certificate, staged rollout, differential update, NSIS, Squirrel
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
tags:
  - electron
  - auto-update
  - deployment
  - security
  - ci-cd
---

# Electron Auto-Updater

## 概要

Electron自動更新機能の実装とデプロイメントに特化したスキル。electron-updaterライブラリを活用し、セキュアで効率的な自動更新システムを構築します。

## ワークフロー

### Phase 1: 要件定義と設計

**目的**: 自動更新の要件を明確化し、アーキテクチャを設計する

**アクション**:

1. 更新ポリシーを分析（強制/任意、頻度）
2. ターゲットプラットフォームを特定
3. セキュリティ要件をリストアップ

**Task**: `agents/architect.md` を参照

### Phase 2: 基本実装

**目的**: electron-updaterの基本セットアップとメインプロセス統合

**アクション**:

1. electron-updaterをインストール
2. メインプロセスに更新ロジックを実装
3. IPC経由でRendererに通知

**Task**: `agents/implementer.md` を参照

**リソース**: `references/update-implementation.md`

### Phase 3: 署名とセキュリティ設定

**目的**: コード署名と証明書管理の実装

**アクション**:

1. プラットフォーム固有の証明書を設定
2. CI/CDに署名シークレットを構成
3. 署名検証を実装

**Task**: `agents/security-engineer.md` を参照

### Phase 4: 更新サーバー構築

**目的**: 更新配信インフラの構築とデプロイ

**アクション**:

1. 配信方法を選択（GitHub Releases/S3/カスタム）
2. electron-builder設定を更新
3. 段階的ロールアウトを設計

**Task**: `agents/devops-engineer.md` を参照

**リソース**: `references/update-server.md`

### Phase 5: テストと検証

**目的**: 自動更新機能の包括的なテスト

**アクション**:

1. 各プラットフォームで更新フローをテスト
2. エラーケースを検証
3. ロールバックシナリオを確認

**Task**: `agents/qa-engineer.md` を参照

### Phase 6: デプロイとモニタリング

**目的**: 段階的ロールアウトと監視体制の確立

**アクション**:

1. 段階的ロールアウトを実行
2. 更新メトリクスを収集
3. インシデント対応手順を整備

**Task**: `agents/release-manager.md` を参照

## Task仕様ナビ

| Task               | エージェント         | 入力                               | 出力                     |
| ------------------ | -------------------- | ---------------------------------- | ------------------------ |
| 要件定義・設計     | architect.md         | 更新ポリシー、プラットフォーム要件 | 設計書、セキュリティ要件 |
| 基本実装           | implementer.md       | 設計書、既存コード                 | 更新ロジック、UIコード   |
| 署名・セキュリティ | security-engineer.md | 証明書、署名要件                   | 署名設定、チェックリスト |
| サーバー構築       | devops-engineer.md   | 配信方法、バージョン戦略           | サーバー設定、デプロイ   |
| テスト             | qa-engineer.md       | 実装コード、テストシナリオ         | テストレポート           |
| デプロイ           | release-manager.md   | 検証済みパッケージ                 | デプロイレポート         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項               | 理由                               |
| ---------------------- | ---------------------------------- |
| HTTPS経由での配信      | 中間者攻撃の防止                   |
| 段階的ロールアウト     | 問題の早期発見と影響範囲の最小化   |
| 差分更新の活用         | 帯域幅とダウンロード時間の削減     |
| ロールバック計画の策定 | 問題発生時の迅速な復旧             |
| 署名検証の徹底         | 改ざん検知とセキュリティ確保       |
| 詳細なエラーログ       | トラブルシューティングの効率化     |
| ユーザー通知           | 更新の透明性確保とユーザー体験向上 |

### 避けるべきこと

| 禁止事項                   | 問題点                           |
| -------------------------- | -------------------------------- |
| 強制的な即時更新           | ユーザーの作業中断による体験悪化 |
| 署名なし配信               | セキュリティリスク               |
| 本番前のテスト不足         | 重大な問題のリリース             |
| バージョン番号の重複       | キャッシュ問題と混乱             |
| HTTPでの配信               | 中間者攻撃のリスク               |
| 秘密鍵のリポジトリコミット | 証明書の漏洩                     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト           | 機能               |
| -------------------- | ------------------ |
| `log_usage.mjs`      | フィードバック記録 |
| `validate-skill.mjs` | スキル構造の検証   |

### references/（詳細知識）

| リソース   | パス                                  | 読込条件       |
| ---------- | ------------------------------------- | -------------- |
| 実装ガイド | `references/update-implementation.md` | 基本実装時     |
| サーバー   | `references/update-server.md`         | サーバー構築時 |

### assets/（テンプレート）

| アセット             | 用途                          |
| -------------------- | ----------------------------- |
| `updater-main.ts`    | Mainプロセステンプレート      |
| `updater-preload.ts` | Preloadスクリプトテンプレート |

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様準拠版に再構築 |
| 1.0.0   | 2025-12-31 | 初版作成                       |
