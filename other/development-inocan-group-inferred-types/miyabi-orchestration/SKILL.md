---
name: miyabi-orchestration
description: |
  Miyabi CoordinatorAgent統合スキル - DAGベースのタスク統括・並列実行制御。
  GitHub Issueを複数タスクに分解し、依存関係グラフを構築して並行実行を統括。

  Use when:
  - 複数タスクの並列実行が必要な時
  - Issueをタスク分解する時
  - DAG（有向非巡回グラフ）で依存関係を管理する時
  - Agent実行の統括・オーケストレーションが必要な時
  - "agent-run", "並列実行", "タスク分解", "DAG" がキーワードに含まれる時
allowed-tools: Read, Grep, Glob, Bash, Task, TodoWrite
---

# Miyabi Orchestration Skill (CoordinatorAgent)

タスク統括・並列実行制御のためのスキル。識学理論に基づく自律オーケストレーション。

## 役割

- Issue → Task分解 (1-3時間単位)
- DAG (有向非巡回グラフ) 構築
- トポロジカルソート実行
- Agent種別の自動判定・割り当て
- 並行度算出 (最大5並行)
- 進捗モニタリング・レポート生成
- 循環依存検出・エスカレーション

## 実行権限

**統括権限**: タスク分解・Agent割り当て・リソース配分を決定可能

## 処理アルゴリズム

- **タスク分解**: チェックボックス/番号リスト/見出し自動検出
- **DAG構築**: Kahn's Algorithm によるトポロジカルソート
- **並行実行**: レベル順実行 (依存関係を保証)
- **循環依存検出**: DFS (深さ優先探索) による検出

## タスク判定ルール

| キーワード | タスク種別 | 割り当てAgent |
|-----------|----------|--------------|
| feature/add/new | feature | CodeGenAgent |
| bug/fix/error | bug | CodeGenAgent |
| refactor/cleanup | refactor | CodeGenAgent |
| doc/documentation | docs | CodeGenAgent |
| test/spec | test | CodeGenAgent |
| deploy/release | deployment | DeploymentAgent |

## Severity判定

| キーワード | Severity | 対応時間 |
|-----------|---------|---------|
| critical/urgent/blocking | Sev.1-Critical | 即座 |
| high priority/important | Sev.2-High | 24時間以内 |
| (デフォルト) | Sev.3-Medium | 1週間以内 |
| minor/small | Sev.4-Low | 2週間以内 |

## 実行コマンド

```bash
# 単一Issue実行
npm run agents:parallel:exec -- --issues=270 --concurrency=2

# 複数Issue並行実行
npm run agents:parallel:exec -- --issues=270,240,276 --concurrency=3

# Task tool統合モード
USE_TASK_TOOL=true npm run agents:parallel:exec -- --issues=270

# Worktree分離モード
USE_WORKTREE=true npm run agents:parallel:exec -- --issues=276
```

## DAG構築例

### 入力 (Issue #300)
```markdown
## タスク一覧
- [ ] Firebase Auth修正 (#270)
- [ ] E2Eテスト追加 (depends: #270)
- [ ] ドキュメント更新 (depends: #270)
```

### 出力 (DAG)
```yaml
levels:
  - [task-270]           # Level 0 (並行実行可能)
  - [task-300-1, task-300-2]  # Level 1 (task-270完了後)
```

## エスカレーション条件

| 問題種別 | エスカレーション先 | 重要度 |
|---------|------------------|--------|
| 循環依存検出 | TechLead | Sev.2-High |
| タスク分解不能 | TechLead | Sev.2-High |
| 要件不明確 | PO | Sev.2-High |

## メトリクス

- **実行時間**: 通常1-3分
- **並行度**: 平均2-3並行
- **成功率**: 95%+
- **DAG構築時間**: <5秒

## 関連Agent

- CodeGenAgent: コード生成実行
- ReviewAgent: 品質判定
- PRAgent: PR作成
- DeploymentAgent: デプロイ実行
