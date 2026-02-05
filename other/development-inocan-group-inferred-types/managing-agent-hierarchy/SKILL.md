---
name: managing-agent-hierarchy
description: Manages Agent hierarchy (PO→Manager→Developer). Required for all code modifications except minor fixes. Optimizes performance through parallel execution.
---

# Agent階層管理システム

## 📚 ナビゲーション

- **[ROLES.md](ROLES.md)** - 各Agent（PO、Manager、Developer）の役割と責任
- **[WORKFLOWS.md](WORKFLOWS.md)** - 実行順序とコンテキスト管理フロー
- **[PARALLEL-EXECUTION.md](PARALLEL-EXECUTION.md)** - 並列/段階的/順次実行パターン
- **[GUIDELINES.md](GUIDELINES.md)** - 判断基準、例外ケース、最適化

## 🎯 使用タイミング

- **コード修正が必要な全タスク（小規模修正以外）**
- **複雑なタスク分解が必要な時**
- **並行開発が必要な時**
- **戦略的な判断が必要な時**

## 🚨 最重要ルール

**小さな修正以外は、必ずPO→Manager→Developerの階層的Agentシステムを使用してください。**

### 基本原則

1. **PO Agent** - 戦略決定とWorktree管理
2. **Manager Agent** - タスク配分とWorktree情報伝達
3. **Developer Agents** - 実装（並列実行）

### Claude Code本体の責任

- **実装は絶対に行わない**
- Agentシステムを起動して指示
- Developer起動時は並列実行を徹底

## 📂 Agent定義ファイルの場所

```
~/.claude/agents/
├── aramaki.md      # PO Agent定義
├── kusanagi.md     # Manager Agent定義
└── tachikoma.md    # Developer Agent定義
```

## ✅ 直接実装可能な例外

以下の場合のみ、Agentシステムを使わず直接実装可能：

- 単純なファイル読み込み（1-2ファイル）
- 1行程度の簡単な修正
- 単純な質問への回答
- ファイル一覧表示

## ❌ 必ずAgentを使用すべきケース

- 新機能実装
- 複数ファイルのバグ修正
- リファクタリング
- テスト実装
- ドキュメント作成（複数ファイル）
- 複雑な調査・分析

## 🚀 並列実行の鉄則

- **Developer起動は必ず1つのメッセージで同時実行**
- **独立タスクは絶対に並列化**
- **段階的実行でも各段階内は並列化**

詳細は [PARALLEL-EXECUTION.md](PARALLEL-EXECUTION.md) を参照してください。

## 📋 実行フロー概要

```
タスク受信
    ↓
コード修正が必要？
    ├─ No → 直接実行可能
    └─ Yes → Agentシステム使用
        ↓
        1. PO Agent起動（戦略決定＋Worktree管理）
        ↓
        2. Manager Agent起動（タスク配分＋Worktree情報伝達）
        ↓
        3. Developer Agents並列起動（実装）
```

詳細は [WORKFLOWS.md](WORKFLOWS.md) を参照してください。

## 🔗 関連スキル

- **managing-as-aramaki**: PO Agentの詳細な使い方
- **coordinating-as-kusanagi**: Manager Agentの詳細な使い方
- **implementing-as-tachikoma**: Developer Agentの詳細な使い方
- **managing-git-worktrees**: Worktree管理の詳細

## 🎓 学習パス

1. このファイル（概要理解）
2. [ROLES.md](ROLES.md)（各Agentの役割理解）
3. [WORKFLOWS.md](WORKFLOWS.md)（実行フロー理解）
4. [PARALLEL-EXECUTION.md](PARALLEL-EXECUTION.md)（並列実行パターン）
5. [GUIDELINES.md](GUIDELINES.md)（判断基準と最適化）
