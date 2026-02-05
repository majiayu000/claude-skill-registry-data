---
name: agent-dependency-design
description: |
  Specializes in agent dependency and interface design. Defines skill references, command coordination, and inter-agent collaboration protocols while preventing circular dependencies to build effective multi-agent systems.

  Anchors:
  • "The Pragmatic Programmer" (Andrew Hunt, David Thomas) / Application: Procedure design and practical improvement / Purpose: Build effective agent collaboration mechanisms
  • "Software Architecture in Practice" (Len Bass, Paul Clements, Rick Kazman) / Application: Interface design patterns / Purpose: Minimize dependencies and improve maintainability

  Trigger:
  Use when defining inter-agent data handoffs, designing multi-agent collaboration, detecting or resolving circular dependencies, or defining handoff protocols.
  agent collaboration, dependency graph, handoff protocol, circular dependency, skill reference, multi-agent system

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# エージェント依存関係デザイン

## 概要

エージェント依存関係とインターフェース設計を専門とするスキル。
スキル参照、コマンド連携、エージェント間協調のプロトコルを定義し、
循環依存を防ぎながら効果的なマルチエージェントシステムを構築します。

このスキルは以下の主要領域をカバーしています：

- **ハンドオフプロトコル**: エージェント間のデータ受け渡し仕様
- **循環依存検出**: 自動的に依存関係の問題を検出・解消
- **エージェントインターフェース設計**: 明確で保守性の高い協調メカニズム
- **スキル参照**: エージェント間のスキル依存関係の管理

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要なリソース、スクリプト、テンプレートを特定
3. エージェント間の依存関係を図示する

**Task**: `agents/analyze-context.md` を参照

### Phase 2: スキル適用と設計

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. `assets/handoff-protocol-template.json` を基に協調プロトコルを定義
3. `scripts/check-circular-deps.mjs` を使用して循環依存をチェック
4. 重要な判断点をメモとして残す

**Task**: `agents/design-dependencies.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す
4. `scripts/check-circular-deps.sh` で最終的な依存関係チェックを実施

**Task**: `agents/validate-dependencies.md` を参照

---

## Task仕様ナビ

| Task                  | 起動タイミング | 入力             | 出力             |
| --------------------- | -------------- | ---------------- | ---------------- |
| analyze-context       | Phase 1開始時  | タスク仕様       | コンテキスト分析 |
| design-dependencies   | Phase 2開始時  | コンテキスト分析 | 設計ドキュメント |
| validate-dependencies | Phase 3開始時  | 設計ドキュメント | 検証結果レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

- エージェント間の情報受け渡しを明確に定義する
- ハンドオフプロトコルを JSON スキーマで厳密に定義する
- `scripts/check-circular-deps.mjs` を使用して定期的に依存関係を検証する
- レベル別リソースを順序通り学習して段階的に理解を深める
- エージェント間のインターフェースを文書化し、チーム全体で共有する
- 依存関係は DAG (有向非環グラフ) 構造を保つ
- エージェント間のエラーハンドリング戦略を事前に定義する

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける
- 循環依存を許容する設計を避ける
- 暗黙的なハンドオフ仕様を避ける
- エージェント間の密結合を避ける
- スキル参照の責任を不明確にすることを避ける
- テンプレートを参照せずに独自のプロトコルを設計することを避ける

## リソース参照

### 学習リソース

| リソース                            | 用途                                              |
| ----------------------------------- | ------------------------------------------------- |
| `references/Level1_basics.md`       | 基本概念と用語の理解                              |
| `references/Level2_intermediate.md` | 実務的な設計パターン                              |
| `references/Level3_advanced.md`     | 応用パターンと最適化                              |
| `references/Level4_expert.md`       | 高度なシステム設計                                |
| `references/dependency-patterns.md` | 4種類の依存関係パターンと標準ハンドオフプロトコル |
| `references/legacy-skill.md`        | 旧SKILL.mdの参考資料                              |

### 実装ツール

| ツール                                  | 機能                             |
| --------------------------------------- | -------------------------------- |
| `scripts/check-circular-deps.mjs`       | Node.js環境での循環依存検出      |
| `scripts/check-circular-deps.sh`        | Shell環境での循環依存検出        |
| `scripts/validate-skill.mjs`            | スキル構造検証                   |
| `scripts/log_usage.mjs`                 | 使用記録・自動評価               |
| `assets/handoff-protocol-template.json` | ハンドオフプロトコルテンプレート |

## コマンドリファレンス

### リソース読み取り

```bash
cat .claude/skills/agent-dependency-design/references/Level1_basics.md
cat .claude/skills/agent-dependency-design/references/Level2_intermediate.md
cat .claude/skills/agent-dependency-design/references/Level3_advanced.md
cat .claude/skills/agent-dependency-design/references/Level4_expert.md
cat .claude/skills/agent-dependency-design/references/dependency-patterns.md
cat .claude/skills/agent-dependency-design/references/legacy-skill.md
```

### スクリプト実行

```bash
node .claude/skills/agent-dependency-design/scripts/check-circular-deps.mjs --help
.claude/skills/agent-dependency-design/scripts/check-circular-deps.sh
node .claude/skills/agent-dependency-design/scripts/log_usage.mjs --help
node .claude/skills/agent-dependency-design/scripts/validate-skill.mjs --help
```

### テンプレート参照

```bash
cat .claude/skills/agent-dependency-design/assets/handoff-protocol-template.json
```

## 変更履歴

| Version | Date       | Changes                                                                                      |
| ------- | ---------- | -------------------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | agents/追加、Task仕様ナビ改善                                                                |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様への完全移行：Trigger追加、Task仕様ナビ実装、allowed-tools定義、日本語化完了 |
