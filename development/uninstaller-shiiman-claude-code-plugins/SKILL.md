---
name: uninstaller
description: 指定したプラグインをアンインストールする。「プラグインを削除」「〇〇をアンインストール」「プラグインを消して」「〇〇を削除して」「プラグインを外して」「〇〇を取り除いて」「プラグインをアンインストール」などで起動。claude plugin uninstall コマンドを使用してアンインストール。
---

# Plugin Uninstaller

指定したプラグインをアンインストールします。

## 実行内容

1. `commands/uninstall.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:uninstall [plugin-name]` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/uninstall.md` - 機能の詳細
- `/shiiman-plugin:uninstall` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:uninstall` に委譲します（SSOT として扱う）
