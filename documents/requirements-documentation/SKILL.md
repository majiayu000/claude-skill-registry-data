---
name: requirements-documentation
description: |
  要件ドキュメントの作成・構造化・品質管理・ハンドオフを支援するスキル。
  カール・ウィーガーズの要求工学理論に基づき、ステークホルダーと開発チームの双方に有用な仕様書を作成する。

  Anchors:
  • Software Requirements (Karl Wiegers) / 適用: 要件管理全般 / 目的: 明確で検証可能な仕様
  • IEEE 830 SRS Standard / 適用: ドキュメント構造 / 目的: 標準準拠の仕様書
  • Don't Make Me Think (Steve Krug) / 適用: 情報設計 / 目的: 読みやすいドキュメント

  Trigger:
  Use when creating requirements documents, writing specifications, preparing stakeholder reviews, or establishing requirements traceability.
  requirements document, specification, SRS, stakeholder review, traceability matrix, 要件定義書, 仕様書
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# 要件ドキュメンテーション

## 概要

要件ドキュメントの構造化、品質メトリクス、ハンドオフプロトコルを提供するスキル。
以下の場面で活用される：

- 要件定義書・仕様書の新規作成
- 既存要件ドキュメントの品質改善
- ステークホルダーレビューの準備
- 設計フェーズへのハンドオフ実施
- 要件トレーサビリティの確立

## ワークフロー

### Phase 1: 要件収集と分析

**目的**: ステークホルダーからの要件を収集し、ドキュメント化の準備を整える

**アクション**:

1. ステークホルダーの特定と役割整理
2. 要件の収集（インタビュー、既存ドキュメント分析）
3. 機能要件と非機能要件の分類
4. 優先度付け（MoSCoW法）
5. 依存関係と制約の整理

**Task**: `agents/analyze-requirements.md` を参照

### Phase 2: ドキュメント構造設計

**目的**: 収集した要件を標準化されたドキュメント形式で構造化する

**アクション**:

1. ドキュメントスコープの決定
2. テンプレート（`assets/requirements-document-template.md`）の適用
3. セクション構成の最適化
4. 受入基準の定義（Given-When-Then形式）
5. ユースケース記述の作成

**Task**: `agents/structure-document.md` を参照

### Phase 3: 検証とレビュー

**目的**: ドキュメントの品質を確保し、ステークホルダーの承認を得る

**アクション**:

1. `scripts/validate-document.mjs` で構造検証
2. 品質メトリクスの確認（完全性、一貫性、検証可能性）
3. ステークホルダーレビューの実施
4. フィードバックの反映と改訂
5. 承認プロセスの完了

**Task**: `agents/validate-document.md` を参照

### Phase 4: トレーサビリティとハンドオフ

**目的**: 要件から設計・実装・テストへの追跡可能性を確立する

**アクション**:

1. 要件追跡マトリクスの作成
2. 設計フェーズへの引き継ぎ資料準備
3. テスト計画との紐付け
4. `scripts/log_usage.mjs` で実行記録を保存
5. ハンドオフ完了の確認

**Task**: `agents/create-traceability.md` を参照

## Task仕様（ナビゲーション）

| Task                 | 起動タイミング | 入力                 | 出力                 |
| -------------------- | -------------- | -------------------- | -------------------- |
| analyze-requirements | Phase 1開始時  | ステークホルダー情報 | 要件分析結果         |
| structure-document   | Phase 2開始時  | 要件分析結果         | 構造化ドキュメント   |
| validate-document    | Phase 3開始時  | ドキュメントドラフト | 検証済みドキュメント |
| create-traceability  | Phase 4開始時  | 確定要件             | トレーサビリティ資料 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- テンプレート（`assets/requirements-document-template.md`）を活用し一貫性を確保
- MoSCoW法で全要件に優先度を付与
- 受入基準をGiven-When-Then形式で具体的に記述
- 要件IDを付与しトレーサビリティを維持
- ステークホルダーレビューを早期かつ頻繁に実施
- `scripts/validate-document.mjs` で定期的に品質検証

### 避けるべきこと

- 曖昧または検証不可能な要件の記述
- 優先度なしでの要件列挙
- ステークホルダー承認前のハンドオフ
- トレーサビリティの欠如
- 品質検証スクリプトの実行省略

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                             | 内容                           |
| -------------------- | -------------------------------------------------------------------------------- | ------------------------------ |
| ドキュメント構造     | See [references/document-structure.md](references/document-structure.md)         | 要件ドキュメントの構造パターン |
| 品質メトリクス       | See [references/quality-metrics.md](references/quality-metrics.md)               | 品質基準と検証方法             |
| ステークホルダー管理 | See [references/stakeholder-management.md](references/stakeholder-management.md) | 関係者管理とレビュープロセス   |

### scripts/（決定論的処理）

| スクリプト              | 用途                 | 使用例                                                          |
| ----------------------- | -------------------- | --------------------------------------------------------------- |
| `validate-document.mjs` | ドキュメント構造検証 | `node scripts/validate-document.mjs [document-path]`            |
| `log_usage.mjs`         | フィードバック記録   | `node scripts/log_usage.mjs --result success --phase "Phase 4"` |

### assets/（テンプレート）

| テンプレート                        | 用途                         |
| ----------------------------------- | ---------------------------- |
| `requirements-document-template.md` | 要件定義書の標準テンプレート |

## 変更履歴

| Version | Date       | Changes                                                                |
| ------- | ---------- | ---------------------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠：agents追加、references再構成、Trigger英語化  |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様への全面更新：YAML frontmatter標準化、Task仕様ナビ追加 |
| 1.0.0   | 2025-12-24 | 初版作成                                                               |
