---
name: commit-prep-helper
description: >
  Gitコミット前に自動で品質チェックを実行するスキル。
  「この修正をコミットして」「コードレビューしてからコミットして」などの依頼に対応し、
  ESLint/BlackによるLint、テスト実行、コードレビューを自動実行後、
  Conventional Commits準拠のコミットメッセージでコミットを作成する。
  プッシュやPR作成は行わず、ローカルコミットまでを実行する。
---

# Commit Prep Helper

## Overview

このスキルはGitコミット前に自動品質チェックを実行し、高品質なコードコミットを支援します。Lint、テスト、コードレビューを自動実行し、Conventional Commits準拠のコミットメッセージを生成します。

## Quick Start

基本的な使用フロー：

```bash
# 1. 変更をステージング
git add .

# 2. スキル実行
/skill: commit-prep-helper

# 3. 自動実行されるチェック：
#    - Lintチェック (ESLint/Black/Prettier)
#    - テスト実行 (Jest/Vitest/pytest)
#    - コードレビュー (セキュリティ・品質チェック)
#    - コミットメッセージ生成
#    - Gitコミット実行
```

## 品質チェックフロー

### Step 1: ステージングファイル検出
`scripts/check_staged_files.py`を実行し、コミット対象の変更を分析：

```bash
python .claude/skills/commit-prep-helper/scripts/check_staged_files.py
```

検出内容：
- 変更ファイル一覧
- ファイルタイプ分析
- 変更行数統計
- テストファイルの有無

### Step 2: Lintチェック実行
プロジェクトタイプを自動検出し、適切なLintツールを実行：

```bash
python .claude/skills/commit-prep-helper/scripts/run_linting.py
```

対応ツール：
- **Node.js**: ESLint + Prettier
- **Python**: Black + (Flake8/pylint)
- **Rust**: cargo-clippy + rustfmt
- **Go**: gofmt + golint

### Step 3: テスト実行
プロジェクトのテストフレームワークを自動検出して実行：

```bash
python .claude/skills/commit-prep-helper/scripts/run_tests.py
```

対応フレームワーク：
- **Node.js**: Jest, Vitest, Mocha
- **Python**: pytest, unittest
- **Rust**: cargo test
- **Go**: go test

### Step 4: コードレビュー実行
静的解析でセキュリティと品質問題を検出：

```bash
python .claude/skills/commit-prep-helper/scripts/code_review.py
```

チェック項目：
- セキュリティ脆弱性 (ハードコード、eval、XSS等)
- コード品質 (console.log、TODO、長すぎる行等)
- 複雑度 (関数の長さ、ネスト深さ)

### Step 5: コミットメッセージ生成とコミット実行
`references/conventional_commits.md`のルールに従い、コミットメッセージを生成：

```bash
python .claude/skills/commit-prep-helper/scripts/create_commit.py
```

生成ルール：
- コミットタイプの自動判定 (feat/fix/docs/test/chore)
- スコープの自動付与 (機能単位)
- 品質チェック結果をBodyに記載

## 品質基準

### Lintチェック基準
- **Errorレベル**: 0件必須 (ブロック要因)
- **Warningレベル**: 5件以内推奨
- **フォーマット**: Prettier/Blackエラー0件

詳細: `references/quality_thresholds.md`

### テスト品質基準
- **テスト成功率**: 100%必須
- **カバレッジ**: 70%以上推奨、80%以上理想
- **タイムアウト**: 5分

### コードレビュー基準
- **セキュリティ**: 高危険度問題0件必須
- **品質スコア**: 80点以上で合格
- **複雑度**: 関数50行以内、ネスト4階層以内

## 対応プロジェクトタイプ

### Node.js/TypeScript
```
package.json          -> 検出
├── jest.config.js    -> Jest使用
├── vite.config.js    -> Vitest使用
└── .eslintrc.js      -> ESLint使用
```

### Python
```
requirements.txt      -> 検出
pyproject.toml       -> 検出
├── pytest.ini      -> pytest使用
└── setup.cfg        -> 設定読み取り
```

### Rust/Go
```
Cargo.toml           -> Rust検出
go.mod              -> Go検出
```

## カスタマイズ設定

### プロジェクト固有設定
プロジェクトルートに `.commit-prep-config.json` を配置：

```json
{
  "project_type": "custom",
  "lint_tools": ["custom-linter"],
  "test_framework": {
    "name": "custom-test",
    "command": "custom-test --coverage"
  },
  "thresholds": {
    "test_coverage_min": 80,
    "max_lint_warnings": 3
  }
}
```

### レビュー設定のカスタマイズ
`assets/review_config.json` でチェック項目を調整：

- セキュリティパターンの追加/削除
- 品質チェックのしきい値調整
- 無視するファイル/ディレクトリ設定

## エラーハンドリング

### Lintエラー時
```bash
# ESLintエラー例
❌ Lint Check Failed
ESLint: 3 errors found
→ Fix lint errors before committing
```

### テスト失敗時
```bash
# テスト失敗例
❌ Test Execution Failed
Jest: 2 tests failed, 15 passed
→ Fix failing tests before committing
```

### セキュリティ問題時
```bash
# セキュリティ警告
⚠️ Security Issues Found
- Hardcoded API key in src/config.js:42
→ Remove sensitive data before committing
```

## 使用例

### 典型的なユースケース

**1. 機能追加後のコミット**
```
ユーザ: 「ユーザー認証機能を実装したのでコミットして」
スキル:
- 検出: auth.ts, user.service.ts, auth.test.ts
- Lint: ESLint✅ Prettier✅
- テスト: Jest✅ 95% coverage
- レビュー: セキュリティ問題✅ 品質問題1件(console.log)
- 生成コミット: "feat(auth): add JWT authentication implementation"
```

**2. バグ修正時のコミット**
```
ユーザ: 「APIのnullハンドリングを修正したのでコミットして」
スキル:
- 検出: api.service.ts
- Lint: ✅
- テスト: ✅ 新規テスト3件追加
- レビュー: ✅
- 生成コミット: "fix(api): handle null response in user endpoint"
```

**3. ドキュメント更新時のコミット**
```
ユーザ: 「READMEとAPIドキュメントを更新したのでコミットして」
スキル:
- 検出: README.md, docs/api.md
- Lint: スキップ (ドキュメントファイル)
- テスト: スキップ
- レビュー: ✅
- 生成コミット: "docs: update installation guide and API documentation"
```

## Resources

### scripts/
実行可能なPythonスクリプト群で、各種品質チェックを自動実行します。

- `check_staged_files.py` - Gitステージングファイルの検出と分析
- `run_linting.py` - プロジェクトタイプ自動検出とLint実行
- `run_tests.py` - テストフレームワーク自動検出とテスト実行
- `code_review.py` - 静的解析によるコードレビュー実行
- `create_commit.py` - Conventional Commits準拠のコミットメッセージ生成

### references/
スキルの動作に関する詳細ドキュメントで、Claudeが参照する情報源です。

- `conventional_commits.md` - コミットメッセージのルールとテンプレート
- `quality_thresholds.md` - 品質チェックのしきい値と設定基準
- `tool_mapping.md` - プロジェクトタイプ別ツール設定のマッピング

### assets/
スキル実行時に使用される設定ファイルとテンプレートです。

- `review_config.json` - コードレビューのチェック項目としきい値設定
- `commit_templates/` - コミットメッセージのテンプレートファイル
  - `feat.template` - 新機能追加用のテンプレート
  - `fix.template` - バグ修正用のテンプレート

---

**重要**: このスキルはpushやPR作成は行いません。ローカルでの品質チェックとコミット作成に特化しています。