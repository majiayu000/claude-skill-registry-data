---
name: research-news
description: Yahoo! Japan ニュースから最新ニュースを収集・整理するスキル。「主要」「国内」「国際」「経済」の4ジャンルから各3件のニュースを取得し、タイトル・概要・ポイントを整理して通知する。ニュースリサーチ、最新情報の収集、ニュースサマリー作成時に使用。
---

# Yahoo! Japan ニュースリサーチ

## 概要

Yahoo! Japan ニュースから4ジャンルのニュースを収集し、整理して報告する。

## カテゴリURL

| カテゴリ | URL |
|---------|-----|
| 主要 | https://news.yahoo.co.jp/ |
| 国内 | https://news.yahoo.co.jp/categories/domestic |
| 国際 | https://news.yahoo.co.jp/categories/world |
| 経済 | https://news.yahoo.co.jp/categories/business |

## 実行手順

1. 上記4つのURLにWebFetchでアクセス
2. 各カテゴリから上位3件のニュース記事を抽出
3. 各記事について以下を取得:
   - タイトル
   - 概要（記事の要約）
   - 記事へのリンク
4. 必要に応じて個別記事ページにアクセスし詳細を取得

## 出力フォーマット

```
## [カテゴリ名]

### 1. [記事タイトル]
**概要**: [記事の概要を2-3文で]

**ポイント**:
- [重要ポイント1]
- [重要ポイント2]

[続きを読む](記事URL)

---
```

## WebFetch プロンプト例

各カテゴリページへのアクセス時:
```
List the top 3 news articles with their titles, brief descriptions, and URLs. Format as structured data.
```

個別記事ページへのアクセス時:
```
Extract the article title, main content summary, and key points from this news article.
```

## 注意事項

- 各カテゴリ3件ずつ、合計12件のニュースを収集
- リンクは必ず元記事のURLを提示
- 概要は簡潔に、ポイントは箇条書きで整理
