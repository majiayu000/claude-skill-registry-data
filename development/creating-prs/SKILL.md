---
name: creating-prs
description: mainブランチからの差分を分析してPull Requestを作成する。Use when the user wants to create a PR (PR作成), merge changes (変更のマージ), or submit code for review (コードレビュー依頼).
allowed-tools: Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(gh pr create:*)
---

# Pull Request作成

## Quick start

git diff/logで変更内容を確認し、PRタイトル・本文を生成して `gh pr create` で作成する。

## 現在のブランチ

!`git branch --show-current`

## mainブランチからの差分

!`git diff main`

## mainブランチからのコミット履歴

!`git log main..HEAD --oneline`

## Instructions

### 1. PRタイトルと本文を生成

- タイトル: 変更内容を簡潔に要約（日本語、80文字以内）
- 本文:
  - ## 概要: 変更の目的と背景
  - ## 変更内容: 主な変更点を箇条書き
  - ## テスト: テスト方法や確認項目（該当する場合）

### 2. Issue番号の確認

ブランチ名に `issue` と番号が含まれているか確認：
- パターン例: `issue-123`, `issue/456`, `fix-issue-789`
- 見つかった場合、PR本文末尾に `Closes #番号` を追加

### 3. PRの作成

```bash
gh pr create --title "タイトル" --body "本文" --base main
```

### 4. 結果確認

作成されたPRのURLを表示。
