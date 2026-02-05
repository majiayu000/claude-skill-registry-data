---
name: new-component
description: React コンポーネントとStorybookストーリーを生成。新しいコンポーネントを作成する際に使用。TailwindCSSカスタムトークン、ArteOdyssey UIライブラリを活用。
---

# 新規コンポーネント生成スキル

このスキルは、k8o プロジェクトの規約に従ったReactコンポーネントを生成します。

## 生成されるファイル

1. **コンポーネントファイル** (`component-name.tsx`) - kebab-case
2. **Storybookストーリー** (`component-name.stories.tsx`) - kebab-case
3. **エクスポートファイル** (`index.ts`) - コンポーネントのエクスポート用

## プロジェクト規約

### 配置場所

- **アプリ共通コンポーネント**: `apps/main/src/app/_components/`
- **ページ固有コンポーネント**: `apps/main/src/app/[page]/_components/`

### スタイリング

- **TailwindCSS**: ArteOdyssey (`@k8o/arte-odyssey/styles.css`) で定義されたカスタムトークンのみ使用
- **禁止**: 標準のTailwindクラス（`text-gray-600`など）は使用禁止

利用可能なカスタムクラス例：
- テキスト色: `text-fg-base`, `text-fg-subtle`, `text-fg-mute`, `text-fg-info`
- 背景色: `bg-bg-base`, `bg-bg-subtle`, `bg-bg-mute`, `bg-primary-bg`
- ボーダー色: `border-border-base`, `border-border-subtle`, `border-primary-border`
- フォントサイズ: `text-xs`, `text-sm`, `text-md`（カスタム定義）
- Font Weight: `font-medium`, `font-bold`（カスタム定義）
- Radius: `rounded-sm`, `rounded-md`, `rounded-lg`（カスタム定義）

### Storybook

- **必須**: すべてのコンポーネントに `.stories.tsx` が必要
- **Import**: `@storybook/nextjs-vite` から `Meta`, `StoryObj` をimport
- **Test**: `storybook/test` から `fn`, `expect`, `userEvent` などをimport（必要に応じて）

## 使用方法

### 基本的な使い方

ユーザーがコンポーネント名と配置場所を指定すると、このスキルが自動的に呼び出されます。

例：
```
「Buttonコンポーネントを apps/main/src/app/_components/ に作成して」
```

### 生成手順

1. **ユーザーに確認**:
   - コンポーネント名（PascalCase）
   - 配置パス（`apps/main/src/app/_components/` または `apps/main/src/app/[page]/_components/`）
   - コンポーネントの用途・機能
   - **実装レベル（新規追加）**:
     - **テンプレートのみ**: 基本的なテンプレートのみ生成（TODOコメント付き）
     - **具体的実装**: ユーザーの要件に基づいて具体的な実装を含むコンポーネントを生成

2. **テンプレートから生成**:
   - `templates/component.tsx.template` からコンポーネントを生成
   - `templates/component.stories.tsx.template` からストーリーを生成
   - プレースホルダーを置換:
     - `{{COMPONENT_NAME}}`: コンポーネント名（例: `Button`）
     - `{{COMPONENT_PATH}}`: コンポーネントへの相対パス（例: `./button`）
     - `{{DESCRIPTION}}`: コンポーネントの説明

3. **ファイルを作成**:
   - `{path}/{component-name}/{component-name}.tsx` (kebab-case)
   - `{path}/{component-name}/{component-name}.stories.tsx` (kebab-case)
   - `{path}/{component-name}/index.ts` (kebab-case)

4. **index.ts を生成**:
   - コンポーネントと型のエクスポートを含む index.ts を作成
   - フォーマット: `export { ComponentName, type ComponentNameProps } from './component-name';`

5. **Storybook URLを提供**:
   - `mcp__storybook-mcp__get-story-urls` ツールを使用してストーリーのURLを取得
   - ユーザーに提供してブラウザで確認可能にする

## テンプレート

### コンポーネントテンプレート (`templates/component.tsx.template`)

基本的なReactコンポーネントのテンプレート：
- TypeScript + React
- Props型定義はFC内に直接記述（外部からclassNameを受け取らない設計）
- ArteOdysseyのUIコンポーネント活用
- TailwindCSSカスタムトークン使用
- 日本語コメント
- Next.js の Image コンポーネントを使用（img タグは禁止）

### Storybookテンプレート (`templates/component.stories.tsx.template`)

Storybook 10の規約に従ったシンプルなストーリー：
- `@storybook/nextjs-vite` からimport
- 基本的なDefaultストーリーのみ
- 必要に応じてストーリーを追加

### index.ts テンプレート (`templates/index.ts.template`)

コンポーネントのエクスポート用：
- コンポーネント名のみをエクスポート
- 型は必要に応じてコンポーネントファイルからインポート

## ArteOdysseyコンポーネント

再利用可能なUIコンポーネントは `@k8o/arte-odyssey` パッケージから利用可能：

```typescript
import { Button } from '@k8o/arte-odyssey';
```

利用可能なコンポーネント例：
- `Button`, `IconButton`
- `Input`, `Textarea`, `Select`
- `Card`, `Dialog`, `Tooltip`
- `Loading`, `ErrorBoundary`

## 注意事項

- **コメント**: 日本語コメント推奨
- **テスト**: Storybookストーリーで基本的なインタラクションテストを記述
- **アクセシビリティ**: ArteOdysseyコンポーネントはアクセシビリティ対応済み
- **スタイル**: 標準のTailwindクラスは使用せず、必ずArteOdysseyのカスタムトークンを使用
- **画像**: img タグは使用禁止。必ず Next.js の Image コンポーネント (`next/image`) を使用
- **ファイル構成**: コンポーネントごとにディレクトリを作成し、その中に `.tsx`, `.stories.tsx`, `index.ts` をまとめる
- **実装レベル**: ユーザーに実装レベル（テンプレートのみ or 具体的実装）を確認してから生成する

## 例

### 使用例1: ボタンコンポーネント

```
「Buttonコンポーネントを apps/main/src/app/_components/ に作成して。
プライマリ、セカンダリ、危険の3つのバリアントを持つボタン」
```

### 使用例2: カード型コンポーネント

```
「BlogCardコンポーネントを apps/main/src/app/blog/_components/ に作成して。
タイトル、説明、タグ、公開日を表示するカード」
```

### 使用例3: フォームコンポーネント

```
「ContactFormコンポーネントを apps/main/src/app/contact/_components/ に作成して。
名前、メール、メッセージの入力フィールドと送信ボタン」
```
