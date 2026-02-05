---
name: github-issue-quality-checker
description: >
  Open状態のGitHub Issueから低品質・曖昧なIssueを検出して分析するスキル。
  「Issueが多すぎてどれから対応すべきか分からない」「質問や報告の質を上げたい」場合に使用。
  環境変数で指定されたリポジトリのIssueを品質評価し、最もスコアの低いIssueを特定する。
---

# GitHub Issue Quality Checker

## Overview

GitHubリポジトリのOpen状態のIssueを自動で分析し、品質が低い・内容が曖昧なIssueを検出するスキル。タイトルの曖昧さ、本文の情報不足、環境情報の欠如などを総合評価し、開発者が対応すべき優先度の高いIssueを特定します。

## Quick Start

### 環境設定

```bash
# GitHub Personal Access Tokenを設定
export GITHUB_TOKEN="ghp_your_token_here"

# 対象リポジトリを設定
export GITHUB_REPOSITORY="owner/repository-name"
```

### 基本実行

```bash
# テキスト形式で結果出力（デフォルト）
python scripts/main.py

# JSON形式で結果出力
python scripts/main.py --output-format json

# コマンドライン引数で直接指定
python scripts/main.py --repository owner/repo --output-format text
```

## Core Capabilities

### 1. Issue品質評価アルゴリズム

#### 評価項目
- **タイトル評価**（40点満点）：文字数、曖昧さパターン
- **本文評価**（60点満点）：文字数、情報量
- **情報量ボーナス**：環境情報、再現手順、エラー情報などの有無
- **その他**：ラベルの有無、コードブロックの有無

#### スコアリング方式
- 満点100点から減点方式
- 低いスコアほど品質が低い
- 詳細な評価基準は `references/quality_criteria.md` を参照

### 2. 出力形式

#### テキスト形式
- Issue詳細情報
- 品質スコアと評価理由
- タイトル・本文のプレビュー
- 対応すべき理由の明示

#### JSON形式
- 機械処理可能な構造化データ
- CI/CDパイプラインでの利用に適した形式

### 3. GitHub API連携

- GitHub REST API v3使用
- 認証済みリクエスト（5,000 req/hour）
- レート制限対応
- エラーハンドリング実装

## 使用例

### 基本的な利用シーン

```bash
# リポジトリのIssue品質をチェック
python scripts/main.py
```

### CI/CDでの活用

```yaml
- name: Check Issue Quality
  run: |
    python .claude/skills/github-issue-quality-checker/scripts/main.py --output-format json > quality_report.json
    # レポートを解析してアクション
```

### 定期メンテナンス

```bash
# 毎週のIssue品質チェック
echo "Weekly Issue Quality Report:"
python scripts/main.py
```

## Resources

### scripts/

**main.py** - メイン実行スクリプト
- GitHub API連携
- Issue品質評価ロジック
- 結果出力とフォーマット
- コマンドライン引数処理

### references/

**quality_criteria.md** - 品質評価基準の詳細
- スコアリングアルゴリズム
- 評価項目と配点
- 具体的な計算例
- 品質判断の目安

**github_api_usage.md** - GitHub API使用ガイド
- APIエンドポイント詳細
- 認証方法と権限
- レート制限情報
- セキュリティ考慮事項

**api_reference.md** - クイックリファレンス
- 環境変数一覧
- コマンドライン使用法
- 出力形式仕様

### assets/

**output_template.md** - 結果出力テンプレート
- テキスト形式の出力フォーマット
- Markdownレポートのテンプレート構造

## Quality Criteria Reference

詳細な品質評価基準は `references/quality_criteria.md` を参照してください。

## GitHub API Usage

GitHub APIの詳細な使用方法は `references/github_api_usage.md` を参照してください。

---

**Dependencies:** Python 3.7+, requests library
