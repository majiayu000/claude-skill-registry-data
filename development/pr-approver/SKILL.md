---
name: pr-approver
description: PR を承認（approve）する。「PR 承認」「PR を approve」「approve して」「PR を通す」「LGTM」「PR OK」「マージ許可」などで起動。レビュー後に承認コメントを投稿。
allowed-tools: [Read, Bash]
---

# PR Approver

PR を承認（approve）します。

## ワークフロー

### 1. 対象 PR の特定

以下から対象 PR を特定:

- ユーザーの指示（「#10 を approve」）
- PR URL
- 直前にレビューした PR

### 2. PR 状態の確認

```bash
gh pr view {pr番号} --json title,state,reviews,mergeable
```

### 3. 承認前チェック

以下を確認:

- 未対応の必須修正がないか
- CI が通っているか
- マージ可能な状態か

### 4. 承認実行

```bash
gh pr review {pr番号} --approve --body "## Approved

{approval_comment}

### 確認済み項目

- [x] コード品質
- [x] テスト
- [x] ドキュメント

LGTM! 🎉"
```

### 5. 結果報告

```
PR #{pr番号} を承認しました。

ステータス: ✅ Approved
マージ可能: {mergeable}

マージする場合:
gh pr merge {pr番号}
```

## 承認コメントのテンプレート

**シンプル**:

```
LGTM! 🎉
```

**詳細**:

```markdown
## Approved

良いコードです！

### 確認済み項目

- [x] コード品質
- [x] テスト
- [x] ドキュメント

LGTM! 🎉
```

## 重要な注意事項

- ✅ レビュー後に承認
- ✅ 承認理由をコメント
- ❌ レビューなしで承認しない
- ❌ 問題があるのに承認しない
