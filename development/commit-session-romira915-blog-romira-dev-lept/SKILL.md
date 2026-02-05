---
name: commit-session
description: Commit and push files modified in this session
allowed-tools: Bash(git:*), Bash(just:*), Bash(cargo:*), Bash(leptosfmt:*)
---

# Commit Session

## Instructions

今回のセッションで修正したファイルのみをcommit、pushする。

1. コミット前にCIチェックを実行
   - `just format` (自動修正)
   - `just clippy`
   - `just test`
2. 全て通ったらセッション中に修正したファイルのみを`git add`
3. 変更内容を簡潔に日本語で記述したコミットメッセージを作成
4. 現在のブランチにpush

## Notes

- コミットメッセージは日本語で簡潔に
- セッション中に修正したファイルのみを対象とする
- 全ての未コミット変更ではなく、今回の作業分のみ
- CIチェックが失敗したらコミットせず、修正を行う
