---
name: weather
description: |
  現在地（IPベース）や指定した主要都市（東京、大阪、名古屋、札幌、福岡）の天気を取得し、現在の状況と向こう3日間の予報を表示する。
---

# Weather CLI Skill Runbook

## 概要
`weathercli` を使用して、現在の天候と 3 日間の予報を取得します。デフォルトでは実行環境の IP アドレスから現在地を自動特定し、その場所の天気を報告します。

## 前提
- 実行コマンド: `weathercli`
- データソース: Open-Meteo API (API キー不要)
- 位置特定: IP-API (IP ベースのジオコーディング)

## 基本コマンド

### 1. 現在地の天気を取得
引数なしで実行すると、IP アドレスから現在地を特定して天気を表示します。
```bash
weathercli
```

### 2. 指定した都市の天気を取得
プリセットされている主要都市を指定して取得します。
```bash
weathercli --location osaka      # 大阪
weathercli --location sapporo    # 札幌
weathercli --location nagoya     # 名古屋
weathercli --location fukuoka    # 福岡
weathercli --location tokyo      # 東京 (明示的な指定)
```

### 3. キャッシュを強制更新
30 分間のキャッシュを無視して、最新の情報を取得します。
```bash
weathercli --sync
```

## AI 秘書としての活用シナリオ
- **朝のサマリー:** `heartbeat` の一環として実行し、「今日の天気」をユーザーに報告する。
- **予定の調整:** カレンダーに外出予定がある場合、その場所や時間帯の天気を事前にチェックして提案する。
- **旅行・出張:** ユーザーが特定の都市（例：大阪）に行く予定がある際、`make ls-osaka` で現地の予報を伝える。

## 運用ルール
- 30 分以内であれば自動的にキャッシュ（`cache/current.json` 等）が使用され、高速にレスポンスを返します。
- 天候コード（WMO Weather interpretation codes）は、人間が読みやすいラベル（晴れ、曇り、雨など）に自動変換して表示されます。
- 位置特定に失敗した場合は、デフォルトで東京（Tokyo）の天気を表示します。

## 出力例
```text
Weather Report: Tokyo (Detected) (Cache)
==============================
Current: 9.6°C, Mainly clear
Wind Speed: 2.6 km/h

--- 3-Day Forecast ---
2026-02-20: 9.7°C / 0°C - Overcast
2026-02-21: 13.2°C / 2.1°C - Mainly clear
2026-02-22: 15.6°C / 4.4°C - Mainly clear
```
