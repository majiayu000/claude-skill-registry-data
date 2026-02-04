---
name: plugin-architecture
description: |
  プラグインアーキテクチャの専門スキル。レジストリパターン、動的ロード、依存性注入を活用し、拡張可能なシステム設計を提供する。

  Anchors:
  • Clean Architecture (Robert C. Martin) / 適用: 拡張性設計 / 目的: 柔軟性確保
  • Dependency Injection Principles and Practices (Mark Seemann) / 適用: DI設計 / 目的: 疎結合実現
  • Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four) / 適用: レジストリパターン / 目的: 型安全な登録管理

  Trigger:
  Use when designing plugin systems, implementing extension points, managing dynamic module loading, creating registry patterns, or building workflow engines with pluggable executors.
  plugin architecture, registry pattern, dependency injection, dynamic loading, extension points, workflow executor
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# プラグインアーキテクチャ

## 概要

動的な機能拡張を可能にするプラグインアーキテクチャの設計を専門とするスキル。レジストリパターン、動的ロード、依存性注入を活用し、機能追加時の既存コード修正を不要にする拡張性の高いシステム設計を提供します。

## ワークフロー

### Phase 1: 要件分析

**目的**: プラグインシステムの拡張要件を分析

**アクション**:

1. 拡張ポイントの特定（どこを拡張可能にするか）
2. プラグインインターフェースの設計要件の整理
3. ライフサイクル管理の必要性を評価

**Task**: `agents/analyze-requirements.md` を参照

### Phase 2: システム設計

**目的**: プラグインシステムの全体設計を確定

**アクション**:

1. レジストリパターンの選択（Map-based, Service Locator等）
2. ロード戦略の決定（Eager, Lazy, On-Demand）
3. 依存性注入方式の設計
4. プラグインライフサイクルフックの定義

**Task**: `agents/design-plugin-system.md` を参照

### Phase 3: レジストリ実装

**目的**: 型安全なレジストリを実装

**アクション**:

1. `assets/registry-implementation.md` を基にレジストリクラスを作成
2. CRUD操作（register, get, list, unregister）を実装
3. エラーハンドリング（重複登録、未登録キーアクセス）を追加
4. `scripts/validate-plugin-structure.mjs` で検証

**Task**: `agents/implement-registry.md` を参照

## Task仕様ナビ

| Task                 | 起動タイミング | 入力                     | 出力                     |
| -------------------- | -------------- | ------------------------ | ------------------------ |
| analyze-requirements | Phase 1開始時  | システム要件             | 拡張要件分析書           |
| design-plugin-system | Phase 2開始時  | 拡張要件分析書           | プラグインシステム設計書 |
| implement-registry   | Phase 3開始時  | プラグインシステム設計書 | Registryクラス実装       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- ワークフローエンジンのプラグインシステムを構築する時
- 機能の動的追加・削除が必要な時
- 疎結合なモジュール設計が必要な時
- 拡張ポイントを提供するフレームワークを設計する時
- 型安全なプラグイン登録メカニズムを実装する時
- ロード順序の依存性を明確に管理する時

### 避けるべきこと

- プラグイン間の循環依存を許可しない
- グローバル状態を使用してプラグイン間通信を行わない
- 型安全性なしでプラグインレジストリを実装しない
- ライフサイクルフックなしで動的ロードを行わない
- 依存性注入なしでプラグイン間の依存を解決しない

## リソース参照

### references/（詳細知識）

| リソース           | パス                                                                         | 内容                       |
| ------------------ | ---------------------------------------------------------------------------- | -------------------------- |
| 基礎知識           | See [references/Level1_basics.md](references/Level1_basics.md)               | プラグインの基本概念       |
| 実装パターン       | See [references/Level2_intermediate.md](references/Level2_intermediate.md)   | レジストリ・DI実装パターン |
| 高度なテクニック   | See [references/Level3_advanced.md](references/Level3_advanced.md)           | 動的ロード・スケーリング   |
| エキスパート知見   | See [references/Level4_expert.md](references/Level4_expert.md)               | 大規模システムの設計知見   |
| レジストリパターン | See [references/registry-pattern.md](references/registry-pattern.md)         | 型安全なレジストリ詳細     |
| ライフサイクル管理 | See [references/plugin-lifecycle.md](references/plugin-lifecycle.md)         | 初期化・シャットダウン     |
| 依存性注入         | See [references/dependency-injection.md](references/dependency-injection.md) | DI Container設計           |
| 動的ロード         | See [references/dynamic-loading.md](references/dynamic-loading.md)           | 動的モジュールロード       |
| サービスロケーター | See [references/service-locator.md](references/service-locator.md)           | Service Locatorパターン    |

### scripts/（決定論的処理）

| スクリプト                      | 用途               | 使用例                                                          |
| ------------------------------- | ------------------ | --------------------------------------------------------------- |
| `validate-plugin-structure.mjs` | プラグイン構造検証 | `node scripts/validate-plugin-structure.mjs src/features`       |
| `validate-skill.mjs`            | スキル構造検証     | `node scripts/validate-skill.mjs`                               |
| `log_usage.mjs`                 | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート                 | 用途                              |
| ---------------------------- | --------------------------------- |
| `plugin-implementation.md`   | IPlugin実装、ライフサイクルフック |
| `registry-implementation.md` | 型安全なRegistry実装              |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、構造再編成 |
| 1.0.0   | 2025-12-31 | 初版                                 |
