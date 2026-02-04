---
name: git-message-guide
description: コミットメッセージとPRメッセージのガイドライン。Conventional Commits形式での日本語コミットメッセージ作成、PRの概要・レビュー観点・関連Issue記載をサポート。git commit、PR作成、コミットメッセージの書き方を聞かれた時に使用する。
---

# Git Message Guide

コミットメッセージとPRメッセージを一貫したフォーマットで作成するためのガイドライン。

## コミットメッセージ

Conventional Commits形式を使用し、日本語で記述する。

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type一覧

| Type | 用途 |
|------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメント変更 |
| `style` | フォーマット変更（コードの意味に影響しない） |
| `refactor` | リファクタリング |
| `perf` | パフォーマンス改善 |
| `test` | テスト追加・修正 |
| `chore` | ビルド・補助ツール変更 |

### 禁止事項
以下のようなCo-Authored-Byを使用してはいけません：

```
 Co-Authored-By: Claude
```

### 例

```
feat(auth): ログイン機能を追加

OAuth2.0を使用したGoogleログインを実装。
セッション管理にはJWTを採用。

Refs: #123
```

詳細は [references/conventional-commits.md](references/conventional-commits.md) を参照。

## PRメッセージ

以下の3セクションで構成する：

1. **概要** - 変更内容の要約（1-3行）
2. **レビュー観点** - レビュアーに確認してほしいポイント
3. **関連Issue** - 関連するIssue/チケットへのリンク

### テンプレート

```markdown
## 概要
[変更内容を1-3行で説明]

## レビュー観点
- [確認してほしいポイント1]
- [確認してほしいポイント2]

## 関連Issue
- Closes #123
- Refs #456
```

詳細は [references/pr-template.md](references/pr-template.md) を参照。
