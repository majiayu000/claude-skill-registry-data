---
name: skill-creation-workflow
description: |
  スキル改善・新規作成を、skill-creator検証からskill_list更新まで一貫実行する指示書。
  単一/複数スキルの処理順、成果物の完全性、言語規則、確認手順を明文化する。

  Anchors:
  • 18-skills.md / 適用: スキル構造・品質基準 / 目的: 仕様準拠の担保
  • skill-creator / 適用: 検証と作成フロー / 目的: 一貫した作業手順
  • Continuous Delivery (Humble) / 適用: 検証・自動化・反復 / 目的: 品質パイプライン構築

  Trigger:
  Use when creating or updating skills, enforcing skill-creator validation, or coordinating multi-skill updates.
  skill creation, skill update, skill-creator validation, skill_list update, multi-skill workflow
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Skill Creation Workflow

## 概要

スキル改善・新規作成の実行指示書。skill-creatorによる検証、成果物の完全性、
言語規則、skill_list更新までを一連のフローで運用する。

---

## 基本原則

| 原則       | 説明                                                         |
| ---------- | ------------------------------------------------------------ |
| 目的最優先 | 既存の内容にとらわれず、目的達成を最優先に判断する           |
| 段階的実行 | 一つのスキルを完全に完了させてから次へ進む                   |
| 並列処理可 | 複数スキルは並列処理してもよいが、各スキルの完了は個別に保証 |
| 完全性     | 省略せず、成果物と確認項目を漏れなく出力する                 |
| 言語規則   | 原則日本語、指示に「英語で記述」がある場合のみ英語           |

---

## ワークフロー

```
verify-skill-creator → implement-skill → build-structure → review-output → update-skill-list
```

### Task 1: skill-creator検証（verify-skill-creator）

skill-creatorスキルを確認し、作成対象の要件を整理する。

**Task**: `agents/verify-skill-creator.md` を参照

### Task 2: スキル実装（implement-skill）

仕様に基づきスキルを実装する。

**Task**: `agents/implement-skill.md` を参照

### Task 3: 構造構築（build-skill-structure）

スキルのファイル構成を作成・更新する。

**Task**: `agents/build-skill-structure.md` を参照

### Task 4: 出力レビュー（review-skill-output）

作成内容の完全性と言語規則を確認する。

**Task**: `agents/review-skill-output.md` を参照

### Task 5: skill_list更新（update-skill-list）

skill_list.mdを更新する。

**Task**: `agents/update-skill-list.md` を参照

---

## Task仕様（ナビゲーション）

| Task                  | 責務              | 入力                     | 出力                  |
| --------------------- | ----------------- | ------------------------ | --------------------- |
| verify-skill-creator  | skill-creator検証 | ユーザー要求、対象リスト | 要件整理メモ          |
| implement-skill       | スキル実装        | 要件整理メモ             | SKILL.md草稿          |
| build-skill-structure | 構造構築          | SKILL.md草稿             | 完全なスキル構成      |
| review-skill-output   | 出力レビュー      | スキル構成               | 確認結果と修正案      |
| update-skill-list     | skill_list更新    | 完成したスキル群         | 更新済みskill_list.md |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照
**注記**: 1 Task = 1 責務。複数スキルの場合はTask 1-4を並列実行可。

---

## 処理フロー詳細

### 単一スキルの処理

```
Step 1: skill-creatorによる検証
  ↓
Step 2: 改善・新規作成の実施
  ↓
Step 3: ファイル構成の作成・更新
  ↓
Step 4: 作成内容の確認
  ↓
Step 5: skill_list.mdの更新
```

### 複数スキルの処理（並列可）

```
スキルA ────┬──→ Step 1-4 を実行
スキルB ────┼──→ Step 1-4 を実行
スキルC ────┘
           ↓
全スキル完了後に skill_list.md を統合更新
```

---

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由           |
| ---------------------------------- | -------------- |
| skill-creatorを毎回実行する        | 品質基準の担保 |
| 目的達成に必要なものは全て作成する | 成果物の完全性 |
| 一つずつ丁寧に処理する             | 品質維持       |
| 言語規則を守る                     | 一貫性の確保   |

### 避けるべきこと

| 禁止事項                          | 問題点               |
| --------------------------------- | -------------------- |
| skill-creatorの実行をスキップする | 品質基準違反のリスク |
| ファイルやエージェントを省略する  | 成果物の不完全性     |
| 既存情報を絶対視する              | 改善機会の喪失       |
| 言語規則を無視する                | 一貫性の欠如         |

---

## 品質基準

### 必須要件

- skill-creatorを毎回実行している
- SKILL.mdが確実に作成されている
- agents/配下に必要なエージェントが全て作成されている
- 仕様通りに作成されている
- 省略せず全て出力されている
- skill_list.mdが更新されている
- 言語規則に従っている

### 完了条件

**単一スキル**:

- [ ] skill-creatorで検証完了
- [ ] 全ファイルの作成・更新完了
- [ ] 作成内容の確認完了
- [ ] 言語規則の確認完了

**複数スキル**:

- [ ] 全スキルの個別処理完了
- [ ] skill_list.mdの統合更新完了

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト           | 用途     | 使用例                                         |
| -------------------- | -------- | ---------------------------------------------- |
| `validate-skill.mjs` | 構造検証 | `node scripts/validate-skill.mjs <skill-path>` |
| `log_usage.mjs`      | 使用記録 | `node scripts/log_usage.mjs --result success`  |

### references/（詳細知識）

| リソース         | パス                                                                       | 読込条件               |
| ---------------- | -------------------------------------------------------------------------- | ---------------------- |
| フェーズ詳細     | [references/phase-details.md](references/phase-details.md)                 | Step 1-5の詳細が必要時 |
| スキル構造ガイド | [references/skill-structure-guide.md](references/skill-structure-guide.md) | 構造確認が必要時       |

### assets/（テンプレート）

| アセット                   | 用途                     |
| -------------------------- | ------------------------ |
| `assets/skill-template.md` | スキル作成チェックリスト |

---

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠で全面改訂 |
| 1.0.0   | 2025-12-28 | 初版作成                       |
