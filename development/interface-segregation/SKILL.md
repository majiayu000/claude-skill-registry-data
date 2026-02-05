---
name: interface-segregation
description: |
  SOLID原則のインターフェース分離原則（ISP）を専門とするスキル。
  クライアントが使用しないメソッドへの依存を強制しない設計を実現する。

  Anchors:
  • 『アジャイルソフトウェア開発の奥義』（Robert C. Martin） / 適用: ISP原則の定義と実践 / 目的: クライアント固有インターフェース設計
  • 『Refactoring』（Martin Fowler） / 適用: Extract Interface, Decompose Interface / 目的: 段階的な分離リファクタリング
  • 『Test-Driven Development』（Kent Beck） / 適用: Simple Design, テスト容易性評価 / 目的: 設計品質検証

  Trigger:
  Use when detecting fat interfaces, segregating bloated interfaces, designing role-based interfaces,
  analyzing ISP violations, refactoring interfaces, implementing interface composition patterns,
  IWorkflowExecutor, IValidatable, IRetryable, empty implementation, exception throwing, conditional implementation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
version: 1.0.0
last_updated: 2025-12-31
tags:
  - solid
  - interface-design
  - architecture
  - refactoring
dependencies:
  - clean-architecture-principles
---

# インターフェース分離原則 (ISP)

## 概要

SOLID原則のインターフェース分離原則（ISP）を専門とするスキル。
Robert C. Martinの『アジャイルソフトウェア開発の奥義』に基づき、
クライアントが使用しないメソッドへの依存を強制しない設計を実現する。

**コア原則**: 「クライアントに不要なメソッドへの依存を強制しない」

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

---

## ワークフロー

### Phase 1: Interface Analysis（分析フェーズ）

**目的**: 既存または新規インターフェースのISP違反を検出

**Task**: `agents/analyze-interfaces.md`（Robert C. Martin手法）

**実行条件**:

- 既存インターフェースの肥大化が疑われる時
- 新規設計のレビューが必要な時
- クライアントが異なる機能セットを必要とする時

**入力**:

- インターフェース定義（TypeScript/Java/C#等）
- クライアントコード（任意、使用パターン分析用）

**出力**:

- インターフェース分析レポート（メトリクス、ISP違反パターン）
- 分離候補リスト（責務グループごとのメソッド分類）

**参照リソース**:

- `references/fat-interface-detection.md`: 肥大化検出手法
- `references/isp-principles.md`: ISP原則の詳細
- `scripts/analyze-interface.mjs`: 自動分析ツール

---

### Phase 2: Interface Segregation Design（設計フェーズ）

**目的**: 分析結果に基づき、インターフェースを適切に分離

**Task**: `agents/design-segregation.md`（Martin Fowler手法）

**実行条件**:

- Phase 1で分離推奨度がMedium以上
- 責務グループが2つ以上特定された時

**入力**:

- インターフェース分析レポート（Phase 1の出力）
- プロジェクト言語仕様（TypeScript/Java/C#等）

**出力**:

- 分離インターフェース設計書（完全な設計ドキュメント）
- 実装コードスニペット（対象言語での実装例）

**参照リソース**:

- `references/role-interface-design.md`: 役割ベース設計手法
- `references/interface-composition.md`: allOf/extends/mixin パターン
- `assets/segregated-interface-template.md`: 設計テンプレート

---

### Phase 3: Design Validation（検証フェーズ）

**目的**: 設計品質の検証と実装可否の判定

**Task**: `agents/validate-design.md`（Kent Beck手法）

**実行条件**:

- Phase 2で設計書が作成された時
- 実装前の最終チェックが必要な時

**入力**:

- 分離インターフェース設計書（Phase 2の出力）
- 元のインターフェース定義（互換性チェック用）
- クライアントコード（任意）

**出力**:

- 検証結果レポート（Pass/Fail/Warning）
- 改善提案リスト（問題検出時）

**参照リソース**:

- `references/Level3_advanced.md`: 高度な検証手法
- `scripts/analyze-interface.mjs`: メトリクス測定

---

### Phase 4: Feedback Recording（記録フェーズ）

**目的**: 実行結果の記録と継続的改善

**アクション**:

1. `scripts/log_usage.mjs` を実行して使用履歴を記録
2. 成功/失敗の理由をメモとして残す
3. 改善提案を `LOGS.md` に追記

**実行形式**:

```bash
node .claude/skills/interface-segregation/scripts/log_usage.mjs \
  --result success \
  --phase "{{phase-name}}" \
  --task "{{task-name}}" \
  --notes "{{feedback}}"
```

---

## Task仕様（ナビゲーション）

各Taskは `agents/` ディレクトリに配置され、実行直前にロードされます。

| Task名                 | 役割                     | 専門家           | 入力                 | 出力                     |
| ---------------------- | ------------------------ | ---------------- | -------------------- | ------------------------ |
| **analyze-interfaces** | ISP違反検出              | Robert C. Martin | インターフェース定義 | 分析レポート、分離候補   |
| **design-segregation** | インターフェース分離設計 | Martin Fowler    | 分析レポート         | 設計書、コードスニペット |
| **validate-design**    | 設計品質検証             | Kent Beck        | 設計書               | 検証レポート、改善提案   |

**読み込みタイミング**:

- Phase開始時に該当Taskのみロード
- 複数Taskを同時にロードしない（コンテキスト節約）

---

## ベストプラクティス

### すべきこと

- IWorkflowExecutorのようなコアインターフェースを設計する時
- 既存インターフェースの肥大化を検出した時（メソッド数>10が目安）
- 複数のクライアントが異なる機能を必要とする時
- 空実装、例外スロー、条件付き実装のパターンを発見した時
- `scripts/analyze-interface.mjs` で定量分析を実施
- テンプレート `assets/segregated-interface-template.md` を活用

### 避けるべきこと

- 分析なしに直感だけでインターフェースを分離する
- 過剰な分離（インターフェースが10個以上）
- 責務が不明確な命名（IData, IHelper等）
- 既存クライアントへの破壊的変更を考慮しない
- 検証フェーズをスキップする

---

## リソース参照

### references/ ディレクトリ

**段階的学習**:

- `Level1_basics.md`: ISPの基礎、Fat Interface検出の基本
- `Level2_intermediate.md`: 役割ベース設計、リファクタリング手法
- `Level3_advanced.md`: 合成パターン、高度な分離戦略
- `Level4_expert.md`: アーキテクチャレベルのISP適用、移行戦略

**専門知識**:

- `isp-principles.md`: ISP原則の定義と設計指針
- `fat-interface-detection.md`: 空実装/例外スロー/条件付き実装による検出
- `role-interface-design.md`: IValidatable/IRetryable等の役割ベース設計
- `interface-composition.md`: allOf/extends/mixin による組み合わせパターン

**プロジェクト連携**:

- `requirements-index.md`: 要求仕様の索引（docs/00-requirements と同期）

---

## scripts/ ディレクトリ

| スクリプト名              | 機能                                      | 引数                                                            |
| ------------------------- | ----------------------------------------- | --------------------------------------------------------------- |
| **analyze-interface.mjs** | インターフェース凝集性とISP違反の自動検出 | `--file <path>`                                                 |
| **log_usage.mjs**         | 使用記録・自動評価                        | `--result <success\|failure>` `--phase <name>` `--notes <text>` |
| **validate-skill.mjs**    | スキル構造検証                            | なし                                                            |

**実行例**:

```bash
# インターフェース分析
node scripts/analyze-interface.mjs --file src/interfaces/IWorkflow.ts

# 使用記録
node scripts/log_usage.mjs --result success --phase analyze --notes "Detected 3 responsibility groups"

# スキル構造検証
node scripts/validate-skill.mjs
```

---

## assets/ ディレクトリ

| テンプレート名                       | 用途                                          |
| ------------------------------------ | --------------------------------------------- |
| **segregated-interface-template.md** | コア+拡張インターフェース分離設計テンプレート |

**使用方法**:
Phase 2（design-segregation）で設計書作成時に使用。
責務グループごとにインターフェースを定義し、合成パターンで組み合わせる。

---

## メトリクスとフィードバック

### 評価指標

**定量的メトリクス**（EVALS.json で追跡）:

- 使用回数、成功率
- Task別成功率（analyze/design/validate）
- 平均メソッド削減数、凝集性改善度

**定性的指標**:

- クライアント満足度
- 保守性向上度
- テスト容易性改善度

### レベル基準

| レベル  | 使用回数 | 成功率 | 習熟度                               |
| ------- | -------- | ------ | ------------------------------------ |
| Level 1 | 0+       | -      | ISPと肥大化検出の基礎理解            |
| Level 2 | 5+       | 60%+   | インターフェース分離設計の習熟       |
| Level 3 | 15+      | 75%+   | 合成パターンの高度な適用             |
| Level 4 | 30+      | 85%+   | アーキテクチャレベルの設計と移行戦略 |

---

## コマンドリファレンス

### リソース読み取り

```bash
# 段階的学習
cat .claude/skills/interface-segregation/references/Level1_basics.md
cat .claude/skills/interface-segregation/references/Level2_intermediate.md
cat .claude/skills/interface-segregation/references/Level3_advanced.md
cat .claude/skills/interface-segregation/references/Level4_expert.md

# 専門知識
cat .claude/skills/interface-segregation/references/isp-principles.md
cat .claude/skills/interface-segregation/references/fat-interface-detection.md
cat .claude/skills/interface-segregation/references/role-interface-design.md
cat .claude/skills/interface-segregation/references/interface-composition.md
```

### Task実行

```bash
# 各Taskは agents/ に配置
cat .claude/skills/interface-segregation/agents/analyze-interfaces.md
cat .claude/skills/interface-segregation/agents/design-segregation.md
cat .claude/skills/interface-segregation/agents/validate-design.md
```

### スクリプト実行

```bash
node .claude/skills/interface-segregation/scripts/analyze-interface.mjs --help
node .claude/skills/interface-segregation/scripts/log_usage.mjs --help
node .claude/skills/interface-segregation/scripts/validate-skill.mjs --help
```

### テンプレート参照

```bash
cat .claude/skills/interface-segregation/assets/segregated-interface-template.md
```

---

## 変更履歴

| Version | Date       | Changes                                                                                                        |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様に準拠した構造改善。agents/ にTask仕様追加、EVALS.json/LOGS.md作成、Progressive Disclosure適用 |
| 0.9.0   | 2025-12-24 | Spec alignment and required artifacts added                                                                    |
