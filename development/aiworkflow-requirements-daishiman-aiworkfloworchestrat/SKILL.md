---
name: aiworkflow-requirements
description: |
  AIWorkflowOrchestratorプロジェクトの仕様管理スキル。
  仕様書を検索・参照するためのインターフェース。
  references/配下に全仕様を格納し、キーワード検索で必要な情報に素早くアクセス。

  Anchors:
  • Specification-Driven Development / 適用: 仕様書正本 / 目的: 実装との一貫性
  • Progressive Disclosure / 適用: 検索→詳細参照 / 目的: コンテキスト効率化
  • MECE原則 / 適用: トピック分類 / 目的: 漏れなく重複なく

  Trigger:
  プロジェクト仕様の検索、アーキテクチャ確認、API設計参照、セキュリティ要件確認、テスト戦略参照を行う場合に使用。
  仕様, 要件, アーキテクチャ, API, データベース, セキュリティ, UI/UX, デプロイ, Claude Code, テスト, MSW, カバレッジ
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# AIWorkflow Requirements Manager

## 概要

AIWorkflowOrchestratorプロジェクトの全仕様（48ファイル・約17,000行）を管理するスキル。
**このスキルが仕様の正本**であり、references/配下のドキュメントを直接編集・参照する。

## ワークフロー

```
                    ┌→ search-spec ────┐
user-request → ┼                       ┼→ read-reference → apply-to-task
                    └→ browse-index ───┘
                              ↓
                    (仕様変更が必要な場合)
                              ↓
              ┌→ create-spec ──────────┐
              ┼                         ┼→ update-index → validate-structure
              └→ update-spec ──────────┘
```

## Task仕様

| Task               | 責務           | 実行パターン | 入力         | 出力             |
| ------------------ | -------------- | ------------ | ------------ | ---------------- |
| search-spec        | 仕様検索       | par          | キーワード   | ファイルパス一覧 |
| browse-index       | 全体像把握     | par          | なし         | トピック構造     |
| read-reference     | 仕様参照       | agg          | ファイルパス | 仕様内容         |
| create-spec        | 新規作成       | par          | 要件         | 新規仕様ファイル |
| update-spec        | 既存更新       | par          | 変更内容     | 更新済みファイル |
| update-index       | インデックス化 | agg          | references/  | indexes/         |
| validate-structure | 構造検証       | seq          | 全体         | 検証レポート     |

## リソース参照

### 仕様ファイル一覧

**48ファイル・10トピック**: See [indexes/topic-map.md](indexes/topic-map.md)

| トピック         | ファイル数 |
| ---------------- | ---------- |
| 概要・品質       | 4          |
| アーキテクチャ   | 6          |
| インターフェース | 6          |
| API設計          | 3          |
| データベース     | 3          |
| UI/UX            | 5          |
| セキュリティ     | 3          |
| 技術スタック     | 3          |
| Claude Code      | 6          |
| その他           | 9          |

**注記**: 18-skills.md（Skill層仕様書）は `skill-creator` スキルで管理。

### scripts/

| スクリプト               | 用途               | 使用例                                       |
| ------------------------ | ------------------ | -------------------------------------------- |
| `search-spec.mjs`        | キーワード検索     | `node scripts/search-spec.mjs "認証" -C 5`   |
| `list-specs.mjs`         | ファイル一覧       | `node scripts/list-specs.mjs --topics`       |
| `generate-index.mjs`     | インデックス再生成 | `node scripts/generate-index.mjs`            |
| `split-reference.mjs`    | 大ファイル分割     | `node scripts/split-reference.mjs --analyze` |
| `validate-structure.mjs` | 構造検証           | `node scripts/validate-structure.mjs`        |

### agents/

| エージェント       | 用途         | 対応Task           |
| ------------------ | ------------ | ------------------ |
| `create-spec.md`   | 新規仕様作成 | create-spec        |
| `update-spec.md`   | 既存仕様更新 | update-spec        |
| `validate-spec.md` | 仕様検証     | validate-structure |

### indexes/

| ファイル        | 内容                       |
| --------------- | -------------------------- |
| `topic-map.md`  | トピック別マップ（詳細）   |
| `keywords.json` | キーワード索引（自動生成） |

### assets/

| ファイル           | 用途                   |
| ------------------ | ---------------------- |
| `spec-template.md` | 新規仕様のテンプレート |

### references/（ガイドライン）

| ファイル             | 内容                       |
| -------------------- | -------------------------- |
| `spec-guidelines.md` | 命名規則・記述ガイドライン |

## ベストプラクティス

### すべきこと

- キーワード検索で情報を素早く特定
- 編集後は `node scripts/generate-index.mjs` を実行
- 500行超過時は `split-reference.mjs` で分割

### 避けるべきこと

- references/以外に仕様情報を分散
- インデックス更新を忘れる
- 詳細ルールをSKILL.mdに追加（→ spec-guidelines.md へ）

**詳細ルール**: See [references/spec-guidelines.md](references/spec-guidelines.md)

## 変更履歴

| Version | Date       | Changes                                         |
| ------- | ---------- | ----------------------------------------------- |
| 5.0.0   | 2026-01-04 | SKILL.md軽量化、詳細をindexes/references/へ分離 |
| 4.0.0   | 2026-01-03 | kebab-case化、大ファイル分割、47ファイル構成    |
| 3.0.0   | 2026-01-03 | 仕様正本化、検索中心に再設計                    |
