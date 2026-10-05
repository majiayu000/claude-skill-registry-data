---
name: gh
description: |
  GitHub CLI (gh) を使用してリポジトリ、PR、Issue、Actions などの GitHub リソースを操作する。
  主な用途: (1) リポジトリの表示・クローン、(2) PR/Issue の一覧表示・作成、(3) GitHub Actions の実行状況確認。
---

# GitHub CLI (gh) Skill

GitHub CLI (`gh`) は、コマンドラインから GitHub の各機能（Issue, Pull Request, Repository, Actions など）をシームレスに操作するためのツールです。

## 基本的な考え方

`gh` は「名詞 + 動詞」の構造でコマンドが構成されています。
例: `gh repo view`, `gh pr create`, `gh issue list`

## 主要なサブコマンドの概要

### リポジトリ操作 (`gh repo`)
- `gh repo view`: 現在のリポジトリ情報を表示
- `gh repo clone <repo>`: リポジトリをクローン
- `gh repo create`: 新規リポジトリを作成

### プルリクエスト操作 (`gh pr`)
- `gh pr list`: プルリクエストの一覧表示
- `gh pr view`: プルリクエストの詳細表示
- `gh pr create`: プルリクエストの作成
- `gh pr checkout <number>`: プルリクエストのブランチへ切り替え

### イシュー操作 (`gh issue`)
- `gh issue list`: イシューの一覧表示
- `gh issue view`: イシューの詳細表示
- `gh issue create`: イシューの作成

### GitHub Actions 操作 (`gh run`, `gh workflow`)
- `gh run list`: ワークフローの実行履歴を表示
- `gh run view`: 実行詳細の表示
- `gh workflow list`: ワークフロー一覧の表示

### その他便利なコマンド
- `gh status`: 自分に関連する Issue, PR, 通知のサマリーを表示
- `gh auth status`: 認証状態の確認
- `gh search <type> <query>`: リポジトリ、Issue、PR の検索
- `gh api`: GitHub API への直接リクエスト

## 使用上の注意
- 操作対象のリポジトリディレクトリ内で実行すると、自動的にそのコンテキストが反映されます。
- `--json` フラグと `--jq` フラグを組み合わせることで、出力を柔軟にパースして後続の処理に利用できます。
- インタラクティブモードが標準で備わっていますが、自動化の際はフラグ（`-t`, `-b` など）を明示的に指定することが推奨されます。
