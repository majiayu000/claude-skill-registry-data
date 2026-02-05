---
name: linting-formatting-automation
description: |
  Code quality automation for linting and formatting. Provides ESLint, Prettier, Biome setup, CI/CD integration, pre-commit hooks, and tool migration strategies for consistent code style enforcement.

  Anchors:
  • ESLint Official Docs / Apply: Rule configuration, plugin integration / Purpose: Correct API usage and best practices
  • Prettier Philosophy / Apply: Opinionated formatting / Purpose: Minimize configuration bikeshedding
  • Biome Performance Model / Apply: Rust-based tooling / Purpose: Optimize development workflow speed

  Trigger:
  Use when setting up linting/formatting for new projects, integrating code quality into CI/CD, configuring pre-commit hooks, or migrating between tools.
  eslint, prettier, biome, lint, format, pre-commit, husky, lint-staged, code quality
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Linting & Formatting Automation

## 概要

コードの品質と一貫性を自動化するスキル。ESLint、Prettier、Biome等のツールセットアップからCI/CD統合、pre-commitフック構成まで、開発ワークフロー全体をカバーする。

## ワークフロー

### Phase 1: 要件分析

**目的**: プロジェクトに適したツール戦略を決定

**アクション**:

1. プロジェクト要件を評価（言語、フレームワーク、チームサイズ）
2. ツール選択を決定（ESLint+Prettier vs Biome）
3. 既存設定の移行要否を判断

**Task**: `agents/analyze-requirements.md` を参照

### Phase 2: ツールセットアップ

**目的**: 選択したツールを設定

**アクション**:

1. 選択ツールの設定ファイルを生成
2. 必要なプラグイン・拡張を追加
3. package.jsonにスクリプトを追加

**Task**: `agents/setup-tools.md` を参照

### Phase 3: ワークフロー統合

**目的**: 開発ワークフローに統合

**アクション**:

1. pre-commitフックを設定（Husky + lint-staged）
2. CI/CDパイプラインを構成
3. エディタ統合を設定

**Task**: `agents/integrate-workflow.md` を参照

### Phase 4: 検証

**目的**: 設定が正しく動作することを確認

**アクション**:

1. ローカルでコミットテストを実行
2. CI/CDパイプラインをテスト
3. チームドキュメントを更新

**Task**: `agents/validate-setup.md` を参照

## Task仕様（ナビゲーション）

| Task                 | 起動タイミング | 入力             | 出力           |
| -------------------- | -------------- | ---------------- | -------------- |
| analyze-requirements | Phase 1開始時  | プロジェクト情報 | ツール選択結果 |
| setup-tools          | Phase 2開始時  | ツール選択結果   | 設定ファイル群 |
| integrate-workflow   | Phase 3開始時  | 設定ファイル群   | フック・CI設定 |
| validate-setup       | Phase 4開始時  | 全設定           | 検証済み設定   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                      | 理由                         |
| ----------------------------- | ---------------------------- |
| 推奨プリセットから始める      | 安定した基盤から段階的に拡張 |
| キャッシュを有効化（--cache） | ビルド時間短縮               |
| エディタ統合を設定            | 即時フィードバック           |
| CIチェックをマージ必須にする  | 品質ゲート確保               |

### 避けるべきこと

| 禁止事項             | 問題点                 |
| -------------------- | ---------------------- |
| 過度なカスタマイズ   | 保守困難、標準から乖離 |
| eslint-disableの乱用 | 根本原因を隠蔽         |
| フォーマット議論     | 生産性低下             |
| キャッシュ未設定     | DX悪化                 |

## リソース参照

### scripts/（決定論的処理）

| スクリプト            | 用途             |
| --------------------- | ---------------- |
| `validate-config.mjs` | 設定ファイル検証 |
| `log_usage.mjs`       | 使用記録         |

### references/（詳細知識）

| リソース     | パス                                             | 読込条件         |
| ------------ | ------------------------------------------------ | ---------------- |
| 基礎知識     | [references/basics.md](references/basics.md)     | ツール概念理解時 |
| 設定パターン | [references/patterns.md](references/patterns.md) | 設定作成時       |

### assets/（テンプレート）

| アセット                  | 用途                         |
| ------------------------- | ---------------------------- |
| `eslint.config.js`        | ESLint flat config雛形       |
| `.prettierrc.json`        | Prettier設定雛形             |
| `biome.json`              | Biome設定雛形                |
| `github-actions-lint.yml` | GitHub Actions lint workflow |
| `lint-staged.config.js`   | lint-staged設定雛形          |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.1.0   | 2026-01-02 | 18-skills.md仕様に完全準拠で再構築 |
| 2.0.0   | 2025-12-31 | 構造改善                           |
