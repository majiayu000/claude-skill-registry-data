---
name: Setting up Prettier
description: Configure Prettier for any JavaScript/TypeScript project with recommended settings. Use when setting up code formatting, adding Prettier to existing projects, or when user mentions Prettier setup/フォーマッター設定.
allowed-tools: Bash, Write, Read, Edit
---

# Setting up Prettier

あらゆるJavaScript/TypeScriptプロジェクトでPrettierを導入・設定するスキル。

## いつ使うか

- 新規プロジェクトにPrettierを導入する時
- 既存プロジェクトにコードフォーマッターを追加する時
- コードフォーマット設定が必要な時
- チーム開発でコードスタイルを統一したい時
- ユーザーが「Prettierセットアップ」「フォーマッター設定」について言及した時

## セットアップ手順

### 1. Prettierのインストール

**基本パッケージ**（必須）：
```bash
pnpm add -D prettier
```

**ESLintと併用する場合**（推奨）：
```bash
pnpm add -D prettier eslint-config-prettier
```

**パッケージの役割**:
- `prettier`: コードフォーマッター本体
- `eslint-config-prettier`: ESLintとPrettierの競合を防ぐ（ESLint使用時のみ）

### 2. プロジェクト固有のプラグイン（任意）

プロジェクトに応じて追加：

```bash
# Tailwind CSS を使用している場合
pnpm add -D prettier-plugin-tailwindcss

# Svelte を使用している場合
pnpm add -D prettier-plugin-svelte

# その他のプラグインも必要に応じて追加可能
```

### 3. 設定ファイルの作成

#### `.prettierrc.json`
プロジェクトルートに作成（推奨設定）：

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "useTabs": false,
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "always"
}
```

**設定項目の説明**：
- `semi`: セミコロンを付ける（true推奨）
- `singleQuote`: シングルクォート使用（チーム次第）
- `trailingComma`: 末尾カンマ（"es5"推奨）
- `tabWidth`: インデント幅（2または4）
- `printWidth`: 1行の最大文字数（80-120推奨）

#### `.prettierignore`（任意）
フォーマット対象外のファイルを指定：

```
# dependencies
node_modules
.pnp
.pnp.js

# builds
dist
build
.next
out

# misc
.DS_Store
*.log
.env*

# lock files
pnpm-lock.yaml
package-lock.json
yarn.lock
```

### 4. ESLintとの統合（ESLint使用時）

`.eslintrc.json` を更新して、Prettierとの競合を防ぐ：

**既存の設定がある場合**：
```json
{
  "extends": [
    "existing-config",
    "prettier"  // ← 最後に追加（重要）
  ]
}
```

**Next.jsの場合の例**：
```json
{
  "extends": ["next/core-web-vitals", "prettier"]
}
```

**Reactの場合の例**：
```json
{
  "extends": ["react-app", "prettier"]
}
```

### 5. package.json スクリプトの追加

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

**使い方**:
- `pnpm run format`: 全ファイルをフォーマット
- `pnpm run format:check`: フォーマットチェックのみ（CI用）

### 6. VS Code 設定の推奨

`.vscode/settings.json` を作成（任意だが推奨）：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## 完全なセットアップフロー

### 新規プロジェクト
```bash
# 1. プロジェクト作成（例：Vite）
pnpm create vite my-app

# 2. ディレクトリ移動
cd my-app

# 3. Prettier追加
pnpm add -D prettier eslint-config-prettier

# 4. 設定ファイル作成
# （このスキルが自動で作成）

# 5. フォーマット実行
pnpm run format
```

### 既存プロジェクト
```bash
# 1. Prettier追加
pnpm add -D prettier eslint-config-prettier

# 2. 設定ファイル追加
# （このスキルが自動で作成）

# 3. ESLint設定更新（使用している場合）
# （このスキルが自動で更新）

# 4. フォーマット実行
pnpm run format
```

## プロジェクトタイプ別の推奨設定

### React / Next.js
```bash
pnpm add -D prettier eslint-config-prettier
# Tailwind使用時は追加
pnpm add -D prettier-plugin-tailwindcss
```

### Vue / Nuxt
```bash
pnpm add -D prettier eslint-config-prettier
```

### Svelte / SvelteKit
```bash
pnpm add -D prettier prettier-plugin-svelte eslint-config-prettier
```

### Node.js / Express
```bash
pnpm add -D prettier eslint-config-prettier
```

## 設定ファイルテンプレート

詳細なテンプレートは [templates/](templates/) を参照。

## チェックリスト

セットアップ完了前に確認：
- [ ] Prettierがインストールされているか
- [ ] `.prettierrc.json` が作成されているか
- [ ] `.prettierignore` が作成されているか（任意）
- [ ] ESLint使用時は `.eslintrc.json` に `prettier` が追加されているか
- [ ] package.json に format スクリプトが追加されているか
- [ ] `pnpm run format` が正常に動作するか
- [ ] `.vscode/settings.json` の作成を検討したか

## トラブルシューティング

### フォーマットが効かない
1. **VS Code拡張がインストールされているか確認**
   - Prettier - Code formatter (`esbenp.prettier-vscode`)
2. **設定ファイルの構文エラーを確認**
   - `.prettierrc.json` の JSON構文
3. **ESLintとの競合を確認**
   - `eslint-config-prettier` がインストールされているか
   - `.eslintrc.json` の extends に `"prettier"` が最後に追加されているか

### 特定のファイルがフォーマットされない
1. `.prettierignore` で除外されていないか確認
2. ファイルの拡張子がPrettierでサポートされているか確認
3. プラグインが必要な場合は追加（例：.svelte ファイル）

### 保存時にフォーマットされない
1. VS Codeの設定を確認
   - `"editor.formatOnSave": true` が設定されているか
   - `"editor.defaultFormatter"` が正しく設定されているか
2. ワークスペース設定とユーザー設定の競合確認

### Tailwind CSSのクラス順序が整わない
1. `prettier-plugin-tailwindcss` がインストールされているか確認
2. `.prettierrc.json` にプラグイン設定を追加（プラグインが自動検出する場合もある）

## CI/CD での使用

### GitHub Actions 例
```yaml
- name: Check code formatting
  run: pnpm run format:check
```

### Pre-commit Hook（Husky使用時）
```bash
pnpm add -D husky lint-staged

# .husky/pre-commit
pnpm lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,json,css,md}": [
      "prettier --write"
    ]
  }
}
```

## 参考リンク

- [Prettier公式ドキュメント](https://prettier.io/docs/en/)
- [Prettier Playground](https://prettier.io/playground/)
- [ESLintとの統合](https://prettier.io/docs/en/integrating-with-linters.html)
- [プラグイン一覧](https://prettier.io/docs/en/plugins.html)
