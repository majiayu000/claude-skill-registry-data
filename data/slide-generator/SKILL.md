---
name: slide-generator
description: Generate professional HTML presentation slides from Markdown files or raw content. Use when creating presentations, slide decks, or when asked to make slides. Fully automated workflow - Markdown analysis → Layout selection → HTML generation → Thumbnail generation → Surge deployment. Supports 16 layouts, Chart.js graphs, and interactive features.
---

# スライド生成スキル

このスキルは、HTML、CSS、SVGロゴを使ったプレゼンテーションスライドを生成します。

## 重要: このスキルはエージェント専用です

このスキルは必ずTask toolのエージェント（subagent_type: general-purpose）経由で実行してください。

### なぜエージェント経由なのか

1. **コンテキストサイズが大きい**
   - Markdownファイルの解析
   - 全レイアウトの仕様確認
   - HTML生成とリソース管理
   - これらを直接実行するとコンテキストを大量に消費

2. **複数ステップの自動化**
   - Markdown作成 → HTML生成 → サムネイル生成 → デプロイまで一貫処理
   - エージェントが各ステップを自律的に実行

3. **対話的な情報収集**
   - 必要に応じてユーザーに画像やデータを要求
   - エージェントが適切なタイミングで確認

### 使い方

```bash
# 直接実行しない
Skill: slide-generator input.md

# エージェント経由で実行
Task(subagent_type: general-purpose): "slide-generator スキルを使って input.md からスライドを生成してデプロイまで完了させてください"
```

## 完全自動化ワークフロー

**ユーザーは内容を提供するだけ。それ以外は全自動で完了します。**

### 自動実行される全ステップ

1. **内容の分析**
   - ユーザーが提供した内容（テキスト、データ、コード等）を読み込み
   - 構成を解析して、スライド構成を理解

2. **レイアウトの自動判断と最適化提案**
   - 各セクションに最適なレイアウトを判断
   - グラフや画像が効果的な箇所を特定
   - **この段階でユーザーに確認**（後述）

3. **必要に応じてユーザーに追加情報を要求**
   - 画像が必要な場合: 「〇〇の画像を提供してください」
   - グラフデータが必要な場合: 「以下の形式でデータを提供してください」
   - ユーザーが「不要」と判断した場合: 代替レイアウトで進める

4. **スライド原稿の作成**
   - 分析結果を元に、スライド用のMarkdownを自動生成
   - frontmatter形式でレイアウトとデータを記述
   - プロジェクトルートに保存（ユーザーは触る必要なし）

5. **HTML生成**
   - `generate-slides.js`でMarkdownをHTMLに変換
   - Chart.js、Prism.jsの自動統合

6. **サムネイル自動生成**
   - Puppeteerで各スライドをスクリーンショット
   - プログレスバーのプレビュー用

7. **デプロイ準備**
   - リソースファイルをdeployディレクトリにコピー
   - パスの自動置換

8. **Surgeへのデプロイ**
   - abalol.surge.sh にサブディレクトリ構造でデプロイ
   - プロジェクト名がサブパスになる

9. **URLの提供**
   - デプロイ完了後、URLをユーザーに提示
   - 例: https://abalol.surge.sh/project-name/
   - ブラウザで自動的に開く

### ユーザーがやること

**スライドにしたい内容を提供するだけです。特定のフォーマットは不要です。**

- スライドの内容（テキスト、データ、コード等）を自由な形式で提供
- 必要に応じて画像を添付またはURLを提供（求められた場合のみ）
- グラフにしたいデータがあれば数値を提供（求められた場合のみ）

### ユーザーがやらないこと

- Markdownファイルの作成
- ファイルフォーマットの整形
- レイアウトの指定
- コマンドの実行
- デプロイ作業
- パスの修正
- スタイルの調整

## 対話的な情報収集プロセス

ユーザーから提供された内容を分析し、レイアウトを検討します。必要に応じてユーザーに追加情報を求めます。

### 画像が効果的な場合

**判断基準**:
- 製品紹介、サービス説明、アーキテクチャ図などのスライド
- ビジュアルで訴求した方が理解しやすい内容

**ユーザーへの確認例**:
```
「スライド3（製品概要）には製品の画像があるとより訴求力が高まります。
推奨サイズ: 800x600px、形式: PNG/JPG
画像を提供できますか？（不要な場合は「不要」とお答えください）」
```

**ユーザーの応答による分岐**:
- 画像提供: `image-center`レイアウトを使用
- 不要: `bullet-slide`または`two-column`レイアウトで進める

### グラフが効果的な場合

**判断基準**:
- 数値データ、時系列データ、比率データなどがある
- データを視覚的に表現した方が分かりやすい

**ユーザーへの確認例**:
```
「スライド5のデータはグラフで表示した方が分かりやすいです。
以下の形式でデータを提供してください：

{
  "type": "bar",
  "labels": ["Q1", "Q2", "Q3", "Q4"],
  "datasets": [{
    "label": "売上（百万円）",
    "data": [100, 150, 120, 180]
  }]
}

データを提供できますか？（不要な場合は「不要」とお答えください）」
```

**ユーザーの応答による分岐**:
- データ提供: `chart-slide`レイアウトを使用
- 不要: `table-slide`レイアウトで進める

### レイアウトの提案

**複数の選択肢がある場合**:
```
「スライド7は以下のレイアウトが適しています：
- two-column: 左右に比較表示（視覚的に対比）
- diff-slide: Before/After形式（変化を強調）

どちらが良いですか？」
```

### 確認のタイミング

**重要**: レイアウトを確定する前に必ず確認すること

1. Markdownファイルを読み込む
2. 全スライドの内容を分析
3. 各スライドの最適レイアウトを判断
4. 画像・グラフが必要な箇所を特定
5. **ユーザーに確認メッセージを送る**
6. ユーザーの応答を待つ
7. 応答に基づいてMarkdownを作成
8. 以降の自動処理を実行

## サブスキルの提案

以下のような場合は、サブスキルの作成を検討してユーザーに提案してください。

### 1. 画像生成が頻繁に必要な場合

**提案メッセージ**:
```
「多くのスライドで画像が必要です。
DALL-E等を使った画像自動生成スキル（image-generator）を作成すると、
テキストプロンプトから自動的に画像を生成できます。
作成しますか？」
```

**サブスキルの機能**:
- テキストプロンプトから画像を生成
- 適切なサイズにリサイズ
- スライドディレクトリに保存

### 2. データの可視化が複雑な場合

**提案メッセージ**:
```
「複雑なデータ可視化が多数含まれています。
専用のdata-visualizerスキルを作成すると、
CSVファイルやJSONから自動的にChart.jsデータを生成できます。
作成しますか？」
```

**サブスキルの機能**:
- CSV/JSONファイルの読み込み
- Chart.js形式への自動変換
- グラフタイプの自動推奨

### 3. 多言語対応が必要な場合

**提案メッセージ**:
```
「このスライドを複数の言語で提供する予定はありますか？
slide-translatorスキルを作成すると、
翻訳版のスライドを自動生成できます。
作成しますか？」
```

**サブスキルの機能**:
- Markdownファイルの翻訳
- 各言語版のスライド生成
- 言語選択メニューの追加

### 4. テンプレートのカスタマイズが必要な場合

**提案メッセージ**:
```
「企業ブランドに合わせたデザインカスタマイズが必要ですか？
design-customizerスキルを作成すると、
カラーパレット、フォント、ロゴを簡単に変更できます。
作成しますか？」
```

**サブスキルの機能**:
- CSSカラーパレットの変更
- カスタムロゴの適用
- フォントの変更

## ファイル構成と相対パス

```
.claude/skills/slide-generator/
├── SKILL.md                                    # このファイル
├── scripts/
│   ├── generate-slides.js                      # Markdown → HTML変換スクリプト
│   └── generate-thumbnails.js                  # サムネイル生成スクリプト
├── resources/
│   ├── styles.css                              # メインスタイルシート
│   ├── script.js                               # インタラクティブ機能
│   ├── logo.svg                                # ロゴ画像
│   └── vendor/
│       ├── chart.min.js                        # Chart.js
│       ├── chartjs-plugin-datalabels.min.js    # Chart.js プラグイン
│       ├── prism.js                            # Prism.js（シンタックスハイライト）
│       ├── prism.css                           # Prism.js スタイル
│       └── prism-javascript.min.js             # Prism.js 言語定義
└── deploy/
    ├── resources/                              # デプロイ用リソース（コピー元）
    │   └── （上記resourcesと同じ構成）
    └── <project-name>/                         # 個別プロジェクトディレクトリ
        ├── index.html                          # 生成されたスライド
        ├── resources/                          # プロジェクト固有のリソース
        │   └── （上記resourcesと同じ構成）
        └── thumbnails/                         # 生成されたサムネイル
            ├── slide-0.png
            ├── slide-1.png
            └── ...
```

### パスの重要性

1. `generate-slides.js`が生成するHTMLは、`resources/`ディレクトリを相対パスで参照します
   - CSS: `<link rel="stylesheet" href="resources/styles.css">`
   - JS: `<script src="resources/script.js"></script>`

2. デプロイディレクトリ構造:
   ```
   deploy/<project-name>/
   ├── index.html          # メインHTMLファイル
   ├── resources/          # スタイル・スクリプト
   └── thumbnails/         # サムネイル画像
   ```

3. この構造により、Surgeなどの静的ホスティングに直接デプロイ可能です

## デプロイ設定

### デプロイ先ドメイン

すべてのプレゼンテーションは `abalol.surge.sh` にサブディレクトリ構造でデプロイされます。

- ルートURL: https://abalol.surge.sh/
- プロジェクトURL: https://abalol.surge.sh/<project-name>/

### ディレクトリ構造

```
deploy/abalol/                     # abalol.surge.sh のルート
├── index.html                     # プロジェクト一覧ページ
├── resources/                     # 共通リソース
│   ├── styles.css
│   ├── script.js
│   └── vendor/
├── climate-tech-final/            # プロジェクト1
│   ├── index.html
│   ├── resources/                 # プロジェクト固有リソース
│   └── thumbnails/
└── <other-projects>/              # プロジェクト2, 3...
```

### デプロイコマンド

```bash
# ステップ1: Markdown → HTML
node .claude/skills/slide-generator/scripts/generate-slides.js input.md output.html

# ステップ2: デプロイ準備（サブディレクトリ作成）
bash .claude/skills/slide-generator/scripts/prepare-presentation.sh output.html project-name

# ステップ3: abalol.surge.sh にデプロイ
cd .claude/skills/slide-generator/deploy/abalol
surge . abalol.surge.sh

# ステップ4: ブラウザで確認
open https://abalol.surge.sh/project-name/
```

### 重要な注意事項

1. すべてのプロジェクトは同じドメイン（abalol.surge.sh）にデプロイされます
2. プロジェクトごとに固有のサブディレクトリ名を使用してください
3. デプロイは `deploy/abalol/` ディレクトリ全体を対象とします
4. 新しいプロジェクトを追加しても、既存のプロジェクトは影響を受けません

## Claude Codeへの重要な指示（必読・厳守）

このスキルを使用する際は、以下のルールを絶対に守ること：

### 禁止事項
1. HTMLファイルを直接WriteツールやEditツールで生成・編集してはいけない
2. `climate-tech-presentation.html`のような名前でHTMLファイルを直接作成してはいけない
3. リソースファイル（styles.css, script.js等）のパスを手動で記述してはいけない
4. **Markdownファイルを生成する際に、勝手に絵文字やアイコンを追加してはいけない**
5. **ユーザーが提供した内容をそのまま使用し、装飾目的で絵文字を追加しないこと**

### 必須事項
1. **必ずMarkdownファイル（.md）から開始する**
2. **必ずプロジェクトルート（claude-slide-templateディレクトリ）で作業する**
3. **必ず以下の3ステップを順番に実行する**：

```bash
# 現在地確認（必ずプロジェクトルートにいること）
pwd  # .../claude-slide-template であることを確認

# ステップ1: Markdownファイルを作成
# Writeツールで climate-tech.md のような名前でMarkdownファイルを作成

# ステップ2: Markdownを元にHTMLを生成
node .claude/skills/slide-generator/scripts/generate-slides.js climate-tech.md climate-tech.html

# ステップ3: プレゼンテーション準備（サムネイル自動生成、リソースコピー、パス置換）
bash .claude/skills/slide-generator/scripts/prepare-presentation.sh climate-tech.html climate-tech

# ステップ4: デプロイ（surge.sh推奨）
surge .claude/skills/slide-generator/deploy/climate-tech your-presentation-name.surge.sh

# ステップ5: ブラウザで確認
open https://your-presentation-name.surge.sh
```

### なぜこのフローが必要なのか

- `generate-slides.js`: Markdownを解析してHTMLに変換。Chart.js、Prism.jsのスクリプトを自動挿入
- `prepare-presentation.sh`: リソースファイルをdeployディレクトリにコピーし、パスを正しく置換。サムネイル自動生成
- この順序を守らないと、スタイルが適用されない、グラフが表示されない、サムネイルが生成されないなどの問題が発生する

### Markdownファイルの書き方

スライドは**frontmatter形式**で記述します。各スライドは `---` で区切ります。

```markdown
---
layout: title-slide
---

# プレゼンテーションタイトル
## サブタイトル

---
layout: bullet-slide
---

## 見出し

- 箇条書き1
- 箇条書き2
- 箇条書き3

---
layout: chart-slide
chart-type: bar
chart-data: {"labels": ["A", "B", "C"], "datasets": [{"data": [10, 20, 30]}]}
---

## グラフタイトル

---
layout: ending-slide
---

## ありがとうございました

お問い合わせ: example@email.com
```

**重要なポイント**:
- 各スライドの先頭に `---` と `layout: xxx` を記述
- グラフスライドの場合は `chart-type` と `chart-data` を追加
- `---` の後にスライドの内容を記述
- 次のスライドとの境界は `---` で区切る

**レイアウトの自動判断について**:

ユーザーが「このテキストでスライド作って」のように内容だけを提供した場合、**Claude Codeが内容を分析して最適なレイアウトを自動的に選択します**。

- テキスト内容を読んで、リストなのか、比較なのか、データなのかを判断
- 各スライドに適切なレイアウト（`layout: bullet-slide`, `layout: table-slide`, `layout: chart-slide` 等）を割り当て
- 文字数が多い場合は自動的に複数のスライドに分割
- グラフが必要な場合は Chart.js のデータ形式に変換

**例**:
```
ユーザー入力: 「売上が増加しています。Q1: 100万円、Q2: 150万円...」
↓ Claude Codeが判断
→ chart-slide を選択、Chart.js形式のデータを生成
```

つまり、Claude Codeは「翻訳者」として、ユーザーの生の内容を適切なレイアウト付きMarkdownに変換します。

## 基本的な使い方

**ユーザーはスライドの内容を貼り付けるだけで、全自動でスライドが完成します。**

1. ユーザーがスライドにしたい内容（テキスト、データ、コードなど）を提供
2. Claude Codeが自動的に内容を分析・最適なレイアウトを選択・分割
3. **Markdownファイル（.md）を作成**
4. `generate-slides.js`でHTMLに変換
5. `prepare-presentation.sh`でデプロイ準備（サムネイル自動生成含む）
6. **surge.shでデプロイ**
7. ブラウザで確認して完成！

**重要**: スタイルを修正した場合は`prepare-presentation.sh`を再実行してください。

## リソースファイル

このスキルには以下のリソースが含まれています：

### 1. HTMLテンプレート
- `resources/template.html` - シンプルなスライドの基本構造
- `resources/layouts-example.html` - 全レイアウトのサンプル集（18スライド）

### 2. CSSスタイル
`resources/styles.css` - すべてのレイアウト用スタイル定義

### 3. SVGロゴ
`resources/logo.svg` - タイトルスライドに表示されるロゴ

### 4. レイアウト仕様書
`resources/layout-specs.md` - 各レイアウトの項目数、文字数制限、推奨内容

### 5. 内容テンプレート
`resources/content-template.md` - スライド内容を記述するためのMarkdownテンプレート

## ⚠️ 重要な注意事項（必読）

### 正しいビルドワークフロー

**必ずこの順序で実行すること**:

```bash
# 1. Markdownからスライド生成
node .claude/skills/slide-generator/scripts/generate-slides.js input.md output.html

# 2. プレゼンテーション準備（サムネイル生成含む）
bash .claude/skills/slide-generator/scripts/prepare-presentation.sh output.html slide-name

# 3. ブラウザで確認
open .claude/skills/slide-generator/deploy/slide-name/index.html
```

**重要**:
- プロジェクトルートから実行する
- prepare-presentation.shがリソースをdeploy/にコピーし、パスを置換する
- スタイル修正後は必ずprepare-presentation.shを再実行

### スタイル修正時の注意

`resources/styles.css`を修正した場合：
1. 修正を保存
2. **必ず**`prepare-presentation.sh`を再実行してdeployディレクトリに反映
3. ブラウザで確認する際は強制リロード（Cmd+Shift+R）

### 検証方法

**Chrome DevTools MCPを使用**:
- スライド表示の確認
- 実際の幅・色の測定
- CSSの適用状況確認

**よくある問題**:
- ブラウザキャッシュでスタイル変更が反映されない → 強制リロード
- パスエラー → プロジェクトルートから実行しているか確認

## ワークフロー

### デフォルト: 全自動生成（推奨）

**これが基本のワークフローです。ユーザーは内容を貼り付けるだけでOK。**

ユーザーがテキスト、データ、コードなどを提供したら、以下を自動で実行：

1. **内容分析**:
   - テキスト全体を読み込んで構造を理解
   - トピックごとにセクション分け
   - 重要度を判断

2. **自動分割**:
   - `resources/layout-specs.md`の文字数制限を参照
   - 各レイアウトの推奨文字数に収まるよう分割
   - 1スライドに収まらない情報は複数スライドに分割

3. **レイアウト自動選択**:
   - 内容の性質に応じて最適なレイアウトを選択
   - リスト → 箇条書きスライド
   - 比較内容 → 2カラムスライドまたはテーブル
   - 数値データ → グラフスライド
   - 重要な一文 → ワンラインテキスト or 引用スライド
   - Before/After → 差分確認スライド
   - コード → コードスライド

4. **スライド構成提案**:
   - タイトルスライドを先頭に追加
   - トピックが変わる箇所にセクション区切りを挿入
   - 終了スライドを最後に追加
   - 全体の流れを確認

5. **Markdownファイルを作成**:
   ```bash
   # Writeツールでプロジェクトルートに presentation.md を作成
   # frontmatter形式で各スライドを記述
   ```

6. **スライド生成とデプロイ準備**:
   ```bash
   # ⚠️ 重要: 必ずプロジェクトルートから実行すること
   pwd  # .../claude-slide-template であることを確認

   # Markdownからスライド生成
   node .claude/skills/slide-generator/scripts/generate-slides.js presentation.md presentation.html

   # プレゼンテーション準備（サムネイル生成含む）
   bash .claude/skills/slide-generator/scripts/prepare-presentation.sh presentation.html my-presentation
   ```

   これで以下が自動実行される：
   - HTMLファイルの生成
   - deploy/my-presentation/にコピー
   - リソース（CSS、JS）のコピーとパス置換
   - Puppeteerによるサムネイル自動生成

7. **デプロイ（surge.sh推奨）**:
   ```bash
   # surge.shでデプロイ
   surge .claude/skills/slide-generator/deploy/my-presentation my-presentation.surge.sh
   ```

8. **確認**:
   ```bash
   # ブラウザで開く
   open https://my-presentation.surge.sh
   ```

   またはChrome DevTools MCPで確認

**分割の目安:**
- 箇条書き: 5項目以上 → 複数スライドに分割
- 段落テキスト: 300文字以上 → 複数スライドまたは要約
- データ: 8データポイント以上 → 複数グラフに分割
- コード: 15行以上 → 重要部分のみ抽出or複数スライド

### その他の方法

**Markdownファイルがある場合**:
- ユーザーがMarkdownファイルを提供したら、それを読み込んで上記のワークフローを実行

**対話的に作成する場合**:
- ユーザーが要件を口頭で伝える場合は、内容を確認しながら段階的に生成

## 利用可能なレイアウト

### 1. タイトルスライド（title-slide）
最初のスライドに使用。ロゴ、タイトル、サブタイトルを含む。

```html
<section class="slide title-slide">
    <div class="logo-container">
        <img src="logo.svg" alt="Logo" class="logo">
    </div>
    <h1>タイトル</h1>
    <p class="subtitle">サブタイトル</p>
</section>
```

### 2. 箇条書きスライド（デフォルト）
一般的な箇条書きリスト。

```html
<section class="slide">
    <h2>見出し</h2>
    <ul>
        <li>ポイント1</li>
        <li>ポイント2</li>
        <li>ポイント3</li>
    </ul>
</section>
```

### 3. 2カラムスライド（two-column）
左右に内容を分割表示。比較や対比に最適。

```html
<section class="slide two-column">
    <div class="column">
        <h2>左側</h2>
        <p>内容...</p>
    </div>
    <div class="column">
        <h2>右側</h2>
        <p>内容...</p>
    </div>
</section>
```

### 4. 画像中心スライド（image-center）
画像を中心に配置し、説明を追加。

```html
<section class="slide image-center">
    <h2>見出し</h2>
    <img src="image.jpg" alt="説明">
    <p>キャプション</p>
</section>
```

### 5. 引用スライド（quote-slide）
重要な引用や印象的なメッセージを大きく表示。

```html
<section class="slide quote-slide">
    <blockquote>
        引用文...
    </blockquote>
    <cite>— 引用元</cite>
</section>
```

### 6. セクション区切りスライド（section-slide）
章やセクションの区切りに使用。

```html
<section class="slide section-slide">
    <h2>第2章</h2>
    <p>セクションの説明</p>
</section>
```

### 7. テーブルスライド（table-slide）
データや比較表の表示。

```html
<section class="slide table-slide">
    <h2>比較表</h2>
    <table>
        <thead>
            <tr><th>項目</th><th>A</th><th>B</th></tr>
        </thead>
        <tbody>
            <tr><td>価格</td><td>100</td><td>200</td></tr>
        </tbody>
    </table>
</section>
```

### 8. コードスライド（code-slide）
ソースコードの表示に最適。

```html
<section class="slide code-slide">
    <h2>コードサンプル</h2>
    <pre><code>function example() {
    return "Hello";
}</code></pre>
</section>
```

### 9. フルサイズ画像背景スライド（full-image）
背景画像全体にテキストを重ねる。

```html
<section class="slide full-image" style="background-image: url('bg.jpg');">
    <div class="content">
        <h2>メッセージ</h2>
        <p>説明</p>
    </div>
</section>
```

### 10. 終了スライド（ending-slide）
プレゼンテーションの最後に使用。

```html
<section class="slide ending-slide">
    <h2>ありがとうございました</h2>
    <p>ご清聴ありがとうございました</p>
    <div class="contact">
        <p>contact@example.com</p>
    </div>
</section>
```

### 11. グラフスライド（chart-slide）
Chart.jsを使ったグラフを1つ表示。棒グラフ、折れ線グラフ、円グラフなど。

```html
<section class="slide chart-slide">
    <h2>売上推移</h2>
    <div class="chart-container">
        <canvas id="myChart"></canvas>
    </div>
</section>
```

**注意**: HTMLの`<head>`にChart.jsのCDNを追加する必要があります：
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

### 12. 2つのグラフ並列（dual-chart-slide）
2つのグラフを左右に並べて表示。

```html
<section class="slide dual-chart-slide">
    <h2>データ分析</h2>
    <div class="chart-wrapper">
        <h3>市場シェア</h3>
        <div class="chart-container">
            <canvas id="chart1"></canvas>
        </div>
    </div>
    <div class="chart-wrapper">
        <h3>成長率</h3>
        <div class="chart-container">
            <canvas id="chart2"></canvas>
        </div>
    </div>
</section>
```

### 13. グラフ+テキスト並列（chart-text-slide）
グラフと説明テキストを並べて表示。

```html
<section class="slide chart-text-slide">
    <div class="chart-section">
        <div class="chart-container">
            <canvas id="chart"></canvas>
        </div>
    </div>
    <div class="text-section">
        <h2>主要な発見</h2>
        <ul>
            <li>ポイント1</li>
            <li>ポイント2</li>
        </ul>
        <p>説明文...</p>
    </div>
</section>
```

## グラフの初期化

グラフを使用する場合は、`<script>`タグ内でChart.jsの初期化が必要です。サンプルは`resources/layouts-example.html`を参照してください。

### 14. 差分確認スライド（diff-slide）
Before/After比較やコード差分を左右に並べて表示。

**テキスト比較の例:**
```html
<section class="slide diff-slide">
    <h2>改善ポイント</h2>
    <div class="diff-container">
        <div class="diff-panel before">
            <h3>Before</h3>
            <div class="diff-content">
                <ul>
                    <li>問題点1</li>
                    <li>問題点2</li>
                </ul>
            </div>
        </div>
        <div class="diff-panel after">
            <h3>After</h3>
            <div class="diff-content">
                <ul>
                    <li>改善点1</li>
                    <li>改善点2</li>
                </ul>
            </div>
        </div>
    </div>
</section>
```

**コード比較の例:**
```html
<section class="slide diff-slide">
    <h2>リファクタリング</h2>
    <div class="diff-container">
        <div class="diff-panel before">
            <h3>Before</h3>
            <div class="diff-content">
                <pre><code>古いコード...</code></pre>
            </div>
        </div>
        <div class="diff-panel after">
            <h3>After</h3>
            <div class="diff-content">
                <pre><code>新しいコード...</code></pre>
            </div>
        </div>
    </div>
</section>
```

### 15. ワンラインテキストオンリー（oneline-slide）
シンプルで大きな1行メッセージを表示。インパクト重視。

**基本形:**
```html
<section class="slide oneline-slide">
    <div class="message">
        Think Different
    </div>
</section>
```

**サブメッセージ付き:**
```html
<section class="slide oneline-slide">
    <div class="message medium">
        メインメッセージ
    </div>
    <p class="submessage">サブメッセージ</p>
</section>
```

**サイズバリエーション:**
- デフォルト（6rem）: `class="message"`
- 中サイズ（5rem）: `class="message medium"`
- 小サイズ（4rem）: `class="message small"`

## 操作方法

生成されたスライドは以下のキーで操作：
- `→` (右矢印): 次のスライド
- `←` (左矢印): 前のスライド
- `Home`: 最初のスライドへ
- `End`: 最後のスライドへ
- URLクエリパラメータ: `?p=5` で直接5ページ目に移動

### プログレスバー機能

画面上部にセグメント化されたプログレスバーが表示されます：
- 各セグメントがスライド1枚に対応
- クリックすると該当スライドに移動
- ホバーするとサムネイルプレビューを表示

## サムネイル生成（自動）

**prepare-presentation.shが自動的に実行します**

サムネイル生成は`prepare-presentation.sh`スクリプト内で自動的に行われます。

### 実行内容

`prepare-presentation.sh`実行時に自動的に：
1. Puppeteerの自動インストール（初回のみ）
2. リソースファイルのコピー
3. 各スライドのスクリーンショット撮影
4. `deploy/slide-name/thumbnails/index/`に保存

### 生成されるファイル

```
.claude/skills/slide-generator/deploy/
└── slide-name/
    ├── index.html
    ├── thumbnails/
    │   └── index/
    │       ├── slide-0.png
    │       ├── slide-1.png
    │       └── ...
    └── resources/  # 自動コピーされる
        ├── styles.css
        ├── script.js
        └── vendor/
```

### 再生成が必要なタイミング

以下の場合はprepare-presentation.shを再実行：
- スライドの内容を変更した後
- 新しいスライドを追加・削除した後
- レイアウトやスタイルを変更した後

```bash
bash .claude/skills/slide-generator/scripts/prepare-presentation.sh output.html slide-name
```

## スライド生成の例

### 例1: テキストを貼り付けるだけ

**ユーザー**: 「このテキストでスライド作って」+ 長文テキスト

**Claude Code**:
1. Markdownファイルを作成（`presentation.md`）
2. `node .claude/skills/slide-generator/scripts/generate-slides.js presentation.md presentation.html`
3. `bash .claude/skills/slide-generator/scripts/prepare-presentation.sh presentation.html my-slides`
4. `surge .claude/skills/slide-generator/deploy/my-slides my-slides.surge.sh`
5. `open https://my-slides.surge.sh` でブラウザ確認

### 例2: データでグラフスライドを作成

**ユーザー**: 「2023年の売上データ: Q1=100万, Q2=150万, Q3=120万, Q4=180万」

**Claude Code**:
1. Chart.js形式のデータを埋め込んだMarkdown（`sales.md`）を作成
2. `node .claude/skills/slide-generator/scripts/generate-slides.js sales.md sales.html`
3. `bash .claude/skills/slide-generator/scripts/prepare-presentation.sh sales.html sales-2023`
4. `surge .claude/skills/slide-generator/deploy/sales-2023 sales-2023.surge.sh`
5. `open https://sales-2023.surge.sh` でグラフ表示を確認

### 例3: コードを含むスライド

**ユーザー**: 「このコードを説明するスライド作って」+ コードブロック

**Claude Code**:
1. コードブロックを含むMarkdown（`code-demo.md`）を作成
2. `node .claude/skills/slide-generator/scripts/generate-slides.js code-demo.md code-demo.html`
3. `bash .claude/skills/slide-generator/scripts/prepare-presentation.sh code-demo.html code-demo`
4. `surge .claude/skills/slide-generator/deploy/code-demo code-demo.surge.sh`
5. `open https://code-demo.surge.sh` でシンタックスハイライトを確認

---

## トラブルシューティング

### スタイルが反映されない

**症状**: CSSを修正したが見た目が変わらない

**解決方法**:
1. prepare-presentation.shを再実行（deployディレクトリに反映）
2. ブラウザで強制リロード（Cmd+Shift+R）
3. Chrome DevTools MCPでCSSの読み込み状況を確認

### スライドが空になる

**症状**: 特定のスライドの内容が表示されない

**原因**: generate-slides.jsのfrontmatter分割ロジックの問題

**確認方法**: Markdownファイルの`---`の使い方を確認
- frontmatter: `---\nlayout: xxx\n---\n`
- スライド区切り: `---\n`（frontmatter後の最初の`---`は次のスライドの開始）

### パスエラー

**症状**: ファイルが見つからないエラー

**解決方法**: プロジェクトルートから実行しているか確認
```bash
pwd  # 現在地確認
# /Users/.../claude-slide-template であるべき
```
