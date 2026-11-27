---
name: writing-style
description: ブログ・教材・技術記事など公開向けの長文を執筆するとき、文体・和文数式 punctuation 等の執筆規約を、別の private リポジトリの docs/style/ から参照する薄いポインタ。ブログを書く・記事を書く・教材を作る・執筆規約・文体・和文数式・punctuation、といった依頼で使う。writing style guide, prose conventions, blog post, technical article、といった英語の文脈でも使う。規約の内容そのものはこのリポジトリに置かない(public リポジトリへの内容汚染を避けるため) — ここは参照先を解決する手順だけを持つ。
---

ブログ記事・教材・技術記事など公開向けの長文を書き始める前に、
`writing-style-hub`(`crates/hub-resolve`、home-manager でデプロイ、
PATH 上で呼べる)を実行してスタイルガイドのハブを解決し、そこの
`docs/style/README.md` の「Consumer contract」節に従う。

```bash
writing-style-hub
```

## 縮退

ハブが未設定・パスが存在しない・レイアウトが想定と違う、いずれの場合も
`writing-style-hub` は明示的なエラーメッセージを stderr に出して非 0 で
終わる(無音で何もしないことはない)。その場合は執筆を進める前に、
出力されたメッセージに従ってハブを設定する(マーカーファイル
`${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/style-hub` に絶対パスを1行、
またはセッション限定で `WRITING_STYLE_HUB` 環境変数を設定する)。

## なぜこのリポジトリに規約の内容そのものを置かないか

執筆規約の正本は別の private リポジトリの `docs/style/` にある。この
dotfiles は public リポジトリであり、規約の内容(文体の癖・特定の記事の
書き方の指針など)を混ぜ込むのは避ける。ここに持つのは「どこを見れば
よいか」を解決する手順だけ。

詳細: `docs/agents/writing-style.md`
