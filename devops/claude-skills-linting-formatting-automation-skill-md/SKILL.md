---
name: .claude/skills/linting-formatting-automation/SKILL.md
description: |
  コード品質とフォーマット自動化の専門スキル。
  ESLint、Prettier、Biome、Stylelintなどのリンターとフォーマッターのセットアップ、
  設定、CI/CD統合、pre-commitフック構築、エディタ統合を提供します。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/linting-formatting-automation/resources/eslint-config-guide.md`: ESLint設定ガイド（ルール選択、プラグイン統合、カスタムルール）
  - `.claude/skills/linting-formatting-automation/resources/prettier-biome-comparison.md`: Prettier vs Biome 比較（パフォーマンス、機能、移行戦略）
  - `.claude/skills/linting-formatting-automation/resources/pre-commit-hook-setup.md`: pre-commitフックセットアップ（husky、lint-staged統合）
  - `.claude/skills/linting-formatting-automation/resources/ci-cd-integration.md`: CI/CD統合ガイド（GitHub Actions、GitLab CI）
  - `.claude/skills/linting-formatting-automation/scripts/setup-linter.sh`: リンター自動セットアップスクリプト
  - `.claude/skills/linting-formatting-automation/templates/eslintrc-template.json`: ESLint設定テンプレート
  - `.claude/skills/linting-formatting-automation/templates/prettier-config-template.json`: Prettier設定テンプレート
  - `.claude/skills/linting-formatting-automation/templates/biome-config-template.json`: Biome設定テンプレート

  使用タイミング:
  - 新規プロジェクトのリンター/フォーマッター初期設定時
  - 既存プロジェクトのコード品質改善時
  - CI/CDパイプラインへのリント追加時
  - pre-commitフック構築時
  - ESLint → Biomeなどのツール移行時

  関連スキル:
  - `.claude/skills/prettier-integration/SKILL.md` - Prettier詳細統合
  - `.claude/skills/code-quality/SKILL.md` - コード品質基準と評価
  - `.claude/skills/github-actions-workflows/SKILL.md` - GitHub Actions CI/CD

  Use proactively when setting up linting/formatting tools,
  integrating code quality checks into CI/CD, or configuring
  pre-commit hooks for consistent code style enforcement.

version: 1.0.0
---

# リンティング・フォーマット自動化スキル

## 概要

このスキルは、コード品質を自動的に維持するためのリンティングツールと
フォーマッターの設定・統合に関する知識を提供します。
一貫したコードスタイルとエラー防止を実現します。

**主要な価値**:

- 一貫したコードスタイルの自動維持
- 潜在的なバグの早期発見
- コードレビューの効率化（スタイル議論の削減）

**対象ユーザー**:

- `.claude/agents/code-quality.md`エージェント
- フロントエンド開発者
- バックエンド開発者
- DevOpsエンジニア

## いつ使うか

### シナリオ 1: 新規プロジェクトセットアップ

**状況**: 新しいプロジェクトでコード品質ツールを設定する

**適用条件**:

- [ ] プロジェクトの言語/フレームワークが決定している
- [ ] チームのコードスタイルガイドがある（またはデフォルト使用）
- [ ] パッケージマネージャーが利用可能

**期待される成果**: 一貫したリンティング/フォーマット環境

### シナリオ 2: CI/CD統合

**状況**: プルリクエスト時に自動でコード品質をチェックしたい

**適用条件**:

- [ ] CI/CDプラットフォームが利用可能
- [ ] リンターの設定が完了している
- [ ] テストとの統合方針が決定している

**期待される成果**: 自動化されたコード品質ゲート

### シナリオ 3: ツール移行

**状況**: ESLint + Prettier から Biome に移行する等

**適用条件**:

- [ ] 移行理由が明確（パフォーマンス、設定簡素化等）
- [ ] 既存ルールの移行計画がある
- [ ] チームの合意が取れている

**期待される成果**: スムーズなツール移行と設定継承

## 主要ツール比較

### JavaScript/TypeScript

| ツール   | 用途               | 特徴                       |
| -------- | ------------------ | -------------------------- |
| ESLint   | リンティング       | 最も成熟、豊富なプラグイン |
| Prettier | フォーマッティング | オピニオネイテッド、設定少 |
| Biome    | 両方               | 高速、Rust製、設定簡素     |

### 推奨組み合わせ

```yaml
シンプル志向:
  - Biome (リンティング + フォーマッティング)
  - メリット: 設定が少ない、高速
  - デメリット: ESLintほどのプラグインエコシステムがない

成熟志向:
  - ESLint + Prettier
  - メリット: 豊富なプラグイン、カスタマイズ性
  - デメリット: 設定が複雑になりがち
```

## セットアップガイド

### ESLint + Prettier (TypeScript)

```bash
# パッケージインストール
pnpm add -D eslint prettier eslint-config-prettier \
  @typescript-eslint/parser @typescript-eslint/eslint-plugin

# 設定ファイル作成
touch eslint.config.js .prettierrc
```

**eslint.config.js** (Flat Config):

```javascript
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import prettier from "eslint-config-prettier";

export default [
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: "./tsconfig.json",
      },
    },
    plugins: {
      "@typescript-eslint": tseslint,
    },
    rules: {
      ...tseslint.configs.recommended.rules,
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/explicit-function-return-type": "warn",
    },
  },
  prettier,
];
```

**.prettierrc**:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

### Biome (オールインワン)

```bash
# インストール
pnpm add -D @biomejs/biome

# 初期化
pnpm biome init
```

**biome.json**:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": {
        "useConst": "error",
        "noVar": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  }
}
```

## Pre-commitフック設定

### Husky + lint-staged

```bash
# インストール
pnpm add -D husky lint-staged

# Husky初期化
pnpm exec husky init

# pre-commitフック作成
echo "pnpm lint-staged" > .husky/pre-commit
```

**package.json**:

```json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

### Biome版

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx,json}": ["biome check --write"]
  }
}
```

## CI/CD統合

### GitHub Actions

```yaml
name: Code Quality

on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install

      # ESLint + Prettier
      - name: Lint
        run: pnpm eslint . --max-warnings 0
      - name: Check Format
        run: pnpm prettier --check .

      # または Biome
      - name: Biome Check
        run: pnpm biome ci .
```

## トラブルシューティング

### 問題 1: ESLintとPrettierの競合

**症状**: フォーマット後にESLintエラーが発生

**原因**: PrettierとESLintのルールが競合

**解決策**:

```bash
# eslint-config-prettierを最後に適用
# eslint.config.js で prettier を配列の最後に追加
```

### 問題 2: pre-commitが遅い

**症状**: コミット時に数十秒待つ

**原因**: 全ファイルをチェックしている

**解決策**:

```json
{
  "lint-staged": {
    "*.ts": ["eslint --fix --cache", "prettier --write"]
  }
}
```

`--cache`オプションで差分のみチェック

### 問題 3: VS Codeで自動フォーマットが効かない

**症状**: 保存時にフォーマットされない

**解決策** (.vscode/settings.json):

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

## ベストプラクティス

### すべきこと

1. **段階的に厳格化**: 最初は警告、安定したらエラーに
2. **キャッシュ活用**: `eslint --cache`でパフォーマンス改善
3. **エディタ統合**: 保存時自動フォーマットを設定
4. **CI必須化**: PRマージ前のリントチェック必須

### 避けるべきこと

1. **過度なカスタマイズ**: 標準ルールセットを尊重
2. **ルールの無効化乱用**: `eslint-disable`は最小限に
3. **フォーマット議論**: Prettierのオピニオンを受け入れる

## チェックリスト

### 初期設定時

- [ ] リンター/フォーマッターをインストール
- [ ] 設定ファイルを作成
- [ ] package.jsonにスクリプト追加
- [ ] エディタ設定を追加(.vscode/settings.json)
- [ ] .gitignoreにキャッシュファイル追加

### pre-commit設定時

- [ ] husky + lint-stagedをインストール
- [ ] pre-commitフックを作成
- [ ] lint-staged設定を追加
- [ ] 全員がフックを有効化（postinstall）

### CI/CD設定時

- [ ] ワークフローファイルを作成
- [ ] キャッシュを設定（node_modules、ESLintキャッシュ）
- [ ] 失敗時のPRブロックを設定
- [ ] エラーレポートのフォーマット調整

## 関連スキル

- **.claude/skills/code-style-guides/SKILL.md** (`.claude/skills/code-style-guides/SKILL.md`): コードスタイルガイドライン
- **.claude/skills/clean-code-practices/SKILL.md** (`.claude/skills/clean-code-practices/SKILL.md`): クリーンコード原則

## 参考文献

- **ESLint**: https://eslint.org/docs/latest/
- **Prettier**: https://prettier.io/docs/en/
- **Biome**: https://biomejs.dev/
- **Husky**: https://typicode.github.io/husky/
- **lint-staged**: https://github.com/lint-staged/lint-staged
