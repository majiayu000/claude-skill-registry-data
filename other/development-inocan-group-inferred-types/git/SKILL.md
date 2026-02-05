---
name: git
description: Git操作を支援します。コミット、ブランチ作成、PRの作成時に使用します。「/git」で明示的に呼び出すこともできます。
---

# Git スキル

## 開発フロー

作業は必ずブランチを切って進める。

```
1. main から作業ブランチを作成
2. ブランチで作業・コミット
3. PR を作成
4. レビュー後、main にマージ
```

### 作業開始時

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-description>
```

### 作業中

- こまめにコミット
- 1つのコミットは1つの変更に絞る
- 作業途中でも適宜プッシュしてバックアップ

### 作業完了時

```bash
git push -u origin <branch-name>
# PR を作成
```

## コミットメッセージ規則

コミットメッセージは以下の形式に従う：

```
<type>: <subject>
```

### Type

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: バグ修正でも機能追加でもないコード変更
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### Subject

- 日本語で記述
- 動詞で始める（「追加した」ではなく「追加」）
- 50文字以内を目安に

### 例

```
feat: ユーザー認証機能を追加
fix: ログイン時のエラーハンドリングを修正
refactor: API呼び出し部分を共通化
```

## ブランチ命名規則

```
<type>/<short-description>
```

- `feature/` - 新機能
- `fix/` - バグ修正
- `refactor/` - リファクタリング

例: `feature/user-auth`, `fix/login-error`

## PR作成時の注意

- タイトルはコミットメッセージと同じ形式
- 説明には変更内容の概要を記載
- 関連するIssueがあればリンク
