---
name: my-desk
description: 本人が習慣として手で打つ「朝の机」の入口(/my-desk)。その日にさばくべき作業(返信が要るメール、日程回答、軽い人手タスク、未消費 PR の裁定、受信箱)を、朝のセッションで 1 か所から順に片付ける入口。手順の正本は、機体ごとに別の private なリポジトリ(個人の機体は person-state リポジトリ、会社の機体は会社側のリポジトリ)にあり、このスキルはそこへ解決して従うだけの薄いポインタ。今日の机・机を開く・朝のルーチン・今日さばくこと・今日の分・daily desk・my desk、といった依頼や、SessionStart の「今日の机は未実施」の注入を受けたときに使う。start my day, work through today's inbox and tasks、といった英語の文脈でも使う。
---

`/my-desk` は、本人が習慣として手で打つ入口の 1 つ(もう 1 つは片付けの `/my-cleanup`)である。旧名の
`daily-desk` はこのスキルへの転送口で、通知役の `daily-desk-reminder`(SessionStart の hook)は実行名のまま変えない。

その日にさばく作業は、手元の資格情報(メールのコネクタ、`gh` のユーザートークン、受信箱の
キャッシュ)を要するので、クラウドの定期実行からは届かない。このスキルは、その入口を
朝のセッションに 1 つだけ置く。手順そのものは持たない。手順を変えるときは、
その機体の机の正本(`desk.md`)を持つリポジトリ側を直す。設計は `docs/agents/my-desk.md`。

## 1. ハブを解決して、手順を読む

`desk-hub`(この機体の机の正本を持つ person-state リポジトリを解決する。`docs/agents/my-desk.md`)で、
person-state リポジトリのチェックアウトを解決する。

```
HUB="$(desk-hub)" || exit 1
```

`"$HUB/state/reviews/daily/desk.md"` を最後まで読み、その手順に上から順に従う(正本の場所は、
個人と会社で同じ)。目印 `desk-hub` が無い機体は、従来どおり `performance-hub` のハブを
`desk-hub` が解決する。会社の機体には個人データ用の `performance-hub` を置かず、`desk-hub` だけで
会社側の person-state リポジトリを指す。
読めないとき(ハブが未設定、ファイルが無い)は、推測で手順を作らず、読めなかったことと
直し方を伝えて止める。手順の中身は、ここに複写しない。

## 2. 実施済みの印

`~/.local/state/claude/desk/` に、JST の日付名の空ファイルを 1 つ作る。これは SessionStart の
hook(`daily-desk-reminder`)が「今日の机は未実施」を出すかを決める唯一の入力である。

```
mkdir -p ~/.local/state/claude/desk
: > ~/.local/state/claude/desk/"$(date -u -d '+9 hours' +%F)"
```

- `desk.md` の最後の段まで終えた日だけ、印を作る。途中で止めたときは作らない。翌日の最初の
  セッションで、また注入される。
- 前回の机の日付が要るときは、このディレクトリの最新のファイル名を読む。
- 印は完了の台帳ではない。完了は、メールの下書き、受信箱の操作ログ、PR のマージ状態、
  カレンダーから読み戻す。

## 他のスキルとの境界

- メールの返信と日程回答は `inbox-adjudication` の日次モードと `slot-availability` に任せる。
- 人手タスクを予定に入れる手順は `handoff` §7 に任せる。
- 受信箱のフィルタ体系は、別のリポジトリが正本で、ここでは変えない。

人手タスクの予定化では `human-task-scheduling/SKILL.md` を必ず全文読んでから進める。
