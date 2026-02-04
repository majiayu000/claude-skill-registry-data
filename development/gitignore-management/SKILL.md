---
name: gitignore-management
description: |
  .gitignore設計と管理スキル。機密ファイルパターン、プロジェクト固有除外、プラットフォーム別パターン、.gitignore検証手法を提供。

  Anchors:
  • Pro Git (Scott Chacon) / 適用: バージョン管理 / 目的: 除外パターンの基礎
  • The Pragmatic Programmer / 適用: 実践的改善 / 目的: 効率的なパターン設計
  • GitHub gitignore templates / 適用: 言語別テンプレート / 目的: 標準パターン

  Trigger:
  Use when designing gitignore files, adding sensitive file patterns, configuring project-specific exclusions, validating gitignore patterns, or optimizing cross-platform exclusion rules.
  gitignore, ignore patterns, secrets, env files, build artifacts, cache
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# .gitignore 管理スキル

## 概要

.gitignore設計と管理スキル。機密ファイルパターン、プロジェクト固有除外、プラットフォーム別パターン、.gitignore検証手法を提供。

## ワークフロー

### Phase 1: 要件分析

**目的**: プロジェクトの除外パターン要件を把握

**アクション**:

1. プロジェクトタイプ（Node.js、Python等）を特定
2. 機密ファイル（.env、秘密鍵）の存在を確認
3. ビルド成果物とキャッシュディレクトリを特定

**Task**: `agents/analyze-requirements.md` を参照

### Phase 2: パターン設計

**目的**: 適切な除外パターンを設計

**アクション**:

1. `assets/gitignore-template.txt` をベースに作成
2. プロジェクト固有パターンを追加
3. クロスプラットフォーム対応を確認

**Task**: `agents/design-patterns.md` を参照

### Phase 3: 検証

**目的**: .gitignoreの正確性を検証

**アクション**:

1. `scripts/validate-gitignore.mjs` で検証
2. 意図しないファイル除外がないか確認
3. `scripts/log_usage.mjs` でフィードバック記録

**Task**: `agents/validate-gitignore.md` を参照

## Task仕様ナビ

| Task                 | 起動タイミング | 入力         | 出力               |
| -------------------- | -------------- | ------------ | ------------------ |
| analyze-requirements | Phase 1開始時  | プロジェクト | 要件リスト         |
| design-patterns      | Phase 2開始時  | 要件リスト   | .gitignoreパターン |
| validate-gitignore   | Phase 3開始時  | .gitignore   | 検証レポート       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 機密ファイル（.env、秘密鍵、API キー）を最優先で除外する
- プロジェクト固有のビルド出力・キャッシュを明確に列挙する
- クロスプラットフォーム対応（OS別、エディタ別）を考慮する
- `scripts/validate-gitignore.mjs` で定期的に検証する
- パターンの意図をコメントで記録する

### 避けるべきこと

- ワイルドカード `*` だけで除外パターンを定義しない
- 既に追跡済みの機密ファイルを後から追加しただけにしない（履歴から削除が必要）
- 特定ディレクトリを除外しながら中のファイルを追跡する矛盾した設定
- 不要になったパターンの削除を忘れない

## リソース参照

### references/（詳細知識）

| リソース           | パス                                                               | 内容             |
| ------------------ | ------------------------------------------------------------------ | ---------------- |
| 基礎知識           | See [references/basics.md](references/basics.md)                   | 構文とパターン   |
| 実装パターン       | See [references/patterns.md](references/patterns.md)               | 実践的パターン集 |
| パターンライブラリ | See [references/pattern-library.md](references/pattern-library.md) | 検証済みパターン |

### scripts/（決定論的処理）

| スクリプト               | 用途               | 使用例                                                  |
| ------------------------ | ------------------ | ------------------------------------------------------- |
| `validate-gitignore.mjs` | パターン検証       | `node scripts/validate-gitignore.mjs --file .gitignore` |
| `log_usage.mjs`          | フィードバック記録 | `node scripts/log_usage.mjs --result success`           |

### assets/（テンプレート）

| テンプレート             | 用途                       |
| ------------------------ | -------------------------- |
| `gitignore-template.txt` | 汎用.gitignoreテンプレート |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、構造再編成 |
| 1.0.0   | 2025-12-31 | 初版                                 |
