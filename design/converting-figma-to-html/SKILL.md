---
name: converting-figma-to-html
description: Provides expertise in converting Figma designs to HTML/CSS using Figma MCP tools, with data attributes for content tracking and comprehensive analysis. Use when converting Figma designs to web code.
compatibility: Claude Code
allowed-tools: Read Write Glob mcp__figma__get_screenshot mcp__figma__get_design_context mcp__figma__get_metadata
---

# Figma to HTML Conversion Skill

Figma MCPツールを使用してFigmaデザインからHTML/CSSを生成し、コンテンツ分析を行うための専門知識を提供するスキルです。

## 目次

1. [概要](#概要)
2. [クイックスタート](#クイックスタート)
3. [詳細ガイド](#詳細ガイド)
4. [生成されるファイル](#生成されるファイル)
5. [使い方](#使い方)

## 概要

このスキルは以下のタスクをサポートします：

1. **Figmaデータ取得**: Figma MCPツールを使用してデザイン情報を取得
2. **HTML/CSS生成**: Tailwind CSSベースのレスポンシブHTMLを生成
3. **data属性埋め込み**: トレーサビリティとコンテンツ管理のための属性を付与
4. **コンテンツ分析**: 静的/動的コンテンツの分類（識別のみ）
5. **プレビュー生成**: デバイスフレーム付きプレビューHTML（オプション）

## 禁止事項

**以下は絶対に行わないこと：**
- API仕様の提案（エンドポイント、リクエスト/レスポンス形式）
- データモデル設計の提案（エンティティ、スキーマ、型定義）
- バックエンド実装に関する提案

コンテンツ分析では「このUIに動的データが必要」という**事実の識別のみ**を行います。

## クイックスタート

### 基本的な使い方

```
以下のFigma URLからHTML/CSSを生成してください：
https://figma.com/design/XXXXX/Project?node-id=1234-5678
```

エージェントは自動的に：
1. Figmaデータを取得（screenshot, design_context, metadata）
2. data属性付きHTMLを生成
3. コンテンツ分析ドキュメントを作成
4. プレビューHTML（オプション）を生成

### 生成されるファイル

**単一画面の場合:**
```
.outputs/{screen-name}/
├── index.html              # メインHTML（data属性付き）
├── index-{state}.html      # 状態バリエーション（該当する場合）
├── spec.md                 # 画面仕様書
├── mapping-overlay.js      # マッピング可視化
└── preview.html            # プレビュー（オプション）
```

**複数画面の場合（画面ごとにディレクトリ分離）:**
```
.outputs/
├── {screen-a}/
│   ├── index.html
│   ├── index-empty.html    # 同一画面の状態バリエーション
│   ├── spec.md
│   └── mapping-overlay.js
├── {screen-b}/
│   ├── index.html
│   ├── spec.md
│   └── mapping-overlay.js
└── ...
```

`{screen-name}` はFigmaの画面名から生成した短い識別名（例: `homework-modal`）

> **注意**:
> - spec.md 内の static/dynamic 分類は**仮決定**です。実装時にレビューしてください。
> - 複数フレームは「同一画面の状態バリエーション」か「別画面」かを判定し、適切な構造で出力します。

## 詳細ガイド

詳細な情報は以下のファイルを参照してください：

### ワークフロー
**[workflow.md](references/workflow.md)**: Figma MCPツールの実行順序と各ステップの詳細

- Step 1: Figmaデータ取得（screenshot, design_context, metadata）
- Step 2: HTML生成ルール（Tailwind CSS、data属性、レイアウト）
- Step 3: spec.md 更新（構造・スタイル、コンテンツ分析セクション）
- Step 4: 品質チェック（ビジュアル確認、属性確認）

### 変換ガイドライン
**[conversion-guidelines.md](references/conversion-guidelines.md)**: 変換時の判断基準と処理ルール

- アイコン・画像アセットの処理
- レイアウト・配置の処理（Flexbox/Grid優先）
- デザイントークンの処理
- OSネイティブUI要素の除外
- コンテンツ分類体系

### クイックリファレンス
**[quick-reference.md](references/quick-reference.md)**: よく使うパターンと命名規則

- 必須data属性一覧
- data-figma-content-XXX 命名例
- HTML構造パターン
- Tailwindクラス早見表

### テンプレート
**[assets/](assets/)**: 各種テンプレートファイル

- **[html-output.html](assets/html-output.html)**: HTMLテンプレート（変数付き）
- **[preview.html](assets/preview.html)**: プレビュー用ラッパー
- **[../../templates/screen-spec.md](../../templates/screen-spec.md)**: 画面仕様書テンプレート

## 主要な機能

### 1. data属性による追跡

#### 画面レベル属性（ルート要素）

ルート要素（`<body>`または主要コンテナ）には画面識別用の属性を付与：

| 属性 | 用途 | 例 |
|------|------|-----|
| `data-figma-node` | FigmaルートノードID | `"2350:6396"` |
| `data-figma-filekey` | FigmaファイルキーID | `"fLUFVpvmfpCJBrgzYHi5PB"` |
| `data-figma-name` | Figmaでの画面名 | `"チュートリアル"` |
| `data-figma-url` | Figmaへのリンク | `"https://www.figma.com/design/..."` |
| `data-screen-id` | 画面識別ID（ハイフン区切り） | `"tutorial"` |
| `data-screen-name` | 画面表示名 | `"チュートリアル"` |

#### 要素レベル属性

全ての主要要素に以下の属性を付与：

| 属性 | 用途 | 例 |
|------|------|-----|
| `data-figma-node` | FigmaノードID | `"5070:65342"` |
| `data-figma-name` | Figmaでのレイヤー名 | `"Button/Primary"` |
| `data-figma-tokens` | デザイントークン（まとめて） | `"background: darkblue"` |
| `data-figma-token-*` | デザイントークン（個別、推奨） | 下記参照 |
| `data-figma-icon-svg` | アイコンノードID（getImages用） | `"3428:18627"` |
| `data-figma-interaction` | インタラクション定義 | `"tap:navigate:/course/1"` |
| `data-figma-states` | サポートするUI状態 | `"default,hover,active,disabled"` |
| `data-figma-navigate` | 画面遷移先 | `"/course/detail"` |
| `data-state` | 現在のUI状態 | `"default"`, `"disabled"`, `"loading"`, `"selected"` |

#### デザイントークン属性 (data-figma-token-*)

Figmaのデザイントークンをプロパティ別に個別の属性で保持する推奨形式：

| 属性 | 用途 | 値の例 |
|------|------|--------|
| `data-figma-token-bg` | 背景色トークン | `"Background/Main/Default"` |
| `data-figma-token-color` | テキスト色/アイコン色トークン | `"Text/Default/Default"`, `"Icon/Main/Default"` |
| `data-figma-token-font` | フォントトークン | `"JP/16 - Bold"` |
| `data-figma-token-radius` | 角丸トークン | `"Radius/200"` |
| `data-figma-token-padding` | パディングトークン | `"Space/200"` |
| `data-figma-token-gap` | ギャップトークン | `"Space/150"` |
| `data-figma-token-height` | 高さトークン | `"56px"` |
| `data-figma-token-border` | ボーダートークン | `"Border/Main/Default"` |
| `data-figma-token-size` | サイズトークン（アイコン等） | `"24px"`, `"32px"` |

**例（画面ルート）:**
```html
<body data-figma-node="2350:6396"
      data-figma-filekey="fLUFVpvmfpCJBrgzYHi5PB"
      data-figma-name="チュートリアル"
      data-figma-url="https://www.figma.com/design/fLUFVpvmfpCJBrgzYHi5PB?node-id=2350:6396"
      data-screen-id="tutorial"
      data-screen-name="チュートリアル"
      class="...">
```

**例（ボタン要素）:**
```html
<button data-figma-node="2350:6410"
        data-figma-token-bg="Background/Main/Default"
        data-figma-token-color="Text/Default/On"
        data-figma-token-font="JP/18 - Bold"
        data-figma-token-radius="Radius/Full"
        data-figma-token-height="56px"
        data-figma-states="default,hover,active,disabled"
        data-figma-interaction="tap:navigate:next-step"
        data-state="default"
        class="w-full h-14 bg-bg-main-default text-text-default-on font-bold rounded-full">
  次へ
</button>
```

**例（アイコン要素）:**
```html
<span data-figma-node="2350:6420"
      data-figma-token-color="Icon/Main/Default"
      data-figma-token-size="24px"
      data-figma-icon-svg="3428:18627"
      class="w-6 h-6 text-icon-main-default">
  <svg viewBox="0 0 24 24"><!-- placeholder --></svg>
</span>
```

### 2. コンテンツ分類

HTMLの各コンテンツを以下のカテゴリで整理：

| 分類 | 説明 | 例 |
|------|------|-----|
| `static` | 固定ラベル・UI文言 | ボタン名、ナビゲーション |
| `dynamic` | ユーザー/時間で変化 | 数値、日付、ユーザー名 |
| `dynamic_list` | 件数可変リスト | 講座一覧、通知一覧 |
| `config` | 画面設定で変わる要素 | ページネーション状態 |
| `asset` | 静的アセット | SVGアイコン、ロゴ |
| `user_asset` | ユーザーアップロード画像 | プロフィール画像 |

### 3. コンテンツ分類属性の埋め込み

分類結果をHTML要素に data 属性として埋め込み、後続のAPI連携フェーズで活用：

| 属性 | 用途 | 例 |
|------|------|-----|
| `data-figma-content-id` | 一意識別子（snake_case） | `"badge_text"` |
| `data-figma-content-type` | コンテンツ種別 | `"text"`, `"icon"`, `"ui_state"` |
| `data-figma-content-classification` | 分類 | `"static"`, `"dynamic"`, `"asset"` |
| `data-figma-content-data-type` | データ型 | `"string"`, `"number"`, `"svg"` |
| `data-figma-content-value` | Figmaでの表示値 | `"テスト運用版"` |
| `data-figma-content-notes` | 補足説明 | `"最終ステップでは「はじめる」"` |

**埋め込み例:**
```html
<span data-figma-node="2350:6414"
      data-figma-content-id="badge_text"
      data-figma-content-type="text"
      data-figma-content-value="テスト運用版"
      data-figma-content-classification="static"
      data-figma-content-data-type="string">テスト運用版</span>
```

### 4. レスポンシブ対応

- Tailwind CSS（CDN経由）を使用
- モバイルファースト（max-w-[375px]等）
- Flexbox/Gridで相対的レイアウト
- absolute/fixed は最小限に

#### Tailwind CDN + Inline Config パターン

standalone HTML 生成時は、Figma トークンを Tailwind config に埋め込む：

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          // Figma Semantic Tokens
          'text-default': {
            'default': '#24243f',
            'secondary': '#67717a',
            'on': '#ffffff',
          },
          'bg-main': {
            'default': '#0070e0',
            'secondary': '#cfe5fc',
          },
        },
        spacing: {
          'space-050': '4px',
          'space-100': '8px',
          'space-200': '16px',
        },
        borderRadius: {
          'radius-100': '8px',
          'radius-200': '16px',
          'radius-full': '9999px',
        },
        fontFamily: {
          'hiragino': ['"Hiragino Sans"', '"Hiragino Kaku Gothic ProN"', '"Meiryo"', 'sans-serif'],
        },
      }
    }
  }
</script>
```

**トークン取得:** `mcp__figma__get_variable_defs` を使用してFigmaから取得

### 5. アイコン処理

複雑なSVGパスは再現せず、シンプルなプレースホルダーに置換：

```html
<div class="w-6 h-6"
     data-figma-icon-svg="3428:18627"
     data-figma-content-settings-icon>
  <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none">
    <rect x="4" y="4" width="16" height="16" rx="2"
          stroke="currentColor" stroke-width="2"/>
  </svg>
</div>
```

### 6. OSネイティブUI除外

以下の要素は自動的に除外：
- ステータスバー（時刻、電波、バッテリー）
- Dynamic Island
- Home Indicator

### 7. インタラクション属性

インタラクティブな要素には動作を定義する属性を付与：

```html
<article class="course-card"
         data-figma-states="default,hover,active"
         data-figma-interaction="tap:navigate:/course/1"
         data-figma-navigate="/course/1"
         tabindex="0" role="button">
  <h3>講座タイトル</h3>
</article>
```

**インタラクション形式**: `{trigger}:{action}:{target}`
- trigger: `tap`, `hover`, `focus`, `longpress`
- action: `navigate`, `show-modal`, `close-modal`, `submit`, `open-dropdown`, `select`, `toggle`
- target: 遷移先パス、モーダルID、ドロップダウンID等

**状態値 (data-state)**: `default`, `hover`, `active`, `disabled`, `loading`, `selected`, `expanded`

### 8. 画面遷移属性の埋め込み

spec.md の「インタラクション」「画面フロー」セクションを参照して、HTMLに画面遷移属性を付与：

| 属性 | 用途 | 例 |
|------|------|-----|
| `data-figma-interaction` | インタラクション定義 | `"tap:navigate:tutorial"` |
| `data-figma-navigate` | 遷移先パス | `"/{locale}/ask_ai/tutorial"` |
| `data-figma-states` | サポートするUI状態 | `"default,hover,active,disabled"` |

**遷移パターン例:**

```html
<!-- 単純な画面遷移 -->
<button data-figma-interaction="tap:navigate:tutorial"
        data-figma-navigate="/{locale}/ask_ai/tutorial">
  ヘルプ
</button>

<!-- 条件付き遷移（同意状態等） -->
<button data-figma-interaction="tap:conditional-navigate"
        data-figma-navigate="consented:/{locale}/ask_ai|unconsented:consent-modal"
        data-figma-states="default,hover,active">
  スキップ
</button>

<!-- 内部ステップ遷移 -->
<button data-figma-interaction="tap:navigate:next-step"
        data-figma-navigate="tutorial-step-{n+1}"
        data-figma-states="default,hover,active">
  次へ
</button>

<!-- 複合アクション -->
<button data-figma-interaction="tap:open-file-dialog|navigate:trim"
        data-figma-navigate="/{locale}/ask_ai/trim"
        data-figma-states="default,hover,active,loading">
  写真を共有
</button>
```

**遷移先の記述形式:**
- 単純遷移: `/{locale}/path/to/screen`
- 条件付き: `condition1:path1|condition2:path2`
- 内部遷移: `screen-step-{n+1}`, `previous-screen`

### 9. mapping-overlay.js

コンテンツマッピングとインタラクション可視化のためのオーバーレイスクリプト：

```html
<!-- HTMLの末尾に自動追加 -->
<script src="mapping-overlay.js"></script>
</body>
</html>
```

**機能**:
- マウスオーバーでコンテンツタイプ（static/dynamic）を表示
- 画面遷移先・モーダル表示対象を表示
- リアルタイムでUI状態（hover/active/focus/selected）を検出・表示
- 凡例クリックでタイプ別フィルタリング（親子関係を考慮）

## ワークフロー（概要）

```
1. figma:get_screenshot
   └─> デザインのビジュアル参照を取得

2. figma:get_design_context (clientLanguages: "html,css")
   └─> ★最重要：構造・スタイル情報を取得

3. figma:get_metadata（必要に応じて）
   └─> 階層構造の詳細確認

4. HTML生成
   ├─> Tailwind CSSでマークアップ
   ├─> data属性を全要素に付与
   └─> プレースホルダーアイコンを配置

5. コンテンツ分析
   └─> static/dynamic分類を整理

6. コンテンツ分類属性の埋め込み ★新規
   ├─> data-figma-content-id（snake_case識別子）
   ├─> data-figma-content-type（text/icon/ui_state等）
   ├─> data-figma-content-classification（static/dynamic/asset等）
   └─> data-figma-content-data-type（string/number/svg等）

7. 画面遷移属性の埋め込み ★新規
   ├─> spec.md のインタラクション/画面フローを参照
   ├─> data-figma-interaction（トリガー:アクション:ターゲット）
   ├─> data-figma-navigate（遷移先パス）
   └─> data-figma-states（対応UI状態）

8. spec.md 更新
   ├─> 「構造・スタイル」セクション
   ├─> 「コンテンツ分析」セクション
   └─> 完了チェックリストを更新

9. プレビュー生成（オプション）
   └─> デバイスフレーム付きプレビュー
```

詳細は **[workflow.md](references/workflow.md)** を参照してください。

## 完了チェックリスト

生成後、以下を確認：

```
- [ ] Figmaスクリーンショットと見た目が一致
- [ ] 全ての主要要素にdata-figma-node属性がある
- [ ] コンテンツ要素にdata-figma-content-XXX属性がある
- [ ] アイコンにdata-figma-icon-svg属性がある
- [ ] インタラクティブ要素にdata-figma-interaction属性がある
- [ ] 状態変化する要素にdata-figma-states属性がある
- [ ] ステータスバー等のOSネイティブUIが除外されている
- [ ] 画面遷移属性が埋め込まれている（Step 7）
  - data-figma-interaction（トリガー:アクション:ターゲット）
  - data-figma-navigate（遷移先パス）
  - data-figma-states（対応UI状態）
- [ ] コンテンツ分類属性が埋め込まれている（Step 6）
  - data-figma-content-id（snake_case）
  - data-figma-content-type
  - data-figma-content-classification
  - data-figma-content-data-type
- [ ] spec.md の「構造・スタイル」セクションが更新されている
- [ ] spec.md の「コンテンツ分析」セクションが更新されている
- [ ] spec.md の「インタラクション」セクションが更新されている
- [ ] プレビューHTMLが正しく表示される（オプション）
```

## 使い方

このスキルは、Figmaデザインを変換するエージェントから参照されます。

### スキルの利用

エージェントは以下のステップでこのスキルを活用します：

1. **ワークフローの参照**: [workflow.md](references/workflow.md) の手順に従う
2. **ガイドラインの適用**: [conversion-guidelines.md](references/conversion-guidelines.md) の変換ルールを適用
3. **テンプレートの使用**: [assets/](assets/) のテンプレートを利用してファイル生成
4. **リファレンスの確認**: [quick-reference.md](references/quick-reference.md) で命名規則やパターンを確認

### 必要なツール

- **Figma MCP**: Figmaデザインデータの取得に必須
- **Read**: テンプレートやガイドラインの読み込み
- **Write**: HTML/分析ドキュメントの生成
- **Glob**: 既存ファイルのパターン検索

## 注意事項

### Figma MCP ツール

このエージェントは **Figma MCP** を使用します。以下を確認してください：

- Figma MCP サーバーが起動している
- Figma URLが有効である
- 必要な権限がある

### アセットURL

- FigmaアセットURLは **7日間で期限切れ** になります
- 本番実装前にアセットをダウンロードまたは再取得が必要です

### ブラウザ確認

生成されたHTMLは以下で確認してください：

```bash
# プレビューHTMLを開く
open {component_name}_preview.html

# またはメインHTMLを直接開く
open {component_name}.html
```

## 参照

- **[workflow.md](references/workflow.md)**: 詳細なワークフロー手順
- **[conversion-guidelines.md](references/conversion-guidelines.md)**: 変換ルールの詳細
- **[quick-reference.md](references/quick-reference.md)**: クイックリファレンス
- **[assets/](assets/)**: 各種テンプレート
