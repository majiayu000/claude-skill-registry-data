---
name: structured-output-design
description: |
  構造化出力の仕様書を設計するためのスキル。スキーマ定義、命名規則、互換性とバージョニング方針を整理し、長期運用に耐える出力契約を作成する。

  Anchors:
  • JSON Schema / 適用: スキーマ設計 / 目的: フィールド仕様の形式化
  • Semantic Versioning 2.0.0 / 適用: バージョニング設計 / 目的: 互換性ルールの明確化
  • Postel's Law / 適用: 互換性判断 / 目的: 入出力の許容範囲を整理

  Trigger:
  Use when defining output contracts, schema evolution rules, or compatibility plans for structured data.
  output contract, schema design, compatibility, versioning, JSON schema
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Structured Output Design

## 概要

構造化出力の「契約」を設計し、スキーマ・命名規則・互換性方針を一貫させるスキル。仕様書を作成して関係者の合意形成を促進する。

詳細は `references/Level1_basics.md` から段階的に参照する。

## ワークフロー

### Phase 1: 契約要件の整理

**目的**: 出力仕様の目的、利用者、互換性要件を明確化する。

**アクション**:

1. 仕様の利用者と運用期間を整理する。
2. 互換性の許容範囲を定義する。
3. 命名規則とバージョン表現を決定する。

### Phase 2: 仕様書とスキーマの設計

**目的**: 出力契約を文書化し、スキーマとテンプレートを整合させる。

**アクション**:

1. `assets/output-contract-template.md` を埋める。
2. `assets/json-schema-template.json` を基にスキーマを作成する。
3. 互換性・移行方針を明記する。

### Phase 3: 検証とレビュー

**目的**: 仕様書とスキーマの不整合を解消する。

**アクション**:

1. `scripts/validate-output-contract.mjs` を実行する。
2. `scripts/validate-schema.mjs` でスキーマの構造を点検する。
3. 指摘事項を反映し版を確定する。

## Task仕様ナビ

| Phase | Task | 目的 | 入力 | 出力 |
| --- | --- | --- | --- | --- |
| 1 | 契約要件整理 | 利用者・互換性要件の確認 | ユーザー要求 | 要件メモ |
| 2 | 契約設計 | 仕様書とスキーマを整備 | 要件メモ | 出力契約書 |
| 3 | 契約検証 | 仕様書/スキーマの検証 | 出力契約書 | 検証レポート |

## ベストプラクティス

### すべきこと

- フィールドに型・制約・例を必ず記載する。
- 互換性の原則を明文化する。
- バージョン表現を出力に含める。
- 仕様変更は影響範囲を記録する。

### 避けるべきこと

- 必須/任意を曖昧にしたまま運用しない。
- 破壊的変更をサイレントに入れない。
- 仕様書とスキーマの不一致を放置しない。

## リソース/スクリプト参照

### references/

- `references/Level1_basics.md`: 基礎指針
- `references/Level2_intermediate.md`: 実務パターン
- `references/Level3_advanced.md`: 高度な設計指針
- `references/Level4_expert.md`: 専門領域の注意点
- `references/schema-patterns.md`: スキーマ設計パターン
- `references/json-schema-patterns.md`: JSON Schemaの具体例
- `references/field-naming.md`: 命名規則
- `references/compatibility-strategies.md`: 互換性戦略
- `references/function-calling-guide.md`: 関数呼び出し形式の注意点
- `references/zod-integration.md`: Zod統合の指針

### assets/

- `assets/output-contract-template.md`: 出力契約書テンプレート
- `assets/json-schema-template.json`: JSON Schema雛形
- `assets/schema-versioning-template.json`: バージョン表現テンプレート
- `assets/zod-schema-template.ts`: Zod用テンプレート

### scripts/

- `scripts/validate-output-contract.mjs`: 仕様書の必須項目検証
- `scripts/validate-schema.mjs`: JSON Schema構造検証

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 2.0.0 | 2026-01-02 | 18-skills.md 仕様に準拠した構造へ更新 |
