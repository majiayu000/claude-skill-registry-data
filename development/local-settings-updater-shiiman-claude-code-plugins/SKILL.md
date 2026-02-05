---
name: local-settings-updater
description: プロジェクトの .claude/settings.local.json を更新する。「ローカル設定を更新して」「local settings を変更」「個人用設定を変えて」「自分だけの設定」「ローカル permissions を追加」「個人設定ファイルを編集」「settings.local を更新」などで起動。Git にコミットされない個人用の Claude Code 設定を管理。
allowed-tools: [Read, Write, Bash, Glob]
---

# Local Settings Updater

プロジェクトの `.claude/settings.local.json` を更新します。

## settings.local.json とは

`settings.local.json` は**個人用のローカル設定ファイル**です:

- **Git にコミットされない**: Claude Code が自動で `.gitignore` に追加
- **settings.json より優先**: 同じ設定がある場合、local が優先される
- **用途**: 個人の好み、実験的な設定、一時的な許可設定

## ワークフロー

### 1. 現在の設定を確認

`.claude/settings.local.json` が存在するか確認:

**ファイルが存在する場合:**

- 内容を読み込む
- 既存の設定を確認

**ファイルが存在しない場合:**

- `.claude` ディレクトリが存在しない場合は作成
- テンプレートから新規作成するか確認

### 2. 変更内容を確認

ユーザーに何を変更したいか確認:

- permissions の追加/削除（個人用の許可設定）
- allowedTools の追加/削除
- env 環境変数の設定（個人の開発環境向け）
- その他の設定

### 3. 設定を更新

`.claude/settings.local.json` を更新または作成。

### 4. 結果を報告

変更内容をユーザーに報告。

## settings.json との使い分け

| 設定内容 | settings.json | settings.local.json |
|----------|---------------|---------------------|
| チーム共通ルール | ✅ | ❌ |
| 個人の許可設定 | ❌ | ✅ |
| 実験的な設定 | ❌ | ✅ |
| セキュリティポリシー | ✅ | ❌ |
| 個人の環境変数 | ❌ | ✅ |

## 設定項目

### permissions

個人用の許可設定（チームの settings.json を上書き）:

```json
{
  "permissions": {
    "allow": ["Bash(docker:*)"],
    "deny": []
  }
}
```

### allowedTools

個人用のツール許可:

```json
{
  "allowedTools": ["Read", "Write", "Bash", "Glob", "Grep", "WebFetch"]
}
```

### env

個人の環境変数（**注意**: 機密情報は直接書かず、環境変数を参照）:

```json
{
  "env": {
    "DEBUG": "true",
    "LOG_LEVEL": "verbose"
  }
}
```

## テンプレートからの新規作成

ファイルが存在しない場合、以下のテンプレートを使用して作成できます。

### 基本テンプレート

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

### 開発者向けテンプレート

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(pnpm:*)",
      "Bash(yarn:*)"
    ],
    "deny": []
  },
  "env": {
    "DEBUG": "true"
  }
}
```

### ディレクトリ作成

`.claude` ディレクトリが存在しない場合:

```bash
mkdir -p .claude
```

## 重要な注意事項

- ✅ Git にコミットされない（個人設定として安全）
- ✅ settings.json の設定を上書きできる
- ✅ 実験的な設定を気軽に試せる
- ✅ ファイルが存在しない場合はテンプレートから作成可能
- ✅ `.claude` ディレクトリがない場合は自動作成
- ❌ チーム全体に適用したい設定は settings.json に記載
- ❌ 機密情報（API キー等）は env に直接書かない（環境変数を推奨）
