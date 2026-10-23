---
name: factory-docs
description: 本リポジトリ(atelier-works)のMarkdown文書(README、AGENTS.md、docs/、自作スキル、subagentの定義(.claude/agents/)、各ディレクトリのREADME)を新しく書く、直す、整理するときに使う。コードの変更に合わせて文書を更新するときも使う。
---

# このリポジトリの文書の書き方(factory-docs)

書き方の決まりは`docs/writing-guidelines.md`にある。このスキルは、その決まりに沿って文書を変更する手順を定める。最初に`docs/writing-guidelines.md`を読む。

## 手順

1. 書く情報の種類を決め、`docs/writing-guidelines.md`の「文書の種類」の表から置き場所を選ぶ。手順なら`docs/operations.md`、内部の挙動なら`docs/internals/`のように、読み手と目的で選ぶ。
2. 同じ情報が既にどこかに書かれていないか、`Grep`で探す。あれば、そこを直す。別の場所にも要るときはリンクにする。
3. 既存の節を直すときは、条件を書き足さず、節全体を今の挙動に合わせて書き直す。前提が崩れた記述は消す。
4. 制約を書くときは、その制約が必要な理由を現在形で1文添える。
5. スケジュール、miseタスク、Windmillの版のように設定ファイルから取れる事実は、`<!-- generated:名前 -->`の範囲に書かれている。手で直さず`mise run docs:gen`を実行する。
6. 書き終えたら`yomiyasu`スキルの原則で文を推敲する。
7. `mise run lint:docs`を実行し、指摘をすべて直す。

## 迷いやすい点

- 日付、「方針変更」「ユーザー決定」「旧形式」「以前は」は書かない。経緯はコミットメッセージとPR本文に書く。
- コード表記は、そのまま入力するものとそのまま目にするものだけに使う。状態の値などの識別子は初出で1回示し、以後は言葉で書く。
- 見出しは言葉だけにする。コード表記、日付、括弧の注釈を入れない。
- 太字で始まる長い箇条書きは、見出しに上げる。
- AGENTS.mdには1〜2行のルールとリンクだけを書く。説明は`docs/`に置く。
- 次のファイルは`wmill`が生成するか外から取り込んだものなので、編集しない。
  - `AGENTS.wmill.md`
  - 管理スキル: `.agents/skills/`のすべてと、`.claude/skills/`のうち自作でないもの(`write-*`や`cli-commands`など)
  - `.claude/skills/yomiyasu/`
