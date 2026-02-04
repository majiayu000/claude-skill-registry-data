---
name: electron-ui-patterns
description: |
  ElectronデスクトップアプリケーションのUI実装パターンと設計知識。
  BrowserWindow管理、ネイティブUI要素、フレームレスウィンドウを提供。

  Anchors:
  • Electron API / 適用: BrowserWindow・Menu・Tray / 目的: ネイティブUI実装
  • Don't Make Me Think / 適用: ウィンドウレイアウト / 目的: ユーザビリティ向上
  • Electron Security / 適用: preload・contextIsolation / 目的: セキュアなUI実装

  Trigger:
  Use when configuring BrowserWindow, implementing custom titlebars, designing native menus, developing system tray apps, or building frameless windows.
  BrowserWindow, Menu, Tray, frameless window, custom titlebar, native UI
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron UI Patterns

## 概要

ElectronデスクトップアプリケーションのUI実装パターンと設計知識を提供。
BrowserWindow管理、ネイティブUI要素の活用、フレームレスウィンドウの実装を支援する。

## ワークフロー

### Phase 1: UI要件の整理

**目的**: 実装対象のUI要素を特定

**アクション**:

1. 実装対象を特定（BrowserWindow、メニュー、ダイアログ）
2. `references/` で対応するパターンを確認
3. プロジェクト要件に合致するパターンを選定

### Phase 2: UI実装

**目的**: UIパターンに従って実装

**アクション**:

1. 該当する`agents/`のTask仕様書を参照
2. `assets/frameless-window.ts` などテンプレートを活用
3. BrowserWindow設定、スタイリング、イベントハンドリングを実装
4. ネイティブUI要素（メニュー、ダイアログ、トレイ）を統合

### Phase 3: 検証と記録

**目的**: 動作検証と記録

**アクション**:

1. ウィンドウ表示、メニュー動作をテスト
2. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                | 起動タイミング             | 入力             | 出力                  |
| ------------------- | -------------------------- | ---------------- | --------------------- |
| browserwindow-setup | BrowserWindow設定時        | プロジェクト要件 | 初期化コード・preload |
| custom-titlebar     | カスタムタイトルバー実装時 | デザイン仕様     | フレームレス設定・CSS |
| native-menu         | ネイティブメニュー実装時   | 機能要件         | メニュー構築コード    |
| system-tray         | システムトレイ設定時       | アイコン画像     | Tray設定コード        |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **コンテキスト分離**: preload.jsでコンテキストを分離
- **BrowserWindow最小化**: 必要最小限の機能のみ有効化
- **IPC通信**: メインとレンダラーの分離
- **ネイティブUI活用**: プラットフォーム固有のMenu/Dialog/Tray
- **状態永続化**: ウィンドウ位置・サイズを保存

### 避けるべきこと

- **nodeIntegration有効化**: セキュリティリスク
- **enableRemoteModule使用**: 直接APIアクセスは避ける
- **synchronous IPC**: 非同期通信を使用
- **プラットフォーム差異無視**: Windows/macOS/Linuxの違いを考慮

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                   | 用途                 |
| -------------- | ---------------------------------------------------------------------- | -------------------- |
| ネイティブUI   | See [references/native-ui.md](references/native-ui.md)                 | メニュー・ダイアログ |
| ウィンドウ管理 | See [references/window-management.md](references/window-management.md) | BrowserWindow詳細    |

### scripts/（決定論的処理）

| スクリプト      | 用途               | 使用例                                                          |
| --------------- | ------------------ | --------------------------------------------------------------- |
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート          | 用途                               |
| --------------------- | ---------------------------------- |
| `frameless-window.ts` | フレームレスウィンドウテンプレート |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、構造最適化 |
| 1.0.0   | 2025-12-31 | 初版作成                             |
