---
name: hallucination-prevention
description: |
  AIのハルシネーション（幻覚・誤情報生成）を防止するスキル。プロンプトレベル、パラメータレベル、検証レベルの3層防御により、信頼性の高いAI出力を実現。

  Anchors:
  • Thinking, Fast and Slow (Daniel Kahneman) / 適用: System 1/2思考分離 / 目的: 直感的推測の抑制と論理的検証の強制
  • Design by Contract (Bertrand Meyer) / 適用: 入出力契約設計 / 目的: 事前条件・事後条件・不変条件による出力保証
  • The Pragmatic Programmer / 適用: 実践的改善と品質維持 / 目的: 段階的検証とフィードバックループ構築

  Trigger:
  Use when preventing AI hallucinations, ensuring factual accuracy, requiring verifiable outputs, or implementing truth constraints.
  hallucination prevention, fact-checking, verification, accuracy, factual output, citation required, ground truth, temperature tuning
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Hallucination Prevention

## 概要

AIのハルシネーション（幻覚・誤情報生成）を防止するスキル。
プロンプトレベル、パラメータレベル、検証レベルの3層防御により、信頼性の高いAI出力を実現する。

## ワークフロー

### Phase 1: タスク分析と前提整理

**目的**: タスクの目的と前提条件を明確にし、ハルシネーションリスクを特定

**アクション**:

1. ユーザー要求の意図を正確に理解
2. 事実要求と推測要求を分離
3. ハルシネーションリスク要素（日付、固有名詞、数値、技術仕様）を洗い出し
4. 必要な参照リソースを決定

**Task**: `agents/phase1-analysis.md` を参照

### Phase 2: ハルシネーション防止策の実装

**目的**: 3層防御（プロンプト、パラメータ、検証）を実装

**アクション**:

1. プロンプトレベル防御を適用（事実要求の明示、推測禁止）
2. パラメータレベル調整（Temperature 0.0-0.3、Top-p設定）
3. 検証メカニズムを組み込み（事実チェックポイント、引用元明示）

**Task**: `agents/phase2-implementation.md` を参照

### Phase 3: 検証と記録

**目的**: 実装結果を検証し、フィードバックループを回す

**アクション**:

1. `assets/verification-checklist.md` による成果物検証
2. `scripts/validate-skill.mjs` によるスキル構造確認
3. `scripts/log_usage.mjs` による実行記録保存
4. 改善提案の記録

**Task**: `agents/phase3-verification.md` を参照

## Task仕様ナビ

| Task                  | 起動タイミング | 入力           | 出力           |
| --------------------- | -------------- | -------------- | -------------- |
| phase1-analysis       | Phase 1開始時  | ユーザー要求   | タスク分析レポ |
| phase2-implementation | Phase 2開始時  | タスク分析レポ | 実装レポート   |
| phase3-verification   | Phase 3開始時  | 実装レポート   | 検証レポート   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 不確実な情報には「可能性がある」「推測される」等の限定詞を使用
- 事実に基づく出力には必ず根拠・引用元を明示
- Temperature設定を0.0-0.3の低値に設定
- 出力前に事実チェックポイントを設定
- 日付、固有名詞、数値は必ず検証可能な情報源を確認
- 検証不可能な情報は明示的に「未確認」とマーク

### 避けるべきこと

- 推測を事実として述べる
- 存在しない情報を捏造する（URL、引用、数値）
- 高Temperature設定での事実要求への回答
- 検証プロセスをスキップ
- 曖昧な情報源への言及（「ある研究によると」等）

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                               | 内容              |
| -------------- | ---------------------------------------------------------------------------------- | ----------------- |
| 基礎知識       | See [references/Level1_basics.md](references/Level1_basics.md)                     | 基本概念と運用    |
| 中級知識       | See [references/Level2_intermediate.md](references/Level2_intermediate.md)         | パターン詳細      |
| 上級知識       | See [references/Level3_advanced.md](references/Level3_advanced.md)                 | 高度な技法        |
| 専門家向け     | See [references/Level4_expert.md](references/Level4_expert.md)                     | 専門的応用        |
| プロンプト防御 | See [references/prompt-level-defense.md](references/prompt-level-defense.md)       | プロンプト設計    |
| パラメータ調整 | See [references/parameter-tuning.md](references/parameter-tuning.md)               | Temperature/Top-p |
| 検証メカニズム | See [references/verification-mechanisms.md](references/verification-mechanisms.md) | 事実チェック手法  |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                                          |
| -------------------- | ------------------ | --------------------------------------------------------------- |
| `validate-skill.mjs` | スキル構造検証     | `node scripts/validate-skill.mjs`                               |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート                | 用途                   |
| --------------------------- | ---------------------- |
| `verification-checklist.md` | 出力検証チェックリスト |

## 変更履歴

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 2.1.0   | 2026-01-02 | 18-skills.md完全準拠、リソース参照テーブル化 |
| 2.0.0   | 2025-12-31 | agents/ Tasks, EVALS.json, LOGS.md追加       |
| 1.0.0   | 2025-12-24 | 初版                                         |
