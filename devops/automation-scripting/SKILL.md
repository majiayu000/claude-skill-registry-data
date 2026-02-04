---
name: automation-scripting
description: |
  自動化スクリプト（Bash/Python/Node）の設計・実装・運用を支援するスキル。
  冪等性、エラーハンドリング、ログ設計、CI/CD統合の指針を整理します。

  Anchors:
  • The Pragmatic Programmer / 適用: 自動化の実務 / 目的: 再現性の高いスクリプト設計
  • Automation Pipeline Patterns / 適用: ワークフロー設計 / 目的: 反復作業の効率化
  • Unix Philosophy / 適用: スクリプト構成 / 目的: 小さな責務分離

  Trigger:
  Use when designing automation scripts, adding error handling/logging, or integrating scripts into CI/CD pipelines.
allowed-tools:
  - bash
  - node
---

# 自動化スクリプティング

## 概要

再利用可能で保守性の高いスクリプトを設計し、反復作業を自動化する。
詳細は `references/` に外部化し、必要時に参照する。

- テンプレは `assets/script-template.sh`
- 実装パターンは `references/script-patterns.md`

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: 自動化対象と制約を整理する

**アクション**:

1. `references/Level1_basics.md` で基礎概念を確認
2. 自動化対象の範囲と入出力を整理
3. 実行環境と権限の制約を確認

**Task**: `agents/analyze-automation-context.md`

### Phase 2: スクリプト設計と実装

**目的**: 冪等性とエラーハンドリングを含む設計を行う

**アクション**:

1. `references/Level2_intermediate.md` で実装パターンを確認
2. `assets/script-template.sh` を基に構造を決定
3. ログとエラー処理を設計する

**Task**:
- `agents/design-automation-script.md`
- `agents/implement-automation-script.md`

### Phase 3: 検証と記録

**目的**: スクリプトの検証と記録を行う

**アクション**:

1. 実行結果を確認して改善点を整理
2. `scripts/validate-skill.mjs` で構造検証
3. `scripts/log_usage.mjs` で改善記録

**Task**: `agents/validate-automation-script.md`

## Task仕様ナビ

| Task | 役割 | 入力 | 出力 | 参照先 | 実行タイミング |
| --- | --- | --- | --- | --- | --- |
| コンテキスト整理 | 目的と制約の整理 | 要件情報 | 目的メモ | `references/Level1_basics.md` | Phase 1 |
| 設計 | 冪等性・エラー設計 | 目的メモ | 設計メモ | `references/Level2_intermediate.md` | Phase 2 前半 |
| 実装 | スクリプト実装 | 設計メモ | 実装結果 | `assets/script-template.sh` | Phase 2 後半 |
| 検証 | 動作検証と改善 | 実装結果 | 検証レポート | `references/Level3_advanced.md` | Phase 3 |

## ベストプラクティス

### すべきこと

- 冪等性を前提に設計する
- 失敗時のエラー出力を明示する
- 実行ログを必ず残す
- 実行環境の差分を考慮する

### 避けるべきこと

- ハードコードされたパスやシークレット
- 例外処理なしの実行
- 実行結果の検証を省略する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: 実装パターン
- `references/Level3_advanced.md`: CI/CD統合
- `references/Level4_expert.md`: 分散処理と高度運用
- `references/script-patterns.md`: スクリプトパターン
- `references/legacy-skill.md`: 旧版要約（移行時のみ参照）

### スクリプト

- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/script-template.sh`: スクリプトテンプレ

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、assets追加            |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に準拠                              |
| 1.0.0   | 2025-12-24 | 初版作成                                            |
