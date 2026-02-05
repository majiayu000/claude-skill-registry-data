---
name: github-issue-improver
description: >
  自動的にGitHub Issueを分析し、構造化された内容に改善するスキル。
  雑なIssueや情報不足のIssueをAIが作業しやすい形式に自動補完・加筆訂正する。
  タイトルの標準化、本文の構造化、適切なラベル付与、不足情報の指摘を行う。
  「このIssueを改善して」「Issue内容を整えて」といった依頼で使用。
---

# GitHub Issue Improver

## Overview

このスキルはGitHub Issueの品質を自動的に改善します。雑な記述のIssueを分析し、構造化されたAIが作業しやすい形式に変換します。Issueの種類を自動分類し、適切なテンプレートを適用して不足情報を指摘します。

## Quick Start

### 基本的な使い方

```bash
# 単一のIssueを改善（コメントとして提案を追加）
python scripts/issue_improver.py --repo owner/repo --issue 123

# Issueを直接更新
python scripts/issue_improver.py --repo owner/repo --issue 123 --mode update --update-title --update-body --update-labels

# 複数のIssueを一括改善
python scripts/issue_improver.py --repo owner/repo --issues 123 124 125 --mode comment

# どのような改善がされるか確認（実際には変更しない）
python scripts/issue_improver.py --repo owner/repo --issue 123 --dry-run

# JSONファイルから一括適用
python scripts/apply_improvements.py --repo owner/repo apply --improvements-file improvements.json

# JSONファイルから適用内容をプレビュー
python scripts/apply_improvements.py --repo owner/repo --dry-run apply --improvements-file improvements.json
```

### 環境設定

**方法1: .envファイルを使用（推奨）**
```bash
# .envファイルを作成
echo "GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> .env

# .envファイルは自動的に読み込まれます
```

**方法2: 環境変数**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**方法3: 直接指定**
```bash
python scripts/issue_improver.py --repo owner/repo --issue 123 --token your_token
```

### 🆕 新機能

#### 1. 自動.envファイル読み込み
- `.env`ファイルを複数の場所から自動検出
- スクリプト実行ディレクトリ、カレントディレクトリ、プロジェクトルート
- python-dotenvがなくても動作（推奨）

#### 2. 完全なDry-runモード
- `--dry-run`で完全にオフラインで動作
- GitHub APIコールなしで改善案を生成
- Token不要でテスト可能

#### 3. JSONベースの一括改善
- `apply_improvements.py`でJSONファイルから改善を適用
- 改善テンプレートの生成機能
- レビューと承認ワークフローに対応

## Core Capabilities

### 1. Issue自動分析
- **種類分類**: bug, feature, documentation, test, refactorなどを自動判定
- **重要度評価**: critical, high, medium, lowの優先度を自動設定
- **コンポーネント抽出**: frontend, backend, apiなどの関連コンポーネントを特定
- **品質スコアリング**: Issueの品質を0-1のスコアで評価

### 2. 標準化されたタイトル生成
- Coventional Commitsスタイルのプレフィックス付与
```
元: login fails
改善: Fix: Login fails with invalid credentials
```

### 3. 構造化された本文生成
- 種類に応じたテンプレート自動適用
- 不足情報の指摘と入力枠の追加
- マークダウン形式での整形

**バグ報告の例:**
```markdown
## Bug Description
[自動生成された説明]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[ここに期待される動作を記述]

## Actual Behavior
[ここに実際の動作を記述]

## Environment
- OS:
- Browser:
- Version:
```

**機能要望の例:**
```markdown
## Feature Description
[自動生成された説明]

## Use Case
[ユーザーストーリーを記述]

## Acceptance Criteria
- [ ]
- [ ]
- [ ]

## Proposed Solution
[解決策の提案]
```

### 4. 適切なラベル付与
- 種類ラベル: `bug`, `feature`, `documentation`
- 優先度ラベル: `priority: critical`, `priority: high`
- エリアラベル: `area: frontend`, `area: backend`

### 5. 不足情報の指摘
- 再現手順の欠如
- 期待する動作の記述漏れ
- 環境情報の不足
- 受け入れ条件の未設定

## Workflow Decision Tree

### 1. 改善モードの選択

**Commentモード（推奨）**
- Issueに改善提案をコメントとして追加
- 元の内容を保持しながら提案を提示
- チームメンバーが改善内容を確認して適用可能

```bash
python scripts/issue_improver.py --repo owner/repo --issue 123 --mode comment
```

**Updateモード**
- Issueを直接更新
- 即座に改善が適用される
- 注意：元の内容が変更されます

```bash
python scripts/issue_improver.py --repo owner/repo --issue 123 --mode update --update-title --update-body
```

### 2. 更新対象の選択

- `--update-title`: タイトルを標準化
- `--update-body`: 本文を構造化
- `--update-labels`: ラベルを適切に設定
- 何も指定しない場合: 分析結果のみを表示

### 3. バッチ処理

複数のIssueを一括処理：

```bash
python scripts/issue_improver.py --repo owner/repo --issues 123 124 125 --mode comment
```

## Scripts Usage

### issue_improver.py
メインの改善スクリプト。GitHub API連携とIssue分析の統括。

```bash
# 基本構文
python scripts/issue_improver.py --repo OWNER/REPO --issue NUMBER [OPTIONS]

# 主なオプション
--mode {update,comment}    # 改善適用モード（デフォルト: comment）
--update-title            # タイトルを更新
--update-body             # 本文を更新
--update-labels           # ラベルを更新
--dry-run                 # 適用せずに改善内容を確認
--output {json,text}      # 出力形式（デフォルト: text）
```

### issue_analyzer.py
Issue内容を分析し、改善案を生成。

```bash
# Issue分析テスト
python scripts/issue_analyzer.py --title "bug found" --body "login is broken" --output json
```

### github_client.py
GitHub APIとの連携処理。

```bash
# Issue取得テスト
python scripts/github_client.py --repo owner/repo --issue 123 --action get

# コメント追加テスト
python scripts/github_client.py --repo owner/repo --issue 123 --action comment --message "Test comment"
```

### apply_improvements.py 🆕
JSONファイルからの改善適用とテンプレート生成。

```bash
# 改善テンプレートを生成
python scripts/apply_improvements.py --repo owner/repo template --issues 123 124 125

# JSONファイルから改善を適用
python scripts/apply_improvements.py --repo owner/repo apply --improvements-file improvements.json

# プレビュー（dry-run）
python scripts/apply_improvements.py --repo owner/repo --dry-run apply --improvements-file improvements.json
```

#### テスト用スクリプト

### test_token_loading.py 🆕
Token読み込み機能のテスト。

```bash
# トークン読み込みのテスト
python test_token_loading.py
```

## References

### references/issue_templates.md
Issue種類ごとのテンプレートと品質ガイドライン。
- バグ報告、機能要望、ドキュメント更新のテンプレート
- タイトル命名規則
- ラベル付けガイドライン
- 品質チェックリスト

### references/api_reference.md
GitHub Issues APIの詳細なリファレンス。
- 認証方法と必要な権限
- 主要なAPIエンドポイントと使用例
- レート制限とエラーハンドリング
- ベストプラクティス

## Integration with Miyabi Framework

このスキルはMiyabiフレームワークの識学理論65ラベル体系と連携可能：

### 自動ラベル分類
- IssueAgentのラベル体系準拠
- `type:*`, `priority:*`, `state:*` ラベルの自動付与
- カテゴリー別自動分類：`frontend`, `backend`, `infra`

### Agent連携
- **IssueAgent**: Issue作成時の自動分析とラベル付与
- **CodeGenAgent**: 改善されたIssueからのコード生成
- **PRAgent**: Issue改善履歴を含むPR自動生成

## Use Cases

### 1. 新規Issueの品質向上
```bash
# 新しく作られた雑なIssueを改善
python scripts/issue_improver.py --repo myorg/myrepo --issue 456 --mode update --update-title --update-body
```

### 2. バックログの一括整理
```bash
# 古い未整理Issueを一括改善
python scripts/issue_improver.py --repo myorg/myrepo --issues 100 101 102 103 --mode comment
```

### 3. Issueテンプレートの適用
```bash
# 特定のプロジェクトでIssue標準化を実施
for issue in $(gh issue list --repo myorg/myrepo --state open --limit 20 --json number | jq -r '.[].number'); do
  python scripts/issue_improver.py --repo myorg/myrepo --issue $issue --mode update --update-labels
done
```

### 4. CI/CD連携
GitHub Actionsでの自動実行例：
```yaml
name: Improve New Issues
on:
  issues:
    types: [opened]

jobs:
  improve-issue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Improve issue
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/issue_improver.py --repo ${{ github.repository }} --issue ${{ github.event.issue.number }} --mode comment
```

## Error Handling

### 共通エラーと対策

**401 Unauthorized**
- 原因: GITHUB_TOKENが無効または期限切れ
- 対策: 新しいPATを生成して設定

**403 Rate Limit Exceeded**
- 原因: APIレート制限超過
- 対策: 1時間待機するか、認証済みトークンを使用

**404 Not Found**
- 原因: リポジトリまたはIssueが存在しない
- 対策: リポジトリ名とIssue番号を確認

### トラブルシューティング

```bash
# デバッグ用詳細出力
python scripts/issue_improver.py --repo owner/repo --issue 123 --output json

# 接続テスト
python scripts/github_client.py --repo owner/repo --issue 123 --action get
```

---

このスキルを使うことで、GitHub Issueの品質が大幅に向上し、開発チームの作業効率が改善されます。特にAIによるIssue処理の前処理として最適です。