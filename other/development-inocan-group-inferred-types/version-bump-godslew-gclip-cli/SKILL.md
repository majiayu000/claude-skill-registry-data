---
name: version-bump
description: Cargo.tomlのversionを更新し、`version bump (vX.Y.Z)`でコミットし、`vX.Y.Z`の軽量タグを作成してoriginへpushする作業で使う。Rust CLIのリリース準備、version bump、git tag/pushの依頼があるときに使う。
---

# Version Bump

## Overview
Cargo.tomlのversionをパッチ更新し、main上でコミット・軽量タグ作成・pushまでを安全に実施する。

## Workflow

### 1) Preflight
- `main`ブランチにいることを確認する
- 作業ツリーがクリーンであることを確認する
- `origin`リモートが存在することを確認する
- 目的のタグ`vX.Y.Z`が未作成であることを確認する
- 条件を満たさない場合は中断し、ユーザーに状況を共有して判断を仰ぐ

### 2) Version決定
- ユーザーが明示したversionがあればそれを採用する
- 明示がない場合はCargo.tomlの`version = "X.Y.Z"`を読み取り、patchを`Z+1`にする

### 3) Cargo.toml更新
- `version = "X.Y.Z"`のみを更新する
- 余計な変更を入れない

### 4) Commit
- `Cargo.toml`のみをstageする
- コミットメッセージは `version bump (vX.Y.Z)` を使う

### 5) Tag作成
- 軽量タグ `vX.Y.Z` を作成する
- 署名やannotatedタグは使わない

### 6) Push
- `main`のコミットを`origin`へpushする
- タグ`vX.Y.Z`を`origin`へpushする

### 7) 完了報告
- 更新したversionと作成したタグ名を明示して報告する

## Commands (例)
- `git status -sb`
- `git switch main`
- `git tag -l "vX.Y.Z"`
- `git add Cargo.toml`
- `git commit -m "version bump (vX.Y.Z)"`
- `git tag vX.Y.Z`
- `git push origin main`
- `git push origin vX.Y.Z`
