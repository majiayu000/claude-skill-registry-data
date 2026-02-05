---
name: tool-permission-management
description: |
  ツール権限の要件整理、ポリシー設計、監査運用を体系化するスキル。
  最小権限の原則と変更履歴を徹底し、安全なツール利用を支援する。

  Anchors:
  • The Pragmatic Programmer / 適用: 権限運用 / 目的: 実務的な安全性
  • Zero Trust Architecture (NIST SP 800-207) / 適用: アクセス制御 / 目的: 最小権限の徹底

  Trigger:
  Use when defining or reviewing tool permissions, access policies, or least-privilege settings.
  permissions, least privilege, access policy
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Tool Permission Management

## 概要

ツール権限の設計と運用を一貫した手順で整備するスキル。要件整理、ポリシー設計、監査の流れを確立し、権限過多や監査不備を防ぐ。

---

## ワークフロー

### Phase 1: 権限要件の整理

**目的**: ツール利用目的と必要権限を整理する

**アクション**:

1. 対象ツールと実行タスクを洗い出す
2. 必要なアクセス範囲と禁止事項を整理する
3. 監査要件とログ要件を定義する

**Task**: `agents/permission-requirements.md` を参照

### Phase 2: ポリシー設計と設定

**目的**: 最小権限のポリシーを設計し設定する

**アクション**:

1. 権限テンプレートをベースにポリシーを設計する
2. リスク評価に基づき権限を最小化する
3. 設定変更の履歴と理由を記録する

**Task**: `agents/permission-policy-design.md` を参照

### Phase 3: 監査と運用

**目的**: 権限の運用状況を監査し改善する

**アクション**:

1. 権限スキャンと監査を実行する
2. 逸脱や過剰権限を洗い出す
3. 実行記録を保存する

**Task**: `agents/permission-audit-ops.md` を参照

---

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| permission-requirements | Phase 1 開始時 | ツール一覧/目的 | 権限要件メモ |
| permission-policy-design | Phase 2 開始時 | 要件/制約 | 権限ポリシー |
| permission-audit-ops | Phase 3 開始時 | 監査ログ/設定 | 監査レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| 最小権限の原則を適用する | リスクを抑えるため |
| 権限変更の理由を記録する | 監査性を高めるため |
| 定期的な権限レビューを実施する | 逸脱を防ぐため |
| 権限テンプレートを統一する | 運用コストを下げるため |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| 管理者権限の乱用 | セキュリティ事故につながる |
| ログを記録しない | 監査不能になる |
| 権限変更の履歴を残さない | 原因追跡が難しくなる |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/analyze-permissions.mjs` | 権限構成を分析する |
| `scripts/validate-skill.mjs` | スキル構造と必須成果物を検証する |
| `scripts/log_usage.mjs` | 実行記録を保存する |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| 基礎概念 | [references/Level1_basics.md](references/Level1_basics.md) | Phase 1 で参照 |
| 実務パターン | [references/Level2_intermediate.md](references/Level2_intermediate.md) | Phase 2 で参照 |
| 応用戦略 | [references/Level3_advanced.md](references/Level3_advanced.md) | 監査時に参照 |
| エキスパート | [references/Level4_expert.md](references/Level4_expert.md) | 大規模運用時に参照 |
| 権限マトリクス | [references/tool-selection-matrix.md](references/tool-selection-matrix.md) | 設計時に参照 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/permission-template.yaml` | 権限ポリシーのテンプレート |

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 2.0.0 | 2026-01-02 | Task仕様と監査フローを再設計し、参照を整理 |
| 1.0.0 | 2025-12-31 | 初期バージョン |
