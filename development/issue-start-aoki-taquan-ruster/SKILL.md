---
name: issue-start
description: GitHub Issueの作業を開始する。ブランチを作成してチェックアウト。「/issue-start 4」のように使用
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Issue Start

## Instructions

1. 引数でIssue番号を受け取る（例: `/issue-start 4`）
2. `gh issue view <number> --json title,labels` でIssueタイトルとラベルを取得
3. `wip` ラベルがあれば警告して中止（既に別のClaude Codeが作業中）
4. タイトルからslugを生成（小文字、スペースをハイフンに、記号削除）
5. `git fetch origin main` でmainを最新に取得
6. `gh issue edit <number> --add-label wip` でラベル追加
7. `git checkout -b feature/<number>-<slug> origin/main` でブランチ作成・切り替え
8. 作業開始を報告

## 注意

- 固定スロット方式: worktreeは事前に作成済み（ruster-1〜5）
- 各worktreeでClaude Codeを起動して、このスキルでブランチ切り替え
- `wip`ラベルで重複作業を防止

## Example

```
/issue-start 9
```

実行結果:
```
Issue #9 "MAC学習・FDB実装" の作業を開始します

✓ wip ラベルを追加
✓ ブランチ作成: feature/9-mac-fdb

作業を開始してください
```
