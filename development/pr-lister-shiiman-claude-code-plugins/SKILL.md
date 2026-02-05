---
name: pr-lister
description: オープン PR の一覧を優先順位付きで表示する。「PR 一覧」「PR リスト」「オープン PR」「PR を見せて」「プルリク一覧」「レビュー待ち PR」「PR 確認」などで起動。レビュー状態と優先度順にソートして表示。
allowed-tools: [Read, Bash]
---

# PR Lister

オープン PR の一覧を優先順位付きで表示します。

## 実行内容

1. `commands/pr-list.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-git:pr-list` を SlashCommand ツールで実行

## コマンド連携

実際の処理は `/shiiman-git:pr-list` に委譲します（SSOT として扱う）
