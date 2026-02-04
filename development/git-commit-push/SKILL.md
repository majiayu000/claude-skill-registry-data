---
name: git-commit-push
description: git add, commit, pushの定型操作を実行。レビュー対応や軽微な修正後のコミット・プッシュに使用。メインエージェントのコンテキスト節約のため、定型的なgit操作をこのSkillに委譲する。
---

# git-commit-push

## 目的

変更されたファイルをステージング、コミット、プッシュする定型的なgit操作を実行し、メインエージェントのコンテキストウィンドウを節約する。

## 使用タイミング

以下の状況でこのスキルを使用する：

- コードレビュー対応後のコミット・プッシュ
- 軽微な修正後の定型的なgit操作
- 複数ファイルの一括コミット
- ドキュメント更新後のコミット

## 実行手順

1. **git status確認**: 現在の変更状況を確認
2. **git add**: 変更されたファイルをステージング（全体 or 指定ファイル）
3. **git commit**: 適切なコミットメッセージでコミット作成
4. **git push**: リモートリポジトリにプッシュ
5. **codexに再レビュー依頼**: `@codex review` とコメントをしてcodexに再レビュー依頼をする
6. **結果報告**: 実行結果を簡潔に報告

コミットメッセージは必ずHEREDOC形式で渡し、末尾にClaude Code署名を含める。

詳細な処理フローは `references/command-details.md` を参照。

## エラーハンドリング

| エラー | 対処方法 |
|-------|---------|
| コミット失敗 | pre-commit hookエラー詳細を報告 |
| プッシュ失敗 | `git pull`を提案 |
| マージコンフリクト | メインエージェントに解決を依頼 |

詳細は `references/command-details.md#エラーハンドリング詳細` を参照。

## 使用例

### ケース1: 全ファイルをコミット

```
Skill: git-commit-push

全ての変更をコミットしてください。
メッセージ: "fix: レビュー指摘対応 - BatteryChecker改善"
```

### ケース2: 特定ファイルのみコミット

```
Skill: git-commit-push

以下のファイルのみコミット:
- app/src/main/java/com/example/Foo.kt
- app/src/test/java/com/example/FooTest.kt

メッセージ: "test: Fooクラスのテストケース追加"
```

その他の使用例は `references/usage-examples.md` を参照。

## 制限事項

このスキルでは**対応しない**操作（メインエージェントで実行）：

- `git rebase`
- `git merge`
- コンフリクト解決
- ブランチ作成・切り替え

## 参照ドキュメント

必要に応じて以下のドキュメントを参照する：

- **`references/command-details.md`**: 処理フロー詳細、コミットメッセージ規約、エラーハンドリング
- **`references/usage-examples.md`**: 具体的な使用例

## 関連Skill

- `git-create-pr`: PR作成まで一括実行（コミット+プッシュ+PR作成）
- `git-review`: PRのレビューコメント取得・整理
