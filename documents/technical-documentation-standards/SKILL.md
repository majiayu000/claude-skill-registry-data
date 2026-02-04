---
name: technical-documentation-standards
description: |
  IEEE 830やDoc as Codeなどの標準に基づき、技術文書の構造と品質基準を整えるスキル。
  テンプレート適用と検証フローを通じて、再利用性と明確性を高める。

  Anchors:
  • IEEE 830 / 適用: 仕様書構造 / 目的: 標準化
  • Documentation as Code / 適用: 文書運用 / 目的: 継続的管理
  • Software Requirements (Karl Wiegers) / 適用: 要求記述 / 目的: 明確性

  Trigger:
  Use when defining documentation standards, creating SRS templates, or reviewing technical docs for consistency.
  documentation standards, IEEE 830, SRS, doc-as-code, documentation review
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
---

# technical-documentation-standards

## 概要

技術文書の標準構造、テンプレート適用、品質検証を一貫して実行するスキル。

---

## ワークフロー

### Phase 1: 文書標準の定義

**目的**: 文書タイプに応じた標準構造と品質基準を確定する。

**アクション**:

1. 文書目的と対象読者を整理する
2. 必須セクションと品質基準を定義する
3. 標準構成を文書化する

**Task**: `agents/define-standard.md` を参照

### Phase 2: テンプレート適用

**目的**: 標準に基づき文書の構成を整備する。

**アクション**:

1. テンプレートを選定する
2. 章構成に沿って内容を配置する
3. 重複表現を統合する

**Task**: `agents/apply-template.md` を参照

### Phase 3: 文書検証と品質レビュー

**目的**: 明確性とDRY観点で品質を検証する。

**アクション**:

1. 構造の抜け漏れを検証する
2. DRY違反を検出する
3. 改善提案を整理する

**Task**: `agents/verify-document.md` を参照

---

## Task仕様ナビ

| Task             | 起動タイミング | 入力             | 出力                 |
| ---------------- | -------------- | ---------------- | -------------------- |
| define-standard  | Phase 1開始時  | 文書目的         | 文書標準定義         |
| apply-template   | Phase 2開始時  | 文書標準定義     | 初期文書ドラフト     |
| verify-document  | Phase 3開始時  | 初期文書ドラフト | 品質レビュー報告     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由                               |
| -------------------------------- | ---------------------------------- |
| 目的と対象読者を明確にする       | 文書の粒度が揃う                   |
| テンプレートを使って構成を統一   | 品質のばらつきを抑える             |
| DRY違反を定期的に検出する         | 保守性が高まる                     |

### 避けるべきこと

| 禁止事項                     | 問題点                             |
| ---------------------------- | ---------------------------------- |
| 標準を定義せずに文書化する   | ばらつきが大きくなる               |
| テンプレートを無視する       | 再利用性が低下する                 |
| 検証を省略する               | 品質低下に気づきにくい             |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト                               | 機能                         |
| ---------------------------------------- | ---------------------------- |
| `scripts/validate-doc-structure.mjs`     | 文書構造を検証する           |
| `scripts/check-dry-violations.mjs`       | DRY違反を検出する            |
| `scripts/log_usage.mjs`                  | 使用記録をLOGS.mdに記録する  |

### references/（詳細知識）

| リソース            | パス                                                     | 読込条件     |
| ------------------- | -------------------------------------------------------- | ------------ |
| 基礎                | [references/Level1_basics.md](references/Level1_basics.md) | 初回利用時   |
| 実務                | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 実務適用時 |
| 高度設計            | [references/Level3_advanced.md](references/Level3_advanced.md) | 品質改善時 |
| エキスパート        | [references/Level4_expert.md](references/Level4_expert.md) | 組織適用時 |
| IEEE 830概要        | [references/ieee-830-overview.md](references/ieee-830-overview.md) | Phase 1 |
| Doc as Code         | [references/doc-as-code.md](references/doc-as-code.md) | Phase 2 |
| DRY適用             | [references/dry-for-documentation.md](references/dry-for-documentation.md) | Phase 2 |
| 明確性チェック      | [references/clarity-checklist.md](references/clarity-checklist.md) | Phase 3 |
| 検証パターン        | [references/verification-patterns.md](references/verification-patterns.md) | Phase 3 |

### assets/（テンプレート）

| アセット                             | 用途                       |
| ------------------------------------ | -------------------------- |
| `assets/srs-template.md`             | SRS作成テンプレート        |
| `assets/document-review-checklist.md` | 文書レビューのチェックリスト |

