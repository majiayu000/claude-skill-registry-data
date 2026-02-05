---
name: starting-issues
description: Issue作業を開始し、ブランチを作成してPlanモードに入る。Use when the user wants to start working on an issue (Issue対応開始), begin a task (タスク開始), or tackle a GitHub issue (課題着手).
allowed-tools: Bash(gh issue:*), Bash(git checkout:*), Bash(git pull:*), Bash(git branch:*), Bash(git stash:*), Bash(git rev-parse:*), Bash(git show-ref:*), Bash(git worktree:*), Bash(mkdir:*), Bash(cd:*), Bash(pwsh:*), Bash(bash:*), AskUserQuestion, EnterPlanMode, WebSearch, WebFetch, Skill
---

# Issue作業開始

## Quick start

Issue番号を決定し、worktreeを作成（または既存worktreeに移動）して、EnterPlanModeで実装計画を立てる。

## リポジトリ情報

!`git remote -v`

## 現在のブランチ

!`git branch --show-current`

## Open Issues一覧

!`gh issue list --state open`

## Instructions

### 1. Issue番号の決定

- 引数 `$1` が指定されている場合: Issue #$1 の作業を開始
- 引数がない場合: Open Issues一覧から `AskUserQuestion` で作業するIssueを選択

### 2. Issueの詳細確認

```bash
gh issue view {番号}
```

### 3. 作業環境の準備

worktreeを作成（または既存worktreeを検出）し、作業ディレクトリへ移動する。

#### 3.1 スクリプトでworktreeを作成

**Windows環境（pwsh）**:
```powershell
$worktreePath = pwsh -File .claude/skills/starting-issues/scripts/Setup-Worktree.ps1 -Issue {番号}
```

**Linux/macOS環境（bash）**:
```bash
worktreePath=$(bash .claude/skills/starting-issues/scripts/setup-worktree.sh {番号})
```

スクリプトは以下を行う:
- リポジトリルートを取得
- worktrees用ディレクトリ `[リポジトリ名]-worktrees/` を作成（存在しない場合）
- ブランチ `fix-issue-{番号}` の存在を確認
- worktreeが既に存在すればそのパスを返す
- 存在しなければ新規作成してパスを返す

**作成されるパス**:
- worktrees用ディレクトリ: `[リポジトリ親ディレクトリ]/[リポジトリ名]-worktrees/`
- worktreeパス: `[worktrees用ディレクトリ]/fix-issue-{番号}`
- ブランチ名: `fix-issue-{番号}`

#### 3.2 作業ディレクトリへ移動

スクリプトが出力したパスに移動する:

```bash
cd "${worktreePath}"
```

### 4. Planモード開始

`EnterPlanMode` ツールでPlanモードに入り、Issueの内容を基に実装計画を立てる。

### 5. 次のアクション確認（実装完了後）

実装が完了したら、AskUserQuestionで「PRを作成しますか？」と確認：
- **はい**: `Skill` ツールで `creating-prs` を呼び出す
- **いいえ**: 終了
