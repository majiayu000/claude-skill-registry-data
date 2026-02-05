---
name: lock-file-management
description: |
  ロックファイル整合性と依存関係再現性の専門スキル。pnpm-lock.yaml、package-lock.json、yarn.lockを管理し、一貫性のあるビルド、マージコンフリクト解決、CI/CD最適化を実現。

  Anchors:
  • The Pragmatic Programmer / 適用: 依存関係管理 / 目的: 再現可能なビルド

  Trigger:
  Use when managing lock files, resolving merge conflicts, verifying integrity, or optimizing CI/CD caching.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Lock File Management

## 概要

ロックファイル（pnpm-lock.yaml、package-lock.json、yarn.lock）の整合性管理と依存関係の再現性確保を専門とするスキル。

## ワークフロー

### Phase 1: 問題診断

**目的**: ロックファイルの問題を特定

**アクション**:

1. ロックファイルの存在と形式を確認
2. package.jsonとの整合性を検証
3. 問題の種類を特定（コンフリクト/不整合/欠損）

**Task**: `agents/diagnose-issue.md` を参照

### Phase 2: 解決実行

**目的**: 特定された問題を解決

**アクション**:

1. 問題に応じた解決戦略を選択
2. ロックファイルを再生成または修復
3. 依存関係を検証

**Task**: `agents/resolve-issue.md` を参照

### Phase 3: 検証

**目的**: 解決結果を検証

**アクション**:

1. ロックファイル整合性を確認
2. インストールテストを実行
3. CI/CD設定を確認

**Task**: `agents/validate-solution.md` を参照

## Task仕様（ナビゲーション）

| Task              | 起動タイミング | 入力             | 出力             |
| ----------------- | -------------- | ---------------- | ---------------- |
| diagnose-issue    | Phase 1開始時  | 問題の症状       | 診断結果         |
| resolve-issue     | Phase 2開始時  | 診断結果         | 修正済みファイル |
| validate-solution | Phase 3開始時  | 修正済みファイル | 検証レポート     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由               |
| ---------------------------- | ------------------ |
| ロックファイルをVCSに含める  | 再現可能ビルド確保 |
| frozen-lockfileをCI/CDで使用 | 環境間の一貫性     |
| 定期的な整合性検証           | 問題の早期発見     |
| パッケージマネージャーを統一 | 混乱を防止         |

### 避けるべきこと

| 禁止事項                      | 問題点             |
| ----------------------------- | ------------------ |
| 手動でロックファイルを編集    | 破損リスク         |
| 複数形式の混在                | 不整合発生         |
| frozen-lockfileなしでデプロイ | 環境差異発生       |
| 古いロックファイルの放置      | セキュリティリスク |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                  | 用途       |
| --------------------------- | ---------- |
| `verify-lock-integrity.mjs` | 整合性検証 |
| `log_usage.mjs`             | 使用記録   |

### references/（詳細知識）

| リソース     | パス                                             | 読込条件   |
| ------------ | ------------------------------------------------ | ---------- |
| 基礎知識     | [references/basics.md](references/basics.md)     | 初回使用時 |
| 解決パターン | [references/patterns.md](references/patterns.md) | 問題解決時 |

### assets/（テンプレート）

| アセット                               | 用途                       |
| -------------------------------------- | -------------------------- |
| `lockfile-troubleshooting-template.md` | トラブルシューティング雛形 |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠で再構築 |
| 1.1.0   | 2025-12-31 | 構造改善                           |
