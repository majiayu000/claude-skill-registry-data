---
name: gog-calendar
description: gog CLI で Google Calendar の予定を確認し、認証・TTY・keyring の問題を切り分ける手順。ユーザーが「今日の予定を確認したい」「gog でカレンダーを見たい」「calendar events のエラーを直したい」と依頼したときに使う。
---

# Gog Calendar Events Check

## 最短チェック（今日の予定）

```bash
/home/yuiseki/bin/gog --account <email> calendar events primary --today --plain --all-pages --max 50
```

- 予定があるかだけ確認する場合:

```bash
/home/yuiseki/bin/gog --account <email> calendar events primary --today --max 1 --plain --fail-empty
```

- `exit code 0`: 1件以上あり
- `exit code 3`: `--fail-empty` で0件

## この環境で分かったこと（2026-02-19）

- 実行バイナリは `./bin/gog` ではなく `/home/yuiseki/bin/gog`。
- config path は `/home/yuiseki/.config/gogcli/config.json`。
- keyring backend は `file`。
- 非 TTY ではトークン読込が失敗することがある:
  - `no TTY available for keyring file backend password prompt; set GOG_KEYRING_PASSWORD`
- 利用アカウントは `yuiseki@gmail.com`。
- `calendar events ... --plain` の出力列は `ID START END SUMMARY`。

## 手順

1. コマンド仕様を確認する。

```bash
/home/yuiseki/bin/gog calendar events --help
```

2. 認証状態と keyring backend を確認する。

```bash
/home/yuiseki/bin/gog auth status
/home/yuiseki/bin/gog auth keyring
```

3. `--account` を明示して予定を取得する。

```bash
/home/yuiseki/bin/gog --account <email> calendar events primary --today --plain --all-pages --max 50
```

4. keyring のパスフレーズ入力待ちになったら TTY で実行する。
5. 非対話で実行する場合は `GOG_KEYRING_PASSWORD` を設定する。

## 次から活用できるノウハウ

- 「有無だけ判定」は `--max 1 --fail-empty` を使う。
- 「今日の全件取得」は `--today --all-pages --max <十分な件数>` を使う。
- 自動化用途は `--json --no-input` を基本にする。
- 全カレンダー横断が必要なら `calendar events --all --today` を使う。
- 期間指定が必要なら `--from`/`--to` または `--days`/`--week` を使う。
- テキスト絞り込みは `--query` を使う。
