---
name: open-closed-principle
description: |
  オープン・クローズド原則（OCP）の専門スキル。
  拡張に対して開き、修正に対して閉じた設計を提供します。

  Anchors:
  • 『Clean Architecture』（Robert C. Martin） / 適用: SOLID原則 / 目的: 保守性向上
  • 『アジャイルソフトウェア開発の奥義』（Robert C. Martin） / 適用: 設計パターン / 目的: 拡張性確保

  Trigger:
  OCP適用時、拡張可能設計時、SOLID原則実装時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Open-Closed Principle (OCP)

## 概要

SOLID原則の開放閉鎖原則（OCP: Open-Closed Principle）は、
ソフトウェアエンティティが拡張に対して開かれ、修正に対して閉じていることを述べています。

このスキルは以下を実現します：

- 既存コードを修正せずに新機能を追加できる拡張可能な設計
- アンチパターン（if-elseチェーン、switch文、型チェック）の識別と改善
- Strategy、Template Method、Plugin Registryなどの拡張パターンの適用
- レガシーコードのOCP準拠への段階的なリファクタリング

詳細な手順や背景は `references/` ディレクトリを参照してください。

## ワークフロー

### Phase 1: 現状分析

**目的**: OCP違反パターンを検出し、改善対象を特定

**アクション**:

1. `references/basics.md` でOCPの基本概念を確認
2. `agents/analyze-violations.md` を参照してコード分析を実施
3. 違反箇所をリストアップし優先度を設定

**Task**: `agents/analyze-violations.md` を参照

### Phase 2: 拡張設計

**目的**: OCP準拠の拡張ポイントを設計

**アクション**:

1. `references/ocp-patterns.md` で適切なパターンを選定
2. `agents/design-extension.md` を参照して設計を実施
3. `assets/extension-point-template.md` でテンプレートを活用

**Task**: `agents/design-extension.md` を参照

### Phase 3: 実装と検証

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/analyze-extensibility.mjs` で改善後のコード品質を再度確認
2. `scripts/validate-skill.mjs` でスキル構造を確認
3. 成果物がOCP原則に準拠しているか確認
4. `scripts/log_usage.mjs` を実行して記録を残す

## Task仕様（ナビゲーション）

| Task               | 起動タイミング | 入力         | 出力         |
| ------------------ | -------------- | ------------ | ------------ |
| analyze-violations | Phase 1開始時  | 対象コード   | 違反レポート |
| design-extension   | Phase 2開始時  | 違反レポート | 拡張設計書   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **拡張ポイントを明確にする**: 新しいタイプ・変数が追加される可能性がある場所を事前に設計
- **抽象化を活用する**: インターフェース、基底クラス、ジェネリクスで変動部を隠蔽
- **段階的に適用する**: すべてを一度にOCP準拠にするのではなく、段階的に改善
- **アンチパターンを避ける**: if-elseチェーン、switch文、型チェック、フラグパラメータを識別・リファクタリング
- **テストを追加する**: リファクタリング前後で拡張性とバグの有無を検証

### 避けるべきこと

- **過度な抽象化**: 実装されない拡張ポイントを設計しない（YAGNI原則に反する）
- **複雑性の増加**: 単純な機能を複雑にしないため、本当に拡張が必要な箇所のみに適用
- **アンチパターンの無視**: switch文やif-elseチェーンを放置しない
- **テストなしのリファクタリング**: 変更前に既存機能が正常に動作することを確認
- **一度に全体をリファクタリング**: 段階的に、失敗しやすい部分から改善

## リソース参照

### references/（詳細知識）

| リソース         | パス                                                                         | 用途                |
| ---------------- | ---------------------------------------------------------------------------- | ------------------- |
| 基礎知識         | See [references/basics.md](references/basics.md)                             | OCP基本概念         |
| 原則詳細         | See [references/ocp-fundamentals.md](references/ocp-fundamentals.md)         | 定義・歴史・検証    |
| パターン集       | See [references/ocp-patterns.md](references/ocp-patterns.md)                 | Strategy/Template等 |
| 拡張メカニズム   | See [references/extension-mechanisms.md](references/extension-mechanisms.md) | パターン選定ガイド  |
| リファクタリング | See [references/refactoring-to-ocp.md](references/refactoring-to-ocp.md)     | 段階的改善手順      |

### assets/（テンプレート）

| リソース     | パス                                 | 用途             |
| ------------ | ------------------------------------ | ---------------- |
| 拡張ポイント | `assets/extension-point-template.md` | 設計テンプレート |

## 変更履歴

| Version | Date       | Changes                      |
| ------- | ---------- | ---------------------------- |
| 2.1.0   | 2026-01-02 | agents/追加、Level構造を統合 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に対応       |
| 1.0.0   | 2025-12-24 | 初期実装                     |
