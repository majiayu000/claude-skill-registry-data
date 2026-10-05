---
name: source-optout
description: "Handle an opt-out, takedown, or removal request from a site being collected — “stop crawling us”, “remove our listings”, “don’t link to us”, 「クロールをやめてほしい」「掲載停止」「調査対象外にしてほしい」「削除依頼」, a robots.txt change discovered mid-run, or a rights-holder complaint. Use when such a request arrives (GitHub Issue, email, or a block detected by tools/fetch_gate.py) and the collection must stop touching that site and its data must be taken down. Registers the site in data/no-crawl.json so the fetch gate blocks it, audits every place the site appears across the CSVs, rosters, sources.json and the skill prose with tools/purge_source.py, removes the published rows, and states plainly what can and cannot be erased."
---

# 調査対象外・掲載停止の申請への対応

## この手順が要る理由

`terms.html` 第6節で、こう公に約束している。

> 掲載内容が権利を侵害している場合、または掲載を希望されない場合は、下記までご連絡ください。
> 確認のうえ、速やかに削除または修正します。
> **サイト単位・施設単位で、以後の収集対象から除外することもできます。**

約束した以上、**申請が来てから手順を考えるのでは遅い。** そして「そのサイトをやめる」は
一言で言えるが、**実際にそのサイトが載っている場所は複数箇所に散っている**。手で
grep して消すと必ずどれかが残り、しかも残ったことに誰も気づかない——翌週の収集タスクが
`data/.prev/` からその行を引き直して復活させても、差分は「変更なし」としか出ない。

法的にも、これは礼儀ではない。**著作権法47条の5の政令基準（著作権法施行令第7条の5）は、
収集後に拒否の意思が示されたと判明したときに記録を消去することを、権利制限を受けるための
条件に挙げている**（`docs/COLLECTION-PROTOCOL.md` 6.5.2）。消し漏らしは、法的な立場を
そのまま損なう。

---

## 0. 着手前に —— 週次ルーチンが動いていないか確認する

```bash
ls -d .claude/logs/.routine.lock 2>/dev/null && echo "実行中。終わるまで待つ"
```

**収集の実行中にデータを消してはいけない。** `append_rows.py --init` は実行時点の
CSVを「前回分」として `data/.prev/` に退避するので、走行中に消すと、消した状態と
消す前の状態が混ざったまま週をまたぐ。ロックがあれば終わるまで待つ。

急ぐ場合でも、**手順2（登録）だけは先にやってよい。** 登録はデータを触らず、
取得を止めるだけなので、走行中でも安全に効く。

---

## 1. 申請の内容を確定する（ここを飛ばさない）

**先方が何を求めているのかを、こちらの解釈で広げも狭めもしない。** 書かれていることを
そのまま記録する。判断に迷う点があれば、推測で処理せず先方に確認する。

| 確認すること             | なぜ                                                                          |
| ------------------------ | ----------------------------------------------------------------------------- |
| **誰からか**             | サイト運営者・権利者本人か。無関係な第三者からの「消せ」に従う理由はない      |
| **対象はどこまでか**     | サイト全体か、特定のディレクトリ・特定のイベントだけか                        |
| **何をやめてほしいのか** | 下の表で `scope` を決める                                                     |
| **いつ受け取ったか**     | `requested_on` に書く。対応の速さを後から示せるようにしておく                 |
| **どこ経由で来たか**     | `via` に書く（Issue番号など）。**後から辿れない申請は、記録として成立しない** |

### `scope` の決め方

| 先方の要望                                     | `scope`      | やること                           |
| ---------------------------------------------- | ------------ | ---------------------------------- |
| 「自動収集をやめてほしい」                     | `crawl+data` | 取得を止め、**掲載も消す**（既定） |
| 「掲載を消してほしい」                         | `crawl+data` | 同上                               |
| 「収集は構わないが、掲載はやめてほしい」       | `crawl+data` | 同上                               |
| 「今後取らないでほしい。今あるものは構わない」 | `crawl`      | 取得だけ止める（`--keep-rows`）    |

> **迷ったら `crawl+data`。** このリポジトリは一貫して「判断に迷ったら取らない」で
> 倒している（`docs/COLLECTION-PROTOCOL.md` 6.5）。**残して怒られる**のと
> **消して困る人がいない**のとでは、釣り合いが取れていない。
>
> `crawl` を選んでよいのは、先方が明示的にそう言った場合だけである。**そして
> `crawl` を選んでも、掲載データは自然には消えない**——収集タスクは取得できなくても
> `prev_rows.py` から前回値を引いて書き戻せてしまう（tier C の持ち越し）。
> 「取得を止めれば、そのうち消える」は成り立たない。

---

## 2. まず登録する —— 出血を止めるのが最初

**データを消すより先に、これをやる。** 登録しないまま行だけ消しても、
**翌週の収集がまた取りに行って復活する。**

`data/no-crawl.json` の `entries` に追加する。

```json
{
  "host": "example.com",
  "include_subdomains": true,
  "scope": "crawl+data",
  "requested_on": "2026-08-11",
  "via": "GitHub Issue #123",
  "note": "自動収集を停止してほしい旨の連絡（先方の文面の要旨）"
}
```

サイトの一部だけが対象なら `paths` を添える（省略するとサイト全体）。

```json
  "paths": ["/members/", "/api/"]
```

登録した時点で、`tools/fetch_gate.py` が **`WebFetch` のたびに走るフック**として
このURLをブロックする。**robots.txt に何が書いてあるかに関わらず、また robots.txt を
取りに行くことすらせず**に断る（断ると決まっている相手のサーバへ、確認のアクセスもしない）。

効いていることを確認する。

```bash
python3 tools/fetch_gate.py --check https://example.com/
# 拒否  https://example.com/
#       理由: 調査対象外の申請（2026-08-11 / GitHub Issue #123）: ...
```

---

## 3. 痕跡を洗い出す

```bash
python3 tools/purge_source.py example.com --audit
```

掲載データ・名簿・`sources.json`・散文・`data/.prev/`・`data/apple-music.json` を
横断して、**そのサイトが出てくる場所を全部**挙げる。1サイトが数十行のデータと
複数箇所の散文にまたがることは珍しくない。**目視の grep では取りこぼす。**

---

## 4. 消す

```bash
python3 tools/purge_source.py example.com --apply              # scope = crawl+data
python3 tools/purge_source.py example.com --apply --keep-rows  # scope = crawl
```

やること・やらないこと：

| 対象                                               | 動作                                                                  |
| -------------------------------------------------- | --------------------------------------------------------------------- |
| `events` / `lives` / `movies` の該当行             | 削除し、`id` を1から振り直す                                          |
| `lineups.csv`                                      | 消えた公演に紐づく日割りも削除                                        |
| 名簿4つ（`spots` `venues` `theaters` `festivals`） | **`blocked` にする（行は残す）**                                      |
| `sources.json`                                     | 「調べたサイト一覧」から削除                                          |
| `apple_music_url` 列（`lives` / `lineups`）        | **行は消さず、そのセルだけ空にする**（下記）                          |
| `apple-music.json`                                 | 該当エントリを削除（**残すと翌週 `fill_apple_music.py` が書き戻す**） |
| **散文**（SKILL.md・docs・README・terms）          | **触らない。該当箇所を挙げるだけ**                                    |

**`apple_music_url` で行を消さないのは、それが「その行が存在する理由」ではないためである。**
公演が載っているのは主催者が公演を打つからであって、Apple Music へのリンクがあるからではない。
`url` や `official_url` が該当する場合は行の根拠そのものなので、そちらは行ごと消す。

> **Apple Music について申請を受けたときの落とし穴。** 掲載しているURLのホストは
> `music.apple.com` だが、**収集が実際に叩くのは `itunes.apple.com`**（Search API）である。
> `no-crawl.json` に `music.apple.com` だけを登録しても `fill_apple_music.py` は止まらない。
> **両方を登録すること。**

**名簿の行を消さないのは、名簿が「どこを見に行くか」であると同時に、座標・種別・キャパを
引く表示側のマスターでもあるためである**（`data.js` は状態を見ずに読む）。`blocked` は
`retired`（閉館）とは別の状態で、「存在するが、こちらが見に行ってはいけない」を意味する。

**散文を自動で書き換えないのは、それが指示そのものだからである**（`docs/COLLECTION-PROTOCOL.md`
7.1節と同じ線引き）。挙がった箇所は手で直す——とくに**収集スキルの横断サイト表に残っていると、
翌週の収集がそこを見に行こうとする**。

未登録のまま `--apply` すると、スクリプトはエラーで止まる（手順2を飛ばさせないため）。

---

## 5. 検証する

```bash
python3 tools/validate_data.py                       # ERROR 0
python3 tools/purge_source.py example.com --audit    # 散文以外に残っていないこと
python3 tools/fetch_gate.py --check https://example.com/   # 拒否になること
```

---

## 6. 反映する

```bash
git add -A && git commit && git push
```

**push して GitHub Pages に反映されて初めて、掲載が消える。** 手元のCSVを消した
だけでは、公開されているページは前のままである。

閲覧者側のキャッシュは Service Worker が `networkFirst` で扱うので（`sw.js`）、
次にオンラインで開いた時点で新しいCSVに入れ替わる。**`VERSION` を上げる必要はない**
（`SHELL` を変えていないため）。

---

## 7. 返信する —— 何ができて、何ができないかを正直に書く

対応した内容をそのまま伝える。**できないことを、できるように言わない。**

- ✅ 今後、このサイトへは自動収集としてアクセスしない（登録簿に入れた）
- ✅ 公開ページから該当する掲載を削除した（反映日を書く）
- ✅ 「調べたサイト一覧」からも外した
- ⚠️ **Gitの履歴には過去の版が残る。** 公開サイトからは消えているが、リポジトリの
  コミット履歴を遡れば見られる状態は続く。**履歴からの完全な削除が必要な場合は、
  その旨を伝えてもらう必要がある**（履歴の書き換えは影響が大きく、別途の判断になる）
- ⚠️ 検索エンジンや外部のキャッシュに残っている分は、こちらでは消せない

---

## 8. 記録を残す

申請と対応は `data/no-crawl.json` の1エントリに集約されている（`requested_on` `via`
`note`）。**それ以外の場所に経緯を書き足さない**——散らばると、次に同じことが起きたときに
どれが正本か分からなくなる。

運用上の気づき（この手順で困ったこと・足りなかったこと）は
`docs/skill-feedback.md` に書く。**このSKILL.md自体は、収集タスクに書き換えさせない。**

---

## 逆のケース：申請が取り下げられたら

`data/no-crawl.json` から該当エントリを削除する。それだけで取得は再開できる。
名簿を `blocked` にしていたなら、あわせて戻す。

```bash
python3 tools/roster.py venues --unblock "○○ホール" --reason "2026-09-01 申請取り下げ"
```

`candidate` ではなく `active` に戻る。`blocked` にしたのは収穫が無かったからではないので、
再開後2回ヒットするまで名簿から外れたままにする理由がないためである。

掲載データは、次回の週次収集が通常どおり拾い直す。

---

## 関連

| どこ                                | 何が書いてあるか                                   |
| ----------------------------------- | -------------------------------------------------- |
| `docs/COLLECTION-PROTOCOL.md` 6.5   | 取得してよいものの規則と、その法的な根拠           |
| `docs/COLLECTION-PROTOCOL.md` 6.5.4 | URL単位の判定（`fetch_gate.py`）がどう効いているか |
| `terms.html` 第6節・第7節           | 利用者・権利者に向けて公開している窓口と方針       |
| `tools/purge_source.py`             | 洗い出しと削除の実装。何を消して何を残すか         |
| `data/no-crawl.json`                | 登録簿そのもの                                     |
