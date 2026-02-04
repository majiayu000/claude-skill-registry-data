---
name: input-validation-security
description: |
  Webアプリケーションにおける包括的な入力検証とサニタイズ。型安全な検証、許可リストフィルタリング、
  コンテキスト対応エンコーディングを通じて、XSS、SQLインジェクション、コマンドインジェクション、
  パストラバーサルなどの入力ベースの攻撃を防止。

  Anchors:
  • OWASP Top 10 / 適用: 全ての入力検証判断 / 目的: 業界標準のセキュリティベースライン
  • CWE-20 (不適切な入力検証) / 適用: 検証戦略設計 / 目的: 一般的な脆弱性パターン防止
  • OWASP ASVS 5.1 / 適用: 検証要件仕様 / 目的: セキュリティ検証標準

  Trigger:
  Use when implementing user input handling, form validation, API request validation, file upload processing,
  database query construction, command execution with user input, URL parameter processing, or any data from untrusted sources.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
---

# 入力検証セキュリティ

## 概要

型安全な検証とコンテキスト対応エンコーディングを通じて、インジェクション攻撃を防止する
多層防御型の入力検証スキル。

主な機能:

- Zodによる型安全な検証
- コンテキスト対応の出力エンコーディング
- 許可リストベースのフィルタリング
- ファイルアップロードセキュリティ
- SQL/XSS/コマンドインジェクション防止

## ワークフロー

### Phase 1: 入力分析

**目的**: すべての入力ベクターをマッピングし、リスクを評価

**アクション**:

1. Task呼び出し: `agents/analyze-inputs.md`
2. 参照: `references/basics.md`
3. 各入力のリスクレベルを分類

**成果物**: リスク分類付き入力インベントリ

### Phase 2: 検証設計

**目的**: 型安全な検証スキーマを設計

**アクション**:

1. Task呼び出し: `agents/design-validation.md`
2. 参照: `references/patterns.md`
3. 許可リストと検証ルールを定義

**成果物**: 検証スキーマ仕様

### Phase 3: 実装

**目的**: 検証コードを実装

**アクション**:

1. Task呼び出し: `agents/implement-validation.md`
2. テンプレート使用: `assets/validation-schema.template.ts`
3. エンコーディング適用: `assets/encoding-helpers.ts`

**成果物**: 本番用検証コード

### Phase 4: セキュリティテスト

**目的**: 攻撃に対する防御を検証

**アクション**:

1. 実行: `node scripts/validate-inputs.mjs --target <path>`
2. Task呼び出し: `agents/security-test.md`
3. 参照: `references/xss-prevention.md`, `references/sql-injection-prevention.md`

**成果物**: セキュリティテストレポート

## Task仕様ナビ

| Taskファイル                     | 使用タイミング | 入力             | 出力             |
| -------------------------------- | -------------- | ---------------- | ---------------- |
| `agents/analyze-inputs.md`       | Phase 1        | コードベース     | 入力インベントリ |
| `agents/design-validation.md`    | Phase 2        | 入力インベントリ | 検証スキーマ     |
| `agents/implement-validation.md` | Phase 3        | スキーマ         | 本番コード       |
| `agents/security-test.md`        | Phase 4        | 実装             | テスト結果       |

## ベストプラクティス

### すべきこと

- 信頼境界で検証する
- セキュアに失敗する（検証失敗時は拒否）
- ブロックリストより許可リストを使用
- 型検証を最初に行う
- 出力コンテキストに応じてエンコード
- 入力長を制限
- 検証失敗をログ記録

### 避けるべきこと

- クライアント側のみの検証に依存
- ブロックリストフィルタリングの使用
- SQL/コマンドの文字列連結
- Referer/Originヘッダーを信頼
- 部分的なエンコーディング
- 複雑な正規表現（ReDoSリスク）
- 使用後に検証

## リソース参照

### 参照資料

| リソース | パス                                                                             | 目的                    |
| -------- | -------------------------------------------------------------------------------- | ----------------------- |
| 基礎     | [references/basics.md](references/basics.md)                                     | 基本概念                |
| パターン | [references/patterns.md](references/patterns.md)                                 | 実装パターン            |
| XSS防止  | [references/xss-prevention.md](references/xss-prevention.md)                     | XSS防御                 |
| SQLi防止 | [references/sql-injection-prevention.md](references/sql-injection-prevention.md) | SQLインジェクション防御 |

### スクリプト

| スクリプト            | 使用方法                                                       | 目的           |
| --------------------- | -------------------------------------------------------------- | -------------- |
| `validate-inputs.mjs` | `node scripts/validate-inputs.mjs --target <path>`             | 脆弱性スキャン |
| `log_usage.mjs`       | `node scripts/log_usage.mjs --result success --phase complete` | 使用状況ログ   |

### アセット

| テンプレート                    | 目的                           |
| ------------------------------- | ------------------------------ |
| `validation-schema.template.ts` | Zodスキーマテンプレート        |
| `encoding-helpers.ts`           | コンテキスト対応エンコード関数 |

## 変更履歴

| Version | Date       | Changes                                                       |
| ------- | ---------- | ------------------------------------------------------------- |
| 1.1.0   | 2026-01-02 | 18-skills.md仕様準拠、日本語化、references/scripts/assets追加 |
| 1.0.0   | 2025-12-31 | 初版作成                                                      |
