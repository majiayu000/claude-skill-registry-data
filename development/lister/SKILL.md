---
name: lister
description: 利用可能なプラグインの一覧を表示する。「プラグイン一覧」「プラグインリスト」「どんなプラグインがある？」「プラグインを見せて」「使えるプラグインは？」「プラグイン確認」「インストール可能なプラグイン」などで起動。各プラグインの名前、説明、バージョン、インストール状態を一覧表示。
---

# Plugin Lister

利用可能なプラグインの一覧を表示します。

## 実行内容

1. `commands/list.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:list` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/list.md` - 機能の詳細
- `/shiiman-plugin:list` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:list` に委譲します（SSOT として扱う）
