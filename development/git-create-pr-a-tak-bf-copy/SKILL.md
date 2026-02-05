---
name: git-create-pr
description: git commit, push, PR作成を一括実行。新機能実装完了後やレビュー対応完了後に使用。メインエージェントのコンテキスト節約のため、定型的なPR作成フローをこのSkillに委譲する。
---

# git-create-pr

## 目的

変更をコミット、プッシュし、GitHub Pull Requestを作成する一連のgit操作を実行し、メインエージェントのコンテキストウィンドウを節約する。

## 使用タイミング

以下の状況でこのスキルを使用する：

- 新機能実装完了後のPR作成
- レビュー指摘対応完了後のPR更新
- ドキュメント更新後のPR作成
- 複数コミットをまとめてPR化

## 実行手順

1. **git status確認**: 現在の変更状況とブランチ情報を確認
2. **git diff確認**: 変更内容を確認してPR説明文を作成
3. **git log確認**: コミット履歴を確認（mainブランチとの差分）
4. **git add & commit**: 変更をコミット（必要な場合）
5. **git push**: リモートリポジトリにプッシュ
6. **gh pr create**: GitHub CLIでPR作成
7. **結果報告**: PR URLを報告

PR説明文とタイトルは規定のフォーマットに従い、末尾にClaude Code署名を含める。

詳細な処理フローは `references/command-details.md` を参照。

## エラーハンドリング

| エラー | 対処方法 |
|-------|---------|
| PR既存 | 既存PRのURLを表示して終了 |
| gh未認証 | `gh auth login`を実行するよう指示 |
| プッシュ失敗 | `git pull`を提案 |
| コンフリクト | メインエージェントに解決を依頼 |

詳細は `references/command-details.md#エラーハンドリング詳細` を参照。

## 使用例

### ケース1: 新機能実装完了後

```
Skill: git-create-pr

新機能: Google Drive復元機能
Issue: #365

全ての変更をコミットしてPRを作成してください。
```

### ケース2: レビュー指摘対応完了後

```
Skill: git-create-pr

レビュー指摘をすべて修正しました。
既存のPR #123を更新するため、コミット・プッシュのみ実行してください。
```

その他の使用例は `references/usage-examples.md` を参照。

## 制限事項

このスキルでは**対応しない**操作（メインエージェントで実行）：

- `git rebase`
- `git merge`
- コンフリクト解決
- 複数ブランチ間のPR

## 参照ドキュメント

必要に応じて以下のドキュメントを参照する：

- **`references/command-details.md`**: 処理フロー詳細、PR説明文フォーマット、PRタイトル命名規則、エラーハンドリング
- **`references/usage-examples.md`**: 具体的な使用例

## 関連Skill

- `git-commit-push`: コミット・プッシュのみ実行
- `git-review`: PRのレビューコメント取得・整理
