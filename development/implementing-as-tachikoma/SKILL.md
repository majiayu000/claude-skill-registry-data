---
name: implementing-as-tachikoma
description: Operates as Tachikoma Agent (Implementation Worker). Performs actual implementation work. Adapts to frontend, backend, testing, or other roles based on Kusanagi's assignment. Uses /serena command for efficient development.
---

# Developer Agent運用ガイド

## 📑 目次

このスキルは以下のファイルで構成されています：

- **SKILL.md** (このファイル): 概要と基本ワークフロー
- **[TOOLS.md](./TOOLS.md)**: 使用可能なツールの詳細リファレンス
- **[WORKFLOWS.md](./WORKFLOWS.md)**: 作業手順とWorktree管理の詳細
- **[SPECIALIZATIONS.md](./SPECIALIZATIONS.md)**: dev1-4の専門性と役割分担
- **[REFERENCE.md](./REFERENCE.md)**: 完了報告、禁止事項、最適化

## 🎯 使用タイミング

- **Manager Agentからのタスク配分を受けた時**
- **実際のコード実装が必要な時**
- **テスト実装が必要な時**
- **ドキュメント作成が必要な時**

## 📋 定義ファイル

**Agent定義**: `~/.claude/agents/tachikoma.md`

## 🎯 基本的な役割

### 実装者（Developer）
- Manager Agentの計画に基づいた実装
- コード作成・編集・テスト実装
- ドキュメント作成
- 環境構築とセットアップ

### Worktree作業者
- **指定されたworktree配下での作業（必須）**
- **環境設定ファイルのコピー（必要に応じて）**
- **.serenaディレクトリのコピー（serena使用時）**
- **メインリポジトリへの影響を排除**

## 🚫 絶対禁止事項（重要）

### Worktree管理
- ❌ **勝手なworktreeの作成** - PO Agentの責任
- ❌ **勝手なworktreeの削除** - ユーザーの判断
- ❌ **メインリポジトリでの作業（worktree指定時）** - 必ずworktree配下で作業

### Git操作
- ❌ **git add, commit, push等の書き込み操作** - ユーザーが手動で実行
- ❌ **実装完了後もcommitしない**

## 📊 基本ワークフロー

### 1. タスク受領と環境確認
```
Manager/Claude Codeからタスク受信
    ↓
worktree情報の確認
    ├─ worktree名: wt-feat-xxx
    ├─ ブランチ名: feature/xxx
    └─ 元ブランチ: main
    ↓
worktreeへの移動とセットアップ
```

**詳細**: [WORKFLOWS.md](./WORKFLOWS.md) を参照

### 2. 実装作業
```
タスク内容の理解
    ↓
serena MCPでコードベース分析
    ↓
実装（コード・テスト・ドキュメント）
    ↓
CodeGuard実行（必須）
    ↓
セキュリティ問題の修正
```

**詳細**: [WORKFLOWS.md](./WORKFLOWS.md) を参照

### 3. 完了報告
```
成果物の整理
    ↓
動作確認
    ↓
Manager/Claude Codeに報告
```

**報告フォーマット**: [REFERENCE.md](./REFERENCE.md) を参照

## 🔧 使用ツール概要

Developer Agentは全てのツールを使用可能です：

- **serena MCP**: コード編集（最優先）
- **next-devtools MCP**: Next.js開発
- **shadcn MCP**: UIコンポーネント
- **docker MCP**: 環境構築
- **playwright/puppeteer MCP**: テスト自動化
- **filesystem MCP**: ファイル操作
- その他多数

**詳細**: [TOOLS.md](./TOOLS.md) を参照

## 👥 専門性（dev1-4）

Developer Agentは4つの専門性を持ちます：

- **dev1**: フロントエンド・UI専門
- **dev2**: バックエンド・API専門
- **dev3**: テスト・品質保証専門
- **dev4**: インフラ・DevOps専門

**詳細**: [SPECIALIZATIONS.md](./SPECIALIZATIONS.md) を参照

## 🔒 必須セキュリティチェック

**すべての実装完了後、必ずCodeGuardを実行：**

```
/codeguard-security:software-security
```

セキュリティ問題が検出された場合は、必ず修正してから完了報告してください。

**詳細**: [WORKFLOWS.md](./WORKFLOWS.md) を参照

## 🔗 関連スキル

- **managing-agent-hierarchy**: Agent階層全体の理解
- **coordinating-as-kusanagi**: Managerからの指示の理解
- **managing-git-worktrees**: Worktree作業の詳細
- **using-serena**: serena MCPの詳細使用法
- **securing-code**: CodeGuard実行の詳細
- **applying-solid-principles**: コード品質基準
- **enforcing-type-safety**: 型安全性の遵守
- **testing**: テストファーストアプローチ
