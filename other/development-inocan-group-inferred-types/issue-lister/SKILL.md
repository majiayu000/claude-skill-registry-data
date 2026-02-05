---
name: issue-lister
description: オープン Issue の一覧を優先順位付きで表示する。「Issue 一覧」「Issue リスト」「オープン Issue」「Issue を見せて」「チケット一覧」「未解決 Issue」「Issue 確認」などで起動。優先度順にソートして表示。
allowed-tools: [Read, Bash]
---

# Issue Lister

オープン Issue の一覧を優先順位付きで表示します。

## 実行内容

1. `commands/issue-list.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-git:issue-list` を SlashCommand ツールで実行

## コマンド連携

実際の処理は `/shiiman-git:issue-list` に委譲します（SSOT として扱う）
