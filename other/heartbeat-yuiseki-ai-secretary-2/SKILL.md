---
name: heartbeat
description: 30分ごとに秘書モードで Yamato/Gmail/Tasks/Calendar を巡回し、(1) yamato-check で明日の受取時間整合をチェック、(2) メール確認、(3) メール由来のタスク追加・更新の提案、(4) 必要な予定のカレンダー追加の提案、(5) 未完了タスクのリマインドを行う。書き込み操作は必ずユーザーの承認を得る。Google Drive と Contacts は対象外。
---

# Heartbeat Assistant Runbook

## 対象と非対象

- 対象:
  - Gmail
  - Google Tasks
  - Google Calendar
- 非対象:
  - Google Drive
  - Contacts/People

## 実行順序（固定）

1. `.codex/skills/weather/SKILL.md` (`make run`) で天気を取得
2. `.codex/skills/news/SKILL.md` (`make run`) でニュースを取得
3. `.codex/skills/gog-gmail/SKILL.md` および `.codex/skills/gog-calendar/SKILL.md` で情報を取得
4. `.codex/skills/hatebu/SKILL.md` (`hatebu ls --json`) でブックマークを取得
5. `.codex/skills/gyazo/SKILL.md` (`gyazo ls --limit 20 --json`) でキャプチャを取得
6. `.codex/skills/gh-check-notification/SKILL.md` および `.codex/skills/gh-check-activity/SKILL.md` で GitHub 状況を取得
7. 取得した全情報を `/home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache/` に保存する
8. メール内容からタスク追加・更新、予定追加の「提案リスト」を作成
9. ユーザーに提案リストを提示し、承認を得る
10. 承認された項目のみ、タスク・カレンダーに反映
11. 未完了タスクをリマインド
12. `.codex/skills/yamato-check/SKILL.md` で明日のヤマト受取時間を確認・必要なら変更を提案

## 前提

- 実行バイナリは `/home/yuiseki/bin/gog` を使う。
- API 操作は `--account <email>` を必ず付与する。
- keyring backend が `file` のため、非 TTY では失敗することがある。
- TTY でパスフレーズプロンプトが混ざる場合、JSON パース前に `sed -n '/^{/,$p'` を通す。
- 必ず .env に書かれた `GOG_KEYRING_PASSWORD` を export する。
- heartbeat の作業ディレクトリは `/home/yuiseki/Workspaces/.ai-secretary/heartbeat` を使う。
- 取得した情報のキャッシュは `/home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache/` を使う。
- 初回実行時に以下を作成する。

```bash
mkdir -p /home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache
mkdir -p /home/yuiseki/Workspaces/.ai-secretary/heartbeat/logs
```

## 状態ファイル（重複防止）

`/home/yuiseki/Workspaces/.ai-secretary/heartbeat/state.json` を使う。存在しない場合は初期化する。

```json
{
  "last_run_at": "",
  "last_mail_scan_at": "",
  "processed_thread_ids": []
}
```

- `processed_thread_ids` は最新 200 件のみ保持する。
- 同一スレッドを再処理しないことを最優先にする。
- 実行ログは `/home/yuiseki/Workspaces/.ai-secretary/heartbeat/logs/` に保存する。

## Personalization Rules

- ルールディレクトリ: `/home/yuiseki/Workspaces/.ai-secretary/heartbeat/personalization-rules/`
- 各ルールは `<rule-name>/RULE.md` 形式で置く。
- heartbeat 実行時はメール分類の前にルールを読み込む。
- 競合時は「無視ルール（ignore）」を優先する。

読み込み確認例:

```bash
find /home/yuiseki/Workspaces/.ai-secretary/heartbeat/personalization-rules -name RULE.md -maxdepth 3 -type f
```

既知ルール例:

- `ignore-yamato`: ヤマト運輸の「お荷物お届けのお知らせ」を無視する。
  - 判定目安: `from` が `mail@kuronekoyamato.co.jp` かつ `subject` に `お荷物お届けのお知らせ` を含む。
  - 動作: 一般メール分類（タスク/予定化）では無視する。`processed_thread_ids` には記録して再判定を防ぐ。
  - 例外: `yamato-check` ステップでは必ず判定対象にする。
- `ignore-vercel`: Vercel の `Failed preview deployment` 通知を無視する。
  - 判定目安: `from` が `notifications@vercel.com` かつ `subject` に `Failed preview deployment` を含む。
  - 動作: タスク/カレンダー化しない。

## 30分ごとの実行手順

1. 現在時刻と認証状態を確認する。

```bash
/home/yuiseki/bin/gog auth status
/home/yuiseki/bin/gog time now --json
```

2. 情報を順番に取得し、`/home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache/` に JSON 形式で保存する。

- **Weather:** 現在地の天気を取得
  ```bash
  cd /home/yuiseki/Workspaces/repos/weathercli && make run > /dev/null && cp cache/current.json /home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache/weather.json
  ```
- **News:** 最新ニュースを取得
  ```bash
  cd /home/yuiseki/Workspaces/repos/newscli && make run > /dev/null && cp cache/news.json /home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache/news.json
  ```
- **Gmail:** `newer_than:1d` で最近のメールを取得
  ```bash
  /home/yuiseki/bin/gog --account <email> gmail search 'newer_than:1d' --json | sed -n '/^{/,$p' > cache/gmail.json
  ```
- **Calendar:** 今日の予定を取得
  ```bash
  /home/yuiseki/bin/gog --account <email> calendar list --json | sed -n '/^{/,$p' > cache/calendar.json
  ```
- **Hatebu:** 今日のブックマークを取得
  ```bash
  hatebu ls --json > cache/hatebu.json
  ```
- **Gyazo:** 直近の画像を取得
  ```bash
  gyazo ls --limit 20 --json > cache/gyazo.json
  ```
- **GitHub:** 通知と活動状況を取得
  ```bash
  gh api notifications > cache/gh_notifications.json
  gh search prs --author "@me" --sort updated --limit 5 --json title,state,repository,updatedAt > cache/gh_prs.json
  gh search issues --author "@me" --sort updated --limit 5 --json title,state,repository,updatedAt > cache/gh_issues.json
  ```

3. 取得した全情報を `/home/yuiseki/Workspaces/.ai-secretary/heartbeat/cache/YYYY-MM-DD-HHMM.json` としてアーカイブ保存する。

4. Gmail の未処理スレッドを抽出し、Personalization Rules を適用して「反映案（提案リスト）」を作成する。
- タスク化提案条件:
  - 返信・提出・確認・対応などの行動が必要
  - 期限や依頼が含まれる
- カレンダー化提案条件:
  - 明確な日時（開始・終了、または日付）を含む予定

5. ユーザーに提案リスト（タスク追加/更新、予定追加）および各ソース（Hatebu, Gyazo, GitHub）のサマリーを提示し、実行の是非を確認する。

6. 承認された項目を反映する（重複防止付き）。
- タスク反映: notes 末尾に必ず `heartbeat-thread:<threadId>` 等を残す。
- カレンダー反映: `calendar search` で `heartbeat-thread:<threadId>` を検索し、重複を確認する。

7. 未完了タスクをリマインドする。
- `tasks list` で `needsAction` を列挙し、上位 5 件を通知する。
- **未完了のToDoは `.ai-secretary/heartbeat/todos/yyyy/mm/dd/todo.md` にチェックボックス形式で書き溜める。**

8. `yamato-check` を実行する。

- 明日以降のヤマト通知を確認する。
- `.codex/skills/gog-calendar/SKILL.md` で明日の予定を確認する。
- **既に受取日時を変更済みの場合はスキップする。**
- 受取時間にズレがあれば、変更案をユーザーに提示し、承認を得てから `.codex/skills/yamato-change/SKILL.md` を実行する。
- 変更を行った場合は `yuiseki@gmail.com` に完了通知を送る。

## 実用コマンド例

タスクリスト ID（`マイタスク`）取得:

```bash
/home/yuiseki/bin/gog --account <email> tasks lists list --json \
| sed -n '/^{/,$p' \
| jq -r '.tasklists[] | select(.title=="マイタスク") | .id'
```

未完了タスク一覧:

```bash
/home/yuiseki/bin/gog --account <email> tasks list <tasklistId> --all --json \
| sed -n '/^{/,$p' \
| jq -r '.tasks // [] | map(select(.status=="needsAction"))'
```

カレンダー重複確認（thread ID をキーに照合）:

```bash
/home/yuiseki/bin/gog --account <email> calendar search 'heartbeat-thread:<threadId>' --calendar primary --max 1 --json \
| sed -n '/^{/,$p'
```

## 出力フォーマット

各回の終了時に必ず次を報告する。

- 実行時刻
- yamato-check 確認対象件数
- yamato-change 提案件数
- **Weather** 現在の天候と気温
- **News** 主要な見出し数点
- 走査メール件数（提案・承認結果を含む）
- **Hatebu** 今日取得した件数
- **Gyazo** 直近のキャプチャ数
- **GitHub** 未読通知件数および活動更新
- 未完了タスクの要約（最大 5 件）
- キャッシュ保存先 (`cache/YYYY-MM-DD-HHMM.json`)

## 運用ルール

- **ユーザーへの報告や提案、対話は、常に日本語（Japanese）で行うこと。**
- **全ての書き込み系操作（追加・更新・削除・設定変更）は、実行前に必ずユーザーに詳細を提示し、明示的な承認を得ること。**
- 曖昧なメールは勝手にカレンダー案に入れず、まずタスク案として提示する。
- **ヤマトの受取日時変更時、既に変更済みであれば何もしない。また、変更先に予定が競合する場合は必ずその情報を添えてユーザーに確認する。**
- **ToDoの管理は Google Tasks と同期しつつ、`.ai-secretary/heartbeat/todos/` 下の markdown ファイルにも記録・更新する。**
- 失敗時は処理を止めず、失敗した対象とエラーを報告して次へ進む。

