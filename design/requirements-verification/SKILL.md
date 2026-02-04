---
name: requirements-verification
description: |
  要件検証の専門スキル。要件の完全性・一貫性・実現可能性・検証可能性を体系的に評価し、品質を保証する。
  品質チェックリストと検証スクリプトを用いて、レビュー結果の整理と改善提案まで行う。

  Anchors:
  • Software Requirements (Karl Wiegers) / 適用: 要件検証全体 / 目的: 完全性・一貫性・実現可能性の評価
  • IEEE 830 SRS Standard / 適用: 要件品質基準 / 目的: 検証可能な構造化
  • Don't Make Me Think (Steve Krug) / 適用: ユーザー要件 / 目的: ユーザビリティ視点の確認

  Trigger:
  Use when verifying requirements quality, checking consistency/completeness, assessing feasibility, or drafting verification reports.
  requirements verification, requirements quality, consistency check, completeness check, feasibility assessment, 要件検証, 要件レビュー
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# 要件検証（Requirements Verification）

## 概要

要件の品質を体系的に評価し、欠陥を早期に検出するためのスキル。
一貫性・完全性・実現可能性・検証可能性の4観点を軸に、チェックリストと検証スクリプトで品質を評価する。

## ワークフロー

### Phase 1: 要件セットの分析

**目的**: 検証対象の要件を把握し、検証観点を定義する

**アクション**:

1. 対象要件ドキュメント（仕様書、ユーザーストーリー等）を収集
2. 要件の分類（FR/NFR/制約/前提）を整理
3. 検証観点（一貫性/完全性/実現可能性/検証可能性）を確定
4. `agents/requirements-analysis.md` を実行し背景と依存関係を整理

### Phase 2: 検証ルール適用と品質評価

**目的**: ルールに基づき問題を検出し、品質メトリクスを算出する

**アクション**:

1. `agents/consistency-checker.md` で一貫性を確認
2. `agents/completeness-validator.md` で完全性を評価
3. `agents/feasibility-assessor.md` で実現可能性を判定
4. `scripts/verify-requirements.mjs` で定量評価を補助
5. 必要に応じて `references/` を参照

### Phase 3: 検証結果報告と改善提案

**目的**: 検出した課題を報告し、改善案を提示する

**アクション**:

1. `assets/verification-report-template.md` で報告書を作成
2. `agents/improvement-suggester.md` で改善提案を整理
3. `assets/verification-checklist.md` の結果を添付
4. `scripts/log_usage.mjs` で実行記録を保存

## Task仕様ナビ

| Task名             | ファイル                           | 役割                                 | 入力                        | 出力                           | 実行タイミング |
| ------------------ | ---------------------------------- | ------------------------------------ | --------------------------- | ------------------------------ | -------------- |
| 要件分析           | `agents/requirements-analysis.md`  | 要件の構造と背景を把握               | 要件ドキュメント            | 分析レポート                   | Phase 1        |
| 一貫性確認         | `agents/consistency-checker.md`    | 要件間の矛盾・重複を検出             | 要件セット + ルール         | 矛盾リスト                     | Phase 2        |
| 完全性検証         | `agents/completeness-validator.md` | 欠落/曖昧な要件を特定                | 要件セット + チェックリスト | 欠落項目リスト                 | Phase 2        |
| 実現可能性評価     | `agents/feasibility-assessor.md`   | 技術/コスト/期間の実現可能性を判定   | 要件セット + 制約           | リスク評価                     | Phase 2        |
| 改善提案           | `agents/improvement-suggester.md`  | 検出課題に対する改善案を作成         | 検証結果                    | 改善提案書                     | Phase 3        |

## ベストプラクティス

### すべきこと

- `assets/verification-checklist.md` を使って漏れを防止
- 受け入れ基準（Given-When-Then）で検証可能性を明示
- 依存関係を洗い出し、矛盾を先に整理
- 重要度/影響度で問題を優先順位付け
- `scripts/verify-requirements.mjs` で定量指標を算出

### 避けるべきこと

- 定性的評価だけで結論を出す
- 要件の背景・前提を無視した検証
- 曖昧な指摘だけで改善案を出さない
- 検証結果の記録漏れ

## リソース参照

### references/（詳細知識）

- [references/Level1_basics.md](references/Level1_basics.md) — 基礎原則と検証観点
- [references/Level2_intermediate.md](references/Level2_intermediate.md) — 実務プロセスと評価指標
- [references/Level3_advanced.md](references/Level3_advanced.md) — 複雑な要件セットの検証
- [references/Level4_expert.md](references/Level4_expert.md) — 組織的検証と高度手法
- [references/verification-techniques.md](references/verification-techniques.md) — 検証技法とルール集

### assets/（テンプレート）

| テンプレート                            | 用途                 |
| --------------------------------------- | -------------------- |
| `verification-checklist.md`             | 検証チェックリスト   |
| `verification-report-template.md`       | 検証報告書テンプレート |

### scripts/（決定論的処理）

| スクリプト                        | 用途                         | 使用例                                                          |
| --------------------------------- | ---------------------------- | --------------------------------------------------------------- |
| `verify-requirements.mjs`         | 要件ファイルの品質検証       | `node scripts/verify-requirements.mjs requirements.md`          |
| `validate-skill.mjs`              | スキル構造の自己検証         | `node scripts/validate-skill.mjs`                               |
| `log_usage.mjs`                   | 実行記録                     | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

## 変更履歴

| Version | Date       | Changes                                                                |
| ------- | ---------- | ---------------------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | agents/assets/references/scriptsを再構成、要件検証スキルに復帰         |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様へ準拠、Task仕様ナビ追加、Anchors・Trigger統合         |
| 0.9.0   | 2025-12-24 | 初版リリース                                                           |
