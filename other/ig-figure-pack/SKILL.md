---
name: ig-figure-pack
description: サイトSVGを、総監・1級土木・技術士建設部門・技術士一次の図解カルーセル下書き（表紙/図/要点/CTA）へ展開する。資格別ラベル・白背景・元図参照・各スライド目視を必須とし、投稿状態は既存SNS台帳で管理する。過去問クイズはig-post-createを使う。
allowed-tools: Bash, Read, Write, Edit
domain: sns
---

# サイト図をInstagramへ展開する

図で答える受験者の疑問を1つ決め、既存サイトSVGを4枚カルーセルへ展開する。追加図の枚数を目的にしない。制作後の公開は `/publish-ig-bs`、公開状態の照合は `/ig-reconcile` に接続する。

## 正典と対象資格

- 図の意味・数値・文言：`content/site/{category}/{slug}/img/figure-*.svg` と親記事。
- 資格名称・略称：`.claude/knowledge/design-system/note-cover-tokens.json` を `exam-palette.mjs` で解決。
- 図解パックのピル・バッジ・誘導文：`.claude/scripts/sns/lib/figure-pack-labels.mjs` の `figurePackLabels(examDir)`。
- サイト図の寸法・色： [figure-canvas-policy.md](../../../knowledge/reference/figure-canvas-policy.md)。SVGは400×500のfeedを使う。`--wide`を縦に引き伸ばさない。
- ファイルの置き場：[asset-storage-policy.md](../../../knowledge/reference/asset-storage-policy.md)。再生成できる入力はGit、手元用PNGはDrive vaultの既存SNS group。生成PNGをGitへ追加しない。

| category | examDir | ピル | バッジ | CTAの学習先 |
|---|---|---|---|---|
| pe-comprehensive-management | cem | 技術士 総監 | 択一 頻出テーマ | 総監キーワード集 |
| civil-construction-1 | civil-1 | 1級土木 | 試験の要点 | 1級土木の学習ページ |
| pe-construction | pe-construction | 技術士 建設部門 | 記述の考え方 | 建設部門の学習ページ |
| pe-first-stage | pe-first-stage | 技術士 第一次 | 計算の考え方 | 第一次の学習ページ |

未知の資格で総監の既定値を流用しない。略称を追加する場合は共通の資格設定・ラベル解決・検査を一緒に更新する。総監の「頻出」表現は元記事・過去問で根拠を確認できる図だけに使う。

## 出力

`content/sns/instagram/{examDir}/keyword-packs/{slug}/carousel/` に `caption.txt` と `img/{00-cover,01-figure,02-text,03-cta}.svg` を置く。`keyword-packs` を省略しない。

パックの `source.json` に元記事・元図のrepo相対パスとSHA-256、図で答える疑問、次の学習先を残す。これは制作入力の出所であり、公開済み・進捗・KPIを複製する台帳ではない。元図が変わったら差分と意味を確認して再生成する。

## 制作手順

1. 元記事とSVGを読み、学習上の疑問と次の行動を決める。既存図で答えられるなら新作しない。問題文・数値・条件に誤りがあれば先に訂正する。
2. 直近の既存パック（例：`content/sns/instagram/cem/keyword-packs/fail-safe/carousel/img/00-cover.svg`）で意匠を確認する。表紙とCTAは本スキルの [表紙テンプレ](templates/00-cover.template.svg)・[CTAテンプレ](templates/03-cta.template.svg)をコピーする。
3. 表紙の `EXAM`・`BADGE`、CTAの `CTA_DEST` は `figurePackLabels(examDir)` の戻り値で置換する。`KANRI` は総監では5管理の正式名、他資格では「コンクリート」「測量」「必須科目I」などの学習分野。未置換の `{{...}}` を残さない。
4. 図スライドは元SVGをコピーし、必要なら `<svg>` 直後に `<rect width="400" height="500" fill="#ffffff"/>` を1つ加える。独自のIGヘッダー・フッターや試験ポイントを図へ追加しない。元図を改良する場合は先にサイト側を更新する。
5. 要点スライドは図の読み方を最大3点と、混同しやすい条件1つに絞る。navyのヘッダー・フッター、白背景、orangeの注意欄を用い、長い本文は記事で説明する。
6. **各SVGを書いた直後にPNGへレンダリングし、1枚ずつ目視してから次へ進む**。全枚を作ってから初めて確認する進め方をしない。

```javascript
import { Resvg } from '@resvg/resvg-js';
import { readFileSync, writeFileSync } from 'node:fs';
const png = new Resvg(readFileSync(svgPath, 'utf8'), {
  background: '#ffffff', fitTo: { mode: 'width', value: 1080 },
  font: { loadSystemFonts: true },
}).render().asPng();
writeFileSync(pngPath, png); // 手元の出力先。Gitに追加しない
```

出力は1080×1350。色はkeyword-pack共通のnavy `#1a3a5c` / orange `#a36b2c`。試験別の人物カバー刷新は既存のSNS意匠方針に従い、図そのものを人物や大見出しで隠さない。

## 視覚・内容の受入条件

- タイトルは最大2行。標準42px、長いとき34→28pxの順で調整し、28px未満へ縮める前に言い換える。
- テキストと枠の重なり、切れ、透明背景がない。図のラベルが375px相当でも読める。
- 表紙に対象資格、CTAに同じ資格の学習先がある。1級土木の図へ総監の文言を混ぜない。
- 図の数字・因果・矢印と、要点・captionが一致する。本文や出典にない合格効果・頻度・実績を付けない。
- 図は構造、要点スライドは誤りやすい条件、記事は詳しい説明と演習を担当する。
- 画像にハッシュタグを入れない。captionでは資格タグを先に置き、無関係なタグを埋め草にしない。

captionは「短い問い→図の読み方→注意条件→次の学習先」の順。Instagram本文のURLは直接クリックできないため、プロフィールのリンクから対象資格へ到達できることを確認する。

## 検証と公開への引継ぎ

```bash
node scripts/check-ig-cover.mjs
node scripts/check-ig-cta.mjs
```

追跡済みのパックは `node scripts/render-figure-pack.mjs --pack civil-1/keyword-packs/{slug}` で4枚PNGを再生成する。`--check` は元記事・元図のSHA-256と入力4枚だけを検証し、`--out-dir .tmp/figure-pack-preview` で出力先を指定できる。ハッシュが変わったら意味を再確認し、必要なスライドとsource.jsonを更新してから再生成する。

表紙・CTA・白背景は機械ゲート、図の意味と可読性は目視で確認する。サイト専用SVG監査をIGのnavy帯へ適用して、正規の濃色帯を違反扱いしない。

公開日は `status.json` / `posted.json` と実機を真実源にし、制作日を公開日として記録しない。7日後の反応確認は既存の資格別business reviewで扱い、欠測を0や効果なしに変換しない。公開済み投稿の図の更新は、元投稿の編集可否とURL・履歴への影響を確認して既存公開フローで行う。

## 単一図の派生画像

図解パックのナレーション付きReelsは `node scripts/figure-reel-create.mjs --pack civil-1/keyword-packs/{slug}` を使う。`carousel/img` の4枚のPNGと `reels/script.txt`（1スライド1行）、VOICEVOX・ffmpegが必要。総監は `--pack cem/keyword-packs/{slug}`。`/ig-reel-create` の過去問quizスキーマとは入力が異なる。

カルーセルとは別に、図1枚をIG・動画サムネ・縦型へ書き出す場合は既存コマンドを使う。資格名は `src/config/categories.json` から自動取得し、`--mgmt` は任意の管理分野・テーマ（16文字以内）とする。総監キーワードの短いslug指定も利用できるが、管理分野は自動推測しない。

```bash
node .claude/scripts/sns/render-figure-sns.mjs \
  --slug civil-construction-1/guide-concrete-key-points \
  --figure figure-aggregate-moisture.svg --concept "骨材の水はどこにある？" \
  --format all --out-dir .tmp/figure-preview
```

`--concept` は44文字以内。未知カテゴリ・形式や長すぎる見出しは書込み前に停止し、文言を黙って切り捨てない。PNGの生成だけで投稿済み・公開済みとは報告しない。

### 同じ図をX下書きへ展開するとき

`content/sns/x/draft/NNN-slug-diagrams/{tweets.md,status.json,images.json}` に、元記事・元図のパスとsha256、学習上の疑問、投稿番号、画像名を記録する。`node scripts/render-x-figure-drafts.mjs --draft NNN-slug-diagrams --check` で下書き状態と元データを確認し、`--check` を外してPNGを生成する。元記事が変わった場合は内容を再確認してからハッシュを更新する。画像はDriveの `x-rendered-image`、公開状態は既存X台帳で管理する。退避対象は番号付き `*-diagrams` 下書きの `img/tweet-NN-名前.png` のみ。既存Xカードはこのgroupの対象外。

図解Reelsの音声クレジットは、生成時にVOICEVOXの話者一覧から実際のspeaker IDの声名を取得し、`reels/caption.txt` に記録する。既定ID 1はずんだもん（あまあま）。声名を数値IDから推測しない。専門用語は生成前に `.claude/scripts/lib/sns-common/reading-dict.mjs` を適用し、実機の読みを確認する。誤読を直した場合は音声・動画を再生成し、Drive台帳とクラウド実体を再照合する。
