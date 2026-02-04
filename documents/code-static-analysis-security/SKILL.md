---
name: code-static-analysis-security
description: |
  静的解析によるセキュリティ脆弱性検出を整理し、SAST運用と検出ルールの設計を支援するスキル。
  SQLインジェクション、XSS、コマンドインジェクションなどの検出と改善方針を扱う。

  Anchors:
  • Web Application Security (Andrew Hoffman) / 適用: 脅威分析と検出観点 / 目的: 脆弱性検出の精度向上
  • OWASP ASVS / 適用: 検出基準の整理 / 目的: セキュリティ要件の明文化
  • Secure by Design (OWASP) / 適用: 改善方針 / 目的: 安全な設計判断

  Trigger:
  Use when running SAST, defining detection rules, auditing injection vulnerabilities, or documenting static analysis findings.
  static analysis, SAST, SQL injection, XSS, command injection, security review
---
# code-static-analysis-security

## 概要

静的解析による脆弱性検出を体系化し、検出ルールと改善方針を一貫して整理する。

## ワークフロー

### Phase 1: 目的と対象整理

**目的**: 対象範囲と検出方針を明確化する。

**アクション**:

1. 対象コードと検出対象（SQLi/XSS等）を整理する。
2. 参照すべき検出パターンを選定する。
3. SAST設定の要件を確認する。

**Task**: `agents/analyze-sast-requirements.md` を参照

### Phase 2: 検出設計

**目的**: 検出ルールと運用手順を設計する。

**アクション**:

1. 検出パターンを基にルールを整備する。
2. SAST設定テンプレートを調整する。
3. 結果レポートの形式を確認する。

**Task**: `agents/design-detection-rules.md` を参照

### Phase 3: 検証と記録

**目的**: 検出結果を検証し、記録を残す。

**アクション**:

1. 検出スクリプトで対象をスキャンする。
2. 結果をレビューして改善方針を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-sast-findings.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-sast-requirements | Phase 1開始時 | 対象コード/検出対象 | 対象範囲メモ、検出観点一覧 |
| design-detection-rules | Phase 2開始時 | 検出観点一覧 | ルール設計、設定方針 |
| validate-sast-findings | Phase 3開始時 | 検出結果 | 検証レポート、改善方針 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| 検出対象を明確にする | 誤検出を抑えるため |
| ルールを段階的に調整する | 運用負荷を下げるため |
| 検出結果を記録する | 改善サイクルを回すため |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| ルールなしでスキャンする | 結果が不安定になる |
| 重大度を評価しない | 優先度が不明になる |
| 記録を残さない | 改善が継続できない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/scan-sql-injection.mjs` | SQLインジェクション検出 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| Level1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 初回整理時 |
| Level2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 検出設計時 |
| Level3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 詳細検討時 |
| Level4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 改善ループ時 |
| 検出パターン | [references/injection-patterns.md](references/injection-patterns.md) | ルール設計時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/sast-config-template.json` | SAST設定テンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
