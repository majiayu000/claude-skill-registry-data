---
name: git-branch-cleanup
description: ローカルGitブランチを分析し、安全にクリーンアップします。マージ状態、古さ、リモート追跡状況によってブランチを分類し、削除すべきブランチを特定します。ユーザーが「ブランチを整理」「古いブランチを削除」と依頼した時にアクティベートします。
---

# Git Branch Cleanup（Gitブランチクリーンアップ）

## 目的
ローカルGitブランチを安全に整理・クリーンアップするためのスキルです。マージ状態、古さ、リモート追跡状況によってブランチを分類し、削除可能なブランチを特定します。

このスキルは、開発者がブランチの整理を依頼した時や、古いブランチが蓄積している時に自動的にアクティベートされます。

## いつアクティベートするか
- ユーザーが「ブランチを整理」「ブランチをクリーンアップ」と依頼した時
- ユーザーが「古いブランチを削除」と依頼した時
- ユーザーが「どのブランチを削除できるか」と質問した時
- ユーザーが「Gitブランチを整理」と依頼した時
- 多数のローカルブランチが存在している時

## ワークフロー

### ステップ1: ブランチ分析
以下のgitコマンドを使用してブランチデータを収集します：

```bash
# すべてのローカルブランチを取得
git branch --format='%(refname:short)|%(upstream:short)|%(upstream:track)'

# 各ブランチのマージ状態を確認
git branch --merged
git branch --no-merged

# 各ブランチの最終コミット日時を取得
git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short)|%(committerdate:relative)'

# リモートで削除されたブランチを確認
git remote prune origin --dry-run
```

### ステップ2: ブランチ分類
ブランチを以下のカテゴリに分類します：

| カテゴリ | 説明 | リスクレベル |
|---------|------|------------|
| **マージ済み** | すでにメインブランチにマージされている | ✅ 安全に削除可能 |
| **リモート削除済み** | リモートで削除されているが、ローカルに残っている | ⚠️ レビュー後削除可能 |
| **古いブランチ** | 30日以上更新されていない | ⚠️ レビュー後削除可能 |
| **未プッシュコミットあり** | リモートより先行しているコミットがある | ❌ 削除注意 |
| **未マージ** | メインブランチにマージされていない | ⚠️ 慎重に判断 |

### ステップ3: 結果表示
カテゴリごとにブランチを整理して表示します：

```markdown
## ブランチクリーンアップ結果

### ✅ 安全に削除可能（マージ済み）
- feature/completed-task-1 (30日前)
- bugfix/fixed-issue-123 (45日前)

### ⚠️ レビュー推奨（リモート削除済み）
- feature/old-feature (60日前、リモート削除済み)

### ⚠️ レビュー推奨（古いブランチ）
- feature/stale-branch (90日前、未マージ)

### ❌ 削除注意（未プッシュコミットあり）
- feature/wip-task (2コミット先行)

### ℹ️ アクティブブランチ（未マージ）
- feature/current-work (3日前)
```

### ステップ4: 安全ガード
以下のブランチは**絶対に削除しない**：

- `main`
- `master`
- `trunk`
- `develop`
- `development`
- 現在チェックアウトしているブランチ

### ステップ5: 削除実行
ユーザーの明示的な確認を得てから削除を実行します。

## クイックチェックリスト

### ブランチ分析前
- [ ] 現在のブランチを確認（保護されたブランチにいないか）
- [ ] リモートの最新状態を取得（`git fetch --prune`）
- [ ] ローカルの変更がコミットされているか確認

### 削除実行前
- [ ] 削除対象のブランチリストをユーザーに確認
- [ ] 保護されたブランチが含まれていないか確認
- [ ] 未プッシュコミットがあるブランチを警告
- [ ] ユーザーの明示的な確認を取得

### 削除実行後
- [ ] 削除結果を報告
- [ ] エラーがあれば詳細を表示
- [ ] 削除されたブランチ数を報告

## 詳細なガイドライン

### 1. ブランチ分析コマンド

#### すべてのローカルブランチを一覧表示
```bash
git branch
```

#### マージ済みブランチを表示
```bash
# mainブランチにマージ済みのブランチ
git branch --merged main

# 現在のブランチにマージ済みのブランチ
git branch --merged
```

#### リモートで削除されたブランチを確認
```bash
# Dry-run（実際には削除しない）
git remote prune origin --dry-run

# 実際に削除
git remote prune origin
```

#### ブランチの最終更新日時を確認
```bash
git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short) - %(committerdate:relative)'
```

#### ブランチのリモート追跡状態を確認
```bash
git branch -vv
```

---

### 2. ブランチ分類ロジック

#### マージ済みブランチ
```bash
# mainにマージ済み
git branch --merged main | grep -v "^\*" | grep -v "main" | grep -v "master" | grep -v "develop"
```

**判定基準**:
- `git branch --merged main`に含まれる
- 保護されたブランチではない
- 現在チェックアウトしているブランチではない

**リスクレベル**: ✅ 安全

#### リモート削除済みブランチ
```bash
# リモートで削除されているブランチを検出
git remote prune origin --dry-run
```

**判定基準**:
- リモートに対応するブランチが存在しない
- ローカルには残っている

**リスクレベル**: ⚠️ レビュー推奨

#### 古いブランチ（30日以上更新なし）
```bash
# 30日以上更新されていないブランチを検出
git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short)|%(committerdate:iso8601)' | \
  awk -F'|' '{
    cmd = "date -d \""$2"\" +%s"
    cmd | getline commit_time
    close(cmd)
    now = systime()
    days = (now - commit_time) / 86400
    if (days > 30) print $1, days"日前"
  }'
```

**判定基準**:
- 最終コミットから30日以上経過
- 未マージの可能性あり

**リスクレベル**: ⚠️ レビュー推奨

#### 未プッシュコミットあり
```bash
# リモートより先行しているブランチを検出
git branch -vv | grep "\[origin/.*: ahead"
```

**判定基準**:
- リモートブランチより先行しているコミットがある
- プッシュされていない作業がある

**リスクレベル**: ❌ 削除注意（作業が失われる可能性）

#### 未マージブランチ
```bash
# mainに未マージのブランチ
git branch --no-merged main | grep -v "^\*"
```

**判定基準**:
- mainブランチにマージされていない
- アクティブな開発ブランチの可能性

**リスクレベル**: ⚠️ 慎重に判断

---

### 3. 安全ガード

#### 保護されたブランチリスト
以下のブランチは**絶対に削除しない**：

```bash
PROTECTED_BRANCHES=(
  "main"
  "master"
  "trunk"
  "develop"
  "development"
)
```

#### 現在のブランチを削除しない
```bash
current_branch=$(git branch --show-current)
# 現在のブランチは削除候補から除外
```

#### 削除前の確認プロンプト
```bash
echo "以下のブランチを削除します："
echo "$branches_to_delete"
read -p "本当に削除しますか？ (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
  echo "削除をキャンセルしました"
  exit 0
fi
```

---

### 4. 削除実行

#### 安全な削除（マージ済みブランチのみ）
```bash
# -d オプション：マージ済みのみ削除可能
git branch -d branch-name
```

#### 強制削除（未マージブランチも削除）
```bash
# -D オプション：未マージでも削除（注意！）
git branch -D branch-name
```

**⚠️ 警告**: `-D`オプションは未マージのブランチも削除します。ユーザーに明示的な確認を取ってから使用してください。

#### 一括削除スクリプト例
```bash
# マージ済みブランチを一括削除
git branch --merged main | \
  grep -v "^\*" | \
  grep -v "main" | \
  grep -v "master" | \
  grep -v "develop" | \
  xargs -r git branch -d
```

---

### 5. Dry-runモード

#### Dry-runモードとは
実際には削除せず、削除されるブランチをプレビューするモードです。

**使用例**:
```bash
# 削除対象をプレビュー
git branch --merged main | \
  grep -v "^\*" | \
  grep -v "main" | \
  grep -v "master" | \
  grep -v "develop"
```

ユーザーに確認を取る前に、必ずDry-runモードで削除対象を表示してください。

---

## 実装例

### 完全なワークフロー実装

```bash
#!/bin/bash

# 設定
STALE_DAYS=30
PROTECTED_BRANCHES=("main" "master" "trunk" "develop" "development")

# 現在のブランチを取得
current_branch=$(git branch --show-current)

echo "=== Gitブランチクリーンアップ ==="
echo ""

# ステップ1: リモートの最新状態を取得
echo "📥 リモートの最新状態を取得中..."
git fetch --prune

# ステップ2: ブランチを分析・分類
echo ""
echo "🔍 ブランチを分析中..."

# マージ済みブランチ
merged_branches=$(git branch --merged main | grep -v "^\*" | grep -v "main" | grep -v "master" | grep -v "develop")

# リモート削除済みブランチ
gone_branches=$(git branch -vv | grep ': gone]' | awk '{print $1}')

# 未プッシュコミットありブランチ
ahead_branches=$(git branch -vv | grep '\[.*: ahead' | awk '{print $1}')

# ステップ3: 結果表示
echo ""
echo "## ブランチクリーンアップ結果"
echo ""

if [ -n "$merged_branches" ]; then
  echo "### ✅ 安全に削除可能（マージ済み）"
  echo "$merged_branches"
  echo ""
fi

if [ -n "$gone_branches" ]; then
  echo "### ⚠️ レビュー推奨（リモート削除済み）"
  echo "$gone_branches"
  echo ""
fi

if [ -n "$ahead_branches" ]; then
  echo "### ❌ 削除注意（未プッシュコミットあり）"
  echo "$ahead_branches"
  echo ""
fi

# ステップ4: ユーザー確認
if [ -n "$merged_branches" ]; then
  echo ""
  read -p "マージ済みブランチを削除しますか？ (yes/no): " confirmation

  if [ "$confirmation" = "yes" ]; then
    echo "$merged_branches" | xargs -r git branch -d
    echo "✅ 削除完了"
  else
    echo "❌ 削除をキャンセルしました"
  fi
fi
```

---

## リファレンス

- [Git公式ドキュメント - Branch Management](https://git-scm.com/book/ja/v2/Git-%E3%81%AE%E3%83%96%E3%83%A9%E3%83%B3%E3%83%81%E6%A9%9F%E8%83%BD-%E3%83%96%E3%83%A9%E3%83%B3%E3%83%81%E3%81%A8%E3%83%9E%E3%83%BC%E3%82%B8%E3%81%AE%E5%9F%BA%E6%9C%AC)
- [project-conventions](../project-conventions/): プロジェクト規約
- [development-workflows](../development-workflows/): 開発ワークフロー

---

## 注意事項

### ⚠️ 削除は取り消せません
ブランチを削除すると、`git reflog`で復元できる可能性はありますが、基本的に取り消せません。削除前に必ず以下を確認してください：

1. **未プッシュのコミットがないか**
2. **作業中のブランチではないか**
3. **重要なブランチではないか**

### 🔒 保護されたブランチ
以下のブランチは**絶対に削除しない**でください：
- `main`, `master`, `trunk`
- `develop`, `development`
- 現在チェックアウトしているブランチ

### 💾 Dry-runを推奨
初回実行時は必ずDry-runモードで削除対象をプレビューし、ユーザーに確認を取ってください。

---

## まとめ

このスキルは、ローカルGitブランチを安全に整理・クリーンアップするためのワークフローを提供します。

### 主な機能
✅ ブランチを安全性レベルで分類
✅ マージ状態、古さ、リモート追跡状況を分析
✅ 保護されたブランチの削除を防止
✅ 未プッシュコミットの警告
✅ Dry-runモードでプレビュー
✅ ユーザー確認後の削除実行

**安全性を最優先**し、必ずユーザーの明示的な確認を取ってから削除を実行してください。
