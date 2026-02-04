---
name: documentation-architecture
description: |
  ドキュメント構造設計・リソース分割・階層設計を専門とするスキル。
  500行制約に基づく適切なファイル分割とトピックベース組織化により、
  保守性と発見可能性の高いドキュメントアーキテクチャを実現する。

  Anchors:
  • Information Architecture (Rosenfeld/Morville) / 適用: 情報組織化パターン / 目的: 発見可能性向上
  • Clean Architecture (Robert C. Martin) / 適用: 依存関係ルール / 目的: 責任分離設計
  • The Pragmatic Programmer (Hunt/Thomas) / 適用: DRY原則 / 目的: 重複回避

  Trigger:
  Use when designing documentation structure, splitting large files over 500 lines, organizing resources with topic-based structure, improving discoverability, or establishing naming conventions.
  documentation structure, file splitting, directory organization, hierarchy design, naming conventions, 500-line constraint
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Documentation Architecture

## 概要

ドキュメント構造設計・リソース分割・階層設計を専門とするスキル。500行制約に基づく適切なファイル分割とトピックベース組織化により、保守性と発見可能性の高いドキュメントアーキテクチャを実現する。

## ワークフロー

### Phase 1: 構造分析

**目的**: 現在のドキュメント構造を評価し、改善点を特定

**アクション**:

1. `scripts/analyze-structure.mjs` で構造を分析
2. 500行超過ファイルを検出
3. 階層深度と命名一貫性を評価
4. 改善優先度を決定

**Task**: `agents/analyze-structure.md` を参照

### Phase 2: 組織化設計

**目的**: 最適なディレクトリ構造とファイル分割を設計

**アクション**:

1. トピックベースの組織化戦略を決定
2. ファイル分割パターンを選択
3. 命名規則を統一
4. 階層構造を設計

**Task**: `agents/design-organization.md` を参照

### Phase 3: 構造再編実装

**目的**: 設計に基づいて構造を再編し、検証する

**アクション**:

1. ディレクトリ構造を作成
2. ファイル分割を実行
3. 相互参照を更新
4. `scripts/validate-structure.mjs` で検証
5. `scripts/log_usage.mjs` で記録

**Task**: `agents/implement-restructure.md` を参照

## Task仕様ナビ

| Task                  | 起動タイミング | 入力             | 出力         |
| --------------------- | -------------- | ---------------- | ------------ |
| analyze-structure     | Phase 1開始時  | 対象ディレクトリ | 分析レポート |
| design-organization   | Phase 2開始時  | 分析レポート     | 設計書       |
| implement-restructure | Phase 3開始時  | 設計書           | 再編済み構造 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                 | 理由                       |
| ------------------------ | -------------------------- |
| 分析スクリプトを先に実行 | 客観的データに基づく設計   |
| 1ファイル1トピック原則   | 発見可能性と保守性の向上   |
| 4層以下の階層に抑える    | 深すぎると発見可能性が低下 |
| 命名規則を統一           | 一貫性による認知負荷軽減   |
| 500行制約を遵守          | 可読性と管理性の確保       |

### 避けるべきこと

| 禁止事項               | 問題点                   |
| ---------------------- | ------------------------ |
| 分析なしでいきなり実装 | 不適切な構造設計のリスク |
| 複数トピックの混在     | 発見可能性と保守性の低下 |
| 過度な分割             | 管理コスト増大           |
| 循環参照               | 依存関係の複雑化         |

## リソース参照

### scripts/（決定論的処理）

| スクリプト               | 機能               |
| ------------------------ | ------------------ |
| `analyze-structure.mjs`  | 構造分析と違反検出 |
| `validate-structure.mjs` | 構造検証           |
| `log_usage.mjs`          | フィードバック記録 |

### references/（詳細知識）

| リソース       | パス                                                                       | 読込条件         |
| -------------- | -------------------------------------------------------------------------- | ---------------- |
| 組織化パターン | [references/organization-patterns.md](references/organization-patterns.md) | 設計時に参照     |
| 命名規則       | [references/naming-conventions.md](references/naming-conventions.md)       | 命名検討時に参照 |
| 分割戦略       | [references/splitting-strategies.md](references/splitting-strategies.md)   | 分割設計時に参照 |

### assets/（テンプレート）

| アセット                | 用途                         |
| ----------------------- | ---------------------------- |
| `structure-template.md` | ドキュメント構造テンプレート |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.1.0   | 2026-01-01 | 18-skills.md仕様完全準拠版に再構築 |
| 2.0.0   | 2025-12-31 | 初版作成                           |
