---
name: safe-command-policy
description: コマンド実行の安全ポリシーを適用し、破壊的・外部影響のある操作は事前確認する
metadata:
  short-description: 危険コマンドは確認
---

# safe-command-policy

この skill は、コマンド実行の安全性を制御する。

## 自動実行可

- git status
- git diff
- git grep
- ls, cat, find（読み取り用途）

## 事前確認必須

- rm -rf
- git reset --hard
- git push --force
- sudo を伴う操作
- curl | sh
- .env や秘密情報の作成・変更

## 注意

- pnpm install / add
- pnpm format
- pnpm lint:fix
  実行前に必要性を説明する。
