---
name: venue-search
description: 合わせ・個人練習の会場(レンタルスタジオ・公民館等の公共施設)を探し、候補を人間に提示する判断知識。会場探し・練習部屋を探す・スタジオ予約・合わせの場所・グランドピアノがある部屋・公民館・区民センター、といった文脈で使う。rehearsal venue search, practice room booking, find a rental studio with a piano、といった英語の文脈でも使う。データの正本(自宅・職場・公共施設の登録状況・常用スタジオ)は別の private な person-state リポジトリの `state/places.toml` にあり、このスキルはそこへの読み取り手順と、会場サービスの一次情報知識を持つ。予約(人間が行う)そのものは代行しない — 探すところまでを担う。
---

会場探しを Instabase・SpaceMarket・Google 検索・使い慣れた店舗の場当たり
巡回にしないための判断知識。API を公開しているサービスは(2026-09-27
時点の調査で)見つからなかったため、エージェントが担うのは「ログイン
不要で見られる空き状況を機械的に確認し、候補を絞る」ところまでで、予約
自体は人間が行う(低コストで済む経路を優先する)。

## 前提: ハブの解決

`state/places.toml` は演奏企画のデータ(`state/performances/`)と同じ
private な person-state リポジトリに置く。ハブの解決は
`music-performance-planning` スキルが使う `performance-hub` をそのまま流用する
— このスキル専用のマーカーは新設しない(同じリポジトリを指すハブ方式を
2つ持つ理由が無い)。

```
HUB="$(performance-hub)" || exit 1
```

`performance-hub` が無い/未設定の場合の縮退はそちら側の挙動に従う
(`docs/agents/music-performance-planning.md` 参照)。

## 1. 要件を集める

- 日時(合わせ・練習の候補日、または探したい期間)
- 希望エリア。対象 rehearsal の `venue-booking` 付随作業の `stage`
  (`music-performance-planning` スキルの手順で `obligations.sh --json` から
  読む、person-state リポジトリ側の決定 — 存在だけ参照する)で分岐する:
  - `book`(`area` 合意済み): rehearsal の `area` を起点にする。
  - `propose`/`confirm-first`(既定会場のポリシーあり): `proposal.venue`
    (`state/places.toml` の `preferred_venues[].id`)が指す店舗そのもの
    を起点にする — 自宅・職場起点の代わりにこれを使う。
  - `agree-area`(既定なし): 従来どおり `state/places.toml` の
    `home`/`work` の駅を起点にする。
- 会場要件(`venue_needs` の閉語彙。現状 `grand-piano`/`upright-piano`)

## 2. 候補サービスを機械的に列挙する

`state/places.toml` の内容(登録済みの公共施設・常用スタジオ)と、ピアノを
要件に含むかどうかから、見に行くべきサービスの一覧を決定的に出す
(候補の取捨選択自体は人間の判断に委ねる会話をブレさせないため):

```
bash scripts/venue-urls.sh --hub "$HUB" --needs grand-piano
```

出力の各要素は `id`/`service`/`branch`/`url`/`login_required`/`note`。
`url` が `null` のものは、このスクリプトが既知の URL を持たない(手動で
確認する)。手順1で `stage` が `propose`/`confirm-first` だった場合は、
`id` が `proposal.venue` と一致する要素だけに絞ってよい。

## 3. 空き状況を確認する

- `login_required` が `false` のページ(例: ノアの週表示)は WebFetch/
  Playwright で直接確認する。JS で後から描画されるページ(Instabase の
  一覧等)は Playwright を使う。
- `login_required` が文字列(条件付き・未確認)のものは、まずそのページ
  自体を一度見て、ログイン無しでどこまで見えるかを確かめてから続ける。
  ログインが避けられないと判明した場合のハンドオフ手順は
  `browser-login-handoff` skill を参照(このスキル自体は基本的に
  ログイン不要な範囲に限定する設計)。
- `note` に書かれた利用規約上の注意(例: Instabase の robots.txt が
  クエリ付き検索 URL を Disallow にし 60 秒間隔を求めている)を守る —
  個別ページを間隔を空けて見る、検索フォームへの連続リクエストはしない。
- 公共施設(えどねっと等)はピアノの有無が施設・部屋ごとに違うため、
  部屋の設備情報のページも合わせて確認する。

### 3.1 ノア(ピアノスタジオノア)の空き確認手順(Playwright)

`grandpiano.jp/noahweb/webs/chart/` は JS で描画され、選択状態(店舗・
スタジオ・週)が URL に反映されない — ブックマークや決定的な URL 組み立て
はできず、毎回このページを操作し直す必要がある(実測 2026-09-28)。
DOM セレクタと抽出関数は `scripts/noah-chart.js` に切り出してある。

1. `browser_navigate` でトップページを開く。
2. STEP01(店舗選択)のテキストボックスをクリックしてドロップダウンを開き
   (`#st_select`)、対象の店舗ラベルを含む `label` をクリックする(最大
   3店舗まで同時選択可)。「この条件で検索」ボタンを押す。
3. STEP02(スタジオ選択)に表示される店舗ごとのブース一覧から、グランド
   ピアノ設置室を選ぶ。ブース名とピアノ機種の対応は店舗ごとに固定なので、
   `grandpiano.jp/grand/` を1回 WebFetch すれば店舗横断で使い回せる
   (2026-09-28 時点: 秋葉原は P1st/P2st/P3st/P5st/P6st/P9st、池袋は
   P1st/P2st/P3st/P5st/P6st/P10st/DUOst/P12st/SSst〔SSst = STEINWAY
   B-211〕がグランドピアノ設置室)。
4. STEP03(日程)は既定で今日を含む週を表示する。対象日を含む週まで
   `browser_click` で `noah-chart.js` の `NOAH_NEXT_WEEK_SELECTOR`/
   `NOAH_PREV_WEEK_SELECTOR` を1週ずつクリックする。`browser_evaluate` で
   `noahWeekHeader()` を呼び、月・曜日ラベルで現在地を確認しながら進める
   (スナップショットを毎回撮ると出力が肥大するため、幅寄せ後の確認は
   `evaluate` に寄せる)。ボタンが `_disabled` になったら、そちらの方向
   にはこれ以上進めない上限(実測: 今日から約13週先)。
5. 対象の曜日ラベル(`noahWeekHeader()` の `days` の要素、例 "7土")と
   必要な時間帯を `noahDaySlots(dayLabel, timeFilter)` に渡し、`avail`
   が全て `true` であることを確認する。料金は `noahSelectedPrice()`。
6. 対象日がまだ表示可能範囲外(上限に達して進めない)なら、「まだ確認
   できない(◯月末頃の予約開放を待って再確認)」として候補表に明記する
   — 空きが無いと誤って報告しない。

## 4. 候補表を提示する

日時ごとに 2〜3 案を目安に、各案へ会場名・料金(分かれば)・ピアノの機種・
予約方法(Web/電話/要利用者登録)・リンクを添えて提示する。複数回の合わせ
をまとめて依頼された場合は、回ごとに表を分ける。

相手向けの提案文は `stage`(手順1参照)で分ける:

- `propose`: 既定会場をそのまま提示する。
- `confirm-first`: 会場を出す前に、合わせの前後の予定(移動)に支障が
  無いかを相手に尋ね、問題なければ既定会場を提示する。
- `agree-area`: 会場の希望を相手に尋ねる旨を含める(area が未合意)。

いずれの場合も、なぜその会場を既定にしているか(相手側の事情)は本人が
口頭で扱う判断であり、提案文には書かない。

## 5. 予約は人間が行う

このスキルは予約を代行しない。確定した会場は、`music-performance-planning`
スキル側の手順で `rehearsal.location` に書き戻す(このスキルの責務は
候補を出すところまで)。

## 外部サービスへの書き込みはサニタイズ対象

候補提示や相手への連絡文は、`agent-tooling-authoring` §3.2
「外部サービスへ送る文」に従ってサニタイズする(禁止項目の一覧は正本のみ)。

## 事例

- **ノアの空き確認(2026-09-28)**: オーボエ協奏曲の合わせ4回(11/7・12/5・
  12/19・1/17)について、秋葉原・池袋の各1室で実際に Playwright を操作し
  空きを確認した。11/7・12/5・12/19 は空きありを確認できたが、1/17 は
  週送りボタンが `_disabled` になり(実測で今日から約13週先が上限)確認
  できなかった — 「空きが無い」と「まだ表示範囲外」を区別する必要がある
  ことが分かった事例(「3.1」手順6の根拠)。

フォーム保存・アクセス障害を扱うときは `reference/browser-operations.md` を必ず全文読む。ログイン引き継ぎは `browser-login-handoff` に従う。
