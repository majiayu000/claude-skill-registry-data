---
name: dependabot-pr
description: Handle Dependabot pull requests for dependency updates. Use when merging multiple Dependabot PRs, resolving conflicts between dependency update PRs, or when asked to review and merge dependency updates.
---

# Dependabot PR Handler

## Overview

複数のDependabot PRを効率的に処理するためのスキル。連鎖的なコンフリクトを回避し、安全にマージする。

## Known Issues

### 1. 連鎖コンフリクト
複数PRが`package.json`と`bun.lock`を変更するため、1つマージすると残りでコンフリクト発生。

### 2. biome更新時のスキーマ漏れ
`@biomejs/biome`更新時、`biome.json`の`$schema`フィールドも更新が必要（Dependabotは自動で行わない）。

### 3. Dependabotブランチの挙動
コンフリクト解決してpushしても、状態によってはPRが自動クローズされる場合あり。

## Recommended Approach

### 方式A: 統合アプローチ（推奨）

複数PRがある場合、mainで一括更新する方が効率的。

```bash
# 1. PRの確認
gh pr list --repo OWNER/REPO --state open --json number,title,headRefName

# 2. mainを最新化
git checkout main && git pull origin main

# 3. package.jsonを直接編集して全依存関係を更新

# 4. lockファイル再生成と検証
bun install
bun typecheck && bun lint && bun test

# 5. コミット＆プッシュ
git add package.json bun.lock
git commit -m "build(deps): bump dependencies"
git push origin main

# 6. 残ったPRはDependabotが自動クローズ
```

### 方式B: 順次マージアプローチ

PRを1つずつ丁寧に対応する場合。

```bash
# 1. PRブランチをチェックアウト
git checkout origin/dependabot/xxx/yyy

# 2. 依存関係インストール＆検証
bun install
bun typecheck && bun lint && bun test

# 3. 問題なければマージ
gh pr merge NUMBER --merge

# 4. 次のPRでコンフリクト発生時
git checkout dependabot/xxx/zzz
git fetch origin main
git merge origin/main --no-edit

# 5. コンフリクト解決
# package.json: 両方の変更を取り込む
# bun.lock: 削除して再生成
rm bun.lock && bun install

# 6. 検証後コミット＆プッシュ
git add package.json bun.lock
git commit -m "chore: resolve merge conflict with main"
git push origin dependabot/xxx/zzz

# 7. マージ
gh pr merge NUMBER --merge
```

## Special Cases

### biome更新時

```bash
# スキーマ更新が必要
bunx biome migrate --write
git add biome.json
git commit -m "chore: update biome.json schema"
```

### PRが自動クローズされた場合

Dependabotがコンフリクト状態と判断してクローズした場合、mainで直接対応する。

```bash
git checkout main
# package.jsonを編集
bun install
bun typecheck && bun lint && bun test
git add package.json bun.lock
git commit -m "build(deps-dev): bump PACKAGE from X to Y"
git push origin main
```

## Verification Checklist

- [ ] `bun install` が成功する
- [ ] `bun typecheck` がエラーなし
- [ ] `bun lint` がエラーなし（警告のみ許容）
- [ ] `bun test` が全パス
- [ ] biome更新時は`biome.json`スキーマも更新

## Merge Method

このリポジトリではsquash mergeが無効。通常のmergeを使用。

```bash
gh pr merge NUMBER --merge  # squash不可
```
