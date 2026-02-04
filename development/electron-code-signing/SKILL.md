---
name: electron-code-signing
description: |
  Electron code signing and notarization workflow for macOS, Windows, and Linux distribution.

  Anchors:
  • electron-builder documentation / 適用: Code signing configuration / 目的: Proper certificate management and platform-specific signing
  • Apple Developer Program / 適用: macOS signing and notarization / 目的: App Store and Gatekeeper compliance
  • Windows Authenticode / 適用: Windows EV/OV certificate signing / 目的: SmartScreen bypass and user trust

  Trigger:
  Use when configuring code signing for Electron apps, setting up certificates for macOS/Windows/Linux, implementing notarization workflows, resolving signing errors, or distributing signed executables.
  Keywords: code signing, electron-builder, notarization, certificate, macOS signing, Windows Authenticode, entitlements, hardened runtime, EV certificate
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Electron Code Signing

## 概要

Electronアプリケーションの配布には、各プラットフォームでの適切なコード署名が必須です。このスキルは、macOS（公証含む）、Windows（Authenticode）、Linuxのコード署名ワークフローを提供します。

## ワークフロー

### Phase 1: Certificate Setup

**目的**: 証明書の取得、インストール、検証

**アクション**:

1. プラットフォームに応じた証明書を取得
2. キーチェーン/証明書ストアにインストール
3. 環境変数を設定

**Task**: `agents/certificate-setup.md` を参照

### Phase 2: Configuration

**目的**: electron-builderの署名設定を構成

**アクション**:

1. electron-builder.ymlに署名設定を追加
2. エンタイトルメント（macOS）を構成
3. CI/CD環境変数を設定

**Task**: `agents/signing-configuration.md` を参照

**リソース**: `references/macos-signing-guide.md`, `references/windows-signing-guide.md`

### Phase 3: Signing & Notarization

**目的**: 実際の署名と公証プロセスを実行

**アクション**:

1. アプリケーションをビルド
2. 署名を実行
3. 公証を申請（macOS）

**Task**: `agents/signing-execution.md` を参照

### Phase 4: Verification

**目的**: 署名とセキュリティ設定を検証

**アクション**:

1. 署名の有効性を確認
2. Gatekeeper/SmartScreenテストを実行
3. 問題を報告・修正

**Task**: `agents/signing-verification.md` を参照

## Task仕様ナビ

| Task              | エージェント             | 入力                       | 出力                   |
| ----------------- | ------------------------ | -------------------------- | ---------------------- |
| Certificate Setup | certificate-setup.md     | プラットフォーム、証明書種 | 証明書インストール確認 |
| Configuration     | signing-configuration.md | プロジェクト構成、証明書   | electron-builder設定   |
| Signing Execution | signing-execution.md     | ビルド済みアプリ           | 署名済みバイナリ       |
| Verification      | signing-verification.md  | 署名済みバイナリ           | 検証レポート           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                        | 理由                   |
| ------------------------------- | ---------------------- |
| 本番証明書は環境変数で管理      | セキュリティ確保       |
| CI/CDで暗号化シークレット使用   | 証明書の安全な管理     |
| 署名前にローカルでテスト        | 問題の早期発見         |
| macOSではHardened Runtime有効化 | 公証に必須             |
| 公証完了後にstaple実行          | オフライン検証サポート |
| 各プラットフォームで署名検証    | 配布前の品質確認       |

### 避けるべきこと

| 禁止事項                     | 問題点                     |
| ---------------------------- | -------------------------- |
| 証明書をリポジトリにコミット | セキュリティリスク         |
| 開発証明書で本番配布         | 信頼性の問題               |
| 公証なしでmacOSアプリ配布    | Gatekeeperにブロックされる |
| Windowsで署名なし配布        | SmartScreen警告            |
| エンタイトルメントの過剰権限 | セキュリティリスク         |

## リソース参照

### scripts/（決定論的処理）

| スクリプト           | 機能               |
| -------------------- | ------------------ |
| `log_usage.mjs`      | フィードバック記録 |
| `validate-skill.mjs` | スキル構造の検証   |

### references/（詳細知識）

| リソース    | パス                                  | 読込条件      |
| ----------- | ------------------------------------- | ------------- |
| macOS署名   | `references/macos-signing-guide.md`   | macOS署名時   |
| Windows署名 | `references/windows-signing-guide.md` | Windows署名時 |
| Linux署名   | `references/linux-signing-guide.md`   | Linux署名時   |

### assets/（テンプレート）

| アセット                       | 用途                    |
| ------------------------------ | ----------------------- |
| `entitlements.plist`           | macOSエンタイトルメント |
| `electron-builder-signing.yml` | 署名設定テンプレート    |

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様準拠版に再構築 |
| 1.0.0   | 2025-12-31 | 初版作成                       |
