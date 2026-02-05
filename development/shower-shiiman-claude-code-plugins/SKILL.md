---
name: shower
description: 指定したプラグインの詳細情報を表示する。「プラグインの詳細」「〇〇プラグインについて教えて」「プラグインの情報」「〇〇の機能は？」「プラグインの中身を見せて」「〇〇プラグインの説明」「プラグインのコマンド一覧」などで起動。コマンド、スキル、エージェント、フック、README、バージョン情報を表示。
---

# Plugin Shower

指定したプラグインの詳細情報を表示します。

## 実行内容

1. `commands/show.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:show [plugin-name]` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/show.md` - 機能の詳細
- `/shiiman-plugin:show` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:show` に委譲します（SSOT として扱う）
