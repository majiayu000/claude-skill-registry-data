---
name: electron-distribution
description: |
  Electronアプリケーションの配布・自動更新に関する専門知識を提供するスキル。
  electron-builder/electron-updaterによるビルド・署名・更新配信、CI/CDリリースフロー、
  各種アプリストア（MAS/Microsoft Store/Snapcraft）への配布を支援する。

  Anchors:
  • electron-builder / 適用: ビルド・署名・パッケージング / 目的: 配布可能なアプリ作成
  • electron-updater / 適用: 自動更新機能 / 目的: セキュアな更新配信
  • Semantic Versioning / 適用: バージョン管理 / 目的: 一貫したリリース戦略

  Trigger:
  Use when implementing auto-update features, configuring release workflows, distributing to app stores, or setting up update servers for Electron applications.
  electron-updater, auto-update, app store, code signing, release workflow, MAS, Microsoft Store
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron Distribution

## 概要

Electronアプリケーションの配布・自動更新に関する専門知識を提供するスキル。
electron-builder/electron-updaterによるビルド・署名・更新配信、CI/CDリリースフロー、各種アプリストアへの配布を支援する。

## ワークフロー

### Phase 1: 配布戦略の決定

**目的**: 配布方式とターゲットプラットフォームを決定

**アクション**:

1. 配布対象プラットフォーム（macOS/Windows/Linux）を特定
2. 配布方式を選択（直接配布/アプリストア/両方）
3. 自動更新要件を確認
4. コード署名要件を整理

### Phase 2: 実装

**目的**: 選択した方式に応じた実装

**アクション**:

1. 目的に応じたTask仕様書を参照
2. electron-builder設定を作成
3. CI/CDワークフローを構築
4. テスト環境で動作確認

**Task参照**: `agents/` 配下の対応Task仕様書を参照

### Phase 3: 検証とリリース

**目的**: 品質確認とリリース実行

**アクション**:

1. `scripts/validate-config.mjs` で設定検証
2. ステージング環境でのテスト
3. リリース実行
4. `scripts/log_usage.mjs` でフィードバック記録

## Task仕様ナビ

| Task                   | 起動タイミング       | 入力             | 出力                  |
| ---------------------- | -------------------- | ---------------- | --------------------- |
| setup-auto-update      | 自動更新機能実装時   | プロジェクト構成 | autoUpdater実装コード |
| configure-release-flow | リリースフロー構築時 | 要件定義         | CI/CDワークフロー     |
| distribute-to-stores   | アプリストア配布時   | ビルド成果物     | ストア提出パッケージ  |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **コード署名**: すべてのプラットフォームでコード署名を実施
- **自動更新テスト**: ステージング環境で更新フローを検証
- **ロールバック計画**: 問題発生時の前バージョン復帰手順を用意
- **Semantic Versioning**: 一貫したバージョン管理戦略を維持
- **差分更新**: 可能な限り差分更新（delta update）を使用

### 避けるべきこと

- **署名なしリリース**: コード署名を省略してリリースしない
- **強制更新**: ユーザーの同意なく更新を強制しない
- **バージョン重複**: 同一バージョン番号で異なるビルドをリリースしない
- **テスト不足**: ステージング環境での検証なしにリリースしない

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                                 | 用途                        |
| -------------------- | ------------------------------------------------------------------------------------ | --------------------------- |
| 自動更新ガイド       | See [references/auto-update.md](references/auto-update.md)                           | electron-updater詳細        |
| リリースワークフロー | See [references/release-workflow-guide.md](references/release-workflow-guide.md)     | CI/CD・署名・バージョン管理 |
| ストア配布ガイド     | See [references/store-distribution-guide.md](references/store-distribution-guide.md) | MAS/MS Store/Snap配布       |

### scripts/（決定論的処理）

| スクリプト            | 用途                     | 使用例                                                          |
| --------------------- | ------------------------ | --------------------------------------------------------------- |
| `validate-config.mjs` | electron-builder設定検証 | `node scripts/validate-config.mjs --config package.json`        |
| `log_usage.mjs`       | フィードバック記録       | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート       | 用途                         |
| ------------------ | ---------------------------- |
| `update-server.ts` | 更新サーバー実装テンプレート |

## 変更履歴

| Version | Date       | Changes                                    |
| ------- | ---------- | ------------------------------------------ |
| 3.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、references再構成 |
| 2.0.0   | 2025-12-31 | Task仕様ナビテーブル追加、日本語Trigger    |
| 1.0.0   | 2025-12-24 | 初版作成                                   |
