---
name: value-object-patterns
description: |
  値オブジェクトパターンの専門スキル。
  不変性、等価性、ドメイン概念のカプセル化を提供します。

  Anchors:
  - Domain-Driven Design（Eric Evans）/ 適用: 値オブジェクト設計 / 目的: ドメインモデル表現
  - Implementing DDD（Vaughn Vernon）/ 適用: 実装パターン / 目的: 実践的コード
  - Refactoring（Martin Fowler）/ 適用: プリミティブ執着検出 / 目的: コードスメル改善

  Trigger:
  Use when implementing value objects, designing immutable domain concepts, refactoring primitive obsession, or integrating value objects into domain models.

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Value Object Patterns

## 概要

値オブジェクト（Value Object）は、ドメイン駆動設計の基本要素であり、不変性、等価性、自己検証を備えたオブジェクトです。4つの専門エージェントによる包括的な値オブジェクト設計・実装を提供します。

## エージェント構成

| エージェント           | 役割                 | 主な機能                               |
| ---------------------- | -------------------- | -------------------------------------- |
| value-designer         | 値オブジェクト設計   | 概念識別、設計判断、プロパティ定義     |
| implementation-builder | 実装構築             | 不変性実装、等価性実装、自己検証       |
| primitive-detector     | プリミティブ執着検出 | コードスメル検出、リファクタリング計画 |
| domain-integrator      | ドメインモデル統合   | ユビキタス言語、集約統合、永続化戦略   |

## ワークフロー

### Phase 1: 要件分析と設計

**目的**: ドメイン概念を分析し、値オブジェクトの設計方針を決定

**アクション**:

1. `value-designer` でドメイン概念を分析
2. 値オブジェクト vs エンティティの判断
3. プロパティと検証ルールを定義

### Phase 2: 実装

**目的**: 不変性・等価性・自己検証を備えた実装

**アクション**:

1. `implementation-builder` で実装コード生成
2. テストケースの作成
3. ファクトリパターンの適用

### Phase 3: 統合と改善

**目的**: ドメインモデルへの統合とコード品質改善

**アクション**:

1. `primitive-detector` で既存コードを分析
2. `domain-integrator` でドメインモデルに統合
3. `scripts/validate-skill.mjs` で検証

## Task仕様ナビ

| タスク               | 担当エージェント       | 参照リソース                   |
| -------------------- | ---------------------- | ------------------------------ |
| 値オブジェクト識別   | value-designer         | `value-object-fundamentals.md` |
| 不変性・等価性実装   | implementation-builder | `common-patterns.md`           |
| 自己検証実装         | implementation-builder | `validation-strategies.md`     |
| プリミティブ執着検出 | primitive-detector     | `common-patterns.md`           |
| ドメイン言語統合     | domain-integrator      | `value-object-fundamentals.md` |

## ベストプラクティス

### すべきこと

- 値オブジェクトは常に**不変**に設計する
- コンストラクタで**自己検証**を実装し、無効な状態を防ぐ
- **等価性（equals/hashCode）** を属性値ベースで実装する
- ドメイン言語を反映した**意味のある名前**を付ける
- `scripts/detect-primitive-obsession.mjs` でコード品質を定期的にチェック

### 避けるべきこと

- 値オブジェクトをミュータブル（可変）に実装すること
- コンストラクタでの検証を怠ること
- **プリミティブ執着**アンチパターンに陥ること
- ドメインロジックを持たない単なるデータホルダーにすること

## リソース参照

### エージェント

| エージェント                       | 説明                 |
| ---------------------------------- | -------------------- |
| `agents/value-designer.md`         | 値オブジェクト設計   |
| `agents/implementation-builder.md` | 実装構築             |
| `agents/primitive-detector.md`     | プリミティブ執着検出 |
| `agents/domain-integrator.md`      | ドメインモデル統合   |

### リファレンス

| リソース                                  | 説明                     |
| ----------------------------------------- | ------------------------ |
| `references/value-object-fundamentals.md` | 値オブジェクトの基本原則 |
| `references/validation-strategies.md`     | 自己検証戦略とエラー処理 |
| `references/common-patterns.md`           | よく使用されるパターン集 |

### アセット

| アセット                           | 説明                           |
| ---------------------------------- | ------------------------------ |
| `assets/simple-value-object.ts`    | 単純値オブジェクトテンプレート |
| `assets/composite-value-object.ts` | 複合値オブジェクトテンプレート |

### スクリプト

| スクリプト                               | 説明                 | 使用方法                                             |
| ---------------------------------------- | -------------------- | ---------------------------------------------------- |
| `scripts/detect-primitive-obsession.mjs` | プリミティブ執着検出 | `node scripts/detect-primitive-obsession.mjs --help` |
| `scripts/validate-skill.mjs`             | スキル構造検証       | `node scripts/validate-skill.mjs -v`                 |
| `scripts/log_usage.mjs`                  | 使用記録             | `node scripts/log_usage.mjs`                         |

## 変更履歴

| バージョン | 日付       | 変更内容                                      |
| ---------- | ---------- | --------------------------------------------- |
| 2.0.0      | 2026-01-01 | 4エージェント体制への再構成、18-skills.md準拠 |
| 1.0.0      | 2025-12-31 | 初版リリース                                  |
