---
name: weather-calendar
description: 指定地点の天気を `weathercli` で取得し、Google Calendar の「1 天気ログ」へ終日予定として記録する。ユーザーが「今日の天気をカレンダーに記録して」「天気ログを作成して」「天気を予定に残して」と依頼したときに使う。
---

# Weather Calendar

## 事前確認
- `weathercli` と `gog` を利用可能にする。
- 実行前に `.env` から `GOG_KEYRING_PASSWORD` を読み込む。

```bash
export $(grep -v '^#' /home/yuiseki/Workspaces/.env | xargs)
```

## 手順

1. `weathercli` で指定座標の天気を JSON 取得する。

```bash
weathercli --lat 35.7126 --lon 139.7799 --json
```

2. 「1 天気ログ」カレンダーの ID を取得する。

```bash
CAL_ID=$(/home/yuiseki/bin/gog --account yuiseki@gmail.com calendar calendars --json | sed -n '/^{/,$p' | jq -r '.calendars[] | select(.summary=="1 天気ログ") | .id')
```

3. `天候 | 最低気温 ～ 最高気温` の形式で終日予定を作成する。

```bash
/home/yuiseki/bin/gog --account yuiseki@gmail.com calendar create "$CAL_ID" \
  --summary "晴れ | 1.4°C ～ 13.3°C" \
  --description "最高気温: 13.3°C / 最低気温: 1.4°C\n天候: 晴れ" \
  --from "2026-02-21" --to "2026-02-21" \
  --all-day --force
```

## 運用ルール
- カレンダー名は必ず `1 天気ログ` を使用する。
- 気温は `daily.temperature_2m_max` と `daily.temperature_2m_min` を使用する。
