---
name: gog-gmail
description: Gmail の未読確認を gog CLI で実行し、TTY・keyring・認証エラーを切り分けるための手順。ユーザーが「未読メールを確認したい」「gog で Gmail 検索したい」「gog の Gmail 認証エラーを直したい」と依頼したときに使う。
---

# Gog Gmail Unread Check

## 最短チェック

未読が 1 件でもあるかだけを確認する:

```bash
/home/yuiseki/bin/gog --account <email> gmail search 'is:unread in:inbox' --max 1 --plain --fail-empty
```

- `exit code 0`: 未読あり
- `exit code 3`: `--fail-empty` で未読なし

## この環境で分かったこと（2026-02-19）

- 実行バイナリは `./bin/gog` ではなく `/home/yuiseki/bin/gog`。
- config path は `/home/yuiseki/.config/gogcli/config.json`。
- keyring backend は `file`。
- 非 TTY では以下エラーでトークン読込に失敗することがある:
  - `no TTY available for keyring file backend password prompt; set GOG_KEYRING_PASSWORD`
- 利用アカウントは `yuiseki@gmail.com`（`auth list` 失敗時のメッセージから確認）。

## 手順

1. コマンド仕様を確認する。

```bash
/home/yuiseki/bin/gog gmail search --help
```

2. 認証状態と keyring backend を確認する。

```bash
/home/yuiseki/bin/gog auth status
/home/yuiseki/bin/gog auth keyring
```

3. `--account` を明示して未読検索を実行する。

```bash
/home/yuiseki/bin/gog --account <email> gmail search 'is:unread in:inbox' --max 20 --json
```

4. keyring のパスフレーズ入力待ちになったら TTY で実行する。
5. 非対話で実行する場合は `GOG_KEYRING_PASSWORD` を設定する。

## 最新順取得（重要）

`gog gmail search` にはソート順を指定するフラグがない。  
返却順は日付降順と一致しないことがあるため、取得後にローカルで再ソートする。

直近 20 件を取得して新しい順の先頭 1 件を取る:

```bash
/home/yuiseki/bin/gog --account <email> gmail search '<query>' --max 20 --json \
| sed -n '/^{/,$p' \
| jq -r '.threads | sort_by(.date) | reverse | .[0]'
```

- `<query>` 例: `is:starred in:inbox`
- 20 件で不足する場合は `--max 50` または `--all` を使う。
- TTY 環境では keyring パスフレーズプロンプトが標準出力に混ざることがあるため、`sed -n '/^{/,$p'` で JSON 開始行までを捨てる。

## 次から活用できるノウハウ

- 「未読があるかだけ」を判定するときは `--max 1 --fail-empty` を使い、件数取得や詳細取得を分離する。
- 自動化用途は `--json --no-input` を基本にする。
- `file` keyring backend では TTY 依存が出るため、CI は `GOG_KEYRING_PASSWORD` 前提で設計する。
- まず read 操作（`gmail search`）で疎通を確認し、write 操作は後に回す。
- `gmail search` の返却順は最新順保証ではないため、`sort_by(.date) | reverse` で必ず再ソートしてから「最新」を判断する。
