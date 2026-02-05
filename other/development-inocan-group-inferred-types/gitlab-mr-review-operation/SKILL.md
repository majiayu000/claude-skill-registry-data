---
name: gitlab-mr-review-operation
description: GitLab Merge Requestのレビュー操作を行うスキル。MR情報取得、差分確認、コメント取得・投稿、インラインコメント、コメント返信をglabコマンドで実行する。MRレビュー、コードレビュー、MR操作が必要な時に使用。
---

# GitLab MR Review Operation

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] GitLab MRをレビューする?
- [ ] MRにコメントを投稿する?
- [ ] インラインコメントを追加する?
- [ ] MR情報を取得する?

### 前提条件
- [ ] `glab` CLIがインストールされているか?
- [ ] `glab auth login`で認証済みか?
- [ ] MR URLから OWNER/REPO/NUMBER を抽出したか?

### 禁止事項の確認
- [ ] 未認証状態で操作しようとしていないか?
- [ ] 権限のないリポジトリを操作しようとしていないか?

---

## トリガー

- GitLab MRレビュー時
- MRへのコメント投稿時
- インラインコメント時
- MR情報取得時

---

## 前提条件

- `glab` インストール済み
- `glab auth login` で認証済み

---

## MR URLのパース

MR URL `https://gitlab.com/OWNER/REPO/-/merge_requests/NUMBER` から以下を抽出して使用:
- `OWNER`: リポジトリオーナー(グループ)
- `REPO`: リポジトリ名
- `NUMBER`: MR番号

---

## 操作一覧

### MR情報取得

```bash
glab mr view NUMBER --repo OWNER/REPO
```

### 差分確認

```bash
glab mr diff NUMBER --repo OWNER/REPO
```

### コメント取得

```bash
glab mr note list NUMBER --repo OWNER/REPO
```

### コメント投稿

```bash
glab mr note NUMBER --repo OWNER/REPO --message "コメント内容"
```

### レビュー承認

```bash
glab mr approve NUMBER --repo OWNER/REPO
```

---

## 🚫 禁止事項まとめ

- 未認証状態での操作
- 権限のないリポジトリへの操作
