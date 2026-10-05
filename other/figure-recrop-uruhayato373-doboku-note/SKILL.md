---
name: figure-recrop
description: >
  既存の記事図クロップ（content/site/**/img/*.webp）を「タイト再クロップ」して、
  図に写り込んだ答え/本文/問題文テキストを除き公開レベルへ上げるオーケストレータスキル。
  元PDFからの再抽出ではなく、既に埋め込まれている画像を切り直す（civil-figure-rework とは別物
  ＝あちらは問題PDFから抽出だが過去問PDFは図なしテキスト版で不成立）。provenance の
  needs=recrop/recrop-urgent を対象に、視覚で切り位置を決め figure-recrop.mjs で機械適用する。
  Use when user asks to [図の写り込みを除く, 図を再クロップ, 答え漏らし図の是正, /figure-recrop].
user-invocable: true
domain: site
---

# /figure-recrop

記事に埋め込み済みの図クロップから、**答え漏らし（「したがって，(N)は適当」「【正解】(N)」）・本文/問題文の写り込み**を、既存画像を切り直して除く。図画素は既に足りている（=画質OKで写り込みだけが問題）ケース専用。

> [!warning] このスキルが直せないもの
> - **画質不足（ボケ/低解像度）**は切り直しでは直らない → `figure-provenance` の needs=rescan（要再スキャン）。
> - **元クロップ時点で図が見切れ**ているものは復元不可 → 再スキャン or SVG。
> - **過去問データグラフの SVG 化は禁止**（幾何が答え＝誤答誘発）。真実源 [figure-provenance.md](../../../../.claude/knowledge/reference/figure-provenance.md)。

## 対象の選び方

1. `npm run audit-figures`（監査→provenance 再生成）。
2. `node scripts/build-figure-provenance.mjs --list recrop-urgent`（続けて `--list recrop`）で公開×掲載の対象を出す。管理画面の記事図版タブは目視確認専用で、needs の絞り込みやバッジは出さない。
3. **対応 needs の精度**: `recrop-urgent`(答え漏らし)・`recrop`(問題文/選択肢＝QA構造で高精度検出) は**ほぼ確実に写り込みあり**＝そのまま対象。`recrop-review`(句点あるが QA 構造なし＝**図の凡例/ラベルの可能性**)は**必ず現物を目視**し、凡例なら触らない（例: 「Uc≥10：粒度分布がよい。」は図の一部＝残す）。着手前に現物を Read するのは全 needs 共通の鉄則。

## 手順（1 図ずつ）

```bash
# ① 現物を見る（webp→png 変換して Read。切り位置＝テキスト帯の場所を判断）
sips -s format png <.local/.../img/NAME.webp> --out /tmp/x.png   # Read で目視

# ② 切り位置を決めて適用（crop+webp再生成+MDX width/height更新+OCR報告を1発）
#    上帯を落とす=--top / 下帯=--bottom(上をFだけ残す) / 中央図=--band Y0 Y1 / 明示=--crop WxH+X+Y
node scripts/figure-recrop.mjs <.local/.../img/NAME.webp> --top 0.15
#   → まず --dry-run で dims/OCR を確認してから本適用してもよい

# ③ 検証: 出力 JSON の ocr.answer_markers が [] であること＋ Read で図が切れていない/テキスト消滅を目視。
#         答え語が残れば切り位置を深くして再実行（例 --top 0.15 → 0.30）。
#         さらに crop_warnings（生クロップの EDGE_CUT/STRAY_SLIVER・自動同梱）が空であること。
#         残る場合は隣接図の切れ端が残存 or 図本体を切りすぎ → 切り位置を見直す。
#         機械での再確認は: node scripts/check-figure-crop-integrity.mjs --file <NAME.png>（STRAY_SLIVER で exit 1）。
```

各図の切り位置は**人（またはエージェント）が図を見て決める**。自動 OCR 帯検出は図の凡例を誤認して切りすぎるため使わない（実証済み）。

## 切り位置の型（今セッションの実績）

| 型 | 症状 | 指定 |
|---|---|---|
| 上帯トリム | 図の**上**に答え/問題文（r01-a/h26-a 型） | `--top F`（F=テキスト帯の高さ割合） |
| 下帯トリム | 図の**下**に答え/表/【正解】（h30-a-fig-07/09/13 型） | `--bottom F`（F=残す上部の割合） |
| 中央帯 | 上にヘッダ＋下に【正解】/次問題（h30-a-fig-05 型） | `--band Y0 Y1`（図の帯だけ残す） |

## 完了処理（ページ単位）

```bash
# webp は figure-recrop.mjs が自動再生成済み。MDX width/height も更新済み。
node .claude/scripts/audit-exam-figures.mjs        # broken_image_reference:0 を確認
grep -c "�" <article.mdx>                          # 文字化け 0
git add <article.mdx> <img/変更した png/webp を明示>   # git add -A 禁止・並行セッション注意
git commit -m "content(<slug>): 過去問図の写り込みを再クロップで除去（fig-NN…）"
npm run audit-figures                              # 監査/provenance を最新化（`--list` の対象に反映）
```

## 鉄則（ハマりどころ）

- **触る前に必ず目視**。クリーンな図（数値ラベルのみ）を写り込みと誤判定して切らない。
- **図の凡例（「Uc≥10：粒度分布がよい。」等）は図の一部**＝残す。答え/本文だけ落とす。
- **MDX の width/height は新寸法に一致必須**（figure-recrop.mjs が `<img>`／`<ArticleImage>` 両方を自動更新。アスペクト比崩れ防止）。pe 系は `<ArticleImage>`＝旧版ツールは `mdx_updated:false` になったので手動更新した（2026-07-09 に両対応化済）。
- **二度切り厳禁**: figure-recrop.mjs は上書き適用。切り位置をやり直すときは**必ず元画像に戻してから**再適用する（既に切った画像に再度 --top を掛けると割合が二重に効いて切りすぎる）。civil-1 過去問図・pe 図は **webp のみ git 追跡**（png は untracked の一時生成物）→ 戻すのは `git checkout -- <webp>` だけ（png を pathspec に混ぜると "did not match" で checkout 全体が中断し戻らない、2026-07-09 実害）。
- **`--top` の割合が効かない/残る時は px 直指定**: テキスト最終行が図に近いと割合推定が外れる。原寸に px グリッド（`-draw "line 0,Y w,Y"`）を重ねて境界 px を読み、`magick -crop WxH+X+Y +repage -trim +repage -bordercolor white -border 12` で直接切ってから webp 化するのが確実（q35 で実施）。ツールは白 12px 枠を足すので出力高さ＝(crop高 − trim + 24)。
- **写真（グレー面）を含む図は figure-recrop.mjs の `-trim` が誤切りする**: 内部の `-trim` は白基準で外周を刈るため、グレーの写真が縁に接する図では**写真の上部/側部まで削られる**（2026-07-16 q8-fig の3枚写真帯で上部を誤切り実害）。写真帯を残す band クロップは figure-recrop を使わず **Pillow で明示 box crop（trim なし）**するのが確実: `python -c "from PIL import Image; im=Image.open(p).convert('RGB'); im.crop((0,Y0,W,Y1)).save(p,'WEBP',quality=82,method=6)"` → MDX の width/height を手動更新。行インク profile（`ink/W<0.01` を白行）で写真帯の Y0/Y1 を機械特定できる。
- **ImageMagick 前提（環境）**: figure-recrop.mjs は `magick`（ImageMagick）を PATH に要求。無い環境（新規 Windows 等）では `winget install ImageMagick.ImageMagick`（GitHub DL・admin 要）で導入、または上記 Pillow（`from PIL import Image`）で代替（crop/webp とも可・node_modules 不要）。Step① の `sips` は Mac 専用＝Windows は `magick <webp> x.png` か Pillow で png 化して Read。会社PCプロキシは GitHub DL は通るが winget の msstore ソースは証明書エラー→`--source winget` を明示。
- **periods は万能でない**: 化学構造式・図の点はOCRで句点として誤カウントされる（q42 で periods:10 だが写り込み無し）。残テキストの真偽は **必ず目視**で判定。図に残す凡例に句点があれば periods は0にならない（q-I2-5 の ● 凡例）→ その場合は再監査後 `manual_needs` の `needs:ok` で確定させる。
- **1 ページ 1 commit**・明示 pathspec（`git add -A` 禁止）。
- 見切れ/画質不足は本スキール対象外 → provenance の rescan / `manual_needs` へ。

## 大量処理（並列 workflow）モード

recrop-review が数十件ある時は、逐次 `figure-recrop.mjs` の代わりに**並列 workflow**で回す（2026-07-09 確立。civil-1 94→0＋他資格 48 図を計 4 本の workflow で処理）。**視覚判定はサブエージェント `figure-crop-worker`（Generator・sonnet）が各図で実行し、親（メイン）が全 crop 図を最終目視 QA してから MDX 寸法・台帳を直列適用する**。

**なぜ並列でも安全か**: PNG/webp は図ごとに別ファイル＝競合なし＝真に並列。**直列でないと壊れるのは 2 つだけ**＝①共有台帳 3 種（provenance/sources/text-audit）②同一記事の `article.mdx`（1 ファイルに複数図）。この 2 つは worker に触らせず親が直列で適用する。

### 手順

1. **worklist を作る**（`figure-provenance.json` の `needs=recrop-review` を対象）。各図 `{figKey, name, img(相対 .png|.webp), kind, imgSize:[w,h]}`。**除外**: `published:false` ドラフト（例 concrete-diagnostician＝著作権凍結）／機材写真 `.jpg`（OCR 偽陽性＝別途 `manual_needs:ok`）。webp-only 図も対象（worker が sharp extract で直接クロップ）。
2. **workflow 起動**: `Workflow({ scriptPath: ".claude/skills/quality/figure-recrop/scripts/figure-crop-batch.workflow.mjs", args: <worklist> })`。各図を `figure-crop-worker` が並列にクロップ→自己検証→`{action, cropBox, newWidth/Height, removed, reason, selfVerify}` を返す。
3. **機械ゲート → 目視 QA の順で絞る**。まず全 crop 図に `node scripts/check-figure-crop-integrity.mjs` を通し（STRAY_SLIVER 等を全数機械検出）、**目視（Read）は「機械が fail させた図」＋「worker の selfVerify が怪しい図」に集中**する。ただし機械が拾えない**切り過ぎ（画素欠損）**は目視でしか分からないため、`removed` が大きい図は fail していなくても確認する（下記「QA で捕捉した実例」）。needs-source は疑わしいものをスポット確認。
4. **MDX 寸法＋台帳を直列適用**（親）。crop 後の実寸を読み、記事ごとに `<img width/height>` を置換（`<ArticleImage>` は寸法属性なし＝更新不要）。`figure-sources.json` の `manual_needs` に crop→`ok`／ok→`ok`／needs-source→`rescan-need-source` を記録し、provenance/text-audit も同期。**MDX は `newline=''` で読み書き**して CRLF/LF を保存（混在を作らない）。
5. **commit（明示 pathspec・`git add -A` 禁止）** → 完了後 `figure-provenance.md` の census が陳腐化するので更新（SSOT）。

### QA で捕捉した実例（親目視ゲートの価値）

- **写り込み残り**: worker が上部プローズ／下部キャプションを残した（fig-2-55・fig-3-9）→ 親が該当帯を再クロップ。
- **フォーム切り過ぎ**: 台帳フォームの下部行を「脚注」と誤認して切った（fig-4-12）→ **原画を `git checkout HEAD -- <png> <webp>` で復元→正しい境界で再クロップ**（脚注が本体と横並びで矩形分離不能なら脚注ごと残す）。
- **見切れ見落とし**: worker が crop 判定したが原画も上端で入力ラベル/見出しを切っていた（q35-fig・fig05）→ **crop→needs-source に是正・原画復元**。判定は「原画（`git show HEAD:<path>`）の端インク」で確認する。
- **SVG 版使用の図**: 記事が `.svg` を参照し scanned `.png` は不使用のオーファン → MDX 参照が無い＝寸法更新不要（無害）。
- **無関係な未コミット削除**（別セッションの孤立画像 D）は巻き込まない（テリトリ不可侵）。

## 連携

- 対象選定＝`figure-provenance.json`（needs）／品質＝`figure-text-audit.json`。真実源 [figure-provenance.md](../../../../.claude/knowledge/reference/figure-provenance.md)。
- 機械化ヘルパ＝`scripts/figure-recrop.mjs`（逐次・crop+webp+MDX+OCR）／並列ワーカー＝`figure-crop-worker`（`scripts/figure-crop-batch.workflow.mjs` が spawn）。
- 別物＝`civil-figure-rework`（問題PDFから抽出・過去問では図なしで不成立）／`scanned-figure-crop-auditor`（スキャン教材の bbox 監査）。
- 大量処理時は本スキルの手順を `civil-exam-figure-auditor` 等の Evaluator で採点させながら回してもよい（Generator/Evaluator 分離）。
