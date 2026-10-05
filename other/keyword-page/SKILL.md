---
name: keyword-page
description: >
  総合技術監理キーワードページの作成・校正。既存の空ページを試験対策コンテンツとして仕上げる。
  Use when user asks to [キーワードページ作成, キーワード記事, keyword page, /keyword-page].
domain: site
---

## 用途

総合技術監理（CEM）キーワードページを新規作成または既存の空ページを仕上げるスキル。
総合技術監理キーワード集2026に基づき、試験対策として必要十分な概要ページを作成する。

**対象スコープ**: `group: keyword`（または group 未設定）のキーワードページのみ。`group: guide` の **ガイド記事は対象外**（受験戦略・学習計画・俯瞰ハブはコンバージョン地点として別構造）。ガイド記事の末尾構成・禁止セクションは [content-principles.md §20](../../../../.claude/knowledge/reference/content-principles.md) を参照。ガイド記事の生成・改善は `group: guide` 品質サイクル（`guide-rewriter`／`guide-qa`／`guide-fact-checker`）経由。

## 引数

| 引数 | 必須 | 説明 | 例 |
|---|---|---|---|
| slug | ○ | キーワードのslug（ディレクトリ名） | `business-continuity-plan` |
| mode | — | `create`（新規）/ `revise`（校正）。デフォルト: 自動判定 | `revise` |

## 実行手順

### Step 1: 対象ファイルの確認

1. `content/site/pe-comprehensive-management/{slug}/article.mdx` を読み込む
2. frontmatter の `section`, `category`, `tags`, `published` を確認
3. 本文が空または「（内容準備中）」のみかを判定 → `create` / `revise` を自動選択

### Step 2: 情報収集

1. **キーワード集の位置づけ**: `src/config/pe-chapters.json` から該当セクションの章・節タイトルを確認
2. **教材原典の参照**（散文構成のベンチマーク）: `content/sources/textbook/技術士（総監）/テキスト/総監標準テキスト/{該当章}.md` を読み、対象キーワードが教材でどのように説明されているかを確認する。教材は散文 60〜65%／表・箇条書き 30〜35% のバランス（content-principles.md §17）で書かれており、これを doboku-note のキーワードページの目標スタイルとする
3. **関連する過去問**: `content/site/pe-comprehensive-management/r*-primary/article.mdx` を Grep して、このキーワードのslugが `<RelatedKeywords>` で参照されている設問を特定
4. **関連キーワードページ**: 同一セクション内の他のキーワードページを確認（相互リンクの候補）
5. **参考資料の検索と検証**:
   - **必ず WebSearch から始める**。URLを推測して WebFetch で当てようとしてはならない
   - 検索クエリ例: `"{キーワード名} 解説 site:go.jp OR site:ac.jp OR site:or.jp"` や `"{キーワード名} 入門 公的機関"`
   - **参考資料の目的はキーワードの内容を理解するのに有用なリソースを提供すること**。試験の公式ページ（キーワード集ダウンロードページ等）は参考資料として不適切
   - 候補URLを WebFetch で実際にアクセスし、200応答かつ内容がキーワードの解説に有用であることを確認する。アクセスできないURL・内容が無関係なURLは候補から除外する

### Step 3: コンテンツ作成

以下のテンプレート構成に従って記事を作成する。**散文を主、表・箇条書き・コンポーネントは補足**（content-principles.md §17）が基本方針。各 H2/H3 セクションは最低 1 段落の散文導入から始める。

#### ページ構成テンプレート

```
# {キーワード名}

## {主要概念}とは
  - 概念の定義・対象範囲・基本的な仕組みを散文 2〜3 段落で説明（目安 200 字以上）
  - 1 段落で済ませない。表・箇条書きから始めない（§17 違反、lint 12-2 検知）
  - 試験での重要性や他管理分野との関連は「総合技術監理における位置づけ」に書く
  ※ ここに <ExamPoint> を置かない。概念を説明する前に試験ポイントを列挙しても読者には文脈がない
  ※ 表・箇条書きの直前に必ず導入文（その情報が何を意味するか）を置く
  ※ 「法律の概要」「基本情報」等のキーバリュー表を作らない。正式名称・目的・所管などは散文で冒頭に統合する（冒頭との情報重複を避ける）

### {サブテーマ1}
  - 散文 1 段落以上で導入してから、詳細説明・比較表・分類表を置く
  - 必要に応じて <Timeline> でプロセス・手順を表現
  - 節の末尾に、その節で扱った内容に限定した <ExamPoint> を配置してよい

### {サブテーマ2}
  - 散文 1 段落以上で導入してから、追加の詳細・関連概念との比較を置く
  - 節の末尾に <ExamPoint> を配置してよい

## 総合技術監理における位置づけ
  - キーワード集での章・節の位置（散文）
  - 複数セクションにまたがる場合はその横断性を説明（散文）
  - 5 管理トレードオフ視点（安全管理・経済性管理・人的資源管理・情報管理・社会環境管理のうち該当するもの）を散文で記述
  - **関連キーワードは本文の自然な流れの中にインラインで埋め込む**（例: 「〜は[推定・検定](/docs/pe-comprehensive-management-estimation-testing)の前提となる」）
  - **`<SeeAlso>` は本文中（関連トピックを言及した直後）に配置する**（content-principles.md §11/§18）。末尾に並べるのは反パターン（lint 12-3 検知）
  - **末尾に `関連キーワード: [A]、[B]、[C]` の列挙行を作らない** — 重複と文脈喪失の原因。`lint-mdx-mobile.mjs` の 8-1 ルールで機械検出される
  - 本文に溶け込ませにくいキーワードは関連性が弱い証拠なので、無理に含めない
  - `<RelatedKeywords>` コンポーネントは **文中のインラインリンクには使わない**（ブロックレベル UI のため）。**`## 参考資料` の直前に末尾標準パターンとして 1 個配置する**（§18）。インラインは Markdown リンク `[名前](/docs/...)` を使う
  - <ExamPoint> で記事全体の出題パターンを総括する（全体まとめとして最も自然な位置）

<RelatedKeywords items={[
  { label: "<関連キーワード名>", slug: "<bare-slug>" },
  // 標準は 5 件、bare slug を渡す（例: slug: "lifecycle-assessment"）
]} />

## 参考資料
  - 官公庁の公開資料へのリンク（箇条書き）
  - 官公庁 > 公的機関 > 学術資料の優先順で選定
```

> **重要**: 上の順序を守ること。`<RelatedKeywords>` は **必ず `## 参考資料` の前** に置く（§18）。逆順にすると Markdown リスト後の JSX を MDX が正しく解釈できず、コンポーネントが描画されないことがある（過去事例: eco-label / csr 等）

#### `<RelatedKeywords>` の API（必須準拠）

コンポーネント定義: `src/components/ui/RelatedKeywords/RelatedKeywords.tsx`

- **prop 名は `items`**（`keywords` ではない）。誤ると `items === undefined` でコンポーネント全体が描画されない
- **slug は bare（カテゴリ接頭辞を含めない）**。`lifecycle-assessment` のように渡す
  - コンポーネント側で `pe-comprehensive-management-` を補完する
  - 既知接頭辞（`pe-comprehensive-management-` / `civil-construction-1-`）を含めても auto-detect で動作するが、規約は bare slug
- 標準件数は 5 件（BCP・LCA・環境基本計画・ISO 14000 等のベンチマークページ準拠）

**❌ 禁止パターン**:

```mdx
<RelatedKeywords keywords={[ ... ]} />              {/* prop 名違い、無描画 */}
<RelatedKeywords items={[
  { label: "X", slug: "pe-comprehensive-management-x" },  {/* 接頭辞付き、規約違反 */}
  { label: "Y", href: "/docs/pe-comprehensive-management-y" },  {/* href は受け付けない */}
]} />
```

#### 末尾コンポーネントの配置原則（§18）

末尾に並べてよいのは `<ExamPoint>` + `<RelatedKeywords>` の **2 点のみ**。`<SeeAlso>` は本文中（関連トピック言及直後）に配置する。3 件以上の連続（SeeAlso + ExamPoint + RelatedKeywords が末尾に塊）は反パターン。

末尾が肥大化したら **本文の散文不足のサイン**。SeeAlso を本文中へ移動し、必要なら散文を厚くしてバランスを整える。

> **注**: `## 過去問での出題` セクションは本文に書かない。過去問MDX側の `<RelatedKeywords>` を真実源とし、`PastExamBacklinks` コンポーネントがキーワードページ下部に自動でカード表示する。手書きで追加すると重複し保守負担が発生する。

#### 文体ルール

- **1文1段落を基本とする**。文と文の間は空行で区切り、段落を分ける
- 長い段落はスマホで読みづらいため、意味の区切りで積極的に改行する
- Markdown の単純な改行は無視されるため、段落を分けるには必ず空行を入れること

#### モバイル視認性ルール

- **計算手順を表で表現しない**。番号付きリストで1行1ステップに記述する
  - 悪い例: `| 時間稼働率 | 420 / 460 | 91.3% |`
  - 良い例: `1. 時間稼働率 = 420 / 460 = **91.3%**`
- 3列以上の表を作る場合、各セルの文字数を15文字以内に保つ

#### 表の使用基準（Table Decision Framework）

表を使う前に以下を順に確認する:

1. **データは本当に2次元か？** — 行と列の両方に意味があり、行間で値を比較する場合のみ表を使う。各行が独立した項目の説明なら箇条書きを使う
2. **冒頭の情報と重複しないか？** — 正式名称・目的・所管等を表にしない。散文として冒頭に統合する
3. **列数は3以下か？** — 4列以上は原則禁止。比較として不可欠な場合のみ、各セル15文字以内
4. **各行を箇条書きで表現できるか？** — `- **用語**: 説明` で自然に読めるなら箇条書きを使う

#### 表の代替パターン

| 元のパターン | 代替 |
|---|---|
| キーバリュー表（項目/内容） | 冒頭の散文に統合 |
| 用語＋説明（各行独立） | `- **用語**: 説明` の箇条書き |
| 計算手順 | 番号付きリスト |
| 時系列・プロセス | `<Timeline>` |
| 比較（A vs B） | 表のまま維持（2-3列、短いセル） |

#### コンポーネント使用ガイドライン

| コンポーネント | 用途 | 使用基準 |
|---|---|---|
| `<ExamPoint>` | 試験対策ポイント | **詳細ルールは `.claude/knowledge/reference/content-principles.md` §5 を参照**（個数は原則1個・最大2個、3個以上禁止、総括位置必須、「誤り選択肢パターン」など過去問解説に属する内容は禁止） |
| `<Timeline>` | プロセス・手順 | 順序が重要なステップがある場合。`time` は省略してシンプルに |
| 表（Markdown table） | **2軸の比較のみ** | 2次元で比較する場合のみ。定義・説明リストには使わない。4列以上は原則禁止。セル15文字以内 |
| `<Callout>` | 注意・補足 | 誤解しやすいポイントや重要な注意事項がある場合のみ |
| `<CustomUnorderedList>` | スタイル付きリスト | 通常のMarkdownリストで十分な場合は使わない |

#### 内部リンク・法令リンクの設置ルール

本文中で法令名や他のキーワード概念に言及する場合、対応するリンクを設置する。

**法令名への言及**:
- 法令名が出たら `content/site/pe-comprehensive-management/` に該当キーワードページが存在するか確認し、存在すれば内部リンクを設置する
  - 例: `[災害対策基本法](/docs/pe-comprehensive-management-disaster-countermeasures-act)`
- 条文番号まで言及する場合は e-Gov 法令検索の該当条文へのアンカーリンクも設置する
  - URL形式: `https://laws.e-gov.go.jp/law/{法令番号}#Mp-At_{条番号}`
  - 例: `[**消防法第8条**](https://laws.e-gov.go.jp/law/323AC1000000186#Mp-At_8)`
  - 法令番号は e-Gov 法令検索で対象法令を検索して確認する
- MDX では `**[text](url)**` が正しくパースされないため、太字はリンクテキストの内側に置く: `[**text**](url)`

**他キーワード概念への言及**:
- BCP、PDCA、リスクアセスメント等の概念を本文で言及する場合、対応するキーワードページが存在するか確認する
  - 確認方法: `ls content/site/pe-comprehensive-management/{想定slug}/article.mdx`
- 存在すれば初出箇所に内部リンクを設置する
  - 例: `[BCP（事業継続計画）](/docs/pe-comprehensive-management-business-continuity-plan)`
- 同一ページ内での 2 回目以降の言及にはリンク不要（過剰リンクを避ける）
- `<RelatedKeywords>` にも関連概念を含める（本文のインラインリンクと補完関係）

#### 参考資料の記載ルール

**詳細ルールは `.claude/knowledge/reference/content-principles.md` §9「参考資料の構成」を参照**（公的資料＋民間記事 各最低1件、WebSearch→WebFetch検証必須、e-Gov法令リンク形式）。

要点のみ：
- 公的資料 **最低1件** ＋ 民間解説記事（Wikipedia/note/技術ブログ等）**最低1件** が必須
- URL は WebSearch→WebFetch で実在確認後に記載。推測禁止
- 試験公式ページ（キーワード集DLページ等）は参考資料として不適切

### Step 4: frontmatter の確認・補完

以下の必須項目が揃っているか確認し、不足があれば補完する。

```yaml
---
title: "{キーワード名}"
seoTitle: "{キーワード名} ｜ 総合技術監理 キーワード集 2026"
description: "{50〜100文字の説明}"
category: pe-comprehensive-management
section: "{X.Y}"
tags:
  - keyword
published: true
publishedAt: "{YYYY-MM-DD}"
---
```

- `title`: 表示用の概念名のみ（サフィックスなし）
- `seoTitle`: `<title>` タグに出力する完全な SEO タイトル（必須）

- `section` が未設定の場合、`src/config/pe-chapters.json` を参照して付与
- `description` は検索結果に表示されるため、キーワードの定義を簡潔にまとめる

### Step 5: 品質チェック（2段階ゲート）

**Generator/Evaluator 分離原則**: keyword-page スキル自身は Generator。完成判定は **機械リンター（Step 5a）** と **cem-qa エージェント（Step 5b）** の2段階ゲートで行う。両方を通過しないと完了とみなさない。

#### Step 5a: 機械リンター（必須）

1. **文字化け検出**: Grep で `U+FFFD`（`�`）を検索し、文字化けがないことを確認
2. **リンク確認**: 過去問リンクのアンカー形式が正しいか確認（`#ⅰ-1-1` 等、小文字ローマ数字）
3. **section 整合性**: frontmatter の `section` と「総合技術監理における位置づけ」の記述が一致しているか
4. **lint-mdx-mobile 実行**: `node .claude/scripts/lint-mdx-mobile.mjs <file>` を実行
   - カテゴリ1（表）・6（導入文）・8（リンク）・**9（コンポーネント原則）** をチェック
   - HIGH/MEDIUM 違反があれば修正 → 再実行 → **ゼロまでループ**
   - 9-1（ExamPoint 3個以上）・9-3（誤り選択肢パターン）・9-6（過去問判定記号）は HIGH なのでブロッカー
5. **`/review-mobile` プロンプトチェック**: 機械判定できないカテゴリ 2（解説の簡潔性）・4（段落構成）・5（コンポーネント）・**10（SVG 追加候補）** を Claude の目視判定で実施
   - HIGH/MEDIUM ゼロまでループ
   - LOW（カテゴリ 10 の SVG 候補を含む）はユーザーに提示して判断を仰ぐ。自動修正はしない
   - SVG 化が選ばれた場合は別途 `/illustrate-concept {path}` を起動する運用

#### Step 5b: cem-qa エージェント評価（必須）

1. `cem-qa` エージェントを呼び出し、対象 slug または mdx パスを渡す
2. 5軸ルーブリック（構造30% / モバイル25% / 原則20% / 参考資料15% / 関連付け10%）で採点
3. **加重スコア < 2.0 なら指摘事項リストに沿って修正 → Step 5a に戻る**
4. **加重スコア ≥ 2.0 で完了**
5. いずれかの軸が 0 点なら即不合格
6. 参考資料軸の合格には `.claude/knowledge/reference/content-principles.md` §9 準拠（公的＋民間 各1件以上）が必要

## 品質基準

| 観点 | 基準 |
|---|---|
| 正確性 | キーワード集の定義に忠実。独自解釈や推測を含めない |
| 網羅性 | 試験で問われる範囲をカバー（過剰な詳細は不要） |
| 構造 | テンプレートの構成順序に従う |
| コンポーネント | 適切な場面でのみ使用。装飾のための多用は避ける |
| 参考資料 | キーワードの学習に有用なリンクを1件以上含む。公的資料と民間解説記事の両方を載せる。組織トップページではなく解説コンテンツへリンクする |
| 過去問リンク | Step 2 で特定した過去問は `<RelatedKeywords>` 側で紐付け（自動バックリンクカードに委ねる）。**本文に `## 過去問での出題` を手書きしない** |
| 導入文 | 表・箇条書き・コンポーネントの前に1〜2文の文脈説明があるか |
| 関連リンク配置 | 本文中にインラインで埋め込む。末尾に `関連キーワード: ...` の列挙行を作らない |
| モバイル視認性 | `/review-mobile` で HIGH/MEDIUM 違反ゼロ（`.claude/scripts/lint-mdx-mobile.mjs` が裏で走る） |

## コンテンツ変更後のインデックス再生成

開発中にキーワードページを作成・改訂した後は `npm run refresh-indexes` で静的インデックスを更新すること（本番 `npm run build` では自動）。詳細は `.claude/knowledge/reference/workflows.md`「コンテンツ変更後の静的インデックス再生成」を参照。

## 参照

- `.claude/knowledge/reference/content-principles.md` — ペルソナ定義、コンテンツ原則（7項目）
- `.claude/knowledge/reference/content-authoring.md` — MDX 作成詳細ルール、MDXコンポーネント一覧
- `src/config/pe-chapters.json` — 章・節構造
- `.claude/skills/conversion/pdf-to-mdx/templates/cem.md` — 過去問MDXの構造ルール（RelatedKeywords の仕様）
- `.claude/skills/quality/check-mdx/SKILL.md` — MDX 検査統合スキル（`--rules syntax` で作成後に実行推奨）
