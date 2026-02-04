---
name: sprint-planning
description: |
  スプリント計画の体系的な立案と実行管理を支援するスキル。
  チームキャパシティの可視化、タスク分解、リスク管理を通じて、
  価値提供と持続可能な速度（サステーナブルペース）を両立させる。

  Anchors:
  • Agile Estimating and Planning (Mike Cohn) / 適用: 見積もり・計画手法 / 目的: スプリント計画の方法論習得
  • Scrum Guide / 適用: スプリント計画イベント / 目的: 公式フレームワークとの整合
  • ストーリーポイント / 適用: キャパシティ計算・タスク見積もり / 目的: チーム能力の可視化と予測精度向上

  Trigger:
  Use when planning sprints, calculating team capacity, estimating stories, setting sprint goals, or managing iteration cycles.
  sprint planning, agile, iteration, capacity, velocity, story points, sprint goal, scrum
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# スプリント計画

## 概要

チームの能力を可視化し、スプリント内で実現可能な価値提供計画を立案するスキル。
キャパシティプランニング、タスク分解、リスク管理の段階的ワークフローで、
持続可能な開発速度と高い予測精度を実現する。

## ワークフロー

```
prepare-sprint → plan-capacity → estimate-items → commit-scope → track-progress
```

### Phase 1: スプリント準備

**目的**: スプリント計画に必要な基礎情報を整理する

**アクション**:

1. チームメンバーのキャパシティ（稼働日数・休暇）を把握する
2. 前スプリントの実績（ベロシティ）を確認する
3. プロダクトバックログの優先順位を確認する

**Task**: `agents/prepare-sprint.md` を参照

### Phase 2: キャパシティ計算

**目的**: チームの実働能力を定量化する

**アクション**:

1. `scripts/calculate-capacity.mjs` でキャパシティを計算する
2. 休暇・祝日・その他の予定を反映する
3. 前スプリントのベロシティと比較検証する

**参照**: `references/capacity-planning.md`

**Task**: `agents/plan-capacity.md` を参照

### Phase 3: アイテム見積もり

**目的**: バックログアイテムの工数を見積もる

**アクション**:

1. プランニングポーカー等で見積もりを実施する
2. 技術的リスクと依存関係を洗い出す
3. タスク分解と責任者アサインを行う

**Task**: `agents/estimate-items.md` を参照

### Phase 4: スコープ確定

**目的**: スプリントゴールとコミットメントを決定する

**アクション**:

1. キャパシティに基づきスコープを確定する
2. スプリントゴールを設定する
3. 完了定義（DoD）を確認する

**テンプレート**: `assets/sprint-plan-template.md` を使用

**Task**: `agents/commit-scope.md` を参照

## Task仕様ナビ

| Task           | 起動タイミング | 入力                             | 出力                     |
| -------------- | -------------- | -------------------------------- | ------------------------ |
| prepare-sprint | Phase 1開始時  | 前スプリント実績、チーム情報     | スプリント準備レポート   |
| plan-capacity  | Phase 2開始時  | チーム稼働予定、ベロシティ履歴   | キャパシティ計算結果     |
| estimate-items | Phase 3開始時  | バックログアイテム、キャパシティ | 見積もり済みアイテム一覧 |
| commit-scope   | Phase 4開始時  | 見積もり結果、キャパシティ       | スプリント計画書         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                             |
| ---------------------------------- | -------------------------------- |
| 計画セッション前の準備を徹底する   | 会議効率化と質の向上             |
| ベロシティに基づくキャパシティ計算 | 楽観的見積もりを避け現実的な計画 |
| スプリントゴールを明確化する       | 全員の方向性を統一               |
| 完了定義を厳格に適用する           | 品質の一貫性を担保               |
| 日次トラッキングと早期対応         | 問題の早期発見と対処             |

### 避けるべきこと

| 禁止事項                               | 問題点                       |
| -------------------------------------- | ---------------------------- |
| 楽観的な見積もりと過度なコミットメント | バーンアウトと品質低下       |
| 依存関係の無視                         | ブロッカーによる遅延         |
| 完了定義の曖昧さ                       | 品質のばらつき               |
| スプリント途中での無制限なスコープ追加 | スコープクリープと予測不能化 |
| レトロスペクティブの省略               | 改善機会の喪失               |

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                           | 読込条件           |
| -------------------- | ------------------------------------------------------------------------------ | ------------------ |
| キャパシティ計算詳細 | [references/capacity-planning.md](references/capacity-planning.md)             | キャパシティ計算時 |
| キャパシティガイド   | [references/capacity-planning-guide.md](references/capacity-planning-guide.md) | 初回計画時         |

### scripts/（決定論的処理）

| スクリプト               | 機能                   | 使用例                                            |
| ------------------------ | ---------------------- | ------------------------------------------------- |
| `calculate-capacity.mjs` | チームキャパシティ計算 | `node scripts/calculate-capacity.mjs --members 5` |
| `log_usage.mjs`          | 使用記録の保存         | `node scripts/log_usage.mjs --result success`     |
| `validate-skill.mjs`     | スキル構造検証         | `node scripts/validate-skill.mjs`                 |

### assets/（テンプレート）

| アセット                      | 用途                       |
| ----------------------------- | -------------------------- |
| `sprint-plan-template.md`     | スプリント計画テンプレート |
| `sprint-planning-template.md` | スプリント計画フォーム     |

## 変更履歴

| Version | Date       | Changes                                          |
| ------- | ---------- | ------------------------------------------------ |
| 3.0.0   | 2026-01-03 | 18-skills.md仕様に完全準拠、agents追加、構造再編 |
| 2.0.0   | 2025-12-31 | ワークフロー改善、Task仕様ナビ追加               |
| 1.0.0   | 2025-12-24 | 初版作成                                         |
