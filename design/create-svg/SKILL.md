---
name: create-svg
description: >
  MDX記事に埋め込むSVG図版を作成する。モバイル視認性を最優先にした
  デザイントークン・レイアウトパターン・viewBox制約を適用。
  Use when user asks to [SVGを作成, 図を作成, フロー図を作成, /create-svg].
domain: site
---

## 用途

MDX 記事に埋め込む SVG 図版（フロー図・比較図・マトリクス・カード等）を作成する。モバイル（375px 幅）での視認性を最優先に設計する。

## 事前チェック（省略禁止）

**既存記事で raw `<img>` を見ても真似しない**。既存の `<img>` は移行未完了の遺物であり、新規追加では必ず `<ArticleImage>` を使う。理由:

- MDX パイプラインは raw `<img>` の `style` / `width` / `height` / `className` 属性を**すべて剥がす**（sanitizer 仕様）
- SVG ファイル内部の `style="width:100%"` も `<img src>` 経由では効かない（ブラウザの replaced element 扱い）
- `<ArticleImage>` は SVG 用に `w-full max-w-2xl mx-auto` コンテナと `max-width:100%;height:auto` inline style を自動付与しレスポンシブ表示する

**コミット前に `/check-mdx --rules svg` を必ず走らせる**。Step 3.5 で詳細。過去事例: raw `<img>` + `style="width:100%"`（`max-width:{viewBox}px` 欠落）で commit 後、ブラウザで SVG が固定サイズ表示される問題が発生し再リライト（PR #43）。スキルに書いてあったルールを守っていれば起きなかった。

## 図と文章の役割分担（必読）

SVG は**全体の流れ・構造を一目で把握させる**ためのもの。詳細な説明は本文（H2/H3 + 箇条書き）に任せる。

- **図に入れるもの**: 要素の名称、フェーズ名、期間、到達目標の1行要約
- **図に入れないもの**: 具体的なタスク・手順・箇条書き・補足説明
- **判断基準**: 直下の本文と情報が重複するなら、図から削る
- **SVG が不要なケース**: 分岐構造が見出し（H3）で十分に表現できている場合はSVGを作らない（例: 不合格要因別の対策は見出しで分岐すれば足りる）

## 引数

```
/create-svg <対象記事のパス> <図の内容の説明>
```

| 引数 | 必須 | 説明 |
|------|------|------|
| 対象記事のパス | 任意 | SVG を配置する記事の MDX パス。省略時はカレントディレクトリ |
| 図の内容の説明 | 任意 | 何を図にするかの自然言語説明。省略時は対話で確認 |

## モバイル視認性ルール（必須）

### viewBox 制約

> [!important] 記事＋SNS 両用の図（`figure-N.svg`）は固定キャンバス必須
> SNS（記事・Instagram）にも使う図は **viewBox を `400 500`（4:5・feed）に固定**する（高さ可変は不可）。
> YouTube 用の横長は別ファイル `figure-N--wide.svg`（viewBox `640 360`・16:9・記事非埋込）として作る。
> 真実源 → [figure-canvas-policy.md](../../../../.claude/knowledge/reference/figure-canvas-policy.md) / `config/figure-canvas.json`。
> ガード `npm run check-figure-canvas` が逸脱を pre-commit で止める。縦の余白は要素拡大・サマリー・凡例で埋めて使い切る。
>
> **Stories / Reels 流用**: 4:5（400×500）で作った figure-*.svg は、9:16 キャンバス中央に配置するだけで IG Stories / Reels の静止画スライドとして使える（SVG 修正不要）。配置ルール → [sns-image-policy.md §13](../../../../.claude/knowledge/reference/sns-image-policy.md)。
>
> 以下の「横幅 ≤400・高さ可変」ルールは **SNS に使わない記事専用の図**にのみ適用する。

- 横幅: **400px 以下**（モバイル 375px での縮小率 93% を確保）
- 縦幅: 制限なし（縦スクロールは自然）
- 横長レイアウトが不可避な場合のみ **500px** まで許容（理由をコメントで明記）

### 最大表示幅の固定（PC でのテキスト巨大化防止・必須）

**SVG ルート要素に `style="max-width:{viewBox の横幅}px;width:100%"` を必ず付与する。**

```xml
<svg viewBox="0 0 380 520" style="max-width:380px;width:100%" ...>
```

理由: `<ArticleImage>` ラッパーは `max-w-2xl`（約 672px）のコンテナに SVG を配置し `width:100%` で表示する。`max-width` 指定がないと viewBox 幅より大きくレンダリングされ、テキスト・図形が**PC 上で 1.5〜1.8 倍に拡大**されて巨大化する（モバイルでは同問題は起きない）。

設計の前提: **viewBox の寸法 = 画面上の最大表示寸法**。SVG 内で `font-size="13px"` と書けば、PC では 13px として表示され、モバイルでは自然縮小（例: 375/380 ≈ 0.99×）で 12.9px になる。最小表示サイズはこの縮小後の値を基準に、下記「フォントサイズ」の最小値を守ればよい。

### フォントサイズ

| 用途 | 最小値 | 推奨値 |
|---|---|---|
| 見出し・タイトル | 14px | 15-16px |
| 本文テキスト | 13px | 13-14px |
| 補足・キャプション | 11px | 11-12px |
| ラベル（STEP 等） | 11px | 11px |

最小値はモバイル縮小後（viewBox=400、画面幅=375 → 縮小率 0.94）の画面上 px を基準とする。viewBox 幅を 400px 以下に保ち、max-width を viewBox と同値に固定していれば、**最大表示サイズは SVG 内 font-size と一致**する。

### レイアウト原則

- 横並びは **最大 2 カラム**（3 カラム以上は縦に積む）
- 3 要素以上のフローは **縦積み**
- 矩形の最小幅は **160px**、最小高さは **50px**
- 要素間の余白は **最低 15px**

## デザイントークン

### カラーパレット（UI・SVG 共通の単一真実源）

サイト全体のセマンティックカラートークンは `src/styles/globals.css` の CSS 変数と Tailwind の `brand` / `ink` / `positive` / `warn` / `danger` に統一されている。**SVG でも同じ値を使う**ことで UI と図版のブランド一貫性を保つ。

| セマンティック | 意味 | 背景（fill） | ストローク | テキスト |
|---|---|---|---|---|
| `brand`（青系） | 情報・基本 | `#e8f0fe` | `#2e6da4` | `#1a3a5c` |
| `positive`（緑系） | 完了・成功・肯定 | `#d0e8d0` | `#3a7d44` | `#1a3a5c` |
| `warn`（黄系） | 注意・強調 | `#fff3cd` | `#d4a017` | `#1a3a5c` |
| `danger`（赤系） | 警告・重要・否定 | `#f8d7da` | `#b22234` | `#1a3a5c` |

| 用途 | 値 | Tailwind トークン |
|---|---|---|
| 本線・見出し | `#222` | `ink-strong` |
| 本文・補助線 | `#555` | `ink-body` |
| ラベル・注釈・弱い補助 | `#8a8a8a` | `ink-muted` |
| 区切り線・枠線 | `#d7d7d7` | `token-border` |
| 弱背景 | `#f5f5f5` | `surface` |

**SVG ファイル内の色指定ルール**:

1. 上記のリテラル hex を使う（`<img src>` 配信のため CSS 変数は効かない）
2. 必ずコメントで対応する semantic トークン名を併記する:
   ```xml
   <rect fill="#e8f0fe" stroke="#2e6da4" />  <!-- brand-fill / brand -->
   <text fill="#222">見出し</text>  <!-- ink-strong -->
   ```
3. **サイトの特色を出すため、パレット外の色は使わない**（既存 197 色のドリフトを再発させない）
4. 原典画像の色を再現するより、**セマンティックに最も近いトークンを選ぶ**（赤が安全を示すなら `danger`、工程完了なら `positive`）

### コントラスト比（WCAG 2.1 AA 準拠）

`.claude/knowledge/design-system/design-system.md` に従い、**テキストと背景のコントラスト比は 4.5:1 以上**を必須とする。

- **濃色背景は使用しない**。すべてのボックスは上記の淡色 fill（`brand-fill` / `positive-fill` / `warn-fill` / `danger-fill`）を使う
- テキストは `#1a3a5c`（見出し）または `#555`（本文）
- `ink-muted`（`#8a8a8a`）は背景が白または淡色の場合のみ使用可

### タイポグラフィ

**font-family は必ず明示指定する**（未指定だとブラウザのデフォルト serif に落ちて本文と不整合になる）。本文は Inter + Noto Sans JP のため、SVG も同じチェーンを揃える:

```xml
<style>
  text { font-family: Inter, "Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif; fill: #222; }
</style>
```

- font-weight: **bold**（見出し・ボックスタイトル）、**normal**（本文・補足）
- font-size: 本文 13px、ラベル 12px、見出し 14px、補足 11px（最小）

### 推奨テンプレート（defs + class 方式）

インラインで色を書くと保守が難しい。**`<defs><style>` に class を定義し、`<rect class="...">` で参照する**:

```xml
<svg width="400" height="260" viewBox="0 0 400 260"
     xmlns="http://www.w3.org/2000/svg"
     style="max-width:400px;width:100%"
     role="img"
     aria-label="[図の目的を 40-80 字で]">
  <defs>
    <style>
      text { font-family: Inter, "Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif; }
      .t-title { font-size: 14px; font-weight: bold; fill: #222; }  /* ink-strong */
      .t-label { font-size: 12px; fill: #555; }                     /* ink-body */
      .t-text  { font-size: 13px; fill: #222; }                     /* ink-strong */
      .box-brand    { fill: #e8f0fe; stroke: #2e6da4; stroke-width: 1.5; }
      .box-positive { fill: #d0e8d0; stroke: #3a7d44; stroke-width: 1.5; }
      .box-warn     { fill: #fff3cd; stroke: #d4a017; stroke-width: 1.5; }
      .box-danger   { fill: #f8d7da; stroke: #b22234; stroke-width: 1.5; }
      .box-surface  { fill: #f5f5f5; stroke: #d7d7d7; stroke-width: 1.5; }
    </style>
    <marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0,0 8,3 0,6" fill="#2e6da4"/>
    </marker>
  </defs>

  <!-- 本体 -->
  <rect class="box-brand" x="20" y="20" width="180" height="60" rx="6"/>
  <text class="t-title" x="110" y="55" text-anchor="middle">見出し</text>
</svg>
```

### 禁止事項

- **濃色背景 + 白/薄色文字の組合せ**（例: `<rect fill="#444"/><text fill="white">`）は `design-system.md §8` 違反。淡色 bg（`box-brand` 等）+ 濃色文字（`t-title` / `t-text`）を使う
- **svg-tokens.json の colorsAllowList 外の hex 使用禁止**（サイト特色の維持）
- **font-family 未指定禁止**（ブラウザデフォルト serif で描画され本文と不整合）

### 形状

- 角丸矩形: `rx="8"`（メインボックス）、`rx="6"`（サブボックス）
- ストローク幅: `1.5`（標準）、`1`（区切り線）
- 矢印マーカー定義:

```xml
<defs>
  <marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0,0 8,3 0,6" fill="#2e6da4"/>
  </marker>
</defs>
```

### 必須属性

- SVG ルート要素に `role="img"` + `aria-label="..."` を付与
- SVG ルート要素に **`style="max-width:{viewBox width}px;width:100%"`** を付与（PC で viewBox 幅を超えた拡大表示を防ぐ。詳細は「最大表示幅の固定」節）
- `<style>` ブロックでフォント定義を共通化

## レイアウトパターン

### パターン 1: 縦フロー（3 要素以上のプロセス）

`viewBox="0 0 380 N"`（N = 要素数 × 110 + 余白 40）

要素を縦に並べ、矢印で接続。各要素は幅 350px、左右余白 15px。
適用例: ワークフロー、手順、PDCA サイクル。

### パターン 2: 横 2 カラム比較

`viewBox="0 0 400 N"`

左右に 2 つのボックスを並べて比較。各カラム幅 180px、間隔 20px、左右余白 10px。
適用例: 一般部門 vs 総監、Before/After。

### パターン 3: マトリクス・表

`viewBox="0 0 400 N"`

セル幅は均等分割。ヘッダー行は濃色背景 + 白文字。
適用例: トレードオフマトリクス、評価表。

### パターン 4: カード縦並び（フェーズ・ステップ）

`viewBox="0 0 380 N"`（N = カード数 × 200 + 余白）

カードを縦に積み、各カードにヘッダー帯（色付き）+ 本文 + 到達目標を含む。
カード間に矢印を配置。
適用例: 学習計画、プロジェクトフェーズ。

## 実行手順

### Step 1: 要件の確認

1. 対象記事のパスと図の目的を確認
2. 図に含める情報を整理（テキスト量が多すぎないか確認）
3. レイアウトパターン（上記 4 種）のどれが適切か判断
4. 同じ記事の `img/` に既存 SVG があれば命名規則（`figure-{N}.svg`）を確認

### Step 2: SVG 作成

1. viewBox を 400px 以下で設定
2. デザイントークンを適用（カラー・フォント・形状）
3. モバイル視認性ルールを遵守
4. `content/site/{slug}/img/` に `figure-{N}.svg` として保存

### Step 3: 目視チェック（機械が判定できないものだけ）

**寸法・属性・フォント・はみ出しは Step 3.5 の `audit.mjs` が機械判定する**（viewBox 幅・`style="max-width"`・font-size 下限・`role`/`aria-label`・`font-family`・テキストクリップ・重なり）。ここで目視するのは機械に見えない意味の問題だけ:

- [ ] **濃色背景を使用していない**（淡色背景のみ。IG 用の navy 帯とは別基準）
- [ ] **制作メモを SVG 内に書かない** — 「※ 原図を概念図として再構成」「※ 本図はイメージです」等のメタコメントは不要。説明は alt 属性・本文で行う。SVG はコンテンツそのものに徹する
- [ ] **原典の図番号参照（図 N.N）を SVG 内に書かない** — SVG 内のタイトルや補足に「図 7.6」のような PDF 表記を残さない（目次・SEO を汚染しない）
- [ ] **横並び要素 ≤ 2 カラム**（情報密度の判断）

### Step 3.5: 自動監査（必須・pre-commit で機械的に強制）

**pre-commit フック**（`scripts/pre-commit-mdx.mjs`）が staged の `content/site/**/img/*.svg` に対して `auditSvgFile` を自動実行し、**HIGH 検出でコミットをブロック**する。MEDIUM/LOW は warning として表示（ブロックしない）。

手動で事前確認したい場合:

```bash
# 単一ファイル（fail-on=HIGH で exit 1）
node .claude/skills/quality/check-mdx/scripts/rules/svg/audit.mjs --file=<作成した .svg> --fail-on=HIGH

# プロジェクト全体
node .claude/skills/quality/check-mdx/scripts/rules/svg/audit.mjs --severity=HIGH
```

検出対象: 文字クリップ（P1）・必須属性欠落（P3: role / aria-label / max-width）・viewBox 超過（P5）・フォント過小（P4）等。詳細は `/check-mdx --rules svg`（`.claude/skills/quality/check-mdx/SKILL.md`）を参照。

### Step 4: MDX への配置

```mdx
<ArticleImage
  src="/posts/{slug}/img/figure-{N}.svg"
  alt="図の説明"
/>
```

**`caption` 属性は使用しない。** `.claude/knowledge/reference/content-principles.md` 「`<ArticleImage>` の caption は使わない」ルールに従い、`alt` のみ設定する。図の内容は本文で説明する。

### Step 5: コミット

記事への埋込と図版の監査後に `npm run build-svg-catalog` を実行し、`.claude/state/svg-catalog.json` も差分へ含める。追加した図の `embedded` と `fitStatus` を確認する。カタログは SNS へ再利用する図を探すための派生台帳なので、本文だけを更新して古い一覧を残さない。

作成完了後、即座にコミットする（CLAUDE.md「コンテンツ編集時のコミット運用」に準拠）。

## 参照

- `.claude/knowledge/design-system/design-system.md` — デザイン原則（コントラスト比 4.5:1 の根拠）
- `.claude/knowledge/design-system/design-system.md §8` — 禁止パターン（純黒禁止・ライトグレー禁止等）
- `.claude/knowledge/reference/content-authoring.md` — MDX コンポーネント・画像配信規約
- `.claude/knowledge/reference/content-principles.md` — コンテンツ品質ルールの真実源
