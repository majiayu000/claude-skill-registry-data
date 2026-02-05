---
name: example-usage-patterns
description: |
  Documentation patterns for creating clear, executable, and maintainable usage examples across APIs, CLIs, libraries, and frameworks.

  Anchors:
  • Docs for Developers (Jared Bhatti et al.) / 適用: 実践的な例示パターン / 目的: 開発者に即座に理解・実行可能な例を提供
  • The Documentation System (Diataxis) / 適用: チュートリアル・ハウツー・リファレンス分類 / 目的: 目的に応じた例の種類と粒度を選択
  • Clean Code (Robert C. Martin) / 適用: 明確な命名・単一責務 / 目的: 自己説明的なサンプルコード

  Trigger:
  Use when creating code examples, writing tutorials, documenting API usage, building sample projects, establishing example conventions, or standardizing example patterns across a codebase.
  example creation, tutorial writing, API documentation, sample code, documentation patterns
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Example Usage Patterns

## 概要

実践的で保守可能な使用例を作成するための体系的なアプローチを提供する。API、CLI、ライブラリ、フレームワークなど、あらゆる種類のソフトウェアコンポーネントに適用可能。

## ワークフロー

### Phase 1: 例示コンテキスト分析

**目的**: 対象技術とユーザーを理解し、適切な例の種類を決定

**アクション**:

1. 対象技術の性質を特定（API / CLI / ライブラリ / フレームワーク）
2. ターゲットユーザーの技術レベルを評価（初心者 / 中級者 / 上級者）
3. Diataxis分類で例の種類を決定（チュートリアル / ハウツー / リファレンス）
4. 例示範囲を定義（最小限 / 実践的 / 完全なアプリケーション）

**Task**: `agents/analyze-context.md` を参照

### Phase 2: 例の設計・実装

**目的**: 実行可能で明確な使用例を作成

**アクション**:

1. `assets/example-template.md` で構造を定義
2. 4原則を適用: 明確性・完全性・実用性・保守性
3. 段階的複雑化: 最小限→エラーハンドリング→高度な機能
4. `scripts/validate_example.mjs` で実行可能性を検証

**Task**: `agents/create-example.md` を参照

### Phase 3: 検証・品質保証

**目的**: 例の品質を確保

**アクション**:

1. `scripts/validate_example.mjs` で構造検証
2. 4原則チェックリストで品質確認
3. 実際に実行して動作確認
4. フィードバックをLOGS.mdに記録

**Task**: `agents/validate-example.md` を参照

## Task仕様ナビ

| Task             | 起動タイミング | 入力         | 出力             |
| ---------------- | -------------- | ------------ | ---------------- |
| analyze-context  | Phase 1開始時  | 対象技術情報 | コンテキスト分析 |
| create-example   | Phase 2開始時  | 分析結果     | 実行可能な例     |
| validate-example | Phase 3開始時  | 作成された例 | 検証結果         |

## ベストプラクティス

### すべきこと

- すべての例はコピー&ペーストで動作させる
- 段階的な複雑化: 基本例→実践的な例→高度な例
- 重要な部分には説明コメントを追加
- 現実的なシナリオに基づいた例を作成
- エラーハンドリングと対処法を含める
- 依存関係のバージョンを明記

### 避けるべきこと

- 複雑すぎる最初の例
- 説明のないマジックナンバー
- 非現実的なシナリオ
- 不完全な例（動作に必要なコンポーネントの欠如）
- 非推奨APIや古いパターンの使用
- セキュリティリスクのある実装パターン

## リソース参照

### references/

| リソース           | パス                              | 用途                   |
| ------------------ | --------------------------------- | ---------------------- |
| 基本原則           | `references/basics.md`            | 例示の4原則と基本構造  |
| 実践パターン       | `references/patterns.md`          | 言語別・用途別パターン |
| 品質チェックリスト | `references/quality-checklist.md` | 品質検証基準           |

### scripts/

| スクリプト             | 用途         | 使用例                                     |
| ---------------------- | ------------ | ------------------------------------------ |
| `validate_example.mjs` | 例の構造検証 | `node scripts/validate_example.mjs <path>` |

### assets/

| テンプレート          | 用途                     |
| --------------------- | ------------------------ |
| `example-template.md` | 基本的な例のテンプレート |

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様準拠版に再構築 |
| 1.0.0   | 2025-12-31 | 初版作成                       |
