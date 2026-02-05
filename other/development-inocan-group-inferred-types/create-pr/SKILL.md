---
name: create-pr
description: Create a pull request for the current branch
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Create PR

## Instructions

現在のブランチのPRを作成する。

1. 現在のブランチとmainの差分を確認
2. 変更内容を要約したPRタイトル・本文を作成
3. pushされていなければ先にpushする
4. `gh pr create --assignee @me` でPRを作成（Assignee は必ず @me を設定）
5. PRのURLを表示する

## PR Format

```
Title: 簡潔な日本語タイトル

## Summary
- 変更点を箇条書きで

## Test Plan
- テスト方法を箇条書きで
```

## Notes

- ベースブランチは `main`
- タイトル・本文は日本語
- **Assignee は必ず `@me` を設定すること**
