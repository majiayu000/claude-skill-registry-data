---
name: create-worktree
description: Git worktree を作成し、並行開発用の独立したブランチ環境を構築する。プラットフォーム固有コード開発時に使用。
---

# Git Worktree Creator

planモード終了後、feature開発用の独立したworktree環境を自動作成します。

## 概要

このスキルは以下を自動で実行します：

1. `.worktrees/<feature-name>/` ディレクトリにworktreeを作成
2. `feature/<feature-name>` ブランチを新規作成
3. 環境変数ファイル（`.env`, `.envrc` など）を自動コピー

## 使用方法

### 基本的な使い方

```bash
bash .opencode/skill/create-worktree/scripts/create_worktree.sh <feature-name>

# 例: Issue #42 用の worktree を作成
bash .opencode/skill/create-worktree/scripts/create_worktree.sh issue-42-auth
```

### 実行結果

```
.worktrees/issue-42-auth/     # worktreeディレクトリ
├── .env                      # ルートからコピー
├── .envrc                    # ルートからコピー
└── ...（その他のファイル）
```

## コピーされる環境変数ファイル

| ファイル | 説明 |
|---------|------|
| `.env` | ルートレベルの環境変数 |
| `.envrc` | direnv設定 |
| `.env.local` | ローカル開発用 |

## 作業完了後

### PR作成とworktree削除を同時に行う（推奨）

**pr-and-cleanup** スキルを使用すると、PR作成とworktree削除を自動で行えます：

```bash
cd .worktrees/<feature-name>
bash ../../.opencode/skill/pr-and-cleanup/scripts/pr_and_cleanup.sh
```

詳細は [pr-and-cleanup スキル](../pr-and-cleanup/SKILL.md) を参照してください。

### 手動でworktreeを削除する場合

```bash
git worktree remove .worktrees/<feature-name>
```

## 詳細

詳細については [REFERENCE.md](REFERENCE.md) を参照してください。
