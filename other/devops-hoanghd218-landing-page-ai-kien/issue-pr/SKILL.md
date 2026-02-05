---
name: issue-pr
description: 現在のブランチでPull Requestを作成し、CIステータスを確認。「/issue-pr」で使用
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Issue PR

## Instructions

1. 現在のブランチ名を取得（`git branch --show-current`）
2. ブランチ名から Issue番号を抽出（`feature/4-xxx` → `4`）
3. `git log main..HEAD` でコミット内容を確認
4. PRタイトルとbodyを生成:
   - タイトル: コミットメッセージまたはIssueタイトルベース
   - body: `Closes #<number>` を含める
5. `gh pr create` でPR作成
6. PR URLを表示
7. 少し待ってから `gh pr checks <PR番号>` でCIステータスを確認
8. 全てpassしたら:
   - `gh issue edit <number> --remove-label wip` でwipラベルを削除
   - ユーザーに報告
9. pendingなら待って再確認
10. failなら原因を調査

## CI確認の流れ

```bash
# PR作成後、CIが開始されるまで少し待つ
sleep 20

# ステータス確認
gh pr checks <PR番号>
```

- **pass**: wipラベル削除、マージ可能
- **pending**: しばらく待って再確認
- **fail**: `gh run view <run_id> --log-failed` で原因調査、修正してpush

## Example

ブランチ `feature/4-ethernet-frame` で実行:

```
/issue-pr
```

実行結果:
- Issue #4 にリンクしたPRを作成
- `Closes #4` がbodyに含まれる
- PR URLを表示
- CIステータスを確認
- 全てpass: wipラベル削除、マージ準備完了を報告
