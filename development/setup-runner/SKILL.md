---
name: setup-runner
description: GitHub 設定ファイルをセットアップする。「GitHub 設定をセットアップ」「.github を作って」「Issue テンプレート作成」「PR テンプレート作成」「GitHub 設定を初期化」「リポジトリ設定をセットアップ」「ラベル設定を作成」などで起動。.github ディレクトリに必要な設定ファイルを一括生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Setup Runner

GitHub 設定ファイルを一括生成します。

## 実行内容

1. `commands/setup.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-git:setup` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/setup.md` - 機能の詳細
- `/shiiman-git:setup` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-git:setup` に委譲します（SSOT として扱う）

## 生成ファイル

テンプレートファイルは `assets/` ディレクトリに配置:

- `assets/ISSUE_TEMPLATE/` - Issue テンプレート
- `assets/pull_request_template.md` - PR テンプレート
- `assets/copilot-instructions.md` - Copilot 設定
- `assets/labels.yml` - ラベル定義
- `assets/labeler.yml` - 自動ラベル付けルール
- `assets/workflows/` - GitHub Actions workflow
