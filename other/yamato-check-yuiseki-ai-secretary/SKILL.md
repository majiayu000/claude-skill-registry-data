---
name: yamato-check
description: 明日以降のヤマト運輸「お荷物お届けのお知らせ」を確認し、明日の Google Calendar 予定と受取時間を突合する。ズレがあれば yamato-change で全件そろえ、変更後に yuiseki@gmail.com へ完了通知メールを送る。
---

# Yamato Check

## 目的

- 明日以降のヤマト運輸配達メールをチェックする。
- 明日のカレンダー予定（受取想定時間）とヤマト受取時間を一致させる。
- ズレがある場合は `yamato-change` で変更し、変更完了通知を `yuiseki@gmail.com` に送る。

## 使うスキル（順序固定）

1. `yamato-check`（本スキル）で対象メールの抽出と差分判定
2. `.codex/skills/gog-calendar/SKILL.md` で明日の予定を取得
3. 差分がある場合のみ `.codex/skills/yamato-change/SKILL.md` で受取日時変更
4. 変更が1件以上あれば `gog send` で完了通知

## 前提

- `gog` バイナリ: `/home/yuiseki/bin/gog`
- アカウント: `yuiseki@gmail.com`
- `gog` は `keyring_backend=file` のため必要なら TTY で実行する

## 実行フロー

### 1) 明日以降のヤマト通知を取得

```bash
/home/yuiseki/bin/gog --account yuiseki@gmail.com gmail search \
  'from:mail@kuronekoyamato.co.jp in:inbox newer_than:7d' \
  --max 20 --json | sed -n '/^{/,$p'
```

- 件名に `お荷物お届けのお知らせ` を含むスレッドを対象にする。
- `【郵便受け】` は時間調整不要として除外してよい。

### 2) 明日のカレンダー予定を取得（ターゲット時間）

```bash
/home/yuiseki/bin/gog --account yuiseki@gmail.com calendar events primary --tomorrow --json \
| sed -n '/^{/,$p'
```

- `summary` に `荷物` または `ヤマト` を含む予定を優先してターゲット時間にする。
- 例: `2026-02-20T19:00:00+09:00` 〜 `2026-02-20T21:00:00+09:00`
- 予定が複数ある場合は、最も具体的な時刻（all-day でない）を採用する。

### 3) ヤマト受取時間との突合

- 各対象メールから荷物詳細リンク（`member.kms.kuronekoyamato.co.jp/parcel/detail`）を抽出する。
- 現在の受取希望時間帯を確認する。
- カレンダーのターゲット時間と一致しない荷物だけを「変更対象」にする。

### 4) 変更対象がある場合のみ `yamato-change` を実行

- `.codex/skills/yamato-change/SKILL.md` の手順で、変更対象すべてを同じ時間帯に合わせる。
- 変更対象が0件なら変更しない。

### 5) 変更完了通知メール（変更があった時だけ）

件名と本文例:

- 件名: `ヤマト受取日時の変更完了（YYYY-MM-DD）`
- 本文:
  - 変更日時
  - 対象件数
  - 各荷物（送り状番号）の変更前/変更後時間
  - 明日のカレンダー基準時間

`gog send` 例（dry-run → 本実行）:

```bash
/home/yuiseki/bin/gog --dry-run --account yuiseki@gmail.com send \
  --to yuiseki@gmail.com \
  --subject 'ヤマト受取日時の変更完了（2026-02-20）' \
  --body 'ヤマト受取日時を明日のカレンダー予定に合わせて変更しました。対象: 1件。変更後: 19時-21時。' \
  --plain
```

```bash
/home/yuiseki/bin/gog --account yuiseki@gmail.com send \
  --to yuiseki@gmail.com \
  --subject 'ヤマト受取日時の変更完了（2026-02-20）' \
  --body 'ヤマト受取日時を明日のカレンダー予定に合わせて変更しました。対象: 1件。変更後: 19時-21時。' \
  --plain
```

## 完了報告フォーマット

- チェック日時
- 対象メール件数
- 変更対象件数
- 実際に変更した件数
- 通知メール送信有無

