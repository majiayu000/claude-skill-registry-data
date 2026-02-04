---
name: multi-turn-conversation
description: |
  複数ターンに渡る対話の設計と状態管理を実現するスキル。エージェント・ユーザー間の対話フロー、コンテキスト管理、ターン管理を通じて、一貫性のある対話体験を構築します。

  Anchors:
  • The Pragmatic Programmer / 適用: ターン設計と状態管理の手順設計 / 目的: 対話フローの体系的な構築
  • Conversation Design Pattern / 適用: マルチターン対話パターン / 目的: 実務的な対話フロー実装

  Trigger:
  Use when designing multi-turn conversation flows, implementing dialogue state management, tracking user intent across turns, managing conversation context, or ensuring consistency in long-running dialogues.
  Keywords: multi-turn, dialogue, conversation flow, context management, state tracking, turn management, conversation design

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep

version: 1.2.0
level: 1
last_updated: 2025-12-31
---

# Multi Turn Conversation

## 概要

複数ターンに渡る対話の設計と状態管理を実現するスキル。エージェント・ユーザー間の対話フロー、コンテキスト管理、ターン管理を通じて、一貫性のある対話体験を構築します。このスキルは以下を実現します：

- **ターン管理**: ユーザーメッセージとエージェント応答の順序と依存関係を管理
- **コンテキスト保持**: 対話全体の履歴と現在の文脈を維持
- **状態追跡**: ユーザー意図、タスク進捗、メタ情報の一貫性確保
- **応答整合性**: 過去の発言との矛盾を防止し、連続性を保証
- **流動的遷移**: 対話パターンの柔軟な状態遷移設計

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: 対話設計タスクの目的と前提条件を明確にする

**参照エージェント**: `agents/requirements-analysis.md`

**アクション**:

1. 対話の目的とユースケースを確認（サポートチャット、ウィザード、分析等）
2. `references/basics.md` で対話パターンの基礎を理解
3. コンテキスト保持方式と状態管理の戦略を選定
4. 必要なリソースを特定

### Phase 2: スキル適用と設計実装

**目的**: マルチターン対話の設計・実装を進める

**参照エージェント**: `agents/dialogue-flow-designer.md`

**アクション**:

1. `references/patterns.md` で実装パターンを確認
2. 対話フロー図またはメッセージスキーマを設計
3. ターン管理メカニズム（メモリ・DB・キャッシュ等）を選定
4. コンテキスト更新ロジックを実装（`references/context-patterns.md` 参照）
5. エラーハンドリング戦略を設計（`references/error-handling-patterns.md` 参照）

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**参照エージェント**: `agents/quality-validator.md`

**アクション**:

1. 対話フローの一貫性と正確性を確認
2. エッジケース（コンテキスト喪失、超長対話等）への対応を検証（`references/edge-cases.md` 参照）
3. `scripts/validate-skill.mjs` でスキル構造を確認
4. `scripts/log_usage.mjs` を実行して使用記録を保存

## ベストプラクティス

### すべきこと

- **ターン番号管理**: 各メッセージにターンIDを付与し、順序を明確化
- **コンテキスト参照**: 最新N個の対話ターンを常に参照可能な構造にする
- **意図の明示**: ユーザー意図を明確に解析し、状態に保存
- **境界の設定**: 超長対話時のコンテキスト折りたたみやサマリー化を実装
- **エラーハンドリング**: コンテキスト喪失時のフォールバック機構を用意
- **監査ログ**: 対話履歴を完全に記録して問題追跡可能にする

### 避けるべきこと

- グローバル状態への直接アクセス（状態オブジェクトを通じた管理）
- ターン情報の削除（監査要件との矛盾）
- ユーザー意図の同期ズレ（毎ターン明示的に更新）
- コンテキスト無制限保持（メモリ圧迫へのリスク）
- 仮定に基づくユーザー状態操作（常に確認メッセージを送信）

## リソース参照

### 参照ドキュメント

| ドキュメント                                                                   | 内容                       |
| ------------------------------------------------------------------------------ | -------------------------- |
| [references/basics.md](references/basics.md)                                   | マルチターン対話基礎概念   |
| [references/patterns.md](references/patterns.md)                               | 実装パターン、設計戦略     |
| [references/context-patterns.md](references/context-patterns.md)               | コンテキスト管理パターン集 |
| [references/state-management-guide.md](references/state-management-guide.md)   | 状態管理ガイド             |
| [references/edge-cases.md](references/edge-cases.md)                           | エッジケース対応           |
| [references/error-handling-patterns.md](references/error-handling-patterns.md) | エラーハンドリングパターン |

### エージェント

| エージェント                       | 役割                       |
| ---------------------------------- | -------------------------- |
| `agents/requirements-analysis.md`  | 要件分析、対話設計方針決定 |
| `agents/dialogue-flow-designer.md` | 対話フロー設計             |
| `agents/quality-validator.md`      | 品質検証、エッジケース確認 |

### スクリプト

| スクリプト                   | 用途           |
| ---------------------------- | -------------- |
| `scripts/validate-skill.mjs` | スキル構造検証 |
| `scripts/log_usage.mjs`      | 使用記録       |
