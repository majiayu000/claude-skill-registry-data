---
name: migrate-env-to-1password
description: Migrate .env secrets to 1Password using the op CLI, replacing plaintext values with op:// references (Japanese). Use when the user wants to move .env secrets into 1Password, mentions the 1Password CLI, or asks to replace environment variables with vault references.
user-invocable: true
allowed-tools: Bash(op *), Bash(which op), Bash(brew install *), Read, Write, Edit, AskUserQuestion
---

プロジェクトの `.env` ファイルに含まれるシークレットを 1Password CLI (`op`) に移行します。

ユーザーの入力: $ARGUMENTS

# Step 1: .env ファイルの確認

プロジェクトルートの `.env` ファイルを読み込み、環境変数の一覧を確認する。

- `.env` が存在しない、または空の場合: 移行対象がない旨を伝えて終了する
- 存在する場合: 変数名と値の一覧をユーザーに表示し、移行対象を確認する

# Step 2: 1Password CLI のインストール確認

```bash
which op && op --version
```

- `op` コマンドが見つからない場合:
  - AskUserQuestion ツールで「1Password CLI をインストールしますか？」と確認する
  - ユーザーが承認したら `brew install --cask 1password-cli` を実行する
  - インストール失敗時はエラーを表示して終了する
- `op` コマンドが存在する場合: 次のステップへ

# Step 3: 1Password CLI の認証確認

```bash
op whoami
```

- 認証済みの場合: アカウント情報を表示して次のステップへ
- 未認証の場合:
  - ユーザーに以下を案内する:
    1. 1Password デスクトップアプリがインストール済みの場合: **1Password > Settings > Developer > Connect with 1Password CLI** を有効にすることを推奨
    2. ターミナルで `eval $(op signin)` を実行してサインインする
  - AskUserQuestion ツールで「サインインが完了したら教えてください」と待機する
  - ユーザーが完了を報告したら、再度 `op whoami` で認証状態を確認する
  - まだ未認証の場合はエラーを表示し、再試行を促す

# Step 4: 1Password Vault の選択

```bash
op vault list --format=json
```

- Vault 一覧を取得し、AskUserQuestion ツールでユーザーに保存先の Vault を選択してもらう
- 選択肢には Vault 名と ID を含める

# Step 5: 1Password にアイテムを作成

`.env` ファイルの各環境変数を 1Password に保存する。

1. プロジェクト名（ディレクトリ名やリポジトリ名）をベースにアイテムのタイトルを提案する
2. AskUserQuestion ツールでアイテムのタイトルを確認する
3. 以下のコマンドで 1Password にアイテムを作成する:

```bash
op item create \
  --category=login \
  --title="{アイテムタイトル}" \
  --vault="{選択されたVault}" \
  "{変数名1}={値1}" \
  "{変数名2}={値2}" \
  ...
```

4. 作成成功を確認する

# Step 6: .env ファイルを op:// 参照に書き換える

`.env` ファイルの各行を `op://` 参照形式に書き換える。

変換前:
```
KEY=secret-value
```

変換後:
```
KEY=op://{Vault名}/{アイテムタイトル}/{フィールド名}
```

- 書き換え前にユーザーに変換内容を表示して確認を取る
- 確認が取れたら `.env` ファイルを上書きする

# Step 7: 動作確認

```bash
op run --env-file=.env -- env | grep {変数名}
```

- 各変数が正しく解決されることを確認する
- 成功したら完了メッセージを表示する

# Step 8: 使い方の案内

移行完了後、以下の使い方を案内する:

## コマンドの実行方法

```bash
# 環境変数を注入してコマンドを実行
op run --env-file=.env -- <your-command>

# 例
op run --env-file=.env -- node script.js
op run --env-file=.env -- python main.py
```

## 注意事項

- `.env` ファイルには平文のシークレットが含まれなくなったため、安全性が向上した
- `op run` を使わずに直接 `.env` を読み込むと `op://` の参照文字列がそのまま使われるため注意
- プロジェクト内で `dotenv` 等を使っている場合は、`op run` 経由で実行するか、スクリプトの起動方法を変更する必要がある

# エラーハンドリング

- 各ステップでエラーが発生した場合、エラー内容を表示して原因と対処法を提案する
- 1Password の API レート制限に達した場合は、少し待ってからリトライするよう案内する
- Vault へのアクセス権限がない場合は、1Password アプリで権限を確認するよう案内する
