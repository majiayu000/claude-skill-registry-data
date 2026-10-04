---
name: new-post
description: 記事のタイトルや書きたい内容から slug を決め、scripts/new-post.sh で posts/ に雛形を作る。
---

1. 渡されたタイトル・内容から、内容を表す短い英語の slug を作る（英小文字・数字・ハイフンのみ、前後のハイフン不可）
2. lang は入力の言語から判断する（指定があればそれに従う。既定は `ja`）
3. `./scripts/new-post.sh <slug> <lang>` を実行する
4. タイトルが渡されていれば、作られたファイルの `title:` に入れる
5. 作ったファイルのパスと slug を返す
