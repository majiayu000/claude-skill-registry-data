---
name: gog-task
description: gog CLI で Google Tasks（ToDo）の追加・更新・完了を実行する手順。ユーザーが「ToDoを追加して」「タスク更新して」「メール確認してタスク更新して」と依頼したときに使う。メール起点の依頼では先に .codex/skills/gog-gmail/SKILL.md を使ってメール内容を確認し、その結果を Tasks に反映する。
---

# Gog Tasks Update

## 前提

- 実行バイナリは `/home/yuiseki/bin/gog` を使う。
- API コマンドは `--account <email>` を常につける。
- この環境は keyring backend が `file` のため、非 TTY では失敗することがある。
- 失敗時の代表エラー:
  - `no TTY available for keyring file backend password prompt; set GOG_KEYRING_PASSWORD`

## 連携フロー（メール確認してタスク更新して）

1. 先に `.codex/skills/gog-gmail/SKILL.md` を使い、対象メールを確定する。
2. メールから最低限の情報を抽出する。
   - `date`
   - `from`
   - `subject`
   - `action`（何をやるか）
3. Tasks に反映する。
   - 同種の未完了タスクがあるなら `update`
   - なければ `add`
4. 完了報告時は `done` を使ってクローズする。

## タスクリスト選択

タスクリスト一覧:

```bash
/home/yuiseki/bin/gog --account <email> tasks lists list --json
```

`マイタスク` の ID を取得:

```bash
/home/yuiseki/bin/gog --account <email> tasks lists list --json \
| sed -n '/^{/,$p' \
| jq -r '.tasklists[] | select(.title=="マイタスク") | .id'
```

## 追加（add）

まず dry-run:

```bash
/home/yuiseki/bin/gog --dry-run --account <email> tasks add <tasklistId> \
  --title '<title>' \
  --notes 'メール: <subject> (<date>) / from: <from> / action: <action>' \
  --json
```

問題なければ本実行:

```bash
/home/yuiseki/bin/gog --account <email> tasks add <tasklistId> \
  --title '<title>' \
  --notes 'メール: <subject> (<date>) / from: <from> / action: <action>' \
  --json
```

## 更新（update）

既存タスクを検索:

```bash
/home/yuiseki/bin/gog --account <email> tasks list <tasklistId> --all --show-completed --json \
| sed -n '/^{/,$p' \
| jq -r '.tasks[] | select(.status=="needsAction" and (.title | contains("<keyword>"))) | .id'
```

更新実行:

```bash
/home/yuiseki/bin/gog --account <email> tasks update <tasklistId> <taskId> \
  --notes '<latest notes>' \
  --json
```

## 完了（done）

```bash
/home/yuiseki/bin/gog --account <email> tasks done <tasklistId> <taskId> --json
```

## 次から活用できるノウハウ

- Write 操作（`add`/`update`/`done`）の前に `--dry-run` で確認する。
- メール起点タスクは `subject` と `date` を notes に残し、追跡可能にする。
- `gmail search` の返却順は最新保証ではないため、メール特定は `.codex/skills/gog-gmail/SKILL.md` の再ソート手順を使う。
- TTY 実行時にパスフレーズプロンプトが標準出力へ混ざる場合があるため、JSON パース前に `sed -n '/^{/,$p'` で先頭ノイズを除去する。
