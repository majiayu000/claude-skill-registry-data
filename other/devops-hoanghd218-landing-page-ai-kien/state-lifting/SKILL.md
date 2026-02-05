---
name: state-lifting
description: |
  Reactにおける状態リフティングと状態配置判断を支援するスキル。
  兄弟コンポーネント間の状態共有、Prop Drilling削減、Context導入判断、
  Compound Componentパターンまで、React状態管理の全体像を扱う。

  Anchors:
  • React Documentation (Lifting State Up) / 適用: 共有状態の配置判断 / 目的: 最小責務での共有設計
  • Thinking in React / 適用: 状態配置の判断フロー / 目的: 最適な状態配置の特定
  • Kent C. Dodds (Colocation) / 適用: 状態と利用箇所の距離 / 目的: 保守性とパフォーマンスの両立

  Trigger:
  Use when lifting state between components, sharing state across siblings, reducing prop drilling, deciding on Context usage, or implementing compound components.
  state lifting, prop drilling, context api, state placement, compound component, react state, colocation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 状態リフティング

## 概要

共有状態の配置と伝播設計を整理し、最小限の状態リフティングで一貫したデータフローを維持するスキル。
Reactにおける状態管理の基本原則から高度なパターンまでをカバーする。

## ワークフロー

```
analyze-requirements → design-state-placement → implement-lifting → evaluate-context → apply-patterns
```

### Phase 1: 状態共有の要件整理

**目的**: 共有状態と共通親の候補を特定する

**アクション**:

1. コンポーネントツリーを把握する
2. 状態を使用するコンポーネントを列挙する
3. 最も近い共通親を特定する

**参照**: `references/state-placement-guide.md`

**Task**: `agents/sl-001-analyze-requirements.md` を参照

### Phase 2: Props経由の状態伝播

**目的**: 状態と更新関数をpropsで一方向に伝播する

**アクション**:

1. 親コンポーネントに状態を集約する
2. 子コンポーネントへpropsで伝播する
3. 更新関数をメモ化し依存関係を整理する

**参照**: `references/colocation-principles.md`

**Task**: `agents/sl-003-props-state-passing.md` を参照

### Phase 3: Context導入判断

**目的**: Prop Drillingが過剰な場合にContext導入を判断する

**アクション**:

1. Props伝播階層と頻度を確認する
2. Prop Drillingの負荷を評価する
3. Context導入のメリット/デメリットを整理する

**参照**: `references/prop-drilling-solutions.md`, `references/context-patterns.md`

**Task**: `agents/sl-005-context-api-introduction.md` を参照

### Phase 4: 複合コンポーネント設計

**目的**: Compound Componentで共有状態を局所化する

**アクション**:

1. 共有状態を局所化する構成を決める
2. 子コンポーネントの役割を定義する
3. APIと使用例を設計する

**テンプレート**: `assets/compound-component-template.md`

**Task**: `agents/sl-007-compound-component-pattern.md` を参照

## Task仕様ナビ

| Task                              | 起動タイミング | 入力                         | 出力                   |
| --------------------------------- | -------------- | ---------------------------- | ---------------------- |
| sl-001-analyze-requirements       | Phase 1開始時  | コンポーネント情報、状態一覧 | 状態共有要件レポート   |
| sl-003-props-state-passing        | Phase 2開始時  | 状態共有要件、既存コード     | Props伝播設計          |
| sl-005-context-api-introduction   | Phase 3開始時  | Props伝播設計                | Context導入判断        |
| sl-007-compound-component-pattern | Phase 4開始時  | Context判断、設計要件        | Compound Component設計 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                           |
| ---------------------------------- | ------------------------------ |
| 共通親が最小の箇所に状態を配置する | 過度なリフティングを避けられる |
| Props経由の一方向フローを維持する  | デバッグ容易性が高まる         |
| Context導入は必要最小限に留める    | 依存範囲が広がり過ぎるのを防ぐ |
| 派生状態は計算で済ませる           | 状態重複を避けられる           |
| コンポジションパターンを検討する   | Prop Drillingを根本解決できる  |

### 避けるべきこと

| 禁止事項                    | 問題点                   |
| --------------------------- | ------------------------ |
| 深いProp Drillingを放置     | 保守性と可読性が低下する |
| 不要なグローバル化          | 影響範囲が拡大する       |
| 状態の重複管理              | 不整合が発生する         |
| Contextの乱用               | 再レンダリングを誘発する |
| 高頻度更新データをContext化 | パフォーマンスが劣化する |

## リソース参照

### references/（詳細知識）

| リソース          | パス                                                                           | 読込条件                   |
| ----------------- | ------------------------------------------------------------------------------ | -------------------------- |
| 状態配置ガイド    | [references/state-placement-guide.md](references/state-placement-guide.md)     | 共有状態の配置判断時       |
| Prop Drilling対策 | [references/prop-drilling-solutions.md](references/prop-drilling-solutions.md) | Prop Drilling対策検討時    |
| Contextパターン   | [references/context-patterns.md](references/context-patterns.md)               | Context導入判断時          |
| Colocation原則    | [references/colocation-principles.md](references/colocation-principles.md)     | 状態と利用箇所の距離判断時 |

### scripts/（決定論的処理）

| スクリプト                    | 機能           | 使用例                                                |
| ----------------------------- | -------------- | ----------------------------------------------------- |
| `analyze-state-structure.mjs` | 状態構造の分析 | `node scripts/analyze-state-structure.mjs <file.tsx>` |
| `log_usage.mjs`               | 使用記録の保存 | `node scripts/log_usage.mjs --result success`         |
| `validate-skill.mjs`          | スキル構造検証 | `node scripts/validate-skill.mjs`                     |

### assets/（テンプレート）

| アセット                         | 用途                         |
| -------------------------------- | ---------------------------- |
| `compound-component-template.md` | Compound Component概要・索引 |
| `select-template.md`             | Selectコンポーネント         |
| `accordion-template.md`          | アコーディオンコンポーネント |
| `tabs-template.md`               | タブコンポーネント           |
| `modal-template.md`              | モーダルコンポーネント       |
| `context-provider-template.md`   | Context Providerテンプレート |

## 変更履歴

| Version | Date       | Changes                                       |
| ------- | ---------- | --------------------------------------------- |
| 2.2.0   | 2026-01-06 | compound-component-template分割、実装事例追加 |
| 2.1.0   | 2026-01-03 | 18-skills.md仕様に完全準拠、構造整理          |
| 2.0.0   | 2026-01-02 | ワークフロー再編                              |
| 1.0.0   | 2025-12-28 | 初版作成                                      |
