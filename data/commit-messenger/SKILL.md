---
name: commit-messenger
description: コミットメッセージの命名規則を設定する。「コミットメッセージ設定」「コミット規則」「コミット形式を設定」「コミットメッセージルール」「commit message 設定」「コミットの書き方を設定」「コミットフォーマット」などで起動。プロジェクト固有のコミットメッセージルールを管理。
allowed-tools: [Read, Write, Bash]
---

# Commit Messenger

コミットメッセージの命名規則を設定・管理します。

## 実行内容

1. `commands/commit-message.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-git:commit-message --set` を SlashCommand ツールで実行

## コマンド連携

実際の処理は `/shiiman-git:commit-message` に委譲します（SSOT として扱う）

## 設定可能な項目

- コミットメッセージ形式（Conventional Commits / 日本語 / カスタム）
- 使用するプレフィックス（feat/fix/docs/refactor/chore/test）
- Issue 参照の有無と形式
