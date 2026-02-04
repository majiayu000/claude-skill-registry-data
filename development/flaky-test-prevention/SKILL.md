---
name: flaky-test-prevention
description: |
  フレーキー（不安定）なテストを検出・修正するスキル。非決定性の排除、リトライロジック、テスト安定性向上パターンを提供。並列実行時の問題解決やタイミング依存の除去を支援。

  Anchors:
  • Test-Driven Development（Kent Beck） / 適用: Red-Green-Refactor / 目的: 安定したテスト設計
  • xUnit Test Patterns（Gerard Meszaros） / 適用: テストダブル / 目的: 非決定性の隔離
  • Continuous Delivery（Jez Humble） / 適用: パイプライン信頼性 / 目的: CI/CDの安定化

  Trigger:
  Use when tests fail intermittently, detecting flaky tests, eliminating non-determinism in tests, fixing timing-dependent failures, or stabilizing CI/CD pipelines.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
---

# フレーキーテスト防止

## 概要

フレーキー（不安定）なテストを検出・修正するスキル。非決定性の排除、リトライロジック、テスト安定性向上パターンを提供し、CI/CDパイプラインの信頼性を向上させる。

## ワークフロー

### Phase 1: フレーキーテスト検出

**目的**: 不安定なテストを特定し、原因を分類

**アクション**:

1. [references/non-determinism-patterns.md](references/non-determinism-patterns.md) で非決定性パターンを確認
2. `scripts/detect-flaky-tests.mjs` でテストの安定性を分析
3. 失敗パターン（タイミング、並列、外部依存）を分類

**Task**: [agents/detect-flaky-tests.md](agents/detect-flaky-tests.md) を参照

### Phase 2: 非決定性分析

**目的**: フレーキーテストの根本原因を特定

**アクション**:

1. タイミング依存（sleep、setTimeout）を特定
2. 外部依存（DB、API、ファイルシステム）を特定
3. 並列実行時の競合状態を分析

**Task**: [agents/analyze-non-determinism.md](agents/analyze-non-determinism.md) を参照

### Phase 3: 修正実装

**目的**: 安定性向上パターンの適用

**アクション**:

1. [references/retry-strategies.md](references/retry-strategies.md) でリトライ戦略を確認
2. [references/stability-checklist.md](references/stability-checklist.md) でチェックリストを確認
3. [assets/stable-test-template.ts](assets/stable-test-template.ts) を参考に修正
4. 修正後のテストを検証

**Task**: [agents/implement-fixes.md](agents/implement-fixes.md) を参照

## Task仕様ナビ

| Task                                                                   | 用途                 | 入力           | 出力                 |
| ---------------------------------------------------------------------- | -------------------- | -------------- | -------------------- |
| [agents/detect-flaky-tests.md](agents/detect-flaky-tests.md)           | フレーキーテスト検出 | テストスイート | 不安定テストリスト   |
| [agents/analyze-non-determinism.md](agents/analyze-non-determinism.md) | 非決定性分析         | 不安定テスト   | 根本原因分析結果     |
| [agents/implement-fixes.md](agents/implement-fixes.md)                 | 修正実装             | 根本原因分析   | 修正済みテストコード |

## ベストプラクティス

### すべきこと

- テスト失敗パターンを記録・分析する
- 固定時間待機（sleep）を条件付き待機に置き換える
- 外部依存をモック・スタブで置き換える
- テストデータを各テストで独立させる
- 並列実行時のリソース競合を防ぐ

### 避けるべきこと

- 失敗したテストを単にリトライで隠す
- グローバル状態に依存するテスト
- 実行順序に依存するテスト
- 共有リソースへの同時アクセス

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                             | 内容                   |
| -------------------- | -------------------------------------------------------------------------------- | ---------------------- |
| 非決定性パターン     | [references/non-determinism-patterns.md](references/non-determinism-patterns.md) | 原因パターンと解決策   |
| リトライ戦略         | [references/retry-strategies.md](references/retry-strategies.md)                 | 適切なリトライ実装     |
| 安定性チェックリスト | [references/stability-checklist.md](references/stability-checklist.md)           | テスト安定化の確認項目 |

### assets/（テンプレート）

| テンプレート            | 用途                   |
| ----------------------- | ---------------------- |
| stable-test-template.ts | 安定したテストの実装例 |

### scripts/（検出・検証）

| スクリプト             | 用途                 | 使用例                                          |
| ---------------------- | -------------------- | ----------------------------------------------- |
| detect-flaky-tests.mjs | フレーキーテスト検出 | `node scripts/detect-flaky-tests.mjs --runs 10` |
| log_usage.mjs          | 利用記録             | `node scripts/log_usage.mjs --result success`   |

## 変更履歴

| Version | Date       | Changes                                                      |
| ------- | ---------- | ------------------------------------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠。frontmatter修正、references/整理 |
| 1.0.0   | 2025-12-24 | 初版作成                                                     |
