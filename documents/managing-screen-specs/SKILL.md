---
name: managing-screen-specs
description: Initializes and updates screen specification documents. Use as a foundation skill for all screen documentation workflows.
allowed-tools: [Read, Write, Glob]
---

# Screen Spec Management Skill

画面仕様書の初期化とセクション更新を管理するヘルパースキルです。

## 概要

各スキル（converting-figma-to-html, documenting-ui-states等）は、このスキルの手順に従って画面仕様書を更新します。

## ファイル構造

```
.agents/
├── templates/
│   └── screen-spec.md          # 画面仕様書テンプレート
└── tmp/
    └── {screen-id}/
        ├── spec.md             # 画面仕様書（メインドキュメント）
        ├── index.html          # 参照用HTML
        └── assets/             # 画像等のアセット
```

## テンプレート構造

統一テンプレートは以下のセクションで構成されます：

| セクション | 説明 |
|-----------|------|
| 概要 | 画面の基本情報（名前、Figma URL、HTML、説明） |
| 構造・スタイル | HTML構造とdata-figma属性 |
| コンテンツ分析 | 静的/動的コンテンツの分類とAPI依存 |
| UI状態 | デフォルト状態、ボタン状態、タブ状態など |
| インタラクション | INT-XXX形式でトリガー、アクション、遷移先を定義 |
| APIマッピング | APIエンドポイントとの関連付け |
| アクセシビリティ | セマンティック要件、フォーカス管理、キーボード操作 |
| デザイントークン | カラー、タイポグラフィ、スペーシング |
| 画面フロー | mermaid stateDiagram-v2と遷移テーブル |
| 変更履歴 | 日付、変更内容、担当の履歴 |

## ワークフロー

### 1. 仕様書の初期化

新しい画面の仕様書を作成する場合：

```bash
# テンプレートをコピー
cp .agents/templates/screen-spec.md .outputs/{screen-id}/spec.md

# 基本情報を置換
- {{SCREEN_NAME}} → 画面名
- {{SCREEN_ID}} → 画面識別子
- {{FIGMA_URL}} → Figma URL
- {{HTML_FILE}} → HTMLファイル名
- {{ROOT_NODE_ID}} → ノードID
- {{DATE}} → 作成日
- {{DESCRIPTION}} → 画面の説明
```

### 2. セクションの更新

各スキルは担当セクションのみを更新します。

#### 更新手順

1. **セクション位置を特定**

```markdown
## {セクション名}

### {サブセクション名}
```

2. **プレースホルダーを内容に置換**

```markdown
{{PLACEHOLDER}} → 実際の内容
```

3. **変更履歴に追記**

```markdown
| {DATE} | {セクション名}を更新 | {担当} |
```

### 3. セクション別の責任範囲

| セクション | 担当スキル | 主なプレースホルダー |
|-----------|-----------|---------------------|
| 概要 | managing-screen-specs | `{{SCREEN_NAME}}`, `{{FIGMA_URL}}`, `{{HTML_FILE}}`, `{{DESCRIPTION}}` |
| 構造・スタイル | converting-figma-to-html | `{{HTML_STRUCTURE}}`, `{{SCREEN_ID}}`, `{{ROOT_NODE_ID}}` |
| コンテンツ分析 | converting-figma-to-html | `{{CONTENT_NAME}}`, `{{DATA_ATTRIBUTE}}`, `{{API_SOURCE}}` |
| UI状態 | documenting-ui-states | `{{ELEMENT_NAME}}`, `{{ELEMENT_STATE}}`, ボタン状態各種 |
| インタラクション | extracting-interactions | `{{INTERACTION_NAME}}`, `{{TRIGGER}}`, `{{ACTION}}`, `{{DESTINATION}}` |
| フォーム仕様 | defining-form-specs | （テンプレートには含まない、必要時に追加） |
| APIマッピング | mapping-html-to-api | `{{API_MAPPING_DESCRIPTION}}` |
| アクセシビリティ | defining-accessibility-requirements | `{{ELEMENT}}`, `{{ROLE}}`, `{{ARIA_ATTRS}}`, フォーカス/キーボード設定 |
| デザイントークン | extracting-design-tokens | カラー/タイポグラフィ/スペーシングの各トークン |
| 画面フロー | documenting-screen-flows | `{{CURRENT_SCREEN}}`, `{{NEXT_SCREEN}}`, 遷移テーブル |

## セクション更新のルール

### 必須

- 自分の担当セクションのみを更新する
- 変更履歴に記録を追加する
- プレースホルダーを具体的な内容に置換する

### 禁止

- 他のセクションの内容を変更しない
- プレースホルダーを削除せずに残さない

## 初期化の例

### 入力

```
画面名: TOP画面
画面ID: top
Figma URL: https://figma.com/design/xxx/Project?node-id=2350:2662
HTMLファイル: top.html
説明: AskAI機能のエントリーポイント画面
```

### 出力（spec.md 冒頭部分）

```markdown
# 画面仕様書: TOP画面

## 概要

| 項目 | 内容 |
| ---- | ---- |
| 画面名 | TOP画面 |
| Figma URL | https://figma.com/design/xxx/Project?node-id=2350:2662 |
| HTML | top.html |
| 説明 | AskAI機能のエントリーポイント画面 |
```

## セクション更新の例

### documenting-ui-states による更新

**Before:**

```markdown
## UI状態

### デフォルト状態

| 要素 | 状態 | 備考 |
| ---- | ---- | ---- |
| {{ELEMENT_NAME}} | {{ELEMENT_STATE}} | {{ELEMENT_NOTES}} |
```

**After:**

```markdown
## UI状態

### デフォルト状態

| 要素 | 状態 | 備考 |
| ---- | ---- | ---- |
| 背景 | 水色グラデーション表示 | #e1f4ff基調 |
| ナビゲーション | 閉じるボタンのみ表示 | - |
| 写真を共有ボタン | 青背景、有効状態 | #0070e0 |
```

### extracting-interactions による更新

**Before:**

```markdown
### INT-001: {{INTERACTION_NAME_1}}

| 項目 | 内容 |
| ---- | ---- |
| トリガー | {{TRIGGER}} |
| 前提条件 | {{PRECONDITION}} |
| アクション | {{ACTION}} |
| API | {{API_CALL}} |
| 遷移先 | {{DESTINATION}} |
```

**After:**

```markdown
### INT-001: 写真を共有ボタンタップ

| 項目 | 内容 |
| ---- | ---- |
| トリガー | 「写真を共有」ボタンをタップ |
| 前提条件 | - |
| アクション | OSのアクションシートを表示 |
| API | なし |
| 遷移先 | action-sheet.html |
```

## 仕様書の完了判定

全ての必須セクションが具体的な内容で埋まったら完了です。

### 必須セクション

- 概要
- 構造・スタイル
- コンテンツ分析
- UI状態
- インタラクション
- APIマッピング
- アクセシビリティ
- デザイントークン
- 画面フロー
- 変更履歴

### 条件付きセクション（必要に応じて追加）

- フォーム仕様: 入力フォームがある場合

## 参照

- **[screen-spec.md](../../templates/screen-spec.md)**: テンプレートファイル
