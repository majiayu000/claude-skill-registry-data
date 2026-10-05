---
name: publish-note
description: browser-use CLI で note.com（note.com/dobokunote）エディタを自動操作し、(1) 総監模範論文ペルソナ別マガジン記事（有料）または (2) 建設部門の無料ファネル記事（入口/キーワード, `--free`）を下書き保存・予約・即時公開する。Use when user says "note投稿", "note公開", "note下書き作成". 本文paste・カバー・タグを自動設定。実行は Mac 推奨（会社PCはプロキシ制約）。
disable-model-invocation: true
user-invocable: true
argument-hint: "<persona> <RXX>[ <M/D> <HH:MM>][, ...] | --free <content/note配下dir>[ <M/D> <HH:MM>|now][, ...]"
domain: product
---

browser-use CLI（Chrome プロファイル経由）で **note.com/dobokunote** のエディタを自動操作し、総監模範論文ペルソナ別マガジンの記事（`content/note/技術士総監/magazines/総監模範論文-<persona>/<RXX>/article.md`）を下書き保存または予約投稿する。

このスキルは stats47 プロジェクトの `publish-note`（note.com 自動投稿の実証済みスキル）を doboku-note 用に適応したもの。**note.com エディタ操作の共通ノウハウは `references/` を参照**し、本 SKILL.md は doboku-note 固有の規約・差分・安全ゲートを定義する。

## 実行環境の前提（重要）

- **browser-use 経路（本スキルの新規公開フロー）は Mac 推奨**。会社 PC（Windows）はプロキシが browser-use の LLM バックエンドを遮断する可能性が高く、browser-use 自体も未導入（[[project_ig_api_posting_setup]] と同根）
- **ただし Windows でも動く Playwright 経路がある**（browser-use 不要・LLM バックエンド不要）: 新規公開＝`scripts/note-publish.mjs`、**公開済み記事への CTA 追記/ライブ反映＝`scripts/note-append-cta.mjs`（`npm run note-append-cta`）**、マガジン設定＝`note-edit-magazine.mjs`。いずれも `<auth root>/profiles/playwright-note-profile`（永続・初回のみ手動ログイン）を使う。update 系の詳細は [references/update-mode.md](references/update-mode.md)
- **browser-use CLI がインストール済み**であること（Mac 経路のみ・`$HOME/.browser-use-env/` 等）
- **Chrome プロファイルが note.com/dobokunote にログイン済み**であること。プロファイル名は環境変数 `NOTE_PROFILE` に設定（例: `export NOTE_PROFILE="Profile 1"`）。references の例にある `Profile 5` は stats47 用なので**使わない**
- **予約投稿**は現在は無料（誰でも可・note プレミアム不要）。Windows Playwright 版は `scripts/note-publish.mjs --schedule "YYYY-MM-DDTHH:MM"`（JST）、時間ずらしバッチは `note-publish-magazine.mjs --list <manifest> --schedule-start ... --interval-hours N`

## 投稿先アカウント（最重要・誤爆防止）

**このスキルの投稿先は `note.com/dobokunote` 固定。** Phase 1 のアカウント照合ゲートを必ず通す（stats47 で 2026-05-20 に別アカウントへ誤公開した事故の再発防止策。プロファイル分離だけではセッションドリフトを防げない）。

## stats47 → doboku-note 差分マップ（references を読む際の読み替え表）

| 項目 | stats47（references の記述） | doboku-note（本プロジェクト） |
|---|---|---|
| アカウント | `note.com/stats47` / Profile 5 / stats47jp@gmail.com | **`note.com/dobokunote`** / `$NOTE_PROFILE` |
| 記事パス | `docs/31_note記事原稿/<vertical>/<slug>/{note.md,draft.md}` | **`content/note/技術士総監/magazines/総監模範論文-<persona>/<RXX>/article.md`** |
| 有料フラグ | frontmatter `is_paid` / `price_jpy` | frontmatter **`notePricing: paid`** / **`price: 500`** |
| 有料境界マーカー | 本文中 `ここから先は有料部分:` 行 | **既定＝`## 試験問題`/`## 予想問題` 行の直前**（intro・「この記事でわかること」・冒頭CTA は無料プレビュー、試験問題＋解答以降が有料）。**境界見出しはコンテンツ型ごとに上書き可**＝Windows/Playwright 版 `note-publish.mjs` が frontmatter `paidBoundary`（H2 見出しの先頭一致 regex）または `--boundary-regex` を読む。**1級土木 完全攻略パック（工事別）は `paidBoundary: 品質管理`**（導入＋冒頭CTA＋想定工事概要が無料・5管理の完成答案以降が有料）。境界が見つからなければ公開中断（boundaryBeforeExam ゲート） |
| マガジン名/説明/価格 | 各 vertical の設定 | **`総監模範論文-<persona>/note掲載文.txt`** からコピペ |
| ハッシュタグ | 記事内 | **`<RXX>/hashtags.txt`**（**90 個以上必須**〜99・**1 行 1 タグ**＝`#` 接頭辞・改行区切り。space 区切り単一行は note 側で 1 タグ扱いになる不良。`npm run check-note-hashtags` が機械検査、`--staged` で pre-commit ゲート。note-publish は 99 で打ち切り） |
| アイキャッチ | 生成画像 | **`<RXX>/img/cover.png`** |
| 購入特典PDF | なし | **`<RXX>/模範論文-*.pdf`**（有料エリアに添付。**Windows/Playwright では `note-attach-pdf`〔`note-attach-file.mjs`〕で自動化済**＝本 browser-use 系では半自動） |
| 公開URL記録 | `note-published.json`（items） | **各記事 frontmatter `noteUrl`/`noteId`** ＋ `src/lib/note-magazines.ts`（マガジンURL・published） |

## 引数（バッチ対応）

```
/publish-note <persona> <RXX>[ <M/D> <HH:MM>] [, <persona2> <RXX2> ...]
```

- **persona**: ペルソナ名（例 `自治体港湾担当`。`総監模範論文-` 接頭辞は不要）
- **RXX**: 年度ディレクトリ（`R03`〜`R07` / `R08-yosou-1` / `R08-yosou-2`）
- **M/D HH:MM**: 予約日時（任意・省略時は下書き保存のみ）

例: `/publish-note 自治体港湾担当 R03 7/1 08:00, 自治体港湾担当 R04 7/1 12:00`

## 一括公開の区切りと成否判定（2026-08-22 実測）

- **1バッチは 25 本まで**。実務立場別小論文集33本を連続投稿したところ、**31本目から「投稿する」が完了しなくなった**（画面は公開設定のまま留まり、記事は 404。再実行でも再現）。**20分空けたら同じ原稿がそのまま公開できた**ので、note 側の連続投稿スロットルとみられる。25本で区切るか、失敗したら 20 分待って再開する。
- **成否は `RESULT` 行で判定しない**。`RESULT` の `"mode":"commit"` は失敗時も出る。`note-publish.mjs` は最後に `[13]` で API 実体検証を行い、失敗時は `[13] FAIL: ...` を出すので、**バッチのループはこの行の有無で判定する**。2026-08-22 に RESULT 行で数えて、失敗した2本を成功として数えた。
- **公開後は API で全数実査する**（`https://note.com/api/v3/notes/{key}` の `status` / `price` / 本文の無料プレビュー字数）。有料記事で `preview=0` は有料境界の崩壊。
- **中断すると下書きが残る**。frontmatter の `noteUrl` を消して再実行すると新しい key で作り直すため、残骸は `note-delete-note.mjs` で消す（ただし同スクリプトは `note.com/notes` の1ページ目しか走査しない）。

## 無料記事モード（建設部門 入口/キーワード記事）— `--free`

総監マガジン（有料・ペルソナ/年度）とは**別系統**で、建設部門の**無料ファネル記事**（`notePricing: free`）を公開する。有料境界の分割・価格設定・特典PDF添付・マガジン設定を**すべてスキップ**する分、フローは単純。`content/note/技術士建設部門/{theme}/article.md`（入口16本・論点キーワード6本）が対象。

### 引数（無料モード）

```
/publish-note --free <技術士建設部門配下のdir>[ <M/D> <HH:MM> | now][, <dir2> ...]
```

- **dir**: `content/note/` からの相対パス（例 `技術士建設部門/防災・減災の論点キーワード`）。スペースを含むので**カンマ区切りのバッチでは各 dir をそのまま**書く
- **日時・`now` 省略 → 下書き保存のみ**（既定・最も安全。まず1本これで挙動確認するのを推奨）
- **`now`** → 即時公開／**`<M/D> <HH:MM>`** → 予約公開（note は現在 無料で予約可）
- 例（下書き）: `/publish-note --free 技術士建設部門/防災・減災の論点キーワード`
- 例（即時公開）: `/publish-note --free 技術士建設部門/社会資本整備の論点キーワード now`

### Phase 0-free: データ読み込み（無料記事版）

`/tmp/note-prepare-free-<slug>.js` に書き出して実行する。**`notePricing: free` でなければ即中断**（有料記事を誤って無料公開しない安全弁）。

```javascript
// /tmp/note-prepare-free-<slug>.js
const fs = require('fs');
const path = require('path');
const projectRoot = '/Users/minamidaisuke/doboku-note';
const relDir = '<DIR>'; // 例: 技術士建設部門/防災・減災の論点キーワード
const articleDir = path.join(projectRoot, 'content/note', relDir);
const articleFile = path.join(articleDir, 'article.md');
if (!fs.existsSync(articleFile)) { console.error('ERROR: article.md not found: ' + articleFile); process.exit(1); }
const raw = fs.readFileSync(articleFile, 'utf8');
const fm = (raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1]) ?? '';
const fmField = (k) => { const m = fm.match(new RegExp('^' + k + ':\\s*(?:"(.*?)"|\'(.*?)\'|(.+?))\\s*$', 'm')); return m ? (m[1] ?? m[2] ?? m[3] ?? '') : ''; };
const notePricing = fmField('notePricing');
if (notePricing !== 'free') { console.error('ABORT: notePricing != free (got "' + notePricing + '"). 無料記事モードは free 専用。'); process.exit(2); }
// タイトルは本文先頭の H1（建設部門の無料記事は frontmatter に title: を持たず `# …` が表示タイトル）
const bodyForTitle = raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n*/, '');
const title = (bodyForTitle.match(/^#\s+(.+)$/m)?.[1] ?? fmField('title')).trim();
if (!title) { console.error('ABORT: タイトル（先頭 # H1）が見つからない。'); process.exit(3); }
let body = raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n*/, '');
body = body.replace(/<!--[\s\S]*?-->\n?/g, '');   // HTML コメント除去
// 本文画像 ![](img/) は除去せず一意トークン化して残し、paste 後に「＋」メニューでアップロードする
// （2026-07-15〜。真実源: lib/note-images.mjs extractBodyImages / insertImagesAtPlaceholders）
// const { body: b2, images } = extractBodyImages(body, articleDir); body = b2;
body = body.replace(/^---$/gm, '');               // 水平線除去
body = body.replace(/^#\s+.*\n+/, '');            // 先頭 H1 除去（タイトル欄へ入れるため）
body = body.trim();
function splitSegments(text){ const segs=[]; let buf=[]; for(const line of text.split('\n')){ if(/^https?:\/\/\S+$/.test(line.trim())){ if(buf.length){segs.push({type:'text',content:buf.join('\n')});buf=[];} segs.push({type:'url',content:line.trim()});} else buf.push(line);} if(buf.length)segs.push({type:'text',content:buf.join('\n')}); return segs; }
const segments = splitSegments(body);
const tagsPath = path.join(articleDir, 'hashtags.txt');
const tags = fs.existsSync(tagsPath) ? fs.readFileSync(tagsPath,'utf8').trim().split('\n').map(s=>s.trim()).filter(Boolean).slice(0,50) : [];
const coverPath = path.join(articleDir, 'img/cover.png');
const cover = fs.existsSync(coverPath) ? coverPath : null;
const slug = relDir.replace(/[\/\s・／]+/g,'-');
const result = { slug, articleDir, articleFile, title, isPaid:false, priceJpy:0, segments, segmentsFree:segments, segmentsPaid:[], tags, cover, segmentCount:segments.length, urlCount:segments.filter(s=>s.type==='url').length };
fs.writeFileSync('/tmp/note-data-'+slug+'.json', JSON.stringify(result,null,2));
console.log(JSON.stringify({ slug, title:title.substring(0,50), notePricing, segments:segments.length, urls:result.urlCount, tags:tags.length, cover: !!cover }));
```

実行: `node /tmp/note-prepare-free-<slug>.js`。中断（exit≠0）したら**その記事は公開しない**。

### フロー（無料記事 = 有料フローからの差分）

[references/editor-operations.md](references/editor-operations.md) の Phase を再利用しつつ、無料記事では次の差分を適用する。

- **Phase 1 アカウント照合ゲート**: 共通（必須）。`dobokunote` 不一致なら即中断
- **Phase 2 アイキャッチ**: `data.cover`（＝`<dir>/img/cover.png`）をアップロード。editor-operations の例にある `images/cover-1280x670.png` は読み替える
- **Phase 3 タイトル**: `data.title`（先頭 H1 は除去済）
- **Phase 4 本文**: `data.segments`（＝全文）を**チャンク注入機構で 1 回 paste**（無料記事は free/paid 分割なし＝全文が無料）。BK-I の note URL・サイト URL 行のカード化は半手動（行末 Enter→4 秒）
- **Phase 4.5 目次**: 見出し（H2）が 3 つ以上の記事（もくじ/総合案内/長文）は、本文先頭に note ネイティブ目次ブロック（`<button id=toc-setting>`）を挿入する（[references/editor-operations.md](references/editor-operations.md) Phase 4.5）。markdown の `#アンカー`は note で機能しないため、見出しジャンプはこのブロックが唯一の手段。短い単一セクション記事はスキップ
- **Phase 5 挿絵**: スキップ（図版なし方針）
- **Phase 6 下書き保存**: 共通
- **Phase 7 公開設定**: **価格設定は行わない（無料）**。`<RXX>` 相当のタグは `data.tags`（hashtags.txt）。日時指定 → 予約公開、`now` → 即時公開、無指定 → 下書きのまま終了
- **Phase 8 検証＆記録**: 偽成功の罠に従い本文文字数・カバー・タグを実体検証。**公開した場合のみ** 記事 URL を当該 `article.md` frontmatter `noteUrl`/`noteId`/`notePublishedAt` に反映（これらは空文字で用意済み）し、`noteStatus` を published（予約投稿時は reserved）へ更新。下書きのみなら記録しない。※予約投稿は go-live が後刻のため weekly の `verify-note-status` が published へ最終是正

### 無料モードのガード

- `notePricing != free` → 即中断（有料記事の無料公開防止）
- 本文に `{{MAGAZINE_URL}}` 等プレースホルダが残存 → 中断
- 既存の note 入口16本は `noteStatus: draft`。**公開順は無料入口→キーワード→有料マガジンの導線が開く順**を意識する（収益導線の整合）

## browser-use 共通設定

```bash
export PATH="$HOME/.browser-use-env/bin:$HOME/.browser-use/bin:$HOME/.local/bin:$PATH"
export NOTE_PROFILE="Profile 1"   # note.com/dobokunote にログイン済みのプロファイル名に置換
```

**全コマンド**: `browser-use --headed --profile "$NOTE_PROFILE" <command>`（references の `--profile "Profile 5"` は `"$NOTE_PROFILE"` に読み替え）

### ⚠️ 必須: 終了時クリーンアップ

スキル完了時／中断時に daemon と使い捨て Chrome を必ず停止する。手順は **[references/editor-operations.md](references/editor-operations.md)** および stats47 由来の3段クリーンアップ（macOS は osascript でエディタタブも閉じる）に従う。**Windows で実行する場合は `pkill`/`osascript` が無いため、`Stop-Process`/タスクマネージャ等で browser-use daemon と chromium を停止する**（が、原則 Mac 実行）。

## 実行フロー

```
引数パース → 記事ごとにループ:
  Phase 0: データ読み込み（Node.js・doboku-note 規約）
  Phase 1: ブラウザ起動 → ★dobokunote アカウント照合ゲート★ → エディタ表示
  Phase 2: アイキャッチ（img/cover.png・本文入力前に実行）
  Phase 3: タイトル入力（frontmatter title から H1 を除いた表示タイトル）
  Phase 4: 本文入力（一括 ClipboardEvent paste・URL は plain text）
  Phase 4.5: 目次ブロック挿入（H2 3 つ以上＝もくじ/長文記事のとき。id=toc-setting。markdown #アンカーは note で機能しないため必須手段）
  Phase 5: （図版なし方針のため通常スキップ）
  Phase 6: 下書き保存
  Phase 7: 公開設定（有料価格・タグ・予約 or 即時）※本 browser-use 系では有料境界とPDF添付は半自動（Windows/Playwright は note-publish〔境界〕・note-attach-pdf〔PDF〕で自動化済）
  Phase 8: 確認スクショ → 公開URLを frontmatter に反映
→ 全記事完了後にブラウザを閉じる + 必須クリーンアップ
```

### Phase 0: データ読み込み（doboku-note 規約）

Node.js で対象記事を読み込み `/tmp/note-data-<persona>-<RXX>.json` に出力する：

1. `content/note/技術士総監/magazines/総監模範論文-<persona>/<RXX>/article.md` を読む
2. frontmatter から `title`（先頭 `# ` 見出しを表示タイトルに採用）/ `notePricing` / `price` を抽出
3. 本文を **`## 試験問題` 行の直前で free / paid に分割**（intro＝無料プレビュー、試験問題以降＝有料）
4. 本文をセグメント分割（URL 単独行 vs テキスト。URL は paste 後に plain text のまま＝カード化は Phase 4-3）
5. `<RXX>/hashtags.txt`（タグ）、`<RXX>/img/cover.png`（アイキャッチ）、`<RXX>/模範論文-*.pdf`（特典）の存在を確認

**Phase 0 ガード**: 本文に未反映プレースホルダー（`{{MAGAZINE_URL}}` または `※note 公開後…予定` 系）が残っていたら、その記事は**公開せず中断**。先に `.claude/scripts/note/inject-magazine-url.cjs <persona> <マガジンURL>` で実 URL を注入しておく。

### Phase 1: dobokunote アカウント照合ゲート（投稿前に必ず）

```bash
browser-use --headed --profile "$NOTE_PROFILE" open "https://note.com/settings/account"
browser-use --headed --profile "$NOTE_PROFILE" state 2>&1 > /tmp/note-acct.txt
```

`state` 出力からログイン中アカウントのハンドルを読み取り、**`dobokunote` と決定論的に文字列照合**する。

- 一致 → Phase 2 へ
- **不一致 / 未ログイン / 確認不能 → 即中断**（1 記事も投稿しない）。「Profile が note.com/dobokunote にログインしていません。投稿を中止しました」と報告。憶測で続行しない

### Phase 2〜8: エディタ操作

具体的な browser-use コマンド・要素検索・paste 機構は **[references/editor-operations.md](references/editor-operations.md)**、有料価格/タグ/予約は **[references/scheduling.md](references/scheduling.md)**、要素ヘルパー/エラー処理は **[references/troubleshooting.md](references/troubleshooting.md)** を参照（アカウント・パスは差分マップで読み替え）。doboku-note 固有の要点：

- **Phase 2 アイキャッチ**: `<RXX>/img/cover.png` をアップロード（本文入力前）
- **Phase 4 本文**: free セグメントを一括 ClipboardEvent paste（H2/H3/太字が変換される唯一の方法。`type` 不可・連続 paste 不可）。**URL カード化は半手動**（本プロジェクトの記事はマガジンCTAの URL を単独行で持つ＝ペースト後に各 URL 行を行末 Enter → 4 秒待ちでカード化。references 4-3）
- **Phase 7-Pricing**: `notePricing: paid` かつ `price>0` のとき有料設定。Shadow DOM 内 `<input id=price>` に JS で価格を上書き（`type` 不可）
- **本 browser-use(Mac) 系では 有料境界の指定 と 特典PDF添付 は半自動**（stats47 でも未到達領域だった）。価格設定までは自動、有料エリア境界の選択と PDF 添付は人間が手動。**※Windows/Playwright 系では両方とも自動化済**＝有料境界は `note-publish`（`boundaryBeforeExam` 検証ゲート）、PDF 添付は `note-attach-pdf`（`note-attach-file.mjs`／既存境界を非破壊検証して再公開）。Windows 会社PCで運用する場合はこちらを使う
- **Playwright 版も目次挿入に対応済（2026-07-02）**＝`note-publish.mjs`（新規公開・Phase 6.5）と `note-update-body.mjs`（全文置換後の再挿入・4.5）が H2>=3 で本文先頭に note ネイティブ目次（`#toc-setting`）を挿入する（`--no-toc` で抑止）。目次は Phase 4.5（browser-use）だけの手作業ではなくなった。検証は screenshot 目視（`.tmp/np-toc.png` / `.tmp/nu-toc-*.png`）
- **macOS 実行の注意（note-update-body）**: 本文全置換の「全選択」は Meta+A（Ctrl+A は行頭移動で空化に失敗→本文二重化）。`note-publish.mjs` は /new 空エディタ paste なので影響なし。無料記事の `--commit` は「更新する」まで自動完走（2026-07-14 実証で旧「未対応」は解消）
- **メンバーシップ連携記事（price=0 だが会員限定）**: `note-update-body` は3段の試し読みフロー（`公開に進む → 試し読みエリアを設定 → 更新する`）に対応。入口LP（まるごとパック等）の無料プレビュー復旧は `--trial-line-bottom`（試し読みラインを末尾-1に設置。絶対末尾は全ロックに戻る罠あり）。無料設定のまま意図して全文ロックしている記事は `--keep-member-lock`。無料記事でどちらも無いと試し読み画面で中断する（ラインなしの更新で全文会員限定になる事故の防止・2026-09-23〜）。詳細 SSOT: `.claude/knowledge/reference/note-api-verification.md`「メンバーシップ試し読みフロー」
- **公開済み記事へのタグ差分追加**: `scripts/note-sync-tags.mjs`（本文非破壊・note上限99・不足分をlive照合で追加。上限99で足せないときは `--prune` で原稿に無いタグを外してから足す）。note-update-body は単発では本文専用だが、`--sync`（未反映の部品だけ）や `--parts body,cover,tags` でカバー・タグも 1 回の更新に含められる（Mac の週次 note-sync はこちらで記事単位にまとめて反映する）。タグdrift は `check-note-republish` が surface
- **frontmatter の note* 行**: `note-publish.mjs` の公開後 writeback は `noteUrl`/`noteId`/`notePublishedAt`/`noteStatus` を **行が無ければ挿入**する（`setFmField`・2026-07-02 是正）。旧実装は replace-only で、テンプレに note* 行が無い記事は URL 記録が無音失敗し、`note-publish-magazine` の冪等ガード（noteUrl 有無）も効かず一括重複公開の危険があった
- **Phase 7-Tags**: `<RXX>/hashtags.txt` の内容を入力
- 予約日時があれば予約投稿、なければ「今すぐ公開」または下書き保存のみ

### Phase 8 後: 公開 URL の反映

公開（即時/予約）したら、その記事 URL（`note.com/dobokunote/n/<id>`）を：

1. 当該記事 `article.md` の frontmatter `noteUrl` / `noteId` / `notePublishedAt` / `noteStatus`（published／予約=reserved）に記入
2. マガジン単位で全 7 記事が公開済みになったら、`src/lib/note-magazines.ts` の該当エントリを `published: true` ＋ マガジン `noteUrl` に更新（マガジンURL は `inject-magazine-url.cjs` で本文にも反映）

下書き保存のみの場合は記録しない。

## 偽成功の罠（必ず実体検証）

「投稿できた」というログを**信用しない**。stats47/publish-x で予約ゼロの空振り事故があった（[[feedback_publish_x_false_success]]）。公開後は **note の公開ページ（または下書き一覧）を実取得して、本文・カバー・タグ・価格・カード化が実際に反映されているか DOM/スクショで確認**してから「完了」と報告する。clipboard paste 不発（本文空）も頻発するため、paste 後に本文の文字数を eval で確認する。

### 幻 noteId（fail=0 なのに未公開）— バッチ公開後の必須ゲート

> **エンジンの分界（DN-0091・2026-08-27 明示）**: 下記「バッチ側の一次ガード」は Playwright 系エンジン
> （`note-publish.mjs` / `note-publish-magazine.mjs`＝本スキルと `note-publish` スキルが共用する実装）の話。
> 一方「バッチ後の確証ゲート」`verify-note-status` は**どのエンジンで公開しても共通**の実在照合で、
> 公開経路を問わず必須。スキル名が似ている `note-publish`（`.claude/skills/social/note-publish/`）と本スキル
> （`.claude/skills/social/publish-note/`）は**同じエンジン群を呼ぶ別入口**であり、ガードは実装側に置かれているため
> どちらから使っても効く。

`note-publish.mjs` の writeback は**ページから拾った URL の id を書くだけ**で、公開が実際は未完了でも幻 id を frontmatter に書きうる。`note-publish-magazine.mjs` は従来 `noteUrl` の有無だけで OK 判定していたため、**`fail=0` と報告しつつ一部が未公開＋幻 id（API で 404）** という偽成功が起きた（2026-06-30 完全攻略パック 工事82-87 の6本・[[project_civil1_flagship_pack]]）。

- **バッチ側の一次ガード（2026-07-01 実装済）**: `note-publish-magazine.mjs` は即時公開分について、書き戻した noteId が note API v3 で実在するか照合する。確定 404（幻 id）なら `fail` で停止する（予約投稿は go-live 後刻ゆえ検証しない）。
- **バッチ後の確証ゲート（必須）**: 公開バッチ完了後・「完了」と報告する前に必ず `npm run verify-note-status` を回す。**fm=published ↔ ライブ=404** を `WARN` で列挙する reconciler で、幻 id・静かな未公開を全件で捕捉する。WARN が出たら該当記事の frontmatter（noteUrl/noteId/notePublishedAt）を空へリセット→`--commit` で再公開→再照合する。ネットワーク依存で遅いため CI ゲートには入れない（weekly-review でも定期実行）。

### 有料記事は「公開・更新しただけ」では未完成（2026-07-31 新設）

有料記事は **公開できたか**だけでなく、**購入前の読者に何が見えているか**まで確認して初めて完了になる。2026-07-31 に 2 つの事故が同時に起きた。

**① 無料プレビューの崩壊（paywall 事故）**: `note-update-body --keep-boundary` で本文にブロックを足したところ、有料境界が記事冒頭へ移動し、**有料2本が無料プレビューほぼ0字の状態で公開された**。スクリプトは「ライブ反映完了」と正常終了しており、公開ページを人が開くまで誰も気づけなかった。

- **`--keep-boundary` は本文のブロック数が変わる更新では使わない**。CTA 追加・段落追加を伴う更新は必ず `--boundary-h2 "<境界H2>"` で境界を再設定する
- `assertLiveBody` が `paid: true` のとき無料プレビュー長を検査するようになった（既定 600 字未満で FAIL）。`note-publish` / `note-update-body` は緑で終わらない
- 全件の実査は `npm run check-note-free-preview`（`:ci` で exit 1）。公開・本文更新の直後と週次で回す

**② 商品導線ゼロ**: 単品有料記事を 8 本公開したのに、**無料プレビューにマガジンへの導線が 1 本も無かった**。単品 ¥500 を読んだ読者がセットに気づけない。`check-note-paid-cta` は「L2 もくじ未定義の資格 14 件（対象外）」として素通りさせていた＝検査ゼロを PASS と呼んでいた。

- 有料記事は**所属マガジン URL を無料域（有料境界の直前）に bare URL 単独行**で置く。価格は本文に書かない（改訂で陳腐化・content-principles §14-c）
- `npm run check-note-paid-cta` が L2 未定義の資格も検査するようになった（導線ゼロは exit 1）

**③ PDF 添付の消失**: 全文置換で添付が消え、**購入者が代金を払って PDF を受け取れなくなった**（施工計画 R08予想 3 本）。note のアップロード 1 日 100 件上限に達して復元が失敗 →「保存しない」で中断 → **エディタには添付削除済みの状態が残る** → 失敗理由を確かめず再実行し、添付 0 を正として上書きした。

- 語句・段落・CTA・カード・節順だけなら **`note-update-partial`**（対象要素限定・PDF 添付不変条件・dry-run は読み取りだけ）
- 全文差し替えが不可避な有料記事だけ **`note-update-body --reattach-pdf`**（置換前に添付を記録し、保存前に貼り直す）
- **中断した記事をそのまま再実行しない**。`note-update-body` は中断を `.claude/state/note-update-aborted.json` に記録し、次回は SKIP する（`--force-retry` で解除）。解除前に必ず live を実査する
- アップロードは **1 日 100 件が上限**。`--reattach-pdf` は done-log を見て 90 件で止まる

**公開・更新後の必須4点**（これを通すまで「完了」と言わない）:

```bash
node scripts/check-note-structure.mjs                          # 無料プレビュー崩壊・境界・価格（FREE_PREVIEW_COLLAPSE/FULL_LOCK）
npm run check-note-attachments:live -- --only <noteId,...>     # 約束した PDF が live に実在するか（要ログイン）
npm run check-note-paid-cta                                    # 無料域に商品導線があるか
npm run verify-note-magazines                                  # マガジン公開状態と SoT の突合
```

**添付を持つ記事を更新したら `check-note-attachments:live` を必ず回す**。2026-07-31 はこれを一度も回さなかったため、3 本の消失に気づくのが遅れた。

### PDF 商品は「公開しただけ」では未完成（2026-07-28 新設）

note の PDF 添付はプラットフォーム機能で **markdown に現れない**。公開と添付は別工程で、添付を忘れても SoT からは分からず、**購入者が代金を払って PDF を受け取れないまま売れ続ける**（1級土木 一次過去問PDF ¥1,980 で発生・PDF はビルド済みでアップロードだけが漏れていた）。

`note-publish --commit` は記事 dir（または `<dir>/pdf/`）に PDF があると公開後に **exit 9「未完成」** で終わり、実行すべき `note-attach-file` コマンドを列挙する。緑で終わるまでが公開作業。→ `note-attach-pdf` スキル

## トラブルシューティング

要素検索ヘルパー（`find_idx`）・実証済み要素パターン・clipboard paste 不発時の対処は **[references/troubleshooting.md](references/troubleshooting.md)**。既存公開記事の更新は **[references/update-mode.md](references/update-mode.md)**。

> [!warning]
> **既存公開記事の更新で paste は使えない**（`/new` 専用。`notes/<id>/edit` では無音失敗）。追記は **type 方式**（URL は type で OGP カード化）、全面差し替えは **`/new` 作り直し**、空更新事故の復旧は **note の変更履歴**。「全消去→再 paste」は禁止（2026-06-16 空更新事故）。詳細は update-mode.md 冒頭の danger ブロック。

## 参照

- `.claude/skills/social/publish-note/references/` — note.com エディタ操作ノウハウ（stats47 由来・差分マップで読み替え）
- `.claude/scripts/note/inject-magazine-url.cjs` — マガジンURLのプレースホルダ一括注入（doboku-note 版）
- `.claude/knowledge/reference/note-essay-review-checklist.md` Step 10 — 公開後 URL 反映フロー
- `.claude/skills/social/publish-x/` — 同系統のブラウザ自動投稿（persistentContext・偽成功検証の設計元）
- `src/lib/note-magazines.ts` — マガジンの published/noteUrl/price 真実源
