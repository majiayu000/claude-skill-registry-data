---
name: GitWorkflow
description: Gitを使用した開発ワークフローのルールです。ブランチの変更、Worktreeの作成、Pull Requestの作成時に必ず確認し遵守してください。
---

# Role
あなたはGitワークフローを遵守する開発アシスタントです。コードの変更を行う前に、必ず現在のブランチ状況を確認し、以下のフローに従ってください。

# Git Workflow Rules

## 1. Pre-work Check (作業前のブランチ確認)
作業を開始する前に、まず `git branch --show-current` 等で現在のブランチを確認してください。

### A. 現在が `main` (または `master`) ブランチの場合
**重要: mainブランチでの直接作業、および `main` ディレクトリでのブランチ切り替え（`checkout -b`）は禁止されています。**
新しい機能開発や修正を行う場合は、必ず `git worktree` を使用して新しい作業ディレクトリを作成してください。

1. **提案**: ユーザーに `/create_worktree` コマンドの使用、または以下の手動手順を提案してください。
2. **手順**:
   - `git pull origin main` で最新化。
   - `git worktree add ../<directory-name> -b <branch-name>` で新しいWorktreeを作成。

### B. 現在が `main` 以外のブランチ（Worktree内）の場合
既に作業用Worktreeにいると判断し、そのまま作業を開始してください。

## 2. Pull Request (PR作成)
作業完了後のPull Request（PR）作成支援においては、以下のルールを適用してください。
- **言語:** タイトルおよび説明文は必ず「日本語」で記述すること。
- 内容: 変更の概要、目的、関連するIssue番号を含めること。

# Behavior Guidelines
- ユーザーからタスクを依頼された際、いきなりコードを生成しないでください。
- まず現在のブランチを確認し、`main` であれば必ず **「新しいWorktreeの作成」** を提案してください（単なるブランチ作成ではありません）。
- `/create_worktree` ワークフローの利用を推奨してください。
