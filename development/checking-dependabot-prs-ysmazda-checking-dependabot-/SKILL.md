---
name: checking-dependabot-prs
description: DependabotのPRをレビューの必要度の観点で検証する。「DependabotのPRを確認して」「Dependabotの更新は安全？」などの依頼時に使用する。
---

# Dependabot PR Security Review

指定リポジトリのDependabot PRについてセキュリティ検証を行う。

## Workflow

```
Progress:
- [ ] Step 1: PR一覧を取得
- [ ] Step 2: セキュリティ面を確認
- [ ] Step 3: 破壊的変更を確認
- [ ] Step 4: 結果を報告
```

### Step 1: PR一覧を取得

```bash
gh pr list --state open --repo OWNER/REPO --author "dependabot[bot]" --json number,title,url,createdAt
```

DependabotのPRが10件を超える場合はユーザーに確認件数を尋ねる。

### Step 2: セキュリティ面を確認

以下の方法で更新対象パッケージの脆弱性を確認する：

curl -s -H "Content-Type: application/json" https://api.osv.dev/v1/query -d QUERY

OSVのQUERY例（エコシステムとパッケージ名を明示する）：

```bash
curl -s -H "Content-Type: application/json" https://api.osv.dev/v1/query -d '{
  "package": {
    "name": "PACKAGE_NAME",
    "ecosystem": "ECOSYSTEM"
  },
  "version": "X.Y.Z"
}'
```

エコシステムが不明な場合はユーザーに確認する。

### Step 3: 破壊的変更を確認

#### 3-1. バージョン番号から破壊的変更の可能性を判断

PRタイトルからバージョン番号を抽出し、セマンティックバージョニングに基づいて判断：
- **メジャーバージョンアップ** (例: 1.x.x → 2.x.x): 破壊的変更の可能性が高い → 詳細確認必須
- **マイナーバージョンアップ** (例: 1.1.x → 1.2.x): 機能追加が中心、破壊的変更の可能性は低い
- **パッチバージョンアップ** (例: 1.1.1 → 1.1.2): バグ修正が中心、破壊的変更の可能性は極めて低い

#### 3-2. PRの破壊的変更を確認

```bash
gh pr view PR_NUMBER --repo OWNER/REPO --json body
```

Dependabotが生成するPR本文には以下の情報が含まれる：
- Release notes（リリースノート）
- Changelog（変更ログ）
- Commits（コミット一覧）

PR本文を読み込んで破壊的変更が加えられていないかどうか確認する。

#### 3-3. 差分の確認（必要に応じて）

メジャーバージョンアップの場合、実際の変更内容を確認：

```bash
gh pr diff PR_NUMBER --repo OWNER/REPO
```

requirements.txt や pyproject.toml などの依存関係ファイルの変更を確認し、他のパッケージへの影響を評価する。

### Step 4: 結果を報告

以下のテンプレートで報告する：

```markdown
## Dependabot PR セキュリティレビュー結果

**リポジトリ:** OWNER/REPO
**確認日:** YYYY-MM-DD
**確認件数:** N件

### サマリ
- ✅ 承認推奨: N件
- ⚠️ 要確認: N件
- ❌ 非推奨: N件

### 各PRの詳細

#### パッケージ名 vX.X.X → vY.Y.Y
- **PR:** https://github.com/...
- **脆弱性チェック:** ✅ 既知の脆弱性なし (OSV: [ID/URL])
- **破壊的変更チェック:** ✅ 破壊的変更なし
- **補足:** エコシステム/影響範囲/判断根拠を簡潔に記載
- **判定:** ✅ 承認推奨
```
