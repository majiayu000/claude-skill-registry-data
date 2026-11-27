---
name: music-performance-planning
description: 演奏本番(アマオケ・室内楽・ソロ)の練習計画提案・合わせ調整の統合・会場確保の委譲・タイムスケジュール資料の取り込み・付随作業(会場確保・ドレスコード・宿泊)の確認・当日タイムテーブルと遠征の Calendar dispatch を行う判断知識。演奏本番・練習計画・合わせ確定・会場が決まった・当日スケジュール・遠征ロジ・キャパ確認・マイルストーン確認・タイムスケジュール表・付随作業の確認、といった文脈で使う。practice plan, rehearsal confirmation, venue confirmed, day-of timetable, travel logistics for a concert, incoming time-schedule sheet、といった英語の文脈でも使う。データの正本(演目・共演者・キャパ宣言値・合わせ/当日の確定時刻・付随作業の事実)は別の private な person-state リポジトリの `state/performances/` にあり、このスキルはそこへの読み書き手順を持つ。候補日程一覧 × カレンダーの当たり判定は slot-availability に、会場探しそのものは venue-search に委譲する(本スキルはその上位で「本番」単位のデータと結びつける)。
---

演奏本番の練習・合わせ・当日ロジを本番のたびに場当たり的に組まないための
判断知識。データモデルの決定根拠は別の private な person-state リポジトリ
側の `docs/adr/0010-music-performance-planning-data-model.md`(合わせ・当日の
確定時刻の射影は ADR-0014、付随作業の定型化は ADR-0015 — いずれも出典は
private リポジトリ側のため、ここでは決定の存在だけを参照する)、設計動機は
`docs/agents/music-performance-planning.md` を参照。

## 前提: ハブの解決

`performance-hub`(home-manager でデプロイ、PATH 上で呼べる)で person-state
リポジトリのチェックアウトパスを解決する。未設定ならユーザーに設定してもらう
(`docs/agents/music-performance-planning.md` 参照)。以降、このパスを `$HUB` と
書く。venue-search スキルも同じハブを使う。

```
HUB="$(performance-hub)" || exit 1
```

## 前提: TOML の読み書きの分担

`$HUB/state/performances/*.toml` の**読み取り**は `yq -p toml -o json` で
JSON 化してから jq で処理する。**書き込み**は yq の TOML エンコーダが
配列・テーブルをサポートしないため(`docs/agents/music-performance-planning.md`
の「TOML への書き込みは yq でサポートされない」参照)、Edit ツールで直接
行う — 決定的スクリプトは「どこを・何に書き換えるべきか」を示すところ
までを担う。

## 1. 練習計画提案

1. 対象本番の需要 vs 供給を確認する:
   ```
   bash "$HUB/state/performances/scripts/capacity-check.sh"
   ```
2. マイルストーン目標日の到来を確認する:
   ```
   bash "$HUB/state/performances/scripts/milestone-check.sh"
   ```
3. 両方の出力(供給不足の警告・見積もり未記入の出番・到来済みの
   マイルストーン)を踏まえ、今週の練習配分案を組み立てて提示する。
   **割当を最適化するソルバではない** — 候補を出すだけで、確定は
   月次レビュー(person-state リポジトリで毎月起きる Issue「月次レビュー
   YYYY-MM」の Cadence 割当節)の中で本人が行う(ADR-0006 D4)。
4. 供給側(`capacity.toml` の `weekly_minutes`)が `0`(未確定)のままなら、
   まずそれを実測値に更新するよう促す — 未確定を偽の「間に合う」と
   混同しない。

## 2. 合わせ調整の統合

候補日程一覧 × カレンダーの当たり判定・確定化そのものは
`config/agents/skills/slot-availability/` の `judge`/`finalize` に委ねる
(手順は同スキルの SKILL.md を参照)。本スキルが追加するのは、確定後に
person-state リポジトリ側の `[[rehearsals]]` へ反映する手順のみ。

こちらから合わせを打診する(発行側)場合の候補の出し方とマーカーの扱いは、
slot-availability の SKILL.md「発行側の打診」に従う。予約型サービスを
使うときは調整中のマーカー(slot-availability の `marker_prefix`)を作らないので、下の手順2(`finalize`)は
通らない — 相手が予約して確定した予定から、手順3 の `start`/`end` を追記
する。

`rehearsal` の `status`(negotiating/confirmed/done)は ADR-0014 により
保存されなくなった — `start`/`end` の有無と `end` が過去かどうかから導出
される。以降の手順は「`status` を書き換える」ではなく「`start`/`end` を
追記する」ことで確定を表す。

1. 対象 performance ファイルを JSON 化し、`coordination_url` が一致し
   `start` キーを持たない(= まだ交渉中の)rehearsal 要素の `key` を
   特定する:
   ```
   yq -p toml -o json "$HUB/state/performances/<id>.toml" \
     | jq --arg url "<候補日程一覧の URL>" \
       '.rehearsals | map(select(.coordination_url == $url and (has("start") | not)))'
   ```
   複数件ヒットした場合(同時に複数の合わせ候補が調整中)は、日付や
   `purpose` で本人に確認してから対象を1件に絞る — 自動で1件目を選んで
   はいけない。
2. slot-availability の `finalize` を実行し、Calendar 側のマーカーを
   確定させる(同スキルの手順どおり)。
3. Edit ツールで、手順1 で特定した rehearsal 要素に確定した日時を
   `start`/`end`(`{date}` または `{dateTime, timeZone}`)として追記する。
   会場が既に分かっていれば `location` も追記する(未定なら「3. 会場確保」
   へ進む)。既存のコメント・他のフィールドはそのまま残す(yq の TOML
   書き込みを使わない理由がここ — 全体を再生成すると手書きの `★ TODO`
   コメント等が失われる)。
4. 対応する `appearances[].milestones` にまだ触れない — 合わせの確定は
   マイルストーン(D8)とは別軸であり、自動で段階を進めない。

## 3. 会場確保

会場探しそのもの(候補サービスの列挙・空き確認・候補提示)は
`config/agents/skills/venue-search/` に委譲する。本スキルが持つのは
「いつ委譲すべきか」「見つかった結果をどこに書き戻すか」の判断だけ。

1. 対象 rehearsal の `venue_by` を確認する(既定は `self`)。
   - `organizer`: 主催者が用意するため venue-search には委譲しない。
     主催者から会場が伝わったら `location` に書くだけでよい。
   - `self`/`partner`: 「6. 付随作業」の `venue-booking` が OPEN なら
     venue-search に委譲する対象。
2. `obligations.sh --json` で当該 rehearsal の `venue-booking` の `stage`
   を読む(閉語彙 `book`/`propose`/`confirm-first`/`agree-area` —
   規則そのものは person-state リポジトリ側の決定〔ADR、存在だけ参照〕に
   あり、このスキルは `stage` で分岐するだけで規則を再導出しない)。
   - `propose`/`confirm-first`: venue-search に `proposal`(既定会場)を
     渡して提案文を作ってもらう。相手が合意したら Edit ツールで `area`
     (駅名)を追記する(→ `book` に進む)。
   - `agree-area`: 相手にエリアの希望を尋ねる(venue-search の従来手順)。
   - `book`: 次の手順(候補提示・予約)へ進む。
3. venue-search スキルに、対象 rehearsal の `area`(あれば)・
   `venue_needs`(グランドピアノ等)を渡して候補を出してもらう。
4. 人間が予約したら、確定した会場名を Edit ツールで対象 rehearsal の
   `location` に追記する(`venue-booking` はこれで完了になる)。

## 4. 資料の取り込み

主催者からタイムスケジュールのシートが払い出されることがあるが、これを
前提にした専用パーサは持たない(相対時刻の表記も資料の形式も主催者ごとに
バラバラで、実例がまだ乏しい — YAGNI、`docs/agents/music-performance-planning.md`
参照)。資料が無い演奏でも、下記の対応表と同じ項目を対話で埋める。

対応表(資料に出てくる典型項目 → フィールド):

| 資料の項目 | フィールド |
|---|---|
| 開場・開演・終演見込み(本番当日) | トップレベル `start`/`end` |
| 各回の合わせ日程・会場 | `rehearsals[].start`/`end`/`location` |
| ドレスコード | トップレベル `dress_code`(無ければ `"none"`) |
| 宿泊の要否・宿泊先 | `travel.lodging.decision`/`name` |
| 集合時刻・搬入等(相対時刻) | `day_timetable`(「5. 当日タイムテーブル」参照) |

1. 資料(PDF・スプレッドシート・メール本文など、形式は問わない)を読み、
   上の対応表に沿って値を拾う。
2. 現在の TOML との差分(追加・更新するフィールドと値)を提示し、
   AskUserQuestion で承認を取る。
3. 承認後、Edit ツールで反映する(TOML 書き込みの分担は「前提」のとおり)。

## 5. 当日タイムテーブル・遠征の Calendar dispatch

確定した当日・遠征の予定は、主カレンダーへ `create_event` で直書きしない。
person-state リポジトリ側の演奏ファイルへ書く PR を出し、CI がそれを一方向に
専用の射影カレンダーへ反映する。主カレンダーは本人の手入力の受付箱で、直書きして
よいのは候補一覧型の仮押さえの `[hold] ` だけ(規則は `human-task-scheduling` の
「何をするか」手順 4 と同じ。`slot-availability` の仮押さえとも矛盾しない — あちらは
複数の候補を出して相手の裁定を待つ間の仮押さえで、当日・遠征の確定予定はこれに当たらない)。

演奏ファイルに書く形(射影は `start` が `dateTime` で確定してから行う):

- `day_timetable[]`: `key`(kebab-case、ファイル内で一意)・`relative_time`
  (本番の `start` からの ISO 8601 の期間。前は負、例 `-PT2H`)・`activity`、
  任意で `duration`(既定 `PT30M`)。時計の時刻は書かない — 射影が `start` から
  導くので、本番の開始が動けば自動でずれる。
- `travel.legs[]`: `key`・`mode`・`segment` に加え、確定した `depart`・`arrive`
  (`{dateTime, timeZone}`)。両方が書かれた区間だけが射影される。
- `calendar_event`(カレンダー予定 ID へのリンク)の欄は廃止された。書かない。

資料の相対時刻の表記を ISO 8601 の期間へ直すところは実例がまだ乏しく、決定的
パーサ化は時期尚早(YAGNI、`docs/agents/music-performance-planning.md` 参照)。
以下は Claude が対話的に行う手順:

1. 対象 performance ファイルを JSON 化し、`day_timetable`・`travel` の
   中身を読む。`★ TODO` のプレースホルダが残っている項目は、書き込み対象から
   除外し、埋まっていないことを本人に伝える。
2. 本番の開始時刻(トップレベル `start` が確定していればそれ、まだ
   未確定なら本人に確認する)を基準に、資料の項目を `key`・`relative_time`・
   `activity`(・`duration`)に直す。`start` が `date` のままなら、
   `day_timetable` は射影されないことを本人に伝える。
3. `travel.legs` の各区間について、確定済みの日時があれば `depart`/`arrive`
   として書く。無ければ「要確定」として一覧に残す(勝手に時刻を仮定しない)。
   `travel.lodging` は射影されない — 「6. 付随作業」の `lodging-decision`/
   `lodging-booking` で追う。
4. 追加・更新するエントリ(`activity`/`segment` と、導かれる開始・終了)の
   一覧を提示し、AskUserQuestion で承認を取る。
5. 承認後、Edit ツールで演奏ファイルへ書き(TOML 書き込みの分担は上記「前提」の
   とおり)、PR を出す。書き込み先は予定データであり、主カレンダーにも
   「Claude プロジェクト管理」カレンダーにも `create_event` しない。
6. 確定情報の書き戻しは、遠征の区間なら `depart`/`arrive`、宿泊なら
   `travel.lodging.name` に Edit ツールで行う(手順 5 の PR に含める)。

## 6. 付随作業(会場確保・ドレスコード・宿泊)の確認

会場確保・ドレスコード確認・スーツ準備/クリーニング・宿泊要否判断/予約は
保存レコードではなく、演奏データから毎回導出するビュー(ADR-0015)。

```
bash "$HUB/state/performances/scripts/obligations.sh"
```

出力の OPEN(未完了)/OVERDUE(期限超過)な項目ごとに対応する:

- `venue-booking`: `stage` に応じて「3. 会場確保」の該当手順へ。
- `dress-code-confirm`: 本人にドレスコードの有無を確認し、`dress_code`
  に記入する(無ければ `"none"` を明記する — キー省略は「未確認」を
  意味するため、区別する)。
- `attire-prep`/`attire-cleaning`: 本人が完了したら `attire.prep`/
  `attire.cleaning` を `done`(または不要なら `not-needed`)に書き換える。
- `lodging-decision`: 本人に宿泊するかどうかを確認し、
  `travel.lodging.decision` に `stay`/`day-trip` を記入する。
- `lodging-booking`: `decision = "stay"` の演奏について、宿泊先が決まったら
  `travel.lodging.name` に記入する(予約自体は人間が行う)。

これらのフィールドを埋めるだけで、対応する期限イベントが Calendar から
自動で消える(`obligations.sh` は導出ビューなので、保存されたレコードを
別途消す操作は不要)。

## 外部サービスへの書き込みはサニタイズ対象

Calendar 等の外部サービスに送る文章は、`agent-tooling-authoring` §3.2
「外部サービスへ送る文」に従ってサニタイズする(禁止項目の一覧は正本のみ)。

## 事例

(まだ無し。新しい失敗事例が出たらここに追記する。)
