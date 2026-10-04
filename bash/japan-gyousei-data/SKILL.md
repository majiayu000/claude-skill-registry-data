---
name: japan-gyousei-data
description: 日本の行政オープンデータにアクセスする。不動産取引価格（国交省）、官公需・入札情報、e-Stat政府統計の3つのデータソースを検索・取得できる。「不動産価格を調べて」「入札情報を検索」「政府統計を取得」「官公需で○○を探して」「地価を調べて」「統計データ」などで使用。MCP server (mcp.n-3.ai) 経由でリアルタイムにデータ取得する。
---

# 行政オープンデータスキル

日本政府のオープンデータに MCP サーバー（`mcp.n-3.ai`）経由でアクセスする。

## データソース

| # | 名前 | 用途 | ツール |
|---|------|------|--------|
| 1 | 不動産取引価格 | 国交省の実取引データ | `reinfolib-real-estate-price`, `reinfolib-city-list` |
| 2 | 官公需（入札） | 政府・自治体の調達案件検索 | `kkj-search` |
| 3 | e-Stat | 政府統計ポータル | `e-stat-get-stats-list`, `e-stat-get-meta-info`, `e-stat-get-data-catalog` |

## 呼び出し方法

`exec` で `curl` を使う。`web_fetch` は SSE 非対応のため不可。

スクリプト `scripts/mcp-call.sh` を使う:

```bash
bash <skill_dir>/scripts/mcp-call.sh <data_source> <tool_name> '<arguments_json>'
```

### 例

```bash
# 不動産: 大阪市の取引価格
bash scripts/mcp-call.sh reinfo reinfolib-real-estate-price '{"year":"2025","quarter":"3","area":"27","city":"27102"}'

# 不動産: 市区町村一覧を取得
bash scripts/mcp-call.sh reinfo reinfolib-city-list '{"area":"27"}'

# 官公需: AI関連の入札検索（カテゴリ3=役務）
bash scripts/mcp-call.sh kkj kkj-search '{"query":"AI 人工知能","category":"3"}'

# e-Stat: 統計一覧検索
bash scripts/mcp-call.sh estat e-stat-get-stats-list '{"searchWord":"人口"}'
```

## ツール詳細

各ツールのパラメータ詳細は `references/tools.md` を参照。

## 注意点

- **官公需の地域フィルタ**: `kkj-search` は都道府県パラメータ未対応。クエリ文字列に地名を含めて絞り込む
- **官公需の詳細情報**: MCP は検索結果一覧のみ返す。仕様書・金額・締切は元ポータルサイトを確認
- **不動産の都道府県コード**: 2桁コード（東京=13, 大阪=27 等）。市区町村コードは `reinfolib-city-list` で取得
- **e-Stat**: まず `get-stats-list` で統計IDを特定し、`get-meta-info` でメタ情報、`get-data-catalog` でデータ取得
- **レート制限**: 公共APIのため常識的な頻度で利用する
