---
name: Setting up Next.js Project
description: Configure Next.js projects with ESLint, Prettier, and recommended settings. Use when initializing Next.js projects, setting up linting, or when user mentions Next.js setup/Next.jsセットアップ.
allowed-tools: Bash, Write, Read, Edit
---

# Setting up Next.js Project

Next.jsプロジェクトのセットアップ時に必要な設定を自動化するスキル。

## いつ使うか

- Next.jsプロジェクトを新規作成する時
- 既存Next.jsプロジェクトにESLint/Prettierを追加する時
- コードフォーマット設定が必要な時
- ユーザーが「Next.jsセットアップ」について言及した時

## セットアップ手順

### 1. ESLint + Prettier の必須インストール

Next.jsはESLintを自動インストールするが、**Prettierも必ず追加**：

```bash
pnpm add -D prettier eslint-config-prettier prettier-plugin-tailwindcss
```

**パッケージの役割**:
- `prettier`: コードフォーマッター
- `eslint-config-prettier`: ESLintとPrettierの競合を防ぐ
- `prettier-plugin-tailwindcss`: Tailwind CSSのクラス順序を整理（Tailwind使用時）

### 2. 設定ファイルの作成

#### `.prettierrc.json`
プロジェクトルートに作成：

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

#### `.eslintrc.json` の更新
既存の設定に `eslint-config-prettier` を追加：

```json
{
  "extends": ["next/core-web-vitals", "prettier"]
}
```

### 3. package.json スクリプトの追加

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
- `pnpm run format:check`: フォーマットチェック（CI用）

### 4. VS Code 設定の推奨

`.vscode/settings.json` を作成（任意）：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## 完全なセットアップフロー

### 新規プロジェクト
```bash
# 1. Next.jsプロジェクト作成
pnpm dlx create-next-app@latest my-app

# 2. ディレクトリ移動
cd my-app

# 3. Prettier追加
pnpm add -D prettier eslint-config-prettier prettier-plugin-tailwindcss

# 4. 設定ファイル作成
# （このスキルが自動で作成）

# 5. フォーマット実行
pnpm run format
```

### 既存プロジェクト
```bash
# 1. Prettier追加
pnpm add -D prettier eslint-config-prettier prettier-plugin-tailwindcss

# 2. 設定ファイル追加
# （このスキルが自動で作成）

# 3. ESLint設定更新
# （このスキルが自動で更新）

# 4. フォーマット実行
pnpm run format
```

## 設定ファイルテンプレート

詳細なテンプレートは [templates/](templates/) を参照。

## チェックリスト

セットアップ完了前に確認：
- [ ] Prettierがインストールされているか
- [ ] `.prettierrc.json` が作成されているか
- [ ] `.eslintrc.json` に `prettier` が追加されているか
- [ ] package.json に format スクリプトが追加されているか
- [ ] `pnpm run format` が正常に動作するか
- [ ] `.vscode/settings.json` の作成を検討したか

## トラブルシューティング

### フォーマットが効かない
1. Prettier拡張がインストールされているか確認
2. `.prettierrc.json` の構文エラーを確認
3. ESLintとの競合を確認（`eslint-config-prettier` が必要）

### Tailwind CSSのクラス順序が整わない
1. `prettier-plugin-tailwindcss` がインストールされているか確認
2. `.prettierrc.json` にプラグイン設定を追加

## 参考リンク

- [Prettier公式ドキュメント](https://prettier.io/docs/en/)
- [Next.js ESLint設定](https://nextjs.org/docs/basic-features/eslint)
