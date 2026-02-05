---
name: tdd-principles
description: |
  テストファーストで仕様を定義し、Red-Green-Refactorを小さなステップで回すためのスキル。
  設計の創発とレガシー対応まで含めて、テスト駆動開発の実務判断を支援する。

  Anchors:
  • Test-Driven Development: By Example / 適用: TDDサイクル / 目的: 仕様の明確化
  • xUnit Test Patterns / 適用: テスト設計 / 目的: 表現の一貫性
  • Working Effectively with Legacy Code / 適用: レガシー適用 / 目的: 安全な変更

  Trigger:
  Use when planning or executing test-driven development, defining test-first strategy, or reviewing red-green-refactor quality.
  TDD, test-first, red-green-refactor, small steps, refactoring
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# tdd-principles

## 概要

テストファーストからRed-Green-Refactorを通じて設計を育てる実践ガイドを提供するスキル。

---

## ワークフロー

### Phase 1: テスト意図の設計

**目的**: 期待する振る舞いを先に定義し、テスト候補を整理する。

**アクション**:

1. 目的と期待結果を明文化する
2. 失敗条件と優先度を付与する
3. テストチャーターをまとめる

**Task**: `agents/test-design.md` を参照

### Phase 2: Red-Green-Refactor実行

**目的**: 小さなサイクルでテストと実装を進める。

**アクション**:

1. Red: 失敗するテストを確認する
2. Green: 最小実装でテストを通す
3. Refactor: 設計を改善し記録する

**Task**: `agents/red-green-cycle.md` を参照

### Phase 3: 設計レビューと拡張

**目的**: 設計品質を見直し、次のテスト拡張方針を決定する。

**アクション**:

1. 改善点と重複を抽出する
2. リファクタ候補を優先付けする
3. 追加テストの方向性を決める

**Task**: `agents/refactor-review.md` を参照

---

## Task仕様ナビ

| Task             | 起動タイミング | 入力             | 出力                 |
| ---------------- | -------------- | ---------------- | -------------------- |
| test-design      | Phase 1開始時  | 要求・仕様       | テストチャーター     |
| red-green-cycle  | Phase 2開始時  | テストチャーター | サイクルログ         |
| refactor-review  | Phase 3開始時  | サイクルログ     | 改善レビュー         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由                               |
| -------------------------------- | ---------------------------------- |
| 失敗理由が明確なテストを書く     | Redの品質が向上する                |
| 1テスト1振る舞いを維持する       | テストの意図が明確になる           |
| 最小実装を徹底する               | 余計な設計を避けられる             |
| Refactorを毎サイクルで行う       | 設計品質を保ちやすい               |

### 避けるべきこと

| 禁止事項                     | 問題点                             |
| ---------------------------- | ---------------------------------- |
| テスト後付けで実装を進める   | TDDの意図が失われる               |
| 大きな変更を一度に行う       | 失敗原因の特定が困難になる         |
| リファクタを後回しにする     | 技術的負債が蓄積する               |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト                         | 機能                         |
| ---------------------------------- | ---------------------------- |
| `scripts/validate-tdd-plan.mjs`    | セッション計画を検証する     |
| `scripts/tdd-cycle-validator.mjs`  | テストファイルを検証する     |
| `scripts/log_usage.mjs`            | 使用記録をLOGS.mdに記録する  |

### references/（詳細知識）

| リソース              | パス                                                     | 読込条件     |
| --------------------- | -------------------------------------------------------- | ------------ |
| 基礎                  | [references/Level1_basics.md](references/Level1_basics.md) | 初回利用時   |
| 実務パターン          | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 実務適用時   |
| 設計強化              | [references/Level3_advanced.md](references/Level3_advanced.md) | 設計改善時   |
| エキスパート          | [references/Level4_expert.md](references/Level4_expert.md) | 高難度対応時 |
| テストファースト原則  | [references/test-first-principles.md](references/test-first-principles.md) | Phase 1      |
| Red-Green-Refactor    | [references/red-green-refactor.md](references/red-green-refactor.md) | Phase 2      |
| 小さなステップ        | [references/small-steps.md](references/small-steps.md) | 全フェーズ   |
| 設計の創発            | [references/design-emergence.md](references/design-emergence.md) | Phase 3      |
| レガシー戦略          | [references/legacy-code-strategies.md](references/legacy-code-strategies.md) | レガシー対応 |

### assets/（テンプレート）

| アセット                                | 用途                       |
| --------------------------------------- | -------------------------- |
| `assets/tdd-session-template.md`        | TDDセッション計画          |
| `assets/test-charter-template.md`       | テスト設計チャーター       |

