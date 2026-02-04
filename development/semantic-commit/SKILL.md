---
name: semantic-commit
description: Git変更の論理的分割、Conventional Commitsメッセージ生成、プロジェクト規約検出。大きな変更を意味のある最小単位に分割してコミットする際に使用。
allowed-tools: Read, Grep, Glob
---

# Semantic Commit Skill

Git変更を意味のある最小単位に分割し、セマンティックなコミットメッセージを生成するための知識ベース。

## 「大きな変更」の検出基準

以下の条件で大きな変更として検出:

1. 変更ファイル数: 5ファイル以上
2. 変更行数: 100行以上
3. 複数機能: 2つ以上の機能領域にまたがる
4. 混在パターン: feat + fix + docs が混在

```bash
# 変更規模の分析
CHANGED_FILES=$(git diff HEAD --name-only | wc -l)
CHANGED_LINES=$(git diff HEAD --stat | tail -1 | grep -o '[0-9]\+ insertions\|[0-9]\+ deletions' | awk '{sum+=$1} END {print sum}')

if [ $CHANGED_FILES -ge 5 ] || [ $CHANGED_LINES -ge 100 ]; then
  echo "大きな変更を検出: 分割を推奨"
fi
```

## 分割戦略

### 1. 機能境界による分割

```bash
# ディレクトリ構造から機能単位を特定
git diff HEAD --name-only | cut -d'/' -f1-2 | sort | uniq
# → src/auth, src/api, components/ui など
```

### 2. 変更種別による分離

```bash
# ファイルの変更タイプを判定
git diff HEAD --name-status | while read status file; do
  case $status in
    A) echo "$file: 新規作成 → feat:" ;;
    M) echo "$file: 修正 → fix/refactor:" ;;
    D) echo "$file: 削除 → chore:" ;;
    R*) echo "$file: リネーム → refactor:" ;;
  esac
done
```

### 3. 依存関係の分析

```bash
# インポート関係の変更を検出
git diff HEAD | grep -E '^[+-].*import|^[+-].*require' | \
cut -d' ' -f2- | sort | uniq
```

### 論理的グループ化の基準

1. 機能単位: 同一機能に関連するファイル
   - `src/auth/` 配下のファイル → 認証機能
   - `components/` 配下のファイル → UIコンポーネント

2. 変更種別: 同じ種類の変更
   - テストファイルのみ → `test:`
   - ドキュメントのみ → `docs:`
   - 設定ファイルのみ → `chore:`

3. 依存関係: 相互に関連するファイル
   - モデル + マイグレーション
   - コンポーネント + スタイル

4. 変更規模: 適切なコミットサイズの維持
   - 1コミットあたり10ファイル以下
   - 関連性の高いファイルをグループ化

## Conventional Commits 形式

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 標準タイプ

必須タイプ:
- feat: 新機能（ユーザーに見える機能追加）
- fix: バグ修正

任意タイプ:
- build: ビルドシステムや外部依存関係の変更
- chore: その他の変更（リリースに影響しない）
- ci: CI設定ファイルやスクリプトの変更
- docs: ドキュメントのみの変更
- style: コードの意味に影響しない変更（空白、フォーマット、セミコロンなど）
- refactor: バグ修正や機能追加を伴わないコード変更
- perf: パフォーマンス改善
- test: テストの追加や修正

### スコープ（任意）

変更の影響範囲を示す:

```
feat(api): add user authentication endpoint
fix(ui): resolve button alignment issue
docs(readme): update installation instructions
```

### Breaking Change

APIの破壊的変更がある場合:

```
feat!: change user API response format

BREAKING CHANGE: user response now includes additional metadata
```

## プロジェクト規約の自動検出

### CommitLint設定ファイル検索順序

1. commitlint.config.mjs
2. commitlint.config.js
3. commitlint.config.cjs
4. commitlint.config.ts
5. .commitlintrc.js
6. .commitlintrc.json
7. .commitlintrc.yml
8. .commitlintrc.yaml
9. package.json の commitlint セクション

```bash
# 設定ファイル例の確認
cat commitlint.config.mjs
cat .commitlintrc.json
grep -A 10 '"commitlint"' package.json
```

### カスタムタイプの検出

プロジェクト独自のタイプ例:

```javascript
// commitlint.config.mjs
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore',
        'wip',      // 作業中
        'hotfix',   // 緊急修正
        'release',  // リリース
        'deps',     // 依存関係更新
        'config'    // 設定変更
      ]
    ]
  }
}
```

### フォールバック動作

設定ファイルが見つからない場合:

1. git log分析による自動推測
   ```bash
   git log --oneline -100 --pretty=format:"%s" | \
   grep -oE '^[a-z]+(\([^)]+\))?' | \
   sort | uniq -c | sort -nr
   ```

2. Conventional Commits標準をデフォルト使用

## 言語判定

デフォルト: 英語（en）

`--lang ja` オプションが指定された場合のみ日本語でコミットメッセージを生成する。

## 技術的実装

### 順次コミットフロー

```bash
# 1. 前処理: 現在の状態を保存
git reset HEAD
CURRENT_BRANCH=$(git branch --show-current)

# 2. グループ別の順次コミット実行
while IFS= read -r commit_plan; do
  group_num=$(echo "$commit_plan" | cut -d':' -f1)
  files=$(echo "$commit_plan" | cut -d':' -f2- | tr ' ' '\n')

  # 該当ファイルのみをステージング
  echo "$files" | while read file; do
    if [ -f "$file" ]; then
      git add "$file"
    fi
  done

  # ステージング状態の確認
  staged_files=$(git diff --staged --name-only)
  if [ -z "$staged_files" ]; then
    continue
  fi

  # コミット実行
  git commit -m "$commit_msg"
done < /tmp/commit_plan.txt

# 3. 完了後の検証
remaining_changes=$(git status --porcelain | wc -l)
if [ $remaining_changes -eq 0 ]; then
  echo "すべての変更がコミットされました"
fi
```

### エラーハンドリング

```bash
# プリコミットフック失敗時の処理
commit_with_retry() {
  local commit_msg="$1"
  local max_retries=2
  local retry_count=0

  while [ $retry_count -lt $max_retries ]; do
    if git commit -m "$commit_msg"; then
      return 0
    else
      # プリコミットフックによる自動修正を取り込み
      if git diff --staged --quiet; then
        git add -u
      fi
      retry_count=$((retry_count + 1))
    fi
  done

  return 1
}
```

## 実際の分割例（Before/After）

### 例1: 大規模な認証システム追加

Before（1つの巨大なコミット）:
```
feat: implement complete user authentication system with login, registration, password reset, API routes, database models, tests and documentation
```

After（意味のある5つのコミットに分割）:

1. `feat(db): add user model and authentication schema`
   - src/database/migrations/001_users.sql
   - src/database/models/user.js
   - src/auth/types.js

2. `feat(auth): implement core authentication functionality`
   - src/auth/login.js
   - src/auth/register.js
   - src/auth/password.js
   - src/middleware/auth.js

3. `feat(api): add authentication API routes`
   - src/api/auth-routes.js

4. `test(auth): add comprehensive authentication tests`
   - tests/auth/login.test.js
   - tests/auth/register.test.js
   - tests/api/auth-routes.test.js

5. `docs(auth): add authentication documentation and configuration`
   - docs/authentication.md
   - package.json
   - README.md
   - .env.example

### 例2: バグ修正とリファクタリングの混在

Before:
```
fix: resolve user validation bugs and refactor validation logic with improved error handling
```

After（種別別に3つのコミットに分割）:

1. `fix: resolve user validation and authentication bugs`
   - src/user/service.js（バグ修正部分のみ）
   - src/auth/middleware.js

2. `refactor: extract and improve user validation logic`
   - src/user/service.js（リファクタリング部分）
   - src/user/validator.js
   - src/api/user-routes.js

3. `chore: update documentation and dependencies`
   - docs/user-api.md
   - package.json

## 分割効果の比較

| 項目 | Before（巨大コミット） | After（適切な分割） |
|------|---------------------|-------------------|
| レビュー性 | 非常に困難 | 各コミットが小さくレビュー可能 |
| バグ追跡 | 問題箇所の特定が困難 | 問題のあるコミットを即座に特定 |
| リバート | 全体をリバートする必要 | 問題部分のみをピンポイントでリバート |
| 並行開発 | コンフリクトが発生しやすい | 機能別でマージが容易 |
| デプロイ | 全機能を一括デプロイ | 段階的なデプロイが可能 |

## トラブルシューティング

### コミット失敗時

- プリコミットフックの確認
- 依存関係の解決
- 個別ファイルでの再試行

### 分割が適切でない場合

- 手動での `edit` モード使用
- より細かい単位での再実行

## 前提条件

- Gitリポジトリ内で実行
- 未コミットの変更が存在すること
- ステージングされた変更は一旦リセットされる

## 注意事項

- 自動プッシュなし: コミット後の `git push` はユーザーが手動実行
- ブランチ作成なし: 現在のブランチでコミット
