---
name: gha-sha-reference
description: ユーザーがGitHub Actionsのタグ参照をSHA参照に変換するよう要求したときに発動してください。uses:フィールドのタグ参照を自動的にSHA参照（コミットハッシュ + コメント付きバージョン）に変換します。
---

# GitHub Actions SHA Reference Skill

## 目的

このスキルはGitHub Actionsワークフローファイル内の`uses:`フィールドで使用されているタグ参照（例: `@v4`）を、セキュリティのベストプラクティスに従ってSHA参照（例: `@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2`）に自動変換します。

## 使用タイミング

<trigger>

以下の場合にこのスキルを発動してください：

- ユーザーが「GitHub ActionsをSHA参照に変換して」と要求したとき
- ユーザーが「actionsのusesをSHAに書き換えて」と言及したとき

</trigger>

## 実行手順

<procedure>

### 1. 変更対象を確認

まず `--check --diff` オプションで、どのファイルが変更されるかを確認します：

```bash
pinact run --check --diff
```

**出力例**:

```
ERROR action isn't pinned
.github/workflows/ci.yaml:10
-       uses: actions/checkout@v4
+       uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955 # v4.3.0
ERROR action isn't pinned
.github/workflows/ci.yaml:11
-     - uses: actions/setup-go@v4
+     - uses: actions/setup-go@4d34df0c2316fe8122ab82dc22947d607c0c91f9 # v4.0.0
ERROR action isn't pinned
.github/workflows/deploy.yaml:15
-       uses: actions/checkout@v4
+       uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955 # v4.3.0
```

### 2. 変換を実行

確認後、`pinact run` を実行してすべての対象ファイルを一括変換します：

```bash
pinact run
```

pinactは以下を自動的に行います：
- タグ参照からコミットSHAを取得
- 最も詳細なバージョンタグ（v4.3.0など）をコメントとして追加
- `.github/workflows/*.{yml,yaml}` と `action.{yml,yaml}` を自動検出して変換

</procedure>

## 実装例

<examples>

### 例1: 基本的な使用方法

<example>

**ステップ1: 変更対象を確認**:

```bash
pinact run --check --diff
```

**出力**:

```
ERROR action isn't pinned
.github/workflows/ci.yaml:10
-       uses: actions/checkout@v4
+       uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955 # v4.3.0
ERROR action isn't pinned
.github/workflows/ci.yaml:11
-     - uses: actions/setup-go@v4
+     - uses: actions/setup-go@4d34df0c2316fe8122ab82dc22947d607c0c91f9 # v4.0.0
```

**ステップ2: 変換を実行**:

```bash
pinact run
```

**変換後のワークフローファイル (.github/workflows/ci.yaml)**:

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955 # v4.3.0
      - uses: actions/setup-go@4d34df0c2316fe8122ab82dc22947d607c0c91f9 # v4.0.0
```

</example>

</examples>

## 重要な注意事項

<important>

### すべきこと

- **pinactを使用**: GitHub Actions SHA参照変換には専用ツールpinactを使用する
- **まず --check --diff で確認**: `pinact run --check --diff` で変更対象を確認する
- **一括実行**: diffで確認した後、`pinact run` で全ファイルを一括変換する
- **変換結果を報告**: 何が変換されたかユーザーに伝える

### してはいけないこと

- **カスタムスクリプトを作成**: pinactという専用ツールがあるので、独自スクリプトは不要
- **いきなり実行**: `--check --diff` で確認せずに `pinact run` を実行しない
- **エラーを無視**: pinactの実行でエラーが出た場合は、そのまま進めずユーザーに報告する

### 実行前チェックリスト

- [ ] pinactがインストールされている（`pinact --version`で確認）
- [ ] `pinact run --check --diff` で変更対象を確認した
- [ ] diffの出力から変換対象のファイル一覧を把握した

</important>

## 参考リンク

- [pinact - GitHub](https://github.com/suzuki-shunsuke/pinact)
- [GitHub Actions セキュリティガイド](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
