---
name: social-post
description: >
  既存 MDX コンテンツ（過去問・キーワード）を元に note.com / X（旧Twitter）向け投稿テキストを生成する統合スキル。
  note は analysis / guide / keywords / desumasu、X は question / keyword のタイプ別。
  Use when user asks to [note 記事, note ドラフト, X 投稿, ツイート生成, ですます化, /social-post].
domain: sns
---

# /social-post — note / X 投稿テキスト生成

doboku-note の既存コンテンツを活用して note.com / X 向けの投稿テキストを生成する統合スキル。旧 `/note-post` `/x-post` `/note-desumasu` を一本化。

## 使い方

```
/social-post note analysis                          # 過去問分析記事
/social-post note guide {テーマ}                    # 学習ガイド記事
/social-post note keywords {N}                      # キーワードまとめ記事
/social-post note desumasu {article-path}           # 既存 note 下書きをですます化
/social-post x question {slug} {問題番号} [--magazine]  # X 過去問投稿（140字）
/social-post x keyword {slug} [--long] [--magazine]    # X キーワード投稿（140字 / 280字）
```

## note 投稿タイプ

### 1. note analysis — 過去問分析記事

17 年分 680 問のデータを分析し、出題傾向を記事にする。

**データソース**: `content/site/pe-comprehensive-management/{h21..r07}-primary/article.mdx`
**分析内容**:
- 5 管理分野（経済性・人的資源・情報・安全・社会環境）の出題比率
- 毎年出る頻出テーマのランキング
- 年度別の出題傾向変化

**構成**:
1. リード文（総監択一式の概要、17 年分分析した旨）
2. 分析結果（表・グラフ代替のテキスト）
3. 管理分野別の傾向と対策ポイント
4. doboku-note への誘導リンク（全過去問の解答解説はこちら）

### 2. note guide — 学習ガイド記事

特定テーマの概要を解説し、詳細は doboku-note へ誘導。

**構成**:
1. テーマの重要性（なぜ試験で問われるか）
2. 基本概念の要約（doboku-note の既存キーワードページから抽出）
3. 過去の出題例（1〜2 問の要約、正答は伏せる）
4. 「詳しい解説と過去問演習はこちら→ doboku-note.com」

### 3. note keywords — キーワードまとめ記事

頻出キーワードを N 個紹介する記事。

**構成**:
1. 「まず覚えるべきキーワード N 選」のリード
2. 各キーワード: 名称 + 1〜2 文の説明 + 関連する管理分野
3. 各キーワードの末尾に doboku-note のリンク
4. まとめ（学習の進め方）

### note 投稿の共通ルール

- **ペルソナ**: doboku-note と同じ（実務経験 10 年以上の技術者）
- **文字数目安**: 無料記事 2,000〜3,000 字 / 有料記事 4,000〜6,000 字
- **マークダウン互換性（必須・実機検証済み 2026-04-29）**:
  - ✅ 動く: 見出し（`#`〜`###`）/ 太字（`**...**`）/ 番号なし箇条書き（`-`）/ 番号付き箇条書き（`1.`）/ インラインリンク（`[text](url)` — 平文中・括弧内連続いずれも OK）/ 画像（`![alt](path)`）/ 水平線（`---`）
  - ❌ 動かない（ペースト時点で壊れる、または無視される）:
    - **pipe 表**（`| ... | ... |`）→ 生のパイプ記号で表示される。比較・対応関係を出したくなったら **PNG 図版に置換**
    - **blockquote**（`>` で始まる行）→ 期待どおりの引用ブロックにならない。特に `>` の中に箇条書きをネストすると確実に崩れる。「この記事でわかること」型のサマリーは **太字見出し + プレーン箇条書き** で書く。引用装飾は note エディタの引用機能（Cmd+Shift+9）をユーザーが後付け
    - **KaTeX 数式**（`$...$` / `$$...$$`）→ 数式は使わない。必要なら画像化
    - **Mermaid 図**（` ```mermaid ` ）→ コードブロックの生テキストとして表示される。図解は SVG→PNG で
- **マークダウン表は PNG に置換**: 上記ルール適用時の実装パターン — `scripts/render-figure-{slug}.mjs` のような記事専用 SVG→PNG レンダラを 1 本書き（`sharp(Buffer.from(svg)).png().toFile(...)`）、`content/note/{slug}/img/figure-{slug}.png` に出力。色は `scripts/generate-note-covers.mjs` の `BRAND` / `BRAND_FILL` / `INK_*` 定数を流用。先行例: `scripts/render-figure-soukan-analysis.mjs`（総監択一式17年分分析）
- **画像指示**: 本文中に図版を入れる位置には `![alt](./img/figure-{slug}.png)` で参照を書く。生成前のドラフト段階では `[画像: ○○の図を挿入]` プレースホルダで OK。**画像は note エディタに別途ドラッグ&ドロップで配置する**（markdown の `![](path)` 記法ではローカルパスが解決されない）
- **キーワード内部リンク（全占有方針）**: doboku-note にキーワードページがある用語は本文中に `[キーワード](https://doboku-note.com/exam/pe-comprehensive-management/keywords/{slug})` 形式で **インラインリンク** を仕込む。実機検証で動作確認済（平文中・括弧内連続・bullet 内の太字いずれも note でハイパーリンク化される 2026-04-29）。**note 記事は doboku-note への導線が主目的**なので、リンクは出し惜しみしない。ルール:
  - **同一キーワードの全 occurrence をリンク化**（「初出のみ」は採らない。読者がどこからクリックしても遷移できる方が導線として強い）。同一目標 URL に複数回リンクが付くのは OK
  - **markdown 見出し（`#`〜`###`）は除外**。ただし bullet list の太字キャプション（`- **キーワード** — 説明`）や本文段落内の太字（`**foo**`）は **リンク化 OK**
  - **「同義語が連続して出てくる場合」は連続リンクを避ける**: `BCP・事業継続計画` のように同一 URL を指す同義語が隣接する場合は、片方だけリンク化（視覚ノイズ防止）。`X理論 ↔ Y理論` のような 1 概念のペアも `[X理論 ↔ Y理論](url)` で 1 リンクにまとめる
  - **note 続編の cross-sell 行も対象**: 「note のおすすめ続編」セクションで列挙されたキーワードも、説明部の用語であればリンク化する（doboku-note の無料解説と note 続編の有料コンテンツは補完関係なので競合しない）
  - **リンク密度の実例**: 90 番ドラフト = 45 リンク / 32 ユニーク slug / 約 4,200 字。1 リンク / 約 100 字
  - **キーワード辞書のソース**: `content/site/pe-comprehensive-management/{slug}/article.mdx` の frontmatter `title` と slug 名。`published: true` のみ対象
  - **マッチ検出は手作業 or 半自動**で OK（650 ページの全文 grep は誤検出が多いため、生成時に「この記事に出るキーワードは何か」を意識的に拾う方が品質が高い）
- **リンク**: 本文中に 2〜3 箇所 + 末尾にまとめリンク
- **冒頭に「この記事でわかること」を 3 行で**（blockquote ではなく **太字 + プレーン箇条書き** で）
- **末尾に doboku-note の URL と簡単な紹介文**
- **正答番号は記事に含めてよい**（note は完結型コンテンツ、ただし全問は載せない）
- **誘導は自然に**。「宣伝」ではなく「詳しくはこちら」の形

### note 下書き生成・編集後の検証チェック

`content/note/{slug}/article.md` を新規作成 / 編集したら、以下を実行して破綻が無いことを確認する:

```bash
# 1. パイプ表が残っていないか（残っていたら note でレンダリングされない）
grep -nc '^|' content/note/{slug}/article.md   # 期待値: 0

# 2. 文字化け（U+FFFD）が混入していないか
grep -nP '\xef\xbf\xbd' content/note/{slug}/article.md   # 期待値: 該当なし

# 3. 画像参照が img/ 内のファイルと一致しているか
grep -n './img/' content/note/{slug}/article.md
ls content/note/{slug}/img/
```

`grep -nc '^|' = 0` を **生成スキル（analysis / guide / keywords）の出力後に必ず実行** すること。1 件でも残っていたら表を PNG 化する。

### 4. note desumasu — ですます調変換

`content/note/{slug}/article.md` の note 下書きを、親しみやすい ですます調 に変換する。v3 合格体験者ポジション戦略（運営者は総監合格済み）と note 媒体の特性（個人の体験・思考の共有が期待される）を踏まえ、「伴走者」トーンを演出する。

#### 適用判断

| コンテンツ | 文体 | 適用 |
|---|---|---|
| サイト本体の教科書・キーワード・過去問解説 | だ・である調 | 適用しない |
| note 下書き（有料販売予定の戦略・学習法）| ですます調 | **本タイプで変換** |
| note 下書きの企画書（00_企画立案 等）| — | 対象外 |

#### 変換ルール

**ですます化する対象**:
- 地の文（通常の段落）
- 箇条書きの説明文（項目自体は体言止めなら維持）
- H2/H3 配下の本文
- 締めの段落

**そのまま残す対象**:
- `# H1` タイトル
- 引用ブロック `> この記事でわかること` 内の体言止めリスト
- コード・URL・数値・英字・数式・年度表記（R07, H30 等）
- 体言止めで終わる箇条書き項目
- 引用ブロック内の専門用語の引用・条文
- 公式・定義（「A とは B である」が専門用語定義の場合は許容）

**変換パターン例**:

| before | after |
|---|---|
| 〜だ。 | 〜です。 |
| 〜である。 | 〜です。 |
| 〜だった。 | 〜でした。 |
| 〜なければならない。 | 〜する必要があります。 |
| 〜してはならない。 | 〜しない方がいいでしょう。 |
| 〜するべきだ。 | 〜するのが現実的です。／〜することをおすすめします。 |
| 〜することだ。 | 〜することです。 |
| 〜と考えた。 | 〜と考えました。 |
| 〜してほしい。 | 〜してみてください。 |
| 〜ではない。 | 〜ではありません。 |

**親しみやすさの表現**（多用すると冗長になるので 1 記事に 5〜10 箇所程度）:
- 〜していきましょう
- 〜してみてください
- 〜してみましょう
- 〜おすすめします
- 〜が現実的です
- 〜ではないでしょうか
- 〜と感じています（個人の経験を語る場面）

#### 作業手順

1. **Read**: 対象ファイルを読み込む
2. **Write で上書き**: 既存構造・見出し階層・箇条書き・改行構造は維持し、地の文のみ置換
3. **検証**:
   - `grep -cE "だ。|である。"` が 0 件（意図的引用を除く）
   - `grep -E "なければならない|してはならない"` が 0 件
   - `grep $'�'` が 0 件（文字化け U+FFFD 無し）
4. **例外の報告**: 意図的に残した箇所（条文引用・公式定義）があれば、完了報告で理由を明記

## X 投稿タイプ

> **正規パスの注記（2026-06-04 更新）**: 新規 X キャンペーンの執筆は **`x-post-writer` エージェント + 真実源 `.claude/knowledge/reference/x-post-policy.md`** が正規パス。本スキルの X セクションは旧式（補完・緊急用）。文字数（280 weighted）・タグ（総監は **`#技術士 #総監`**。`#技術士総監` は 2026-05-29 廃止）・投稿型（**切り口分割 angle-slice** = 結論/理由/体験/反論/数字/ハウツーの 6 投稿化 等）は policy §4・§5 を参照。**以下の旧フォーマット例のタグ（`#技術士総監`）は古い**ので policy のタグに置き換えて使う。

### 1. x question — 過去問投稿

**手順**:
1. 対象ファイル: `content/site/pe-comprehensive-management/{slug}/article.mdx`
2. 指定された問題番号の H2 見出しと問題文を読む
3. 以下のフォーマットで生成:

```
【総監 {年度} {設問番号}】
{問題のテーマを1文で要約。答えを明かさず興味を引く問いかけ}

正答・解説はこちら
https://doboku-note.com/exam/pe-comprehensive-management/past-exams/{slug}

#技術士 #技術士総監 #過去問対策
```

**`--magazine` 付きフォーマット**:
```
【総監 {年度} {設問番号}】
{問題のテーマを1文で要約。答えを明かさず興味を引く問いかけ}

正答・解説はこちら
https://doboku-note.com/exam/pe-comprehensive-management/past-exams/{slug}

5管理の論点まとめ → https://note.com/dobokunote/m/m607bf095b02a

#技術士 #技術士総監 #過去問対策
```

**ポイント**:
- 正答番号は投稿に含めない（サイトに来てもらうため）
- 問題文をそのまま貼らない（長すぎる）。テーマを要約して問いかけ形式にする
- 年度表記: `h30-primary` → `H30`, `r07-primary` → `R07`

### 2. x keyword — キーワード投稿

**手順**:
1. 対象ファイル: `content/site/pe-comprehensive-management/{slug}/article.mdx`
2. frontmatter の title と本文の冒頭セクションを読む
3. 以下のフォーマットで生成:

> **注**: 戦略 v6（2026-05-22）でキーワード解説の X 用要約は **廃止** 判定（IG/YT へ集約）。x keyword は緊急 / 補完用に残置するのみで、新規キャンペーンでは使わない。

**140 字版（デフォルト）**:
```
【総監キーワード】{タイトル}

{概念の本質を1〜2文で。試験での重要性に触れる}

https://doboku-note.com/exam/pe-comprehensive-management/keywords/{slug}

#技術士 #技術士総監
```

**280 字版（--long）**:
```
【総監キーワード】{タイトル}

{概念の本質を2〜3文で説明}

{試験での出題ポイントや関連する管理分野を1文}

詳しい解説・過去問での出題例はこちら
https://doboku-note.com/exam/pe-comprehensive-management/keywords/{slug}

#技術士 #技術士総監 #{該当管理}
```

**`--magazine` 付き（140字版・280字版いずれも適用）**:
サイトURL の直後に以下の行を追加する:
```
5管理の論点まとめ → https://note.com/dobokunote/m/m607bf095b02a
```

### X 投稿の共通ルール

- テキストをそのまま表示する（ユーザーがコピーして X に貼る想定）
- URL はフルパスで出力（X が og:image を自動取得してカード表示する）
- 文字数をカウントして表示: `(XXX文字 / 280文字)`
- **`--magazine` フラグ**:
  - サイト URL の直後に `5管理の論点まとめ → https://note.com/dobokunote/m/m607bf095b02a` を追加
  - X の URL は t.co 短縮で 23 文字固定カウントのため、2本目 URL の文字数圧迫は最小
  - 文字数カウントは URL 2 本ぶんを正確に反映する（各 URL = 23 文字として計算）
  - CTA テキスト（「5管理の論点まとめ」部分）は A/B テストで差し替え可能 → `content/sns/x/magazine-ab-test.md` 参照
- **禁止**:
  - 正答番号を投稿テキストに含めない
  - 問題文の全文を貼らない
  - 絵文字を使わない（ハッシュタグの # は除く）
  - 「いいね・RT お願いします」等のエンゲージメント乞いを入れない

### slug の省略記法

`pe-comprehensive-management-` プレフィックスは省略可能:
- `/social-post x question h30-primary 1` → `pe-comprehensive-management-h30-primary` として処理
- `/social-post x keyword business-continuity-plan` → `pe-comprehensive-management-business-continuity-plan` として処理

## サイト URL

- トップ: `https://doboku-note.com`
- カテゴリ: `https://doboku-note.com/exam/pe-comprehensive-management`
- 個別記事: `https://doboku-note.com/exam/pe-comprehensive-management/{種別}/{slug}`（種別＝keywords / past-exams / guide。旧 `/docs/...` は 301 なので使わない。対応表は `public/_redirects`）

## ハーネス設計上の位置づけ

- **Generator（model: sonnet）** — テキスト生成・変換は定型作業
- **別エージェント評価は不要** — note は人間チェックで公開前に推敲、X は短文で即投稿

## 旧スキルからの移行

- `/note-post analysis` → `/social-post note analysis`
- `/note-post guide {テーマ}` → `/social-post note guide {テーマ}`
- `/note-post keywords {N}` → `/social-post note keywords {N}`
- `/note-desumasu {path}` → `/social-post note desumasu {path}`
- `/x-post question {slug} {num}` → `/social-post x question {slug} {num}`
- `/x-post keyword {slug} [--long]` → `/social-post x keyword {slug} [--long]`
