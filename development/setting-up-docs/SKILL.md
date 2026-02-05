---
name: setting-up-docs
description: >
  コードベース分析から環境セットアップガイドドキュメントを生成。
  パッケージマネージャ、必要なツール、環境変数、起動コマンドを検出。
  トリガー: setup guide, environment setup, development environment,
  installation guide, getting started, prerequisites.
allowed-tools: Read, Write, Grep, Glob, Bash, Task
---

# docs:setup - 環境セットアップガイド生成

コードベース分析からセットアップドキュメントを自動生成。

## 検出項目

| カテゴリ | 対象 |
| --- | --- |
| パッケージマネージャ | package.json, yarn.lock, pnpm-lock, pyproject.toml, Cargo.toml, go.mod, pubspec.yaml, Gemfile, pom.xml |
| ツールバージョン | .nvmrc, .python-version, .ruby-version, .tool-versions, rust-toolchain.toml |
| 環境 | .env.example, .env.sample, .env.template |
| コンテナ | Dockerfile, docker-compose.yml, .devcontainer/ |
| コマンド | package.json scripts, Makefile, README |

## 生成構造

```markdown
# 環境セットアップガイド

## 前提条件
- ランタイム & バージョン
- 必要なツール

## インストール手順
1. リポジトリをクローン
2. 依存関係をインストール
3. 環境変数を設定

## 環境変数
| 変数 | 説明 | 必須 |

## プロジェクトの実行
- 開発サーバーを起動
- ビルド
- テストを実行

## Docker（オプション）
```

## 使用方法

```bash
/docs:setup                   # セットアップガイド生成
"Generate environment setup"  # 自然言語
```

## Markdownバリデーション

生成後、出力を検証:

```bash
~/.claude/skills/scripts/validate-markdown.sh {output-file}
```

ブロッキングなし（警告のみ） - スタイル問題はドキュメント作成をブロックしない。

## 参照

- 関連: `documenting-architecture`, `documenting-apis`, `documenting-domains`
