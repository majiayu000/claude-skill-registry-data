---
name: prompt-review-push
description: >
  ~/prompt-reviews/ 内の未コミットのレポートを git commit & push する。
  「レビュー結果をプッシュして」「prompt-review を push して」などで呼び出す。
allowed-tools: Bash
---

# prompt-review-push スキル

`~/prompt-reviews/` リポジトリ内の未コミットのレポートファイルを commit & push する。

## 手順

1. `~/prompt-reviews/` で `git status` を実行し、未コミットのファイルを確認する
2. 未コミットのファイルがなければ「プッシュするレポートはありません」と通知して終了
3. 未コミットのレポートファイルをステージング・コミット・プッシュする:
   ```bash
   cd ~/prompt-reviews && git add *.md && git commit -m "Add prompt reviews" && git push
   ```
4. 完了後、コミットしたファイル一覧をユーザーに通知する
