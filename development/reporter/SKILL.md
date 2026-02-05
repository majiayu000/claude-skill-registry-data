---
name: reporter
description: プラグインに関する要望、改善提案、バグ報告を作成する。「バグを報告」「要望を送りたい」「改善提案」「Issue を報告」「フィードバック」「機能リクエスト」「不具合報告」「プラグインの要望」「改善してほしい」「バグがある」「問題を報告」などで起動。shiiman/claude-code-plugins に Issue を作成。
---

# Plugin Reporter

プラグインに関する要望、改善提案、バグ報告を作成します。

## 実行内容

1. `commands/report.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:report` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/report.md` - 機能の詳細
- `/shiiman-plugin:report` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:report` に委譲します（SSOT として扱う）
