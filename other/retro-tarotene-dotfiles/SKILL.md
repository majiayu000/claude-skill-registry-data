---
name: retro
description: 作業の終わりに、このセッションの指摘・気付き・詰まり・hook に当たった事実を全て振り返り、仕組み化の候補として記録して起票経路(wrap-up inbox)に流す手順。PR を作ったセッション、またはその場で書いたコード(scratchpad のスクリプト・形を持つコマンド)の痕跡があるセッションでは、Stop hook が自動で求める。痕跡の少ない調査・設計だけのセッションや、途中で区切りを付けたいときに手動で呼ぶ。レトロ・振り返り・レトロスペクティブ・retro・retrospective・今日の作業を振り返って・仕組み化の検討、といった文脈で使う。
---

PR を作ったセッション、またはその場で書いたコードの痕跡があるセッションでは、最初の Stop で
`session-wrapup stop` がレトロを求める(ADR-697、ADR-1276)。このスキルは、自動で求められない
セッションで同じ手順を手動で踏むためのもの。
手順の正本は `session-retrospective --retro-procedure` の出力で、ここには書き写さない。

## 手順

1. セッション ID を確かめる。SessionStart で渡されたものか、Stop の指示文
   (`--retro-procedure '<session_id>'`)に出ているものを使う。
2. 手順書を取る:
   ```
   ~/.claude/hooks/session-retrospective --retro-procedure '<session_id>'
   ```
   手動のセッションでは transcript のパスが hook に渡っていないので、ユーザー発言の一覧は
   出ない。その場合は会話を自分で見返して、ユーザーの指摘・不満・言い直しを拾う。
3. 出力に従って `--retro-add` で行を書く。語彙は閉じていて、語彙外は exit 64 になる。
   「何も無かった」は `kind: none` の 1 行で表す。黙って飛ばさない。
4. 全行がそろったら `--retro-close '<session_id>'` を実行する。台帳の全行を kind ごとの表にして、vault の
   `retro/<年>/` に 1 件のノートとして書き出し、読み戻してから完了にする(PR にはコメントしない。表を
   自分で書き直さない)。vault の無い機体では、台帳に残したまま完了になる。
5. `disposition: inbox` にした行は、通常の気づきと同じく inbox(vault のノート、vault の無い機体では
   jsonl)に入る。Issue にはならず、`/my-cleanup` で本人が裁定する。ここで直接
   `gh issue create` しない。ただし `kind: user-correction` の行は `inbox` にできない(共有 AGENTS.md の
   「フィードバックは Issue 化」)。先に `gh issue create` で Issue にして `issue:#<N>` と書くか、
   プロジェクト固有・機微な内容なら `none:<理由>` と書く。

## 判断の目安

- **指摘(user-correction)**: ユーザーが方針・結果を直した発言。`mechanism` は、それを
  次から防ぐのに実際に効く最も上位の手段(`eliminate` > `unrepresentable` > `gate` > `tool` >
  `prose`)。`signal` で理由(兆候)を選び、その既定の段と違う段には `level_reason` を書く。
  `prose` 以外の段は `existing`(採用|拡張|自前)と `searched` も要る。リポジトリ内は必ず探し、
  外部は `自前` のときだけ 1 回探す。`searched` は、範囲の名前だけでなく、見つけたものを `<範囲>:<名前>` で
  書く(`crates:issue-index`、`skills:retro`、何も当たらなければ `inbox:none`)。範囲の名前だけの候補は、
  「既存で足りた」で却下される例が続いた(5・6・8 件と増えた)。`自前` にする前に、検討した既存の仕組みを 1 つ挙げ、
  なぜ足りないかを `what` に書く。すでに gate があるのに漏れたなら
  `existing:<名前>` とし、その gate の欠陥として `what` に名前を書く。語彙と事例は
  `docs/agents/codify-signals.md`(手順書の出力にも兆候の一覧が出る)。
- **気付き(insight)**: 次に効く発見。仕組みにするほどでなければ `disposition: none:<理由>`。
- **詰まり(friction)**: 手戻り・待ち・迷い。
- **gate 発火(gate-hit)**: deny や block に当たった事実。手順書の「events」に出る id を
  `evidence` にそのまま書く(書かないと完了にならない)。
- 同じ内容が既に Inbox のノートになっていてもよい。同じ題の気付きはノートの行として積まれ、
  行数が ADR-543 の昇格判断の材料になる(`issue-inbox --list-open` の `count`、ADR-1136)。
