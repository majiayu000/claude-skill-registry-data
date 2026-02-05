---
name: electron-security-hardening
description: |
  Electronデスクトップアプリケーションのセキュリティ強化専門知識。
  XSS、コードインジェクション、プロセス隔離違反などの脅威から保護。

  Anchors:
  • Electron Security / 適用: プロセス隔離・IPC保護 / 目的: 安全なデスクトップアプリ
  • OWASP / 適用: 脆弱性評価・脅威モデリング / 目的: 継続的なセキュリティ監査
  • Content Security Policy / 適用: CSP実装 / 目的: XSS防御とリソース制限

  Trigger:
  Use when implementing Electron security hardening, configuring CSP, designing secure IPC channels, conducting security audits, managing vulnerabilities, or implementing sandboxing.
  electron security, CSP, IPC protection, context isolation, sandbox, preload
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron Security Hardening

## 概要

Electronデスクトップアプリケーションをセキュリティ脅威から保護するための包括的なスキル。
CSP、IPC通信の保護、プロセス隔離、サンドボックス化、脆弱性管理の実装パターンを提供。

## ワークフロー

### Phase 1: セキュリティ評価

**目的**: 現状のセキュリティ状態を評価

**アクション**:

1. `scripts/security-audit.mjs` でアプリケーションを監査
2. `agents/security-audit.md` に従ってセキュリティ評価
3. 優先順位付きの改善計画を策定

### Phase 2: セキュリティ実装

**目的**: セキュリティ対策を実装

**アクション**:

1. `agents/csp-configuration.md` でCSPを実装
2. `agents/ipc-protection.md` でIPC保護
3. `agents/process-isolation.md` でプロセス隔離
4. `agents/sandboxing.md` でサンドボックス化
5. `agents/vulnerability-management.md` で脆弱性管理

### Phase 3: 検証と記録

**目的**: 実装を検証し記録

**アクション**:

1. CSP違反チェック、IPC動作確認
2. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                     | 起動タイミング     | 入力             | 出力               |
| ------------------------ | ------------------ | ---------------- | ------------------ |
| security-audit           | セキュリティ評価時 | プロジェクトパス | 監査レポート       |
| csp-configuration        | CSP設定時          | 監査レポート     | CSP設定ファイル    |
| ipc-protection           | IPC保護設計時      | アプリ要件       | Preloadスクリプト  |
| process-isolation        | プロセス隔離実装時 | 監査レポート     | BrowserWindow設定  |
| sandboxing               | サンドボックス化時 | 権限要件         | サンドボックス設定 |
| vulnerability-management | 脆弱性管理設定時   | 依存関係情報     | CI/CD設定          |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **最小権限原則**: `nodeIntegration: false`, `contextIsolation: true`
- **厳密なCSP**: `default-src 'none'`から始める
- **IPC検証**: すべてのIPC通信にスキーマ検証
- **脆弱性監視**: 定期的な`pnpm audit`実行
- **サンドボックス**: OS固有のサンドボックス機能を活用

### 避けるべきこと

- **nodeIntegration有効化**: セキュリティリスク
- **検証なしIPC**: ユーザー入力の検証は必須
- **依存関係放置**: セキュリティパッチの無視
- **機密情報ハードコード**: 設定ファイルへの埋め込み

## リソース参照

### references/（詳細知識）

| リソース    | パス                                                                   | 用途               |
| ----------- | ---------------------------------------------------------------------- | ------------------ |
| CSP設定詳細 | See [references/csp-configuration.md](references/csp-configuration.md) | ディレクティブ詳細 |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                                          |
| -------------------- | ------------------ | --------------------------------------------------------------- |
| `security-audit.mjs` | セキュリティ監査   | `node scripts/security-audit.mjs --path ./src`                  |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート        | 用途                          |
| ------------------- | ----------------------------- |
| `secure-preload.ts` | セキュアなPreloadテンプレート |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 3.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、構造最適化 |
| 2.0.0   | 2025-12-31 | Task仕様ナビテーブル追加             |
| 1.0.0   | 2025-12-24 | 初版作成                             |
