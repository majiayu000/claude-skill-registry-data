---
name: multi-agent-systems
description: |
  マルチエージェントシステム設計を専門とするスキル。
  複数のエージェント間の効果的な協調、ハンドオフプロトコルの設計、情報受け渡しメカニズムにより、
  スケーラブルで保守性の高い分散システムを構築する。

  Anchors:
  • Building Microservices (Sam Newman) / 適用: サービス間の協調設計 / 目的: 疎結合で信頼性の高いエージェント連携
  • Patterns of Enterprise Application Architecture (Martin Fowler) / 適用: ハンドオフパターン / 目的: 明確なプロトコル設計
  • Working Effectively with Legacy Code (Michael Feathers) / 適用: 既存システムとの統合 / 目的: 段階的なエージェント導入

  Trigger:
  Use when designing multi-agent collaboration, defining handoff protocols, optimizing inter-agent communication, or managing agent dependencies.
  multi-agent, agent collaboration, handoff protocol, delegation, chaining, parallel agents, feedback loop, orchestration
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# マルチエージェントシステム設計

## 概要

複数のインテリジェントエージェントが協働するシステムの設計と実装を専門とするスキル。
エージェント間の効果的なコミュニケーション、ハンドオフプロトコルの実装、情報受け渡しの最適化を通じて、
スケーラブルで信頼性の高い分散システムを構築する。

## ワークフロー

### Phase 1: 要件分析と協調パターン選定

**目的**: マルチエージェントシステムの要件を分析し、最適な協調パターンを選定

**参照エージェント**: `agents/requirements-analyst.md`

**アクション**:

1. ビジネス要件と制約条件を分析
2. `references/collaboration-patterns.md` で協調パターンを理解
3. 4パターン（委譲・連鎖・並行・フィードバック）から最適なものを選定
4. エージェント数、役割、相互作用パターンを特定

### Phase 2: プロトコル設計と実装

**目的**: ハンドオフプロトコルと協調メカニズムを設計・実装

**参照エージェント**: `agents/protocol-designer.md`

**アクション**:

1. `assets/handoff-protocol-template.json` を参考にプロトコル定義
2. エージェント間の依存関係グラフを作成
3. 情報受け渡しフロー（input/output）を明確化
4. エラーハンドリングと同期メカニズムを設計
5. `scripts/analyze-collaboration.mjs` で設計を検証

### Phase 3: 品質検証と最適化

**目的**: 成果物の品質確認と実装の最適化

**参照エージェント**: `agents/quality-validator.md`

**アクション**:

1. エージェント間の通信オーバーヘッドを分析
2. スケーラビリティと信頼性を検証
3. 終了条件とタイムアウトの妥当性を確認（特にフィードバックパターン）
4. `scripts/log_usage.mjs` で実行記録を保存

## リソース参照

### 参照ドキュメント

| ドキュメント                                                                 | 内容                       |
| ---------------------------------------------------------------------------- | -------------------------- |
| [references/basics.md](references/basics.md)                                 | マルチエージェント基本概念 |
| [references/patterns.md](references/patterns.md)                             | 実装パターン、設計戦略     |
| [references/collaboration-patterns.md](references/collaboration-patterns.md) | 4協調パターン詳細          |

### エージェント

| エージェント                     | 役割                       |
| -------------------------------- | -------------------------- |
| `agents/requirements-analyst.md` | 要件分析、協調パターン選定 |
| `agents/protocol-designer.md`    | ハンドオフプロトコル設計   |
| `agents/quality-validator.md`    | 品質検証、最適化提案       |

### スクリプト

| スクリプト                          | 用途                       |
| ----------------------------------- | -------------------------- |
| `scripts/analyze-collaboration.mjs` | 協調パターン分析、設計検証 |
| `scripts/validate-skill.mjs`        | スキル構造検証             |
| `scripts/log_usage.mjs`             | 使用記録                   |

### テンプレート

| テンプレート                            | 用途                     |
| --------------------------------------- | ------------------------ |
| `assets/handoff-protocol-template.json` | ハンドオフプロトコル定義 |

## ベストプラクティス

### すべきこと

- 明確なハンドオフプロトコル定義（標準フォーマット使用）
- エラーハンドリング戦略の事前設計
- 終了条件とタイムアウトの設定（特にフィードバックパターン）
- 依存関係の可視化とドキュメント化
- 非同期通信の活用（スケーラビリティ確保）

### 避けるべきこと

- 循環依存（エージェント間の循環参照）
- 無限フィードバックループ（終了条件なし）
- 過度な並行化（リソース枯渇）
- プロトコルなしの通信
- エラーハンドリングの省略
