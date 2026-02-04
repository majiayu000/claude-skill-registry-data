---
name: release-procedure
description: Use when user says 'release', 'リリース', 'deploy', 'publish', 'vtag', 'version up', 'バージョンアップ', or discusses merging to main/develop. Guides through version bump and release flow.
allowed-tools: [Bash, Read, Edit, Grep, Glob]
---

# リリース手順ガイド

## 目的

バージョンアップとリリースが正しい手順で行われることを担保する。

## リリースブランチ作成時のチェックリスト

**release/* ブランチを作成したら、必ず以下を実行:**

```bash
# 1. バージョン自動更新（ブランチ名から検出）
deno task bump-version

# 2. 確認
grep '"version"' deno.json
grep 'CLIMPT_VERSION' src/version.ts

# 3. ローカルCI
deno task ci

# 4. コミット & プッシュ
git add deno.json src/version.ts
git commit -m "chore: bump version to x.y.z"
git push -u origin release/x.y.z
```

## ドキュメント更新（リリース前必須）

**重要**: リリース前に以下の2つのスキルを使用してドキュメントを更新すること。

### 1. CHANGELOG 更新

`/update-changelog` スキルを使用:
- 変更内容を [Unreleased] セクションに記載
- 検索可能なキーワードを含める（コマンド名、オプション名、設定名）
- リリース時に [x.y.z] - YYYY-MM-DD へ移動

### 2. ドキュメント更新

`/update-docs` スキルを使用:
- 変更の種類に応じて適切な場所を更新
- CLI オプション変更 → `--help` 必須、README 推奨
- 新機能 → README に簡潔な説明とサンプル
- 設定変更 → スキーマ説明、README/docs

### チェックリスト

```
□ CHANGELOG.md に変更を記載（/update-changelog）
□ 必要なドキュメントを更新（/update-docs）
  □ CLI変更 → --help 出力確認
  □ 新機能 → README.md / README.ja.md
  □ Agent変更 → agents/README.md
  □ 設定変更 → スキーマ説明
```

**重要**: `deno task bump-version` は release/* ブランチ名からバージョンを自動検出する。
手動指定も可能: `deno task bump-version 1.10.2`

## 重要: 連続マージの禁止事項

**release/* → develop → main への連続マージは、必ずユーザーの明示的な指示を受けてから実行すること。**

禁止事項:
- ユーザーの指示なしに連続マージを実行
- 「リリースして」等の曖昧な指示で main まで一気にマージ
- 独自判断での develop → main マージ

正しい手順:
1. 各 PR 作成後、ユーザーに報告して次の指示を待つ
2. 「develop まで」「main まで」等の明示的な指示を確認
3. vtag 作成もユーザーの指示を待つ

## トリガー条件

以下の操作について議論・作業する際に自動的に実行:

- `release/*` ブランチへの push
- `release/*` → `develop` への PR 作成・マージ
- `develop` → `main` への PR 作成・マージ
- バージョンアップ・リリースに関する議論
- vtag の作成

## バージョン管理ファイル

このプロジェクトでは以下の2ファイルでバージョンを管理:

| ファイル | 用途 |
|---------|------|
| `deno.json` | JSR パッケージバージョン（`"version": "x.y.z"`） |
| `src/version.ts` | CLI バージョン定数（`CLIMPT_VERSION = "x.y.z"`） |

**重要**: 両ファイルのバージョンは必ず一致させること。CIで自動チェックされる。

## バージョンアップ手順

### 1. バージョン番号の決定

```
パッチ (x.y.Z): バグ修正、ドキュメント改善
マイナー (x.Y.0): 新機能追加（後方互換あり）
メジャー (X.0.0): 破壊的変更
```

### 2. ファイル更新

```bash
# deno.json
# "version": "1.9.13" → "version": "1.9.14"

# src/version.ts
# export const CLIMPT_VERSION = "1.9.13"; → "1.9.14";
```

### 3. 確認コマンド

```bash
# バージョン一致確認
grep '"version"' deno.json | head -1
grep 'CLIMPT_VERSION' src/version.ts | grep export
```

## リリースフロー

### フロー図

```mermaid
sequenceDiagram
    participant R as release/x.y.z
    participant D as develop
    participant M as main
    participant T as vtag

    Note over R: 1. バージョンアップ
    R->>R: deno.json, version.ts 更新
    Note over R: 2. ローカルCI確認
    R->>R: deno task ci
    R->>R: 3. git commit & push

    R->>D: 4. PR作成 (release → develop)
    Note over D: 5. CI確認（全てpass）
    D->>D: PRマージ

    D->>M: 6. PR作成 (develop → main)
    Note over M: 7. CI確認（全てpass）
    M->>M: PRマージ
    Note over M: JSR publish 自動実行

    M->>T: 8. vtag作成
    Note over T: git tag vx.y.z
```

### 手順詳細

#### ステップ 0: 準備

```bash
# 作業ブランチを release/* に統合済みか確認
git checkout release/x.y.z
git log --oneline -10
```

#### ステップ 1: release/* ブランチでバージョンアップ

```bash
# develop から新規作成する場合
git checkout develop
git checkout -b release/x.y.z

# または既存 release/* で作業
git checkout release/x.y.z
```

バージョン更新（自動スクリプト使用）:

```bash
# ブランチ名から自動検出してバージョン更新
deno task bump-version

# または明示的に指定
deno task bump-version x.y.z

# 確認
grep '"version"' deno.json
grep 'export const CLIMPT_VERSION' src/version.ts
```

#### ステップ 2: ローカルCI確認

**重要**: プッシュ前に必ずローカルでCIを通すこと

```bash
deno task ci
```

全てのステージがパスすることを確認してから次のステップへ進む。

#### ステップ 3: コミット & プッシュ

```bash
git add deno.json src/version.ts
git commit -m "chore: bump version to x.y.z"
git push -u origin release/x.y.z
```

**注意**: `dangerouslyDisableSandbox: true` が必要

#### ステップ 4: release/* → develop PR

```bash
gh pr create --base develop --head release/x.y.z \
  --title "Release x.y.z: <変更概要>" \
  --body "## Summary
- <変更点>

## Version
- x.y.z"
```

#### ステップ 5: CI確認 & develop へマージ

**重要**: マージ前にPRのCIが全てパスすることを確認

```bash
# CI確認（全てpassになるまで待機）
gh pr checks <PR番号> --watch

# CIがpassしたらマージ
gh pr merge <PR番号> --merge
```

#### ステップ 6: develop → main PR

```bash
gh pr create --base main --head develop \
  --title "Release x.y.z" \
  --body "Release version x.y.z to production"
```

#### ステップ 7: CI確認 & main へマージ

**重要**: マージ前にPRのCIが全てパスすることを確認

```bash
# CI確認（全てpassになるまで待機）
gh pr checks <PR番号> --watch

# CIがpassしたらマージ
gh pr merge <PR番号> --merge
```

**自動処理**: main マージ時に JSR publish が自動実行される

#### ステップ 8: vtag 作成

```bash
# main の最新コミットを取得
git fetch origin main

# vtag 作成 & push
git tag vx.y.z origin/main
git push origin vx.y.z
```

**重要**: vtag は必ず main ブランチのコミットに付与する

#### ステップ 9: クリーンアップ（ブランチ削除）

**重要**: このリポジトリは `deleteBranchOnMerge` が無効のため、マージ後の手動削除が必要。

##### ブランチ削除判断基準

| ブランチ | 削除タイミング | 削除可否 |
|---------|---------------|---------|
| `feature/*`, `fix/*`, `refactor/*`, `docs/*` | release/* へマージ後 | ✓ 削除する |
| `release/*` | develop へマージ後（かつ vtag 作成後） | ✓ 削除する |
| `develop` | - | ✗ 削除禁止（長期ブランチ） |
| `main` | - | ✗ 削除禁止（長期ブランチ） |

##### マージ済み確認方法

```bash
# ブランチが特定ブランチにマージ済みか確認
git fetch origin
git merge-base --is-ancestor origin/<source-branch> origin/<target-branch> && echo "マージ済み" || echo "未マージ"

# 例: feature/xxx が release/1.10.2 にマージ済みか
git merge-base --is-ancestor origin/feature/xxx origin/release/1.10.2 && echo "マージ済み"

# 例: release/1.10.2 が develop にマージ済みか
git merge-base --is-ancestor origin/release/1.10.2 origin/develop && echo "マージ済み"
```

##### 削除実行

```bash
# develop に戻る
git checkout develop
git pull origin develop

# ローカル + リモート両方を削除
git branch -D <branch-name>
git push origin --delete <branch-name>

# release ブランチ削除例
git branch -D release/x.y.z
git push origin --delete release/x.y.z

# feature ブランチ削除例
git branch -D feature/xxx
git push origin --delete feature/xxx
```

##### 削除漏れチェック

```bash
# マージ済みなのに残っているブランチを検出
git fetch --prune origin
git branch -r | grep -E "feature/|fix/|refactor/|docs/|release/" | while read branch; do
  branch_name=${branch#origin/}
  if git merge-base --is-ancestor "$branch" origin/develop 2>/dev/null; then
    echo "削除可能: $branch_name (develop にマージ済み)"
  fi
done
```

## CI バージョンチェック

`.github/workflows/test.yml` で以下を自動チェック:

### チェック内容

| チェック項目 | 対象ブランチ | 失敗時のエラー |
|-------------|-------------|---------------|
| deno.json と version.ts の一致 | 全ブランチ | `Version mismatch: deno.json=X, version.ts=Y` |
| ブランチ名とバージョンの一致 | release/* のみ | `Branch version mismatch: branch=X, deno.json=Y` |

### release/* ブランチでの追加チェック

```
release/1.9.15 ブランチでは:
- deno.json の version が "1.9.15" であること
- src/version.ts の CLIMPT_VERSION が "1.9.15" であること
```

### チェックを通すための確認コマンド

```bash
# 現在のブランチ名からバージョンを確認
git branch --show-current | sed 's|release/||'

# deno.json のバージョン
grep '"version"' deno.json | head -1 | sed 's/.*"\([0-9.]*\)".*/\1/'

# version.ts のバージョン
grep 'export const CLIMPT_VERSION' src/version.ts | sed 's/.*"\([0-9.]*\)".*/\1/'

# 3つが全て一致することを確認
```

### チェック失敗時の対処

```bash
# release/1.9.15 でバージョンが 1.9.14 のままだった場合
# 1. deno.json を編集: "version": "1.9.15"
# 2. version.ts を編集: CLIMPT_VERSION = "1.9.15"
# 3. コミット & push
git add deno.json src/version.ts
git commit -m "fix: correct version to 1.9.15"
git push origin release/1.9.15
```

## クイックリファレンス

```
バージョンアップ:
  1. deno.json の version を更新
  2. src/version.ts の CLIMPT_VERSION を更新
  3. deno task ci  ← ローカルCIを通す（重要）
  4. git commit -m "chore: bump version to x.y.z"

ドキュメント更新（リリース前必須）:
  1. /update-changelog → CHANGELOG.md に変更を記載
  2. /update-docs → README, --help 等を必要に応じて更新

リリースフロー:
  1. release/* → develop PR作成
  2. gh pr checks <PR番号> --watch  ← CIがpassするまで待機
  3. gh pr merge <PR番号> --merge
  4. develop → main PR作成
  5. gh pr checks <PR番号> --watch  ← CIがpassするまで待機
  6. gh pr merge <PR番号> --merge (JSR publish 自動)
  7. vtag作成: git tag vx.y.z origin/main && git push origin vx.y.z
  8. クリーンアップ: release/*, 作業ブランチ削除（ローカル+リモート）

ブランチ削除判断:
  - feature/*, fix/*, refactor/*, docs/*  → release/* マージ後に削除
  - release/*  → develop マージ後（vtag作成後）に削除
  - develop/main → 削除禁止（長期ブランチ）
  - 確認: git merge-base --is-ancestor origin/<branch> origin/develop

サンドボックス注意:
  git push, gh コマンドは dangerouslyDisableSandbox: true が必要
```

## トラブルシューティング

### JSR publish がスキップされた

原因: deno.json のバージョンが既存と同じ

```bash
# 確認
gh run view <run-id> --log | grep -i "skip"

# 対処: バージョンを上げて再リリース
```

### CI バージョンチェック失敗

原因: deno.json と version.ts の不一致、またはブランチ名との不一致

```bash
# 確認
grep '"version"' deno.json
grep 'export const CLIMPT_VERSION' src/version.ts
git branch --show-current

# 対処: 全て同じバージョンに統一
```

### vtag が古いコミットを指している

```bash
# 確認
git show vx.y.z --oneline

# 対処: タグ削除 & 再作成
git tag -d vx.y.z
git push origin :refs/tags/vx.y.z
git tag vx.y.z origin/main
git push origin vx.y.z
```
