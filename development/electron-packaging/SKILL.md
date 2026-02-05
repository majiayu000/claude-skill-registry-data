---
name: electron-packaging
description: |
  Electronアプリケーションのビルド・パッケージング・配布を統一的に管理する専門知識。
  electron-builderによるクロスプラットフォーム対応、コード署名、インストーラー生成を支援。

  Anchors:
  • electron-builder / 適用: ビルド設定・パッケージング / 目的: クロスプラットフォーム配布
  • Code Signing / 適用: macOS/Windows署名 / 目的: セキュアな配布
  • The Pragmatic Programmer / 適用: ビルドプロセス設計 / 目的: 繰り返し可能なワークフロー

  Trigger:
  Use when building production Electron applications, generating installers for macOS/Windows/Linux, implementing code signing, or packaging desktop apps for release.
  electron-builder, dmg, exe, AppImage, code signing, packaging
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron Packaging

## 概要

Electronアプリケーションのビルド・パッケージング・配布を一貫して実現する専門知識。
electron-builderによるクロスプラットフォーム対応、デジタル署名、インストーラー生成を支援する。

## ワークフロー

### Phase 1: ビルド設定の準備

**目的**: ターゲットプラットフォームとビルド設定を確認

**アクション**:

1. ターゲットプラットフォーム（macOS/Windows/Linux）を特定
2. `references/build-config-guide.md` でビルド設定を確認
3. `assets/electron-builder.yml` をベースに設定ファイルを作成

### Phase 2: ビルドとパッケージング

**目的**: アプリケーションをビルドしパッケージング

**アクション**:

1. `agents/validate-build-config.md` で設定を検証
2. `agents/execute-build.md` でビルドを実行
3. `scripts/generate-icons.mjs` でアイコンを生成

### Phase 3: コード署名とインストーラー生成

**目的**: 署名済みインストーラーを生成

**アクション**:

1. `agents/apply-code-signing.md` でコード署名
2. `agents/generate-installers.md` でインストーラー生成
3. 成果物の動作確認

### Phase 4: 検証と記録

**目的**: 成果物の検証と記録

**アクション**:

1. 生成されたパッケージの動作確認
2. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                  | 起動タイミング       | 入力              | 出力                |
| --------------------- | -------------------- | ----------------- | ------------------- |
| validate-build-config | ビルド前             | package.json/設定 | 検証結果            |
| execute-build         | ビルド実行時         | ビルド設定        | バイナリファイル    |
| apply-code-signing    | 署名実行時           | 証明書・バイナリ  | 署名済みバイナリ    |
| generate-installers   | インストーラー生成時 | ビルド成果物      | .dmg/.exe/.AppImage |
| configure-auto-update | 自動更新設定時       | サーバー設定      | updater設定         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **ステージング環境テスト**: 本番前に完全なビルド・署名フローを検証
- **CI/CD自動化**: 各プラットフォーム用パイプラインを構築
- **認証情報管理**: 署名用認証情報をセキュアに管理
- **クロスプラットフォーム検証**: 全ターゲットで動作確認
- **段階的リリース**: ロールバック策を備えたリリース戦略

### 避けるべきこと

- **認証情報埋め込み**: コードベースに直接埋め込まない
- **署名なし配布**: セキュリティリスク
- **バージョン重複**: 同一バージョンで異なるビルド
- **本番初テスト**: 設定変更を本番環境で初めてテストしない

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                               | 用途               |
| -------------------- | ---------------------------------------------------------------------------------- | ------------------ |
| ビルド設定ガイド     | See [references/build-config-guide.md](references/build-config-guide.md)           | ビルド設定の詳細   |
| ビルドプロセスガイド | See [references/build-process-guide.md](references/build-process-guide.md)         | ビルドフロー       |
| コード署名           | See [references/code-signing.md](references/code-signing.md)                       | 署名手順           |
| electron-builder設定 | See [references/electron-builder-config.md](references/electron-builder-config.md) | 設定オプション     |
| インストーラー生成   | See [references/installer-generation.md](references/installer-generation.md)       | インストーラー作成 |
| 自動更新ガイド       | See [references/auto-update-guide.md](references/auto-update-guide.md)             | 自動更新設定       |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                                          |
| -------------------- | ------------------ | --------------------------------------------------------------- |
| `generate-icons.mjs` | アイコン生成       | `node scripts/generate-icons.mjs --input icon.png`              |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 4"` |

### assets/（テンプレート）

| テンプレート           | 用途                             |
| ---------------------- | -------------------------------- |
| `electron-builder.yml` | electron-builder設定テンプレート |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、構造最適化 |
| 1.0.0   | 2025-12-31 | 初版作成                             |
