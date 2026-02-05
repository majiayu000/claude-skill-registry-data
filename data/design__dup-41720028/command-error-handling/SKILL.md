---
name: command-error-handling
description: |
  コマンドのエラーハンドリング（引数検証/事前チェック/ロールバック/ユーザー確認/エラーメッセージ設計）を整理し、失敗時の安全性と説明の一貫性を支援するスキル。
  パターン選定、検証手順、テンプレート運用を一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: エラーハンドリング設計 / 目的: 安定した実行フローの確立

  Trigger:
  Use when designing command error handling, validating failure paths, or implementing rollback and user confirmation flows.
  command error handling, validation, rollback, user confirmation, error messages
---
# command-error-handling

## 概要

コマンドのエラーハンドリング（引数検証/事前チェック/ロールバック/ユーザー確認/エラーメッセージ設計）を整理し、失敗時の安全性と説明の一貫性を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: エラー要件と失敗時フローを明確化する。

**アクション**:

1. 対象コマンドと失敗シナリオを整理する。
2. 必須の検証・ロールバック・確認手順を整理する。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-error-requirements.md` を参照

### Phase 2: エラーフロー設計

**目的**: エラーハンドリング設計を具体化する。

**アクション**:

1. エラーパターンと対処手順を定義する。
2. エラーメッセージ方針とユーザー確認を設計する。
3. テンプレートで表現を統一する。

**Task**: `agents/design-error-handling.md` を参照

### Phase 3: 検証と記録

**目的**: エラーフローを検証し、記録を残す。

**アクション**:

1. 検証スクリプトで整合性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-error-handling.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-error-requirements | Phase 1開始時 | 失敗シナリオ/制約 | 要件整理メモ、失敗一覧 |
| design-error-handling | Phase 2開始時 | 要件整理メモ | エラーフロー設計、メッセージ方針 |
| validate-error-handling | Phase 3開始時 | エラーフロー設計 | 検証レポート、改善方針 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| 失敗シナリオを網羅する | 例外漏れを防ぐため |
| エラーメッセージの粒度を揃える | 利用者の判断が容易になるため |
| 検証と記録をセットで実施する | 改善が継続できるため |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| 失敗時フローを曖昧にする | 回復不能になる |
| エラーメッセージを省略する | 利用者が迷う |
| 記録を残さない | 改善が続かない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/validate-error-handling.mjs` | エラーハンドリング検証 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 初回整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 詳細設計時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 改善ループ時 |
| エラーパターン | [references/error-patterns.md](references/error-patterns.md) | パターン選定時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/command-with-error-handling.md` | エラーハンドリング付きコマンドテンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
