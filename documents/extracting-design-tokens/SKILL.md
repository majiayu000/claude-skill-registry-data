---
name: extracting-design-tokens
description: Extracts and documents design tokens (colors, typography, spacing, shadows, etc.) from Figma designs. Updates the "デザイントークン" section in screen spec.md.
allowed-tools: [Read, Write, Glob, mcp__figma__get_screenshot, mcp__figma__get_design_context, mcp__figma__get_metadata, mcp__figma__get_variable_defs]
---

# Design Token Extraction Skill

Figmaデザインからデザイントークン（色、タイポグラフィ、スペーシング、シャドウ等）を抽出・整理するスキルです。

## 目次

1. [概要](#概要)
2. [対象範囲](#対象範囲)
3. [クイックスタート](#クイックスタート)
4. [詳細ガイド](#詳細ガイド)
5. [出力形式](#出力形式)

## 概要

このスキルは以下のタスクをサポートします：

1. **カラートークン**: プライマリ、セカンダリ、セマンティック色
2. **タイポグラフィ**: フォントファミリー、サイズ、ウェイト、行間
3. **スペーシング**: マージン、パディング、ギャップ
4. **シャドウ**: エレベーション、ボックスシャドウ
5. **ボーダー**: 角丸、線幅、スタイル
6. **アニメーション**: duration、easing

## 禁止事項

**以下は絶対に行わないこと：**
- CSS/Sass/CSS-in-JSの実装コード生成
- 特定のデザインシステムライブラリの提案
- 技術スタック固有の実装詳細

このスキルの目的は「どのようなデザイントークンがあるか」の**情報整理のみ**です。

## 対象範囲

### このスキルで抽出するもの

| カテゴリ | トークン例 |
|---------|----------|
| Color | primary, secondary, error, success, background, text |
| Typography | heading-1, body-large, caption |
| Spacing | xs, sm, md, lg, xl |
| Shadow | elevation-1, elevation-2, elevation-3 |
| Border | radius-sm, radius-md, radius-full |
| Animation | duration-fast, duration-normal, easing-default |

### 抽出レベル

1. **画面レベル**: この画面で使用されているトークン
2. **プロジェクトレベル**: Figma Variables（利用可能な場合）

## 出力先

このスキルは**画面仕様書（spec.md）の「デザイントークン」セクション**を更新します。

```
.outputs/{screen-id}/
├── spec.md                 # ← このスキルが「デザイントークン」セクションを更新
├── index.html              # 参照用HTML
└── assets/
```

## クイックスタート

### 基本的な使い方

```
以下のFigma画面で使用されているデザイントークンを抽出してください：
https://figma.com/design/XXXXX/Project?node-id=1234-5678
```

エージェントは自動的に：
1. Figma Variablesを取得（利用可能な場合）
2. 画面内で使用されている色・フォント・スペーシングを分析
3. トークン一覧を整理
4. **spec.md の「デザイントークン」セクションを更新**

## 詳細ガイド

詳細な情報は以下のファイルを参照してください：

- **[workflow.md](references/workflow.md)**: トークン抽出のワークフロー
- **[token-categories.md](references/token-categories.md)**: トークンカテゴリと命名規則
- **[section-template.md](references/section-template.md)**: セクション出力テンプレート

## Workflow

デザイントークン抽出時にこのチェックリストをコピー：

```
Design Token Extraction Progress:
- [ ] Step 0: spec.md の存在確認
- [ ] Step 1: Figma Variablesを取得
- [ ] Step 2: カラートークンを抽出
- [ ] Step 3: タイポグラフィトークンを抽出
- [ ] Step 4: スペーシングトークンを抽出
- [ ] Step 5: シャドウトークンを抽出
- [ ] Step 6: その他のトークンを抽出
- [ ] Step 7: トークン使用箇所をマッピング
- [ ] Step 8: spec.md の「デザイントークン」セクションを更新
```

### Step 0: spec.md の存在確認

```bash
ls .outputs/{screen-id}/spec.md
```

### Step 1: Figma Variablesを取得

```bash
mcp__figma__get_variable_defs(fileKey, nodeId)
```

Figma Variablesが定義されている場合、トークン名と値のマッピングを取得。

### Step 2: カラートークンを抽出

画面内で使用されている色を収集：

- 背景色
- テキスト色
- ボーダー色
- アイコン色
- セマンティック色（success, error, warning, info）

### Step 3: タイポグラフィトークンを抽出

- フォントファミリー
- フォントサイズ
- フォントウェイト
- 行間（line-height）
- 字間（letter-spacing）

### Step 4: スペーシングトークンを抽出

- コンポーネント間の余白
- パディング
- ギャップ（Flexbox/Grid）

### Step 5: シャドウトークンを抽出

- ボックスシャドウの値
- エレベーションレベル

### Step 6: その他のトークンを抽出

- ボーダー角丸
- ボーダー幅
- アニメーション duration
- z-index

### Step 7: トークン使用箇所をマッピング

各トークンがどの要素で使用されているかを整理：

| トークン | 使用箇所 |
|---------|---------|
| color/primary | ボタン背景、リンクテキスト |
| color/text/primary | 見出し、本文 |
| spacing/md | カード内パディング |

### Step 8: spec.md の「デザイントークン」セクションを更新

1. セクションを特定（`## デザイントークン`）
2. ステータスを「完了 ✓」に更新
3. `{{DESIGN_TOKENS_CONTENT}}` を内容に置換
4. 完了チェックリストを更新
5. 変更履歴に追記

## 出力形式

### spec.md「デザイントークン」セクションの内容

```markdown
## デザイントークン

> **ステータス**: 完了 ✓  
> **生成スキル**: extracting-design-tokens  
> **更新日**: 2024-01-15

### カラー

#### プライマリ

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| color/primary/default | #0070E0 | ボタン、リンク |
| color/primary/hover | #005BB5 | ホバー状態 |
| color/primary/pressed | #004A99 | 押下状態 |

#### テキスト

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| color/text/primary | #24243F | 見出し、本文 |
| color/text/secondary | #67717A | 補足テキスト |
| color/text/disabled | #9E9E9E | 非活性テキスト |
| color/text/inverse | #FFFFFF | 暗い背景上のテキスト |

#### 背景

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| color/background/primary | #FFFFFF | ページ背景 |
| color/background/secondary | #F8F9F9 | セクション背景 |
| color/background/tertiary | #E8EAED | カード背景 |

#### セマンティック

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| color/success | #2E7D32 | 成功状態 |
| color/error | #D32F2F | エラー状態 |
| color/warning | #F57C00 | 警告状態 |
| color/info | #1976D2 | 情報 |

### タイポグラフィ

| トークン名 | フォント | サイズ | ウェイト | 行間 | 用途 |
|-----------|---------|--------|---------|------|------|
| typography/heading-1 | Noto Sans JP | 32px | 700 | 1.4 | ページタイトル |
| typography/heading-2 | Noto Sans JP | 24px | 700 | 1.4 | セクション見出し |
| typography/heading-3 | Noto Sans JP | 20px | 600 | 1.4 | サブ見出し |
| typography/body-large | Noto Sans JP | 16px | 400 | 1.6 | 本文（強調） |
| typography/body | Noto Sans JP | 14px | 400 | 1.6 | 本文 |
| typography/caption | Noto Sans JP | 12px | 400 | 1.5 | キャプション |
| typography/button | Noto Sans JP | 14px | 600 | 1.0 | ボタンテキスト |

### スペーシング

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| spacing/2xs | 4px | 最小間隔 |
| spacing/xs | 8px | アイコンとテキスト間 |
| spacing/sm | 12px | 関連要素間 |
| spacing/md | 16px | コンポーネント内パディング |
| spacing/lg | 24px | セクション間 |
| spacing/xl | 32px | 大きなセクション間 |
| spacing/2xl | 48px | ページセクション間 |

### シャドウ

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| shadow/sm | 0 1px 2px rgba(0,0,0,0.05) | 軽いエレベーション |
| shadow/md | 0 2px 4px rgba(0,0,0,0.1) | カード |
| shadow/lg | 0 4px 12px rgba(0,0,0,0.15) | ホバー状態 |
| shadow/xl | 0 8px 24px rgba(0,0,0,0.2) | モーダル |

### ボーダー

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| border/radius/sm | 4px | ボタン、入力フィールド |
| border/radius/md | 8px | カード |
| border/radius/lg | 16px | モーダル |
| border/radius/full | 9999px | 円形、ピル型 |
| border/width/default | 1px | 標準線幅 |
| border/color/default | #E0E0E0 | 区切り線、入力ボーダー |

### アニメーション

| トークン名 | 値 | 用途 |
|-----------|-----|------|
| animation/duration/fast | 100ms | 即時フィードバック |
| animation/duration/normal | 200ms | 標準トランジション |
| animation/duration/slow | 300ms | モーダル、大きな変化 |
| animation/easing/default | ease-out | 標準イージング |
| animation/easing/enter | ease-out | 要素の登場 |
| animation/easing/exit | ease-in | 要素の退場 |

### この画面で使用されているトークン

| カテゴリ | トークン | 使用箇所 |
|---------|---------|---------|
| Color | color/primary/default | 送信ボタン背景、講座リンク |
| Color | color/text/primary | ページタイトル、本文 |
| Color | color/background/secondary | カード背景 |
| Typography | typography/heading-1 | ページタイトル |
| Typography | typography/body | 講座説明文 |
| Spacing | spacing/md | カード内パディング |
| Spacing | spacing/lg | カード間ギャップ |
| Shadow | shadow/md | 講座カード |
| Border | border/radius/md | 講座カード |

### 特記事項

- Figma Variablesから取得したトークンは「Figma定義」列に ✓ を記載
- 画面から推測したトークンは「要確認」として明示
```

## 完了チェックリスト

生成後、以下を確認：

```
- [ ] spec.md の「デザイントークン」セクションが更新されている
- [ ] ステータスが「完了 ✓」になっている
- [ ] カラートークンが網羅されている
- [ ] タイポグラフィトークンが網羅されている
- [ ] スペーシングトークンが網羅されている
- [ ] 使用箇所がマッピングされている
- [ ] 完了チェックリストが更新されている
- [ ] 変更履歴に記録が追加されている
```

## 注意事項

### 他のセクションを変更しない

このスキルは「デザイントークン」セクションのみを更新します。

### Figma Variablesがない場合

Figma Variablesが定義されていない場合：

1. 画面内で使用されている値を直接抽出
2. 一般的な命名規則でトークン名を推測
3. 「要確認」として明示

### トークン命名規則

詳細は [token-categories.md](references/token-categories.md) を参照。

基本形式: `{category}/{subcategory}/{variant}`

例：
- `color/primary/default`
- `typography/heading/1`
- `spacing/md`

## 参照

- **[workflow.md](references/workflow.md)**: 詳細なワークフロー
- **[token-categories.md](references/token-categories.md)**: トークンカテゴリと命名規則
- **[section-template.md](references/section-template.md)**: セクション出力テンプレート
- **[managing-screen-specs](../managing-screen-specs/SKILL.md)**: 仕様書管理スキル
