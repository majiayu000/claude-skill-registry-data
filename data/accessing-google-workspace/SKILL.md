---
name: accessing-google-workspace
description: >
  gcloud CLI を使用して Google Sheets/Docs にアクセス。
  ユーザーが Google Sheets/Docs の URL を共有したとき、または
  スプレッドシート, Sheets, Docs, Google ドキュメントに言及したときに使用。
allowed-tools:
  - Bash
  - Read
user-invocable: false
---

# Google Workspace アクセス

CLI 経由で Google Sheets/Docs にアクセスするスキル。

## URL 検出

| パターン                          | タイプ        |
| --------------------------------- | ------------- |
| `docs.google.com/spreadsheets/d/` | Google Sheets |
| `docs.google.com/document/d/`     | Google Docs   |

## コマンド

### Google Sheets

```bash
# CSV形式
gsheet "URL"

# JSONL形式（構造化データ向け）
gsheet "URL" json
```

### Google Docs

```bash
# テキスト形式
gdoc "URL"

# Markdown形式
gdoc "URL" md
```

## フォーマット選択

| データ種別     | 推奨フォーマット     |
| -------------- | -------------------- |
| 表形式データ   | `json` (JSONL)       |
| 文書・仕様書   | `md` (Markdown)      |
| シンプルな取得 | デフォルト (CSV/txt) |
