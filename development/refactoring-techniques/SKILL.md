---
name: refactoring-techniques
description: |
  マーティン・ファウラーの『Refactoring』に基づくコード改善技術を提供するスキル。
  外部動作を変えずに内部構造を改善する体系的手法を通じて、保守性・可読性を向上させる。

  Anchors:
  • Refactoring (Martin Fowler) / 適用: 全般 / 目的: 体系的なリファクタリング手法
  • Clean Code (Robert C. Martin) / 適用: 命名・構造 / 目的: 可読性向上
  • Working Effectively with Legacy Code (Michael Feathers) / 適用: レガシー対応 / 目的: 安全なリファクタリング

  Trigger:
  Use when improving code structure, detecting code smells, reducing technical debt, or refactoring legacy code.
  refactoring, code smell, extract method, decompose conditional, technical debt, リファクタリング
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
---

# リファクタリング技法

## 概要

外部から見た振る舞いを変えずに、内部構造を改善する体系的手法を提供するスキル。
コードスメルの検出、適切なリファクタリングパターンの選択、テスト保護下での安全な実施を支援する。

---

## ワークフロー

### Phase 1: コードスメル分析

**目的**: リファクタリングが必要な箇所を特定する

**アクション**:

1. 対象コードをスキャンしてコードスメルを検出
2. 優先度に基づいて対処順序を決定
3. 影響範囲と依存関係を把握

**Task**: `agents/analyze-code-smells.md` を参照

### Phase 2: リファクタリング計画

**目的**: 適切なリファクタリングパターンを選択し計画を立てる

**アクション**:

1. 検出されたスメルに対応するパターンを選択
2. 段階的な実施計画を策定
3. テスト戦略を確認

**Task**: `agents/plan-refactoring.md` を参照

### Phase 3: リファクタリング実施

**目的**: 計画に基づいて安全にリファクタリングを実行

**アクション**:

1. テストが通ることを確認
2. 小さな変更を順次適用
3. 各ステップでテストを実行
4. 完了後に全テストを実行

**Task**: `agents/apply-refactoring.md` を参照

---

## Task仕様ナビ

| Task                | 起動タイミング | 入力                 | 出力                       |
| ------------------- | -------------- | -------------------- | -------------------------- |
| analyze-code-smells | Phase 1開始時  | ソースコード         | スメル検出レポート         |
| plan-refactoring    | Phase 2開始時  | スメル検出レポート   | リファクタリング計画書     |
| apply-refactoring   | Phase 3開始時  | リファクタリング計画 | リファクタリング済みコード |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

- テストが通っている状態でのみリファクタリングを開始する
- 一度に一つのリファクタリングに集中する
- 小さなコミットで変更を記録する
- 変更後は必ずテストを実行する
- コードの意図を明確にする命名を心がける

### 避けるべきこと

- テストなしでのリファクタリング
- 複数のリファクタリングの同時実施
- 外部インターフェースの変更
- パフォーマンスを検証せずに進める
- リファクタリングと機能追加の混在

---

## リソース参照

### references/（詳細知識）

| リソース   | パス                                                   | 読込条件                     |
| ---------- | ------------------------------------------------------ | ---------------------------- |
| 基本概念   | [references/basics.md](references/basics.md)           | 原則と基本手法を確認するとき |
| パターン集 | [references/patterns.md](references/patterns.md)       | 具体的な手法を参照するとき   |
| スメル検出 | [references/code-smells.md](references/code-smells.md) | コードスメルを特定するとき   |

### scripts/（検証・実行）

| スクリプト                 | 用途                 | 使用例                                                   |
| -------------------------- | -------------------- | -------------------------------------------------------- |
| `detect-code-smells.mjs`   | コードスメル検出     | `node scripts/detect-code-smells.mjs <file>`             |
| `validate-refactoring.mjs` | リファクタリング検証 | `node scripts/validate-refactoring.mjs --before --after` |
| `log_usage.mjs`            | 使用記録             | `node scripts/log_usage.mjs --result success`            |

### assets/（テンプレート）

| テンプレート               | 用途                                 |
| -------------------------- | ------------------------------------ |
| `refactoring-checklist.md` | リファクタリング実施時チェックリスト |
| `refactoring-plan.md`      | リファクタリング計画テンプレート     |

---

## 変更履歴

| Version | Date       | Changes                                        |
| ------- | ---------- | ---------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠。agents追加、構造刷新 |
| 1.0.0   | 2025-12-31 | 初版作成                                       |
