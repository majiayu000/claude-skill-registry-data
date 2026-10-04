---
name: git-commit
description: Git リポジトリへの変更をコミットする。Conventional Commits 形式で日本語のコミットメッセージを作成する。過去の履歴を参考にしつつ、「何を解決したか」を明確に記述する。TODO/計画がある場合はそのステップ単位でコミットを分割する。ユーザーが「コミットして」「変更をコミット」「/commit」「git commit」などと言ったときに使用する。
---

# Git Commit

変更内容を確認し、Conventional Commits 形式でコミットを作成する。

## コミットメッセージのルール

- **言語**: 日本語
- **スコープ**: 機能名を使用（auth, api, ui, db など）
- **内容**: 「何をしたか」ではなく「何を解決したか」を書く

**形式:**
```
<type>(scope): <description>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**良い例・悪い例:**
```
# NG: 何をしたか（実装の説明）
fix(auth): validateUser関数を修正
feat(ui): ボタンコンポーネントを追加

# OK: 何を解決したか（目的・価値の説明）
fix(auth): 無効なトークンでもログインできてしまう問題を修正
feat(ui): ユーザーが直感的に操作を完了できるようCTAボタンを追加
```

**タイプ一覧:**
| タイプ | 用途 |
|--------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメント |
| `style` | フォーマット（動作に影響なし） |
| `refactor` | リファクタリング |
| `perf` | パフォーマンス改善 |
| `test` | テスト |
| `build` | ビルド設定 |
| `ci` | CI設定 |
| `chore` | その他 |

詳細は [references/conventional-commits.md](references/conventional-commits.md) を参照。

## コミット粒度

### TODO/計画がある場合

以下を確認し、各ステップを1コミット単位とする：
- **TodoWrite のタスクリスト**: 現在のセッションで管理しているタスク
- **develop:read-todo スキル**: プロジェクトの TODO ファイル

### 計画がない場合

以下の基準で論理的に分割：
- 機能追加・バグ修正・リファクタリングは別コミット
- 関連するファイル群を1コミットにまとめる
- 独立して意味を持つ変更単位で分割

**分割の例:**
```bash
# 例: 機能追加とバグ修正が混在している場合

# 1. まずバグ修正をコミット
git add <bug-fix-files>
git commit -m "fix(auth): 無効なトークンでログインできる脆弱性を修正"

# 2. 次に機能追加をコミット
git add <feature-files>
git commit -m "feat(auth): パスワード忘れ時に自己解決できるようリセット機能を追加"
```

## ワークフロー

### 1. 状態確認

```bash
git status
git diff --staged
git diff
```

### 2. 過去履歴の確認

```bash
git log --oneline -20
```

過去のコミットメッセージのスタイル（言語、スコープの付け方、記述の粒度）を確認し、参考にする。ただし、より良い表現があれば提案する。

### 3. TODO/計画の確認

- TodoWrite のタスクリストを確認
- develop:read-todo スキルで TODO ファイルを確認
- 計画がある場合、どのステップに対応する変更かを特定

### 4. コミット単位の設計

差分を確認し、以下を特定：
- 変更の種類（新機能、バグ修正、リファクタリング等）
- 影響範囲（スコープ）→ 機能名を使用
- 破壊的変更の有無
- コミットの分割方法（計画ステップ or 論理的単位）

### 5. 各コミットのステージング＆実行

```bash
# ステージング
git add <files>

# コミット（HEREDOCで複数行対応）
git commit -m "$(cat <<'EOF'
<type>(scope): <何を解決したか>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 6. コミット後の確認

```bash
git log --oneline -3
git status
```

## 注意事項

- コミット前に必ず `git diff` で変更内容を確認する
- `.env` や認証情報を含むファイルをコミットしない
- コミットは明示的にユーザーから依頼された場合のみ実行する
- `--amend` は直前のコミットが自分で作成し、まだプッシュしていない場合のみ使用可能
- 破壊的変更がある場合はタイプの後に `!` を付ける（例: `feat!:`）。ただし、`!` を付ける前に必ずユーザーに確認する
