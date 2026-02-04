---
name: conventional-commits
description: Enforces conventional commit message and branch naming conventions with specific prefixes (feat, fix, docs, style, refactor, perf, test, chore). Use when creating git commits, suggesting branch names, reviewing commit messages, or when the user asks about git workflow.
---

# Conventional Commits & Branch Naming

このスキルは、一貫性のあるgit commitメッセージとbranch名の作成を支援します。

## Commit Message Prefix Rules

すべてのコミットメッセージは以下のprefixで始める必要があります：

| Prefix | 用途 | 例 |
|--------|------|-----|
| `feat:` | 新しい機能 | `feat: add user authentication` |
| `fix:` | バグの修正 | `fix: resolve login redirect issue` |
| `docs:` | ドキュメントのみの変更 | `docs: update API documentation` |
| `style:` | 空白、フォーマット、セミコロン追加など | `style: format code with prettier` |
| `refactor:` | 仕様に影響がないコード改善 | `refactor: simplify user validation logic` |
| `perf:` | パフォーマンス向上関連 | `perf: optimize database queries` |
| `test:` | テスト関連 | `test: add unit tests for auth module` |
| `chore:` | ビルド、補助ツール、ライブラリ関連 | `chore: update dependencies` |

## Branch Naming Convention

ブランチ名も同じprefixを使用します：

### フォーマット
```
<prefix>/<short-description>
```

### 例
```bash
feat/user-authentication
fix/login-redirect
docs/api-documentation
style/prettier-formatting
refactor/user-validation
perf/database-optimization
test/auth-unit-tests
chore/dependency-updates
```

## Commit Message フォーマット

```
<prefix>: <subject>

<optional body>

<optional footer>
```

### 例（フルフォーマット）
```
feat: add user authentication system

Implement JWT-based authentication with refresh tokens.
Includes login, logout, and token refresh endpoints.

Closes #123
```

### 例（シンプル）
```
fix: resolve login redirect issue
```

## 判断基準

変更内容に応じて適切なprefixを選択：

- **ユーザーに見える新機能** → `feat:`
- **バグ修正** → `fix:`
- **README、コメント、ドキュメント** → `docs:`
- **コードフォーマット、空白、スタイル** → `style:`
- **動作は同じだが実装を改善** → `refactor:`
- **速度・メモリなど性能改善** → `perf:`
- **テストコード追加・修正** → `test:`
- **ビルドツール、CI、依存関係** → `chore:`

## 迷った場合のフローチャート

```
ユーザーに見える変更？
├─ Yes → 新機能？
│   ├─ Yes → feat:
│   └─ No → fix:
└─ No → コードの変更？
    ├─ Yes → 性能向上？
    │   ├─ Yes → perf:
    │   └─ No → ロジック改善？
    │       ├─ Yes → refactor:
    │       └─ No → test:
    └─ No → ドキュメント？
        ├─ Yes → docs:
        └─ No → chore:
```

## 実行時のルール

### Commit作成時
1. 変更内容を分析
2. 上記の判断基準に従って適切なprefixを選択
3. 簡潔で明確な説明を英語で記述
4. 必要に応じてbodyを追加

### Branch作成時
1. 作業内容から適切なprefixを選択
2. スラッシュ区切りで短い説明を追加
3. ケバブケース（lowercase + ハイフン）を使用

### 例外
- 初回コミット: `chore: initial commit`
- マージコミット: prefix不要（自動生成されるため）
- Revert: `revert: <元のコミットメッセージ>`

## 参考資料
- Conventional Commits: https://www.conventionalcommits.org/
