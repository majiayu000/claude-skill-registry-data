---
name: pdf-to-mdx
description: >
  PDF / 画像から MDX を生成する統合変換スキル。`--exam` フラグで試験別テンプレートを切替え、
  出力ディレクトリ構造・frontmatter スキーマ・カテゴリ推定・PDF 残骸除去を自動化する。
  `--scanned` でテキスト層なしスキャン書籍を視覚 OCR（pdfimages＋サブエージェント）で内部リファレンス .md ＋図に変換するモードも持つ。
  Use when user asks to [PDFをMDXに, PDF変換, 過去問取込, スキャン教材の文字起こし, 書籍OCR, 総監PDF変換, 1級土木PDF変換, /pdf-to-mdx, /pdf-to-mdx --scanned].
domain: material
---

PDF または画像ファイルから doboku-note 用 MDX を生成する統合スキル。**旧 `/pdf-to-mdx` / `/cem-pdf-to-mdx` / `/civil-construction-1-pdf-to-mdx` / `/clean-pdf-artifacts` を吸収**し、試験別の変換ルールを `templates/{exam}.md` に外出しして管理する。

## 引数

```
/pdf-to-mdx <pdf-path> --exam {general|cem|civil-construction-1|civil-construction-2} [--pages N-M] [--output-dir ...]
```

| 引数 | 必須 | 説明 |
|---|---|---|
| `pdf-path` | 必須 | PDF または画像ファイルのパス（ディレクトリ指定で一括処理） |
| `--exam` | 必須 | 試験ルールを指定。template 切替に使用 |
| `--pages` | 任意 | PDF のページ範囲（例: `1-50`）。省略時は全ページ |
| `--output-dir` | 任意 | MDX 出力先。省略時は `--exam` から自動推定 |
| `--skip-artifacts` | 任意 | PDF 残骸除去（重複ヘッダー・ページ番号等）をスキップ |
| `--scanned` | 任意 | **テキスト層なしスキャン書籍モード**。下記参照 |

## スキャン書籍モード（`--scanned`）

テキスト抽出ができないスキャン書籍（自炊した教材・参考書・基準書）を、**視覚 OCR で内部リファレンス Markdown（`content/sources/textbook/`）＋図**に変換する。通常モード（テキスト層 → 公開 MDX）とは抽出方式・出力先・図処理がすべて異なるため、**手順は別ファイルに分離**:

→ **`references/scanned-image-pipeline.md`** を参照。**着手前に、まず経路C（テキスト層の有無）を機械判定し、視覚OCRが要る本だけ1ページ目視で経路A/Bを判定**する:

- **経路A: pdfimages 見開き** — 見開き2ページが90°回転で格納されたスキャン。手順書 Step 1-7（bash。pdfimages 抽出→回転/分割→並列OCR→章分割→図クロップ。bash3.2/zsh/ディスク/破損ページの落とし穴も収録）。
- **経路B: PyMuPDF 単ページ** — 1 PDF ページ＝1 書籍ページ・正立。pdfimages/ImageMagick が無い環境（会社 Windows 等）でも可。再利用スクリプト一式 **`scripts/scanned/`**（`render_pages.py`→OCR Workflow `ocr_fanout.workflow.js`→**校正 Workflow `proofread.workflow.js`**→`concat_chapters.py`→`prep_figures.py`→図 locate Workflow `figure_bbox.workflow.js`→`crop_embed_figures.py --crop-only`→**図 audit/refine ループ**（`prep_audit_jobs.py`→`figure_crop_audit.workflow.js`→`apply_deltas_recrop.py` を反復）→`crop_embed_figures.py`→`trim_placeholders.py`。runbook = `scripts/scanned/README.md`）。解像度 2200px・図 bbox の候補窓＋groupSize 順次処理（レート制限回避）・確信度しきい値・冪等性の知見を織り込み済み。

- **経路C: テキスト層抽出（born-digital）** — 原本に使えるテキスト層があり、視覚OCRを1ページも回さずに全文が取れる本。**視覚OCRに着手する前に必ず判定する**（`scripts/text-layer/classify_text_layer.py`）。`book-manifest.json` の `renderProfile.mode` は**ページ画像の作り方**でテキスト層の有無ではないので、`born-digital` を「OCR不要」の根拠にしない（Kindle 画面取込などテキスト層の無い `born-digital` が多数ある）。構造は `pdftohtml -xml` の行頭/行末 x（版面の幾何）で決め、`-layout` の空白数は使わない。runbook = `scripts/text-layer/README.md`。

**着手前の必須チェック（経路A/B 共通）**: 自炊の手持ち撮影は指が写り込んで本文を隠す。視覚OCRは隠れた文字を文脈から埋め、出来上がった文が自然な日本語になるため**後段の校正では検出できない**。OCR に入る前に `scripts/occlusion/detect_occlusion.py` で候補を挙げ、本文が隠れている版面は撮り直しに回す。読めない箇所は 〔判読不能〕 と書き、埋めない。**候補率は「本文が隠れている率」ではない**（肌色の絵・余白を押さえる指・書影も候補に挙がる）。絞り込みに使い、要否は候補ページの目視で決める。実測の内訳は scripts/occlusion/README.md、スキャン結果は .claude/state/assets/reference-book-occlusion-scan.json。

- **経路D: 参考文献 bundle の視覚OCR** — `content/sources/books/` の bundle（Drive の `pages/pNNNN.jpg`）を、Sonnet 第1読（6p/体）→ Tesseract 第二読（無料）→ 一致率の低いページだけ Sonnet 第2読 → 48 ページ part へ連結 → `record-reference-book-artifacts` で Drive と台帳へ、の順で起こす。モデルが読むのは全ページ 1 回＋食い違ったページだけもう 1 回。runbook = `scripts/book-ocr/README.md`。マーカーは画像 id `<!-- p0001 -->`（印字ノンブルではない）。

ワーカー: 本文 OCR/校正 = サブエージェント `scanned-textbook-transcriber`（Generator・sonnet）／図 locate = `civil-exam-figure-extractor` と同型の Generator／**図クロップ品質監査 = `scanned-figure-crop-auditor`（Evaluator・sonnet。実クロップ PNG を4軸採点し `adjust_bbox` を返す。locate 単発では枠が緩く本文写り込み・切れが残るため必須）**。**市販書籍スキャンは内部リファレンス専用＝公開しない**（`content/sources/textbook/**/img` は r2-sync 対象外＝公開R2へ同期されない。README に明記）。文字起こしには `config/reference-sources.json` の ID を示す frontmatter を付け、`source-transcript` group で Drive に同期する。

## 利用可能な exam テンプレート

| exam | 用途 | テンプレート | 出力先 |
|---|---|---|---|
| `general` | 汎用変換（土木一般・施工管理・法律等） | `templates/general.md` | `content/site/{category}/` |
| `cem` | 技術士総合技術監理（論文・事例） | `templates/cem.md` | `content/site/pe-comprehensive-management/` |
| `civil-construction-1` | 1級土木施工管理（教科書・ガイド・基準類） | `templates/civil-construction-1.md` | `content/site/civil-construction-1/` |
| `civil-construction-2` | 2級土木施工管理（教科書・ガイド・基準類） | `templates/civil-construction-2.md` | `content/site/civil-construction-2/` |

新試験を追加する場合は `templates/{exam-id}.md` を新規作成するのみ（スキル本体は変更不要）。

## 共通変換ルール（全 exam 共通）

### Step 1: 入力ファイルの確認

- ファイルの存在確認・形式判定（PDF / PNG / JPG）
- PDF の場合はページ数を確認（大規模 PDF はサブエージェントに委任）
- ディレクトリ指定の場合は対象ファイル一覧を表示

### Step 2: テンプレート読み込み

```
.claude/skills/conversion/pdf-to-mdx/templates/{exam}.md
```

テンプレートから以下を取得:
- 出力ディレクトリ構造
- frontmatter スキーマ
- カテゴリ推定ロジック
- 試験固有の MDX コンポーネント使用規約
- 試験固有の post_hooks（例: `/check-mdx --rules all`）

### Step 3: テキスト抽出

- **PDF**: Read ツールの `pages` パラメータで 20 ページずつ読み取り
- **画像**: Read ツールで直接読み取り
- **大規模 PDF（20 ページ超）**: Agent tool でサブエージェントに委任。メインでは全体構造の把握のみ

### Step 4: コンテンツ分析

抽出テキストから以下を判定（テンプレート依存）:
1. **カテゴリの推定**: テンプレートのカテゴリマッピング表に従う
2. **コンテンツの構造**: 章・節・項の階層、数式・表・図の有無

### Step 5: MDX 変換（共通ルール）

#### 見出し
- 章 → `## 見出し`
- 節 → `### 見出し`
- 項 → `#### 見出し`
- `# H1 見出し` は使わない（frontmatter の `title` が自動的に h1 になる）

#### 数式（KaTeX）
- ブロック数式: `$$...$$`（開始・終了を**必ず別行**に配置）
- インライン数式: `$...$`
- 数式番号: `\tag{N}`
- `\text{}` を含む分数は `\dfrac{}{}`（CJK 縮小回避）

#### 表
- Markdown テーブル記法
- **4 列以上は原則禁止**。3 列以上は各セル 15 字以内
- キーバリュー表は作らない（散文化）

#### 箇条書き
- 元テキストの箇条書きはそのまま維持
- 冗長な箇条書きは自然な文章に変換

#### 絶対に変えないこと
- 原文の意味・内容
- 数値・数式の正確性
- 法律の条文番号・判例番号
- 技術用語

#### 変換時に行うこと
- 文字化け・OCR 誤認識の修正（文脈から推定）
- 全角/半角の統一（数字は半角、日本語は全角）
- 不要な改行・空白の除去

### Step 6: PDF 残骸の除去（旧 `/clean-pdf-artifacts` 吸収）

`--skip-artifacts` 指定がない限り、以下を自動検出・除去:

| 問題 | 検出 | 修正 |
|---|---|---|
| 重複ページヘッダー | 同一 `##` が 3 回以上 | 最初の出現のみ残し、以降を削除 |
| 壊れた見出し | `## 第N章 ` + 2〜4 文字の不完全な末尾 | 該当行を削除 |
| h1 見出しの混入 | `^# [^#]` | `# ` → `## ` |
| 孤立ページヘッダー | `^第N編$` のみの行 | 削除 |
| 表ヘッダー重複 | 同一ヘッダー行が近接 | 2 回目以降を削除 |

詳細アルゴリズムは [`references/clean-pdf-artifacts.md`](./references/clean-pdf-artifacts.md) を参照。

### Step 7: frontmatter の付与

テンプレートで定義された必須フィールドを埋める（`title`, `description`, `category`, `tags`, `published`, その他 exam 固有項目）。原本・一次資料を参照した記事は `sources` に `config/reference-sources.json` の ID を入れ、自由記述の書名は使わない。

### Step 8: ファイル保存

- テンプレートの出力パス規則に従う
- 既存ファイルがある場合は上書き確認
- CLAUDE.md §3「MDX 書き込みは `writeMdxFile` 経由」に従い、`.claude/scripts/lib/mdx-io.mjs` 経由で書き込み（CRLF 維持）

### Step 9: post_hooks の実行

テンプレートで定義された後処理を実行（例: `/check-mdx --rules all`）。

### Step 10: 静的インデックス再生成

```bash
npm run refresh-indexes
```

本番 `npm run build` では自動実行されるが、開発中は手動で実行。

## 画像の取り扱い（R2）

コンテンツ画像は Cloudflare R2 (`storage.doboku-note.com`) から配信。Git には含めない。

### 画像抽出パイプライン

PDF 内の図・写真・複雑な表を高品質 PNG として抽出する。**本文テキストの混入と図の切断を防ぐ**ことが最重要。

#### Step A: PDF ページを PNG 変換（300dpi）

```bash
pdftoppm -png -r 300 input.pdf /tmp/page
```

- **必ず 300dpi** を使用（150dpi では文字が潰れ、クロップ精度が下がる）

#### Step B: 図の位置特定

各ページの PNG を Read ツールで読み取り、以下を特定:
1. 図の存在有無と図番号（「図 X.X」「写真 X.X」）
2. 図の上端・下端・左端・右端のおおよそのピクセル座標
3. 周囲の本文テキスト回り込み
4. 複数図が同一ページにあるか

#### Step C: ImageMagick でクロップ

```bash
magick /tmp/page-03.png -crop 1500x1000+100+250 +repage fig-6-2.png
```

**テキスト回り込み対策（White-out 技法）**:
```bash
# 広めにクロップ後、テキスト部分を白塗り
magick raw.png -fill white -draw "rectangle 0,0 300,700" out.png
```

#### Step D: 抽出後の目視検証

| チェック項目 | OK | NG |
|---|---|---|
| 図の内容が完全か | 図全体が見える | 端が切れている |
| 本文テキスト | なし | 「...である。」等の文章が映り込み |
| 隣接図の混入 | なし | 別の図やキャプションが入っている |
| 解像度 | 文字が判読可能 | 文字が潰れている |

#### Step E: 画像配置

```
content/site/{category}/{slug}/img/fig-X-Y.png
```

MDX での参照は `<ArticleImage src="/posts/{category}/{slug}/img/fig-X-Y.png" alt="..." />`（raw `<img>` は禁止、`.claude/knowledge/reference/content-authoring.md` 参照）。

**過去問図の場合は caption / alt に注意**: 問題文に無い情報（構造説明、並列/直列、PDCA など）を絶対に書かない。受験者の判断材料を奪わない。詳細は [.claude/knowledge/reference/image-policy.md §過去問図の caption / alt](../../../knowledge/reference/image-policy.md#過去問図の-caption--alt--問題文に無い情報を絶対に追加しない) 参照。

#### Step F: R2 アップロード

```bash
node .claude/scripts/upload-images-to-r2.mjs --prefix {category}/{slug}
```

## 旧スキルからの移行

| 旧コマンド | 新コマンド |
|---|---|
| `/pdf-to-mdx <pdf>` | `/pdf-to-mdx <pdf> --exam general` |
| `/cem-pdf-to-mdx <pdf>` | `/pdf-to-mdx <pdf> --exam cem` |
| `/civil-construction-1-pdf-to-mdx <pdf>` | `/pdf-to-mdx <pdf> --exam civil-construction-1` |
| `/clean-pdf-artifacts <mdx>` | `/pdf-to-mdx` の Step 6 に吸収（自動実行）。単独実行は `references/clean-pdf-artifacts.md` の手順を直接適用 |

## 使い方の例

```bash
# 汎用変換（土木一般・法律等）
/pdf-to-mdx _sources/general/concrete.pdf --exam general

# 総監 論文・事例集
/pdf-to-mdx _sources/cem/case-studies.pdf --exam cem

# 1級土木 過去問・基準類
/pdf-to-mdx _sources/civil-construction-1/r07-primary.pdf --exam civil-construction-1 --pages 1-60

# ディレクトリ一括（exam 自動推定は未対応、明示必須）
/pdf-to-mdx _sources/civil-construction-1/ --exam civil-construction-1
```

## 関連スキル・エージェント

| 連携先 | 役割 |
|---|---|
| `/check-mdx --rules all` | 変換後の構文・frontmatter 検証（post_hook で自動実行） |
| `/improve-article --mode verify` | PDF 原典との 5 軸 QA 照合（旧 `/verify-pdf-mdx` / `/qa-pdf-mdx` を吸収） |
| `content-qa` / `cem-qa` / `civil-construction-qa` | 試験別の QA Evaluator（`/improve-article` 経由で自動振り分け） |
| `/exam-questions-import --exam {civil-primary\|civil-secondary}` | 過去問集の取込（PDF→MDX の特化版） |

## ハーネス設計上の位置づけ

- **Generator スキル** — PDF を読んで MDX を生成する
- **Evaluator は別**: 生成後の QA は `/improve-article --mode verify` が担当
- **テンプレート駆動**: 新試験追加時はスキル本体を変更せず、`templates/{exam}.md` を追加

## 参照

- `.claude/knowledge/reference/content-authoring.md` — MDX 作成詳細ルール
- `.claude/skills/conversion/pdf-to-mdx/templates/` — 試験別テンプレート
- `.claude/skills/conversion/pdf-to-mdx/references/clean-pdf-artifacts.md` — PDF 残骸除去詳細
- `.claude/skills/conversion/pdf-to-mdx/references/scanned-image-pipeline.md` — `--scanned` 手順書（経路A/B）
- `.claude/skills/conversion/pdf-to-mdx/scripts/scanned/` — 経路B（PyMuPDF 単ページ）再利用スクリプト一式＋runbook
- `.claude/skills/conversion/pdf-to-mdx/scripts/text-layer/` — 経路C（テキスト層抽出）判定スクリプト＋実装例＋runbook
- `.claude/skills/conversion/pdf-to-mdx/scripts/occlusion/` — 指の写り込み検出（OCR 着手前のゲート）
- `.claude/skills/conversion/pdf-to-mdx/scripts/book-ocr/` — 経路D（参考文献 bundle の視覚OCR）prep/fanout/tesseract/compare/proofread/concat ＋ runbook
- `.claude/scripts/lib/mdx-io.mjs` — CRLF 保持 I/O（必須）
