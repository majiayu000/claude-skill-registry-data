---
name: new-windows-forms-component
description: Windows Forms風のAstroコンポーネントとデモページを一貫性を持って自動生成します。コンポーネント名を指定すると、.astroファイル、デモページ、ナビゲーションリンクを自動作成します。
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash"
---

# 新規Windows Formsコンポーネント作成

このスキルは、Windows Forms風のAstroコンポーネントとそのデモページを一貫性を持って自動生成します。

## 実行手順

1. **ユーザーにコンポーネント名を質問**
   - 「作成したいコンポーネント名を入力してください（例: Slider, ListView, DatePicker）」
   - コンポーネント名はPascalCaseで受け取る

2. **コンポーネントファイルの作成**
   - ファイルパス: `src/components/ui/{ComponentName}.astro`
   - 以下の要素を含める：
     * TypeScriptインターフェースでProps定義（JSDocコメント付き）
     * デフォルト値の設定（分割代入）
     * `<slot>`による子要素の受け取り
     * Windows Forms風のスタイル：
       - `font-family: 'Segoe UI', Tahoma, sans-serif`
       - グラデーション背景（`linear-gradient`）
       - 立体的なボーダー（`border: 1px solid #adadad`）
       - ホバー、アクティブ、無効化状態の実装
       - フォーカススタイル（`outline: 1px dotted #000`）
   - 既存コンポーネント（Button.astro等）を参考にする

3. **デモページの作成**
   - ファイルパス: `src/pages/{componentname}-demo.mdx`
   - 内容：
     * `BaseLayout`をimportして使用
     * コンポーネントをimport
     * タイトル（h1）とコンポーネントの説明
     * 使用例セクション（複数のバリエーション）
     * Props一覧表（マークダウンテーブル形式）
   - 既存デモページ（button-demo.mdx等）を参考にする

4. **ナビゲーションへの追加**
   - `src/layouts/BaseLayout.astro`のnavセクションにリンクを追加
   - 形式: `<a href="/{componentname}-demo">{日本語名}</a>`
   - アルファベット順または適切な位置に挿入

5. **確認**
   - 作成したファイルの内容をユーザーに報告
   - `npm run dev`で動作確認するよう提案

## 注意事項

- コンポーネント名は必ずPascalCaseで統一
- デモページのファイル名は小文字のkebab-case
- 日本語のドキュメントを作成
- Windows Formsのデザインパターンに厳密に従う
- 既存コンポーネントとの一貫性を保つ
