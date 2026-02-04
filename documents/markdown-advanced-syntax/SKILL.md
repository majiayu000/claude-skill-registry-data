---
name: markdown-advanced-syntax
description: |
  技術ドキュメント向けMarkdown高度構文スキル。Mermaid図、複雑テーブル、コードブロック、数式表現を活用。

  Anchors:
  • GitHub Flavored Markdown Spec / 適用: 拡張構文 / 目的: プラットフォーム互換ドキュメント
  • CommonMark Spec / 適用: 基本構文 / 目的: クロスプラットフォーム互換性
  • Mermaid Official Docs / 適用: ダイアグラム / 目的: ビジュアル技術文書

  Trigger:
  Use when creating technical documentation with Mermaid diagrams, complex tables,
  syntax-highlighted code blocks, mathematical expressions, or YAML front-matter.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Markdown Advanced Syntax

> **相対パス**: `SKILL.md`
> **読込条件**: スキル使用時（自動）

---

## 概要

Markdown 高度構文を活用した技術文書作成スキル。

**対象構文**:

| 構文         | 用途                         | ツール/仕様         |
| ------------ | ---------------------------- | ------------------- |
| Mermaid      | フロー図、シーケンス図、ER図 | Mermaid.js          |
| Tables       | データ構造、API仕様          | GFM Tables          |
| Code Blocks  | 実装例、設定サンプル         | Syntax Highlighting |
| Math         | 数式、アルゴリズム表現       | LaTeX/KaTeX         |
| Front-matter | メタデータ定義               | YAML                |

---

## ワークフロー

### Phase 1: 文書設計

**Task**: `agents/planning.md`

| 入力       | 出力         |
| ---------- | ------------ |
| 文書化要求 | 文書設計仕様 |

**参照**: `references/basics.md`

### Phase 2: 実装

**Task**: `agents/implementation.md`

| 入力         | 出力             |
| ------------ | ---------------- |
| 文書設計仕様 | 実装済み技術文書 |

**参照**: `references/patterns.md`, 構文別リソース

### Phase 3: 検証

**Task**: `agents/validation.md`

| 入力             | 出力         |
| ---------------- | ------------ |
| 実装済み技術文書 | 検証レポート |

---

## ベストプラクティス

| すべきこと                         | 避けるべきこと          |
| ---------------------------------- | ----------------------- |
| 複雑なフローを Mermaid で図解      | 検証なしの Mermaid 出力 |
| API/データモデルを表形式で整理     | 過度に複雑なネスト表    |
| コード例に言語タイプと説明を含める | コード例の省略          |
| 数式は LaTeX 表記で正確に表現      | プレーンテキスト数式    |
| YAML front-matter でメタデータ定義 | メタデータなしの文書    |

---

## Task ナビゲーション

| Task                | 目的                         | 参照リソース          |
| ------------------- | ---------------------------- | --------------------- |
| `planning.md`       | 目的・対象読者・構文要素特定 | `basics.md`           |
| `implementation.md` | 技術文書の実装               | `patterns.md`, 構文別 |
| `validation.md`     | 品質検証                     | scripts               |

---

## リソース参照

### References

| ファイル              | 内容                            | 読込条件       |
| --------------------- | ------------------------------- | -------------- |
| `basics.md`           | Markdown 基礎構文・用語         | 初回使用時     |
| `patterns.md`         | 高度構文パターン・組み合わせ    | 実装時         |
| `mermaid-diagrams.md` | フロー/シーケンス/ER/状態遷移図 | 図解時         |
| `advanced-tables.md`  | 複雑テーブル・カラム整列        | テーブル作成時 |
| `code-blocks.md`      | 言語ハイライト・差分表示        | コード記載時   |
| `math-expressions.md` | LaTeX/KaTeX 数式記法            | 数式記載時     |
| `front-matter.md`     | YAML メタデータ定義             | 文書作成時     |

### Assets

| ファイル                    | 内容               |
| --------------------------- | ------------------ |
| `specification-template.md` | 仕様書テンプレート |

### Scripts

| スクリプト             | 用途             |
| ---------------------- | ---------------- |
| `validate-mermaid.mjs` | Mermaid 構文検証 |
| `log_usage.mjs`        | 使用記録         |

---

## 関連スキル

- `api-documentation-best-practices` - API ドキュメント
- `tutorial-design` - チュートリアル設計
- `output-formatting` - 出力フォーマット
