---
name: factory-patterns
description: |
  GoFのFactory系パターン（Factory Method、Abstract Factory、Builder等）の設計・実装を支援するスキル。
  Erich Gammaの『Design Patterns』に基づき、オブジェクト生成の柔軟性と拡張性を実現する戦略を提供します。

  Anchors:
  • Design Patterns / 適用: 全Factory系パターン共通の基本原則 / 目的: Gang of Fourの標準的設計思想に準拠
  • Factory Method / 適用: サブクラスによるオブジェクト生成 / 目的: 生成ロジックをサブクラスへ委譲
  • Abstract Factory / 適用: 関連オブジェクトの族単位の生成 / 目的: プロダクトファミリ間の一貫性確保
  • Builder / 適用: 複雑なオブジェクトの段階的構築 / 目的: 構築ロジックと表現の分離

  Trigger:
  以下の場合に使用してください：オブジェクト生成ロジックが複雑化している時、複数のオブジェクト族を扱う時、
  生成戦略を動的に切り替える必要がある時、フレームワークやライブラリのファクトリパターン実装が必要な時。
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Factory Patterns

## 概要

GoFのFactory系パターンの設計と実装を支援するスキル。Factory Methodパターン、Abstract Factoryパターン、Builderパターン等を通じて、オブジェクト生成ロジックの複雑性を管理し、システムの拡張性と保守性を向上させます。

詳細な手順や各パターンの背景については、`references/Level1_basics.md`（基礎）から `references/Level4_expert.md`（専門知識）を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要なパターン（Factory Method / Abstract Factory / Builder / Registry Factory）を特定
3. 関連するリソース、スクリプト、テンプレートを特定

### Phase 2: パターン選択と設計

**目的**: 適切なパターンを選択し、実装設計を立案する

**アクション**:

1. パターンの特性（生成戦略、拡張性、複雑度）を理解
2. 関連リソースやテンプレートを参照しながら設計を実施
3. 重要な判断ポイント（パターン選択、スコープ等）をメモとして残す

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 実装がパターンの原則に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す

## Task仕様ナビ

Factory Patternsスキルで利用可能なタスク。適切なパターンを選択し、対応する詳細ガイドを参照してください。

| パターン名           | ファイル                         | 適用場面                                               | 入力                                          | 出力                                                                 |
| -------------------- | -------------------------------- | ------------------------------------------------------ | --------------------------------------------- | -------------------------------------------------------------------- |
| **Factory Method**   | `references/factory-method.md`   | サブクラスがオブジェクト生成を担当する設計が必要       | 生成すべきクラスの要件                        | Factory Methodパターンの実装コード / 設計図                          |
| **Abstract Factory** | `references/abstract-factory.md` | 関連するオブジェクト族の生成を一貫性持って管理する必要 | プロダクトファミリ定義 / ファクトリクラス設計 | Abstract Factoryパターンの実装 / インターフェース定義                |
| **Builder Pattern**  | `references/builder-pattern.md`  | 複雑なオブジェクトを段階的に構築する必要               | ターゲットクラスの構造と制約条件              | Builderパターンの実装 / テンプレート（`assets/builder-template.md`） |
| **Registry Factory** | `references/registry-factory.md` | 動的にオブジェクト型を登録・生成する必要               | レジストリ対象のクラス一覧                    | Registry Factoryの実装 / レジストリ登録機構                          |

## ベストプラクティス

### すべきこと

- パターンを選択する前に、各パターンの特性（Purpose、Participants、Motivation等）を確認する
- 複雑なオブジェクト生成ロジックは必ずFactory系パターンで管理する
- Abstract Factoryを使う場合は、プロダクトファミリ間の一貫性を強制する仕組みを組み込む
- Builderを使う場合は、段階的構築の不変条件をチェックできる検証ロジックを含める
- 新しいワークフロータイプやプロダクト族を追加する際は、スクリプト化して再利用可能にする
- 実装後は `scripts/log_usage.mjs` で記録を残し、継続的な改善を促進する

### 避けるべきこと

- 生成ロジックをクライアントコードに混在させる（Factoryパターンで抽象化すべき）
- パターンの選択基準を不明確なまま進める（Phase 1で必ず明確化する）
- 複数のパターンを無差別に組み合わせて過剰な複雑性を招く
- アンチパターンや注意点を確認せずに進める

## リソース参照

### パターン別詳細ガイド

- **Factory Methodの詳細**: `references/factory-method.md`
- **Abstract Factoryの詳細**: `references/abstract-factory.md`
- **Builderパターンの詳細**: `references/builder-pattern.md`
- **Registry Factoryの詳細**: `references/registry-factory.md`

### レベル別学習リソース

- **レベル1（基礎）**: `references/Level1_basics.md` - Factory系パターンの概要と基本的な選択基準
- **レベル2（実務）**: `references/Level2_intermediate.md` - 実装レベルの設計パターンと応用例
- **レベル3（応用）**: `references/Level3_advanced.md` - 複雑なシステムへの適用戦略
- **レベル4（専門）**: `references/Level4_expert.md` - パターン組み合わせと実装最適化

### スクリプト

- `scripts/generate-factory.mjs` - Factory実装の自動生成ツール（`--help` で詳細を確認）
- `scripts/log_usage.mjs` - 実行記録と自動評価（`--help` で詳細を確認）
- `scripts/validate-skill.mjs` - スキル構造検証（`--help` で詳細を確認）

### テンプレート

- `assets/factory-method-template.md` - Factory Methodパターンの実装テンプレート
- `assets/builder-template.md` - Builderパターンの実装テンプレート

## 変更履歴

| バージョン | 日付       | 変更内容                                                                                                         |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| 1.0.0      | 2025-12-31 | 18-skills.md仕様に準拠。Task仕様ナビ（テーブル）を追加、Anchorsとトリガー条件を日本語で統合、frontmatterを簡潔化 |
