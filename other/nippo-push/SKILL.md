---
name: nippo-push
description: >
  ~/nippo の未コミットの日報を git commit & push する。
  「日報をプッシュして」「nippo を push して」などで呼び出す。
allowed-tools: Bash
---

# nippo-push スキル

`~/nippo`（`github.com/NakamuraFumiya/nippo`、private）の未コミットの日報を commit & push する。

日報の作成・補完は `/nippo` の担当。このスキルは push だけを行う。

## 手順

1. `~/nippo` で `git status --short` を実行し、未コミットのファイルを確認する

2. 未コミットのファイルがなければ「プッシュする日報はありません」と通知して終了する。
   このとき、リモートより先行しているコミットがあれば（`git log @{u}..HEAD --oneline`）、
   その push だけを行う

3. 変更内容をユーザーに提示する。日報には社内の PR 番号・チケット内容・障害情報が含まれるため、
   push 前に対象ファイル一覧を必ず見せる

4. commit & push する。コミットメッセージは対象日付から組む

   ```bash
   cd ~/nippo && git add -A && git commit -m "日報: YYYY-MM-DD" && git push
   ```

   - 複数日分をまとめる場合は `"日報: YYYY-MM-DD〜YYYY-MM-DD"`
   - **同じ日を再度 push する場合**（既にその日のコミットがある。
     `git log --oneline --grep "日報: YYYY-MM-DD"` で確認）は
     `"日報: YYYY-MM-DD (更新)"` とする。1 日に何度実行しても、
     どれが後から足したぶんか履歴で見分けられるようにする

5. 完了後、コミットしたファイル一覧とコミットハッシュを通知する

## 注意

- push 先が private リポジトリであることを確認してから push する
  （`gh repo view NakamuraFumiya/nippo --json isPrivate`）
- push が拒否された場合、force push はしない。ユーザーに状況を伝えて指示を仰ぐ
