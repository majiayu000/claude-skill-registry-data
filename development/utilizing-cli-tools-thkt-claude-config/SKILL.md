---
name: utilizing-cli-tools
description: >
  git、gh、npm、その他の開発ツールのCLIツールガイド。
  開発ワークフローでのコマンドライン操作のベストプラクティス。
  トリガー: CLI, command line, git, gh, npm, yarn, pnpm, terminal,
  コマンドライン, ターミナル, GitHub CLI, package manager,
  パッケージマネージャ, Conventional Commits, HEREDOC, シェル.
allowed-tools: Bash, Read, Glob
---

# CLIツールガイド

開発ワークフローでのCLIツール使用のベストプラクティス。

## 目的

効果的なCLIツール使用のガイダンスを提供:

- バージョン管理操作（git）
- GitHubインタラクション（gh）
- パッケージ管理（npm, yarn, pnpm）
- 外部コードレビュー（coderabbit）

## ツールカテゴリ

| カテゴリ | ツール | 参照 |
| --- | --- | --- |
| バージョン管理 | git | [@./tools/git-essentials.md](./tools/git-essentials.md) |
| GitHub | gh | [@./tools/gh-github-cli.md](./tools/gh-github-cli.md) |
| パッケージ管理 | npm, yarn, pnpm | [@./tools/npm-scripts.md](./tools/npm-scripts.md) |
| コードレビュー | coderabbit | [@./tools/coderabbit.md](./tools/coderabbit.md) |

## クイックリファレンス

### Git

| アクション | コマンド |
| --- | --- |
| ステータス | `git status --short` |
| Diff | `git diff --staged` |
| ブランチ | `git branch --show-current` |
| ログ | `git log --oneline -10` |
| コミット（HEREDOC） | 以下を参照 |

**HEREDOCコミット（シェルエスケープ問題を回避）**:

```bash
git commit -m "$(cat <<'EOF'
feat(auth): OAuth認証を追加

- Google OAuthプロバイダーを追加
- セッション管理を追加
EOF
)"
```

### GitHub CLI（gh）

| アクション | コマンド |
| --- | --- |
| PR作成 | `gh pr create --title "..." --body "..."` |
| Issue作成 | `gh issue create --title "..." --body "..."` |
| PR表示 | `gh pr view [number]` |
| PRステータス | `gh pr status` |
| チェック実行 | `gh pr checks` |

### npm/yarn/pnpm

| アクション | npm | yarn | pnpm |
| --- | --- | --- | --- |
| インストール | `npm install` | `yarn` | `pnpm install` |
| スクリプト実行 | `npm run <script>` | `yarn <script>` | `pnpm <script>` |
| 依存追加 | `npm install <pkg>` | `yarn add <pkg>` | `pnpm add <pkg>` |
| dev依存 | `npm install -D <pkg>` | `yarn add -D <pkg>` | `pnpm add -D <pkg>` |

## ベストプラクティス

### 1. アトミックコミット

1コミット1論理変更:

```bash
# Bad: 複数の無関係な変更
git commit -m "fix bug and add feature and update docs"

# Good: 一度に1つの変更
git commit -m "fix(auth): トークンリフレッシュ問題を解決"
git commit -m "feat(user): プロフィール設定ページを追加"
```

### 2. Conventional Commits

形式: `type(scope): description`

| タイプ | 目的 |
| --- | --- |
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメント |
| `refactor` | コード再構築 |
| `test` | テスト変更 |
| `chore` | ビルド/ツール |

### 3. 安全第一

**確認なしで実行禁止**:

- `git push --force`（代わりに`--force-with-lease`を使用）
- `git reset --hard`
- `rm -rf`（代わりに`mv ~/.Trash/`を使用）

## 参照

### 原則（rules/）

- [@~/.claude/rules/core/AI_OPERATION_PRINCIPLES.md](~/.claude/rules/core/AI_OPERATION_PRINCIPLES.md) - 安全第一の操作

### 関連スキル

- `generating-tdd-tests` - CLIテストランナーでのTDD
- `creating-hooks` - Gitフック設定

### 使用コマンド

- `/commit` - Conventional Commits形式を生成
- `/pr` - PRを作成してプッシュ
- `/branch` - ブランチ名を提案
- `/issue` - GitHub Issueを作成
- `/rabbit` - CodeRabbit AIレビュー
