---
name: mf-invoice-fetch
description: 課税仕入の仕訳に対応する受領請求書PDFを、Gmail添付および各サービスの顧客ポータル（マネーフォワード／カゴヤ・ジャパン／Amazon／スイッチサイエンス）から取得し、references/invoices/ に配置して matches.json に登録するスキル。mf-invoice-check で「請求書PDF未登録」と出た仕訳を埋めるときに使う。「請求書を取ってきて」「請求書ダウンロード」「PDFを落として」「ポータルから取得」「メールから請求書」などのフレーズで起動。
---

# 受領請求書PDFの取得・登録

`mf-invoice-check` が検出した「請求書PDF未登録」の仕訳に対して、実際のPDFを取得し
`references/invoices/<年度>/` に配置して `matches.json` に登録する。

取得経路は2種類:

1. **Gmail添付** — Anthropic / Supabase / GitHub / Google Cloud / Cloudflare / SQLBAK
2. **顧客ポータル** — マネーフォワード / カゴヤ・ジャパン / Amazon / スイッチサイエンス
   （メール添付なし。Chrome MCP でブラウザ操作する）

## Step 0: 未登録リストを作る

```bash
python c:/moneyforward/.claude/skills/mf-invoice-check/scripts/check_invoices.py <journals.json> --year 2026
```

出力の「請求書PDF未登録」が作業対象。各仕訳の **取引日・摘要・金額(税込)** を控える。
税込金額 = `branches[].debitor.value + debitor.tax_value`。これが請求書の合計額と一致するかで
突合の正しさを検証する（日付だけで紐付けない）。

## Step 1: Gmail添付から取得

`scripts/gmail_fetch.py` を使う。`~/.gmail-mcp/credentials.json` のリフレッシュトークンで
Gmail API を直接叩く（接続中の Gmail MCP には添付ダウンロード用ツールが無いため）。

```bash
python c:/moneyforward/.claude/skills/mf-invoice-fetch/scripts/gmail_fetch.py \
  --after 2026/04/28 --out <staging_dir>
```

### 重要: トークン失効

`invalid_grant` が返ったらリフレッシュトークンが切れている（Google の testing モードは
7日で失効）。ユーザーに以下を実行してもらう。**Claude Code の再起動は不要** —
このスクリプトは MCP 経由ではなく `credentials.json` を直接読むため、認証が通った時点で
同一セッションのまま続行できる。

```bash
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

### サービス別の検索クエリと採用する添付

| サービス | クエリ | 採用する添付 |
|---------|--------|------------|
| Anthropic | `from:invoice+statements@mail.anthropic.com` | `Receipt-*.pdf`（`Invoice-*` ではない） |
| Supabase | `from:invoice+statements@supabase.com` | `Receipt-*.pdf` |
| GitHub | `from:noreply@github.com subject:receipt` | `github-<org>-receipt-<date>.pdf` |
| Google Cloud | `from:payments-noreply@google.com` | `<請求書番号>.pdf` |
| Cloudflare | `from:noreply@notify.cloudflare.com subject:"invoice is attached"` | `cloudflare-invoice-<日付>.pdf` |
| SQLBak | `from:noreply@sqlbak.com Payment Received` | `payment_*.pdf` |

### Google Cloud は請求先アカウントが2つある

`0167AE-67A318-FEC0D4` と `01833F-DE3AE7-E73305` の2アカウントがあり、**毎月2通**の
請求書メールが届く。2026年4月請求分以降、`0167AE` は **¥0** で課金が発生していないため、
仕訳は月1件しかない。`01833F` 側のPDFだけを仕訳に紐付け、¥0 の方は登録しない。

PDF内の金額は `fitz`（PyMuPDF）で `￥([\d,]+)` を拾えば確認できる。

## Step 2: 顧客ポータルから取得（Chrome MCP）

`mcp__claude-in-chrome__*` を使う（ログイン済みセッションが必要なため in-app Browser では不可）。

**ログインが必要な画面でパスワードを入力してはいけない。** ログイン画面に当たったらタブを
開いたままユーザーにログインを依頼する。

### マネーフォワード クラウド利用料

```
https://erp.moneyforward.com/office_usage_detail_statements
```
到達経路: クラウド会計 → 右上アカウントメニュー → ご利用プランの管理 →
「プランの変更、ご利用料金の確認はこちら」→ 料金明細タブ。

各行の「請求書」ボタンは `.../office_usage_detail_statements/<ID>/bills` を新規タブで開く。
**PDFダウンロードは無く `window.print()` のみ**（ネイティブ印刷ダイアログは自動操作不可）。
→ ページHTMLを保存してローカルで headless Chrome によりPDF化する（Step 3）。

請求書一覧の各行のリンクは JS でまとめて取れる:

```js
Array.from(document.querySelectorAll('table tr')).map(tr=>({
  d: tr.querySelector('td')?.innerText?.trim(),
  a: Array.from(tr.querySelectorAll('a')).map(x=>x.href)
})).filter(x=>x.d)
```

**日付対応**: カード請求日は毎月5日、対応する請求日は前月末、PDF内の**発行日は翌月2〜3日**。
例: 仕訳 2026-07-05 ← 請求日 2026-06-30 ← 発行日 2026-07-03。
ファイル名は **発行日** を使う（既存ファイルもその規則）。

### カゴヤ・ジャパン

```
https://kagoyaid.kagoya.jp/kagoyaid/invoice_list/<アカウント別トークン>
```
KAGOYA会員サイトの「請求管理」。トークンは会員サイトにログインして遷移すると得られる
（アカウント固有なのでリポジトリに書かない）。

手順: 上部のセレクトで対象年月を選ぶ → 行のチェックボックスをON → 「ダウンロード」→
PDFが**新規タブで開く**（ダウンロードされない）。そのタブで以下を実行して保存する:

```js
const r=await fetch(location.href); const b=await r.blob();
const a=document.createElement('a'); a.href=URL.createObjectURL(b);
a.download='kagoya_2026-04.pdf'; document.body.appendChild(a); a.click();
```

**日付対応**: カード請求日は翌月5〜8日。PDFの発行日は請求月の月末。
例: 仕訳 2026-05-08 ← 2026年4月分 ← 発行日 2026-04-30。

注意: PDFタブを `tabs_close_mcp` で閉じるとタブグループの追跡が壊れることがある。
閉じずに残し、最後にまとめて片付ける。

### Amazon

注文番号がわかれば領収書ページに直接飛べる:

```
https://www.amazon.co.jp/gp/css/summary/print.html?orderID=<注文番号>
```
注文番号は仕訳の摘要に入っている（例: `注文250-4797853-6277405`）。
PDFダウンロードは無いので、HTMLを保存してローカルでPDF化する（Step 3）。
ファイル名は**注文日**を使う。

### スイッチサイエンス

注文確認メールに含まれる認証付きURLから注文ページへ入り、「注文後メニュー」に進む:

```
https://menu.switch-science.com/#/menu/<注文別トークン>/download
```

注文別トークンは注文ページの「注文後メニュー」リンクから取得する。メールの検索:

```
subject:(<注文番号>) スイッチサイエンス
```
本文中の `https://www.switch-science.com/<shop_id>/orders/<order_id>/authenticate?key=...`
を開く → ページ内の「注文後メニュー」リンクを取得。

書類ダウンロード画面で **「納品書兼適格請求書【インボイス】（発送後）」** を選び、
お名前に `本多 優鷹`（様）を入れて「ダウンロード」。数秒後に
`Y<注文番号>_invoice_delivery_note_<timestamp>_<id>.pdf` が落ちる。

**フォームに氏名を入れて送信する操作なので、ユーザーの承認を得てから実行すること。**
宛名は既存の請求書に合わせて `本多 優鷹`。

同一注文日に複数注文があると発行日が同じになるため、ファイル名に注文番号を付ける
（例: `2026-07-13_スイッチサイエンス_Y219311.pdf`）。

## Step 3: HTML → PDF 変換

PDFダウンロードが無いポータル（マネーフォワード・Amazon）用。

ブラウザ側でページHTMLを丸ごと落とす:

```js
const a=document.createElement('a');
a.href=URL.createObjectURL(new Blob([document.documentElement.outerHTML],{type:'text/html'}));
a.download='<name>.html'; document.body.appendChild(a); a.click();
```

同一ページから2回連続でダウンロードすると Chrome にブロックされる。1ページ1ダウンロード。

ローカルで変換:

```bash
python c:/moneyforward/.claude/skills/mf-invoice-fetch/scripts/html_to_pdf.py <in.html> <out.pdf>
```

**やってはいけないこと**: `getComputedStyle` の結果を全要素にインライン化して保存する方法は
真っ白なPDFになる。外部CSSは `link` ごと捨てて、スクリプト・スタイル・class/style属性を
除去したうえで最小限の自前CSSを当てる（`html_to_pdf.py` はそれをやっている）。

変換後は `fitz` でテキストを抽出し、**金額・発行日が読み取れること**を必ず確認する。
空白ページが付くので `get_text().strip()` が空のページは削除する。

## Step 4: 配置と matches.json 登録

配置先: `references/invoices/<年度>/<発行日>_<取引先>.pdf`

```python
m = json.load(open('references/invoices/matches.json', encoding='utf-8'))
m['2026'][str(仕訳No)] = f'2026/{ファイル名}'
json.dump(m, open(..., 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
```

登録前に必ず `assert str(num) not in y` と `assert not os.path.exists(dst)` を入れて、
既存エントリ・既存ファイルを上書きしないようにする。

## Step 5: 再突合

Step 0 のスクリプトを再実行し、対象が消えたことを確認する。

## メールでもポータルでも取れないもの

- **紙レシート**（飲食店など）— スキャンが必要。ユーザーに依頼する
- **税務署（事業税等）** — e-Tax 電子納付のため領収書なし。matches.json 登録不要

## 既知の命名の揺れ

Google Cloud の既存2件 `2026-04-01_..._5536103869.pdf` / `2026-04-02_..._5539071350.pdf` は
どちらも 4/2 着メールで、PDF内の発行日（2月末・3月末）とも一致しない。以降は
**PDF内の発行日**で統一している。既存2件は未修正。
