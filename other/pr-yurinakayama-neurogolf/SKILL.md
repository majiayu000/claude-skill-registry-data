---
description: >
  Pull Request creation flow based on GitHub flow. Use whenever the user wants to
  open a PR, create a pull request, "PR を作って", merge feature work into main, or
  prepare changes for review. The skill walks through commit history checks, fills
  the repo's `.github/PULL_REQUEST_TEMPLATE.md`, picks an appropriate label, and
  runs `gh pr create --base main`. It does not handle release tagging — for that
  see the release-tag skill.
---

# PR Creation Flow (GitHub flow)

GitHub flow ベースの Pull Request 作成スキル。`main` が常にデプロイ可能な唯一の長命ブランチで、すべての変更は短命の feature / fix ブランチから `main` への PR としてマージされる。

## Branch Strategy

```
feature/<topic>  → main   # 新機能・改善
fix/<topic>      → main   # バグ修正・hotfix（緊急かどうかは関係なく fix で統一）
```

ブランチ名の命名は短く、目的が読み取れる単語にする（例: `feature/dvc-data-control`, `fix/replay-loser-obs-fields`）。 release / develop / hotfix といった長命ブランチは存在しない。リリースは `main` から直接タグを打って行う（`release-tag` skill を参照）。

## Steps

### 1. Check Commit History

PR の中身を頭に入れるために、本ブランチが `main` から派生して以降のコミットを見る。

```bash
git log --oneline main..HEAD
git log --graph --oneline main..HEAD
```

差分も把握しておく:

```bash
git diff --stat main..HEAD
```

### 2. Verify Branch and Remote State

ブランチ名が `feature/*` または `fix/*` であること、リモートに push されていることを確認する。未 push なら最初に push する:

```bash
git branch --show-current
git push -u origin "$(git branch --show-current)"
```

### 3. Prepare the PR Body

リポジトリのテンプレを使う。既存テンプレに無理に skill 独自セクションを足すと書式が崩れるので、**そのままコピーして埋める**:

```bash
cp .github/PULL_REQUEST_TEMPLATE.md tmp-pull-request-template.tmp
```

`tmp-pull-request-template.tmp` を開き、各セクションを以下の流儀で埋める:

- **概要**: なぜこの PR が必要か、1〜3 行
- **変更内容**: 「変更したファイル」ではなく「読み手が把握しておくべき変化」を箇条書き。コミット単位ではなく論理単位でまとめる
- **コメント**: レビュアーへの注意点、レビュー観点、後続作業など補足

### 4. Pick a Label

ラベルは PR の性質を一目で示すために付ける。既存のラベルから選ぶ:

```bash
gh label list
```

迷ったら以下を目安に:
- 機能追加: `enhancement` / `feature`
- バグ修正: `bug` / `fix`
- リファクタ: `refactor`
- ドキュメント: `documentation`

リポジトリにそのラベルが無ければ `--label` を省く（無理に作らない）。

### 5. Create the Pull Request

`main` を base にして PR を作成する。タイトルは「変更の主旨が独立して読める一文」にする:

```bash
gh pr create \
  --base main \
  --head "$(git branch --show-current)" \
  --title "<変更の主旨が読み取れる短いタイトル>" \
  --body-file tmp-pull-request-template.tmp \
  --assignee @me \
  --label "<選んだラベル>"
```

複数ラベルなら `--label` を複数回繰り返す。

### 6. Cleanup

```bash
rm tmp-pull-request-template.tmp
```

## PR Template (repo 実体)

`.github/PULL_REQUEST_TEMPLATE.md` の中身は以下のとおり。skill 内では独自テンプレを定義せず、これをそのまま使う:

```markdown
#### 概要

#### 変更内容

#### コメント
```

## Commit Message Format

タイトルは絵文字 + 簡潔な説明。本文は必要に応じて追加。

```
:<emoji>: <description>

<optional body>
```

| Emoji | Code | Type |
|-------|------|------|
| ✨ | `:sparkles:` | feat |
| 🐛 | `:bug:` | fix |
| ♻️ | `:recycle:` | refactor |
| 📚 | `:books:` | docs |
| ✅ | `:white_check_mark:` | test |
| 🔧 | `:wrench:` | chore |
| ⚡ | `:zap:` | perf |
| 👷 | `:construction_worker:` | ci |
| 🔥 | `:fire:` | remove |
| 🎨 | `:art:` | style |

## Notes

- マージ方式は **squash merge を既定** とする（main の履歴を線形に保つため）。リポジトリ設定で squash がデフォルトになっていればそれに従い、わざわざ override しない
- PR は **小さく、1 トピック 1 PR** を心がける。複数の関心が混ざっていたらコミットを分けて 2 本に切る方が良い
- レビュー前に `dev/test-backend` 等の CI 相当チェックをローカルで通しておくと往復が減る
- マージ済みの feature / fix ブランチは GitHub 側で削除して構わない（`gh pr merge --delete-branch` または UI から）

## Language

すべてのユーザーへの出力、PR タイトル、PR 本文、コミットメッセージは **日本語** で書く（リポジトリ規約）。
