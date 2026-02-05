---
name: ubiquitous-language
description: |
  ドメイン駆動設計におけるユビキタス言語の確立と適用を専門とするスキル。
  ドメインエキスパートと開発者が共有する厳密な語彙体系を構築し、コミュニケーションの齟齬を防ぐ。

  Anchors:
  • Domain-Driven Design (Eric Evans) / 適用: ユビキタス言語の原則と実践 / 目的: コードとドメインの一貫性確保
  • Bounded Context / 適用: コンテキスト境界での用語の意味の違いを管理 / 目的: 用語の曖昧さ排除

  Trigger:
  Use when establishing domain terminology, creating glossaries, aligning business and technical vocabulary,
  extracting terms from requirements, defining ubiquitous language for DDD projects,
  resolving naming conflicts in code, or maintaining domain vocabulary consistency.
version: 1.2.0
tags:
  - domain-driven-design
  - terminology
  - glossary
  - naming
  - ubiquitous-language
---

# Ubiquitous Language

## 概要

ドメイン駆動設計におけるユビキタス言語の確立と適用を支援するスキル。
ドメインエキスパートと開発者が共有する厳密な語彙体系を構築し、コードがドメインを正確に表現することを目指す。

## ワークフロー

### Phase 1: 用語収集

**目的**: ドメインで使用される用語を網羅的に収集

**Task**: `agents/terminology-extraction.md`

**入力**:

- 要件定義書、ドメインエキスパートとの会話記録、既存ドキュメント

**出力**:

- 用語候補リスト（CSV または Markdown）

**判断ポイント**:

- 主要なドメイン概念が網羅されているか
- ビジネスプロセスで使用される用語が含まれているか
- 状態や遷移を表す用語が特定されているか

### Phase 2: 用語定義

**目的**: 各用語の意味を明確に定義し、用語集を作成

**Task**: `agents/glossary-creation.md`

**入力**:

- 用語候補リスト（Phase 1の出力）

**出力**:

- ドメイン用語集（`assets/domain-glossary-template.md` 形式）

**判断ポイント**:

- 各用語に明確な定義があるか
- 同義語が排除されているか
- コンテキストごとの用語の違いが記述されているか

### Phase 3: コードへの適用

**目的**: 定義された用語をコードの命名規則に反映

**Task**: `agents/code-naming.md`

**入力**:

- ドメイン用語集（Phase 2の出力）
- 対象コードベース

**出力**:

- 命名規則ドキュメント
- リファクタリング提案リスト

**判断ポイント**:

- クラス名・メソッド名が用語集と一致しているか
- 技術的な言い換えを避けているか
- ドメインエキスパートがコードを読める状態か

### Phase 4: 用語集の維持管理

**目的**: 用語集を継続的に更新・改善

**Task**: `agents/glossary-maintenance.md`

**入力**:

- 既存の用語集
- 新規用語候補、変更提案

**出力**:

- 更新された用語集
- 変更履歴

**判断ポイント**:

- 新規用語が既存用語と矛盾していないか
- 用語の変更が影響範囲を考慮しているか
- バージョン管理が適切に行われているか

## Task仕様（ナビゲーション）

| Task                      | 役割                 | 参照先                             |
| ------------------------- | -------------------- | ---------------------------------- |
| terminology-extraction.md | 用語収集専門家       | `agents/terminology-extraction.md` |
| glossary-creation.md      | 用語定義専門家       | `agents/glossary-creation.md`      |
| code-naming.md            | コード命名専門家     | `agents/code-naming.md`            |
| glossary-maintenance.md   | 用語集維持管理専門家 | `agents/glossary-maintenance.md`   |

## ベストプラクティス

### すべきこと

- ドメインエキスパートの言葉をそのまま採用する
- 一つの概念に一つの用語を使用する
- 用語をコード（クラス名、メソッド名）に直接反映する
- コンテキスト境界を意識し、用語の適用範囲を明確にする
- 用語集を継続的に更新する

### 避けるべきこと

- 技術的な言い換えを勝手に行う
- 同義語を放置する
- 曖昧な用語定義のまま進める
- コンテキストをまたいで同じ用語を無理に使う
- 用語集を作成後放置する

## リソース参照

### 知識リソース（references/）

**Progressive Disclosure パターン**: 必要時にのみ参照

| リソース                    | 読むタイミング               | 内容                           |
| --------------------------- | ---------------------------- | ------------------------------ |
| `Level1_basics.md`          | スキル初学者                 | 基本概念と使用タイミング       |
| `Level2_intermediate.md`    | Phase実行中                  | 実務手順と判断基準             |
| `Level3_advanced.md`        | 複雑な状況に遭遇時           | 応用パターンと高度な技法       |
| `Level4_expert.md`          | 大規模プロジェクト・最適化時 | 専門的知見とベストプラクティス |
| `terminology-extraction.md` | Phase 1実行時                | 用語抽出の詳細手法             |
| `glossary-creation.md`      | Phase 2実行時                | 用語定義のフォーマットと手法   |
| `naming-conventions.md`     | Phase 3実行時                | コード命名規則の詳細           |
| `glossary-maintenance.md`   | Phase 4実行時                | 用語集維持管理の詳細           |

### スクリプト（scripts/）

| スクリプト                | 用途               | 実行タイミング        |
| ------------------------- | ------------------ | --------------------- |
| `analyze-terminology.mjs` | 用語一貫性分析     | Phase 3完了後         |
| `validate-skill.mjs`      | スキル構造検証     | スキル更新後          |
| `log_usage.mjs`           | 使用記録・自動評価 | 各Phase完了後（必須） |

**スクリプト実行例**:

```bash
# 用語一貫性分析
node .claude/skills/ubiquitous-language/scripts/analyze-terminology.mjs src/shared/core/

# スキル構造検証
node .claude/skills/ubiquitous-language/scripts/validate-skill.mjs

# 使用記録（Phase完了時に必ず実行）
node .claude/skills/ubiquitous-language/scripts/log_usage.mjs \
  --result success \
  --phase "Phase 2: 用語定義" \
  --agent "glossary-creation"
```

### アセット（assets/）

| アセット                      | 用途                       | 使用タイミング |
| ----------------------------- | -------------------------- | -------------- |
| `domain-glossary-template.md` | ドメイン用語集テンプレート | Phase 2実行時  |

## コマンドリファレンス

### クイックスタート

```bash
# 1. レベル1基礎を確認
cat .claude/skills/ubiquitous-language/references/Level1_basics.md

# 2. Phase 1: 用語収集を実行（Taskとして）
# → agents/terminology-extraction.md を参照

# 3. Phase 2: 用語定義を実行（Taskとして）
# → agents/glossary-creation.md を参照

# 4. Phase 3: コードへの適用（Taskとして）
# → agents/code-naming.md を参照

# 5. 使用記録を残す（必須）
node .claude/skills/ubiquitous-language/scripts/log_usage.mjs \
  --result success \
  --phase "Phase 1-3" \
  --notes "Initial glossary created"
```

## フィードバックループ

各Phase完了後、必ず `scripts/log_usage.mjs` を実行してフィードバックを記録する。
これにより、スキルの継続的改善とメトリクス追跡が可能になる。

## 変更履歴

| Version | Date       | Changes                                                              |
| ------- | ---------- | -------------------------------------------------------------------- |
| 1.2.0   | 2026-01-01 | agents/にTask仕様書を作成、references/にglossary-creation.md追加     |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様準拠に更新、Task仕様追加、Progressive Disclosure対応 |
| 1.0.0   | 2025-12-24 | 初版リリース                                                         |
