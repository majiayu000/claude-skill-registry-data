---
name: local-ci
description: remote CI (GitHub Actions) 相当のチェックをローカルで実行。Biome check、テスト、ビルドを並列実行し、全てのチェックが成功したことを確認する。PR作成前の事前チェックに使用。
---

# Local CI スキル

**このスキルの役割**: remote CI (GitHub Actions) 相当のチェックを**ローカルマシン上**で実行するスキル。

## 詳細な実装手順

詳細な実装手順、使い方、エラーハンドリングについては **`.claude/commands/local-ci.md`** を参照してください。

このスキルは、`.claude/commands/local-ci.md` に記載された手順に従って以下を実行します：

1. 開始メッセージを表示
2. 3つの sub agent（biome-check、test-check、build-check）を**並列起動**
3. TaskOutput で各 sub agent の出力を取得
4. 結果を集計してサマリーを表示

## 使い方

```bash
/local-ci
```

このコマンドを実行すると、Claude が `.claude/commands/local-ci.md` の手順を実行します（3つのチェックは並列実行されます）。
