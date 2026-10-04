---
name: hugo-quality
description: Hugo品質チェック。ビルド/リンクチェック/テンプレート解析時に使用。「Hugoの品質チェック」「ビルド検証」で起動。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
build: `hugo` | links: `htmltest` | metrics: `hugo --templateMetrics` | content: `hugo list drafts/expired/future`

## Standards

| 項目 | 目標 |
|------|------|
| ビルド | エラー0 |
| リンク切れ | 0件 |
| 下書き | 本番デプロイ時は0 |

## Reference
- [reference.md](reference.md)
