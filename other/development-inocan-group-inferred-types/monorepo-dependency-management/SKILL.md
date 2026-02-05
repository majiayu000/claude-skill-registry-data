---
name: monorepo-dependency-management
description: |
  モノレポ環境での依存関係管理、ワークスペース間の整合性維持を専門とするスキル。
  pnpm workspaces、変更影響分析、パッケージ間バージョン同期、循環依存検出の方法論を提供する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt) / 適用: 実践的改善と品質維持 / 目的: モノレポの段階的構築と保守性向上
  • Program Development in Java (Barbara Liskov) / 適用: 抽象化と依存関係設計 / 目的: パッケージ間の明確な境界定義
  • pnpm workspace protocol / 適用: workspace:*による内部依存定義 / 目的: ワークスペース構造の標準化

  Trigger:
  Use when managing monorepo dependencies, analyzing workspace relationships, synchronizing package versions, detecting circular dependencies, or configuring pnpm workspaces.
  monorepo, pnpm, workspace, dependency graph, version sync, circular dependency, hoisting, turborepo
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# モノレポ依存関係管理

## 概要

モノレポ環境での依存関係管理、ワークスペース間の整合性維持を専門とするスキル。
pnpm workspaces、変更影響分析、パッケージ間バージョン同期の方法論を提供する。

## ワークフロー

### Phase 1: ワークスペース構造の理解

**目的**: モノレポの現在の構造と依存関係を把握

**参照エージェント**: `agents/dependency-analysis.md`

**アクション**:

1. pnpm-workspace.yaml の構造を確認
2. `scripts/analyze-workspace-deps.mjs` で依存グラフを可視化
3. 循環依存の有無を検出
4. 各パッケージの役割と依存関係を整理

### Phase 2: 設計と実装

**目的**: ワークスペース構成の最適化または新規セットアップ

**参照エージェント**: `agents/workspace-setup.md`, `agents/version-sync.md`

**アクション**:

1. pnpm-workspace.yamlの設計・更新
2. workspace:\*プロトコルによる内部依存設定
3. バージョン同期戦略の決定（カタログ機能活用）
4. `references/pnpm-workspace-setup.md` で設定パターンを確認

### Phase 3: ホイスティング最適化と検証

**目的**: 依存解決の最適化と構造検証

**参照エージェント**: `agents/hoisting-optimization.md`

**アクション**:

1. shamefully-hoist設定の検討
2. public-hoist-patternの設定
3. `scripts/analyze-workspace-deps.mjs` で最終検証
4. `scripts/log_usage.mjs` で実行記録

## リソース参照

### 参照ドキュメント

| ドキュメント                                                                   | 内容                                 |
| ------------------------------------------------------------------------------ | ------------------------------------ |
| [references/basics.md](references/basics.md)                                   | モノレポ基本概念、pnpm workspace基礎 |
| [references/patterns.md](references/patterns.md)                               | 依存管理パターン、設計戦略           |
| [references/pnpm-workspace-setup.md](references/pnpm-workspace-setup.md)       | pnpm-workspace.yaml設定詳細          |
| [references/change-impact-analysis.md](references/change-impact-analysis.md)   | 変更影響分析、依存グラフ解析         |
| [references/version-synchronization.md](references/version-synchronization.md) | バージョン同期戦略                   |
| [references/dependency-hoisting.md](references/dependency-hoisting.md)         | ホイスティング設定最適化             |

### エージェント

| エージェント                      | 役割                         |
| --------------------------------- | ---------------------------- |
| `agents/dependency-analysis.md`   | 依存グラフ分析、循環依存検出 |
| `agents/workspace-setup.md`       | ワークスペース初期設定       |
| `agents/version-sync.md`          | バージョン同期管理           |
| `agents/hoisting-optimization.md` | ホイスティング最適化         |

### スクリプト

| スクリプト                           | 用途                         |
| ------------------------------------ | ---------------------------- |
| `scripts/analyze-workspace-deps.mjs` | 依存グラフ分析、循環依存検出 |
| `scripts/validate-skill.mjs`         | スキル構造検証               |
| `scripts/log_usage.mjs`              | 使用記録                     |

## ベストプラクティス

### すべきこと

- workspace:\*プロトコルで内部依存を明示
- 循環依存は検出したら即座に解決
- バージョン同期はカタログ機能で自動化
- 定期的な依存グラフ分析で健全性維持
- 変更前に影響範囲を確認

### 避けるべきこと

- 循環依存の放置
- バージョンの不整合（共有パッケージのバージョン分散）
- 過度なホイスティング（必要に応じて制御）
- レベルをスキップした設定（基本を理解してから応用）
