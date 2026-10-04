---
name: searchcans-market-watch-zh
description: 使用 SearchCans Google 搜索、Google News、Bing 搜索和选定 Reader 提取创建有界、地域化、可追溯的市场观察快照。适用于竞品与品类监测、公关和新闻追踪、发布情报，以及两个有限运行之间的 URL 级变化检查；在 Reader 前拒绝格式异常、占位或无法归属的新闻候选。
metadata:
  author: SearchCans
  version: 1.1.0
  tags: [serp-api, google-news-api, bing-search-api, market-intelligence, chinese]
---

# SearchCans 市场观察

为一个查询和一个市场建立可追溯的市场快照。默认获取 Google 网页、Google News 与 Bing 结果，再读取数量严格受限、域名尽量多样且可用的新闻页面。它是按需运行的快照，不是后台监测或告警服务。

## 先定义市场问题

确认查询、`country`、`language`、业务问题，以及是否需要与既有 JSON 快照比较。若市场选择会实质改变结论，不得擅自假设。

仅在执行环境中设置 `SEARCHCANS_API_KEY`；不得将 Key 写入提示词、源码、产物或提交。

```bash
python scripts/market_watch.py "AI 搜索 API" \
  --country us --language zh --max-source-reads 3 \
  --out market-watch.json
```

仅当 Google 双搜索面已足够时使用 `--without-bing`。使用 `--baseline prior-market-watch.json` 时，只报告新观察到或不再观察到的 URL；这不等同于页面新发布、删除或不可访问。

## 让账户决定安全范围

默认的 `--account-mode auto` 发起一次脱敏的 Account API 预检，估算三次 SERP 调用和所请求 Reader 调用，并在可行时只收缩 Reader 范围；并行数不超过账户报告的 Parallel Lane 数。

- `auto`：按可用预算收缩 Reader 来源数。
- `enforce`：预算不足时在业务请求前停止。
- `warn`：保留范围，但记录预算警告。
- `off`：跳过预检。

输出仅保留安全的预算摘要，不写入账户身份或 Key。从 `--proxy 0` 开始；更高代理档位会改变 Reader 成本，只能用于已确认的访问问题。

## 正确解释证据

将 `google_news.results` 视为标题和发布时间元数据，将 `news_source_quality` 视为候选接受/拒绝状态，将 `read_sources` 视为更完整的页面证据。只有 Reader 成功返回内容的 URL 才会进入 `claim_eligible_urls`。

只有标题和发布者非空、URL 有效且不是 Google 占位页、并通过质量检查的候选才可交给 Reader。若 `news_source_quality.status` 为 `no_usable_news_sources`，应报告该市场和查询在 News 搜索面没有可用的新闻文章证据；不得重试被拒绝的占位 URL，也不得将其写成新闻事实。

使用 [报告模板](references/market-watch-report.md) 输出：

1. 市场/查询定义和准确检索时间。
2. 按搜索面分开的网页与新闻观察。
3. 每项确认发展及其 Reader URL。
4. 跨引擎差异、未解决问题和下一次运行建议。

SERP 标题、摘要、日期和排名仅是发现线索，不能单独证明事实、品牌定位、新闻重要性或商业影响。

## 官网

[SearchCans 官网](https://www.searchcans.com/)

## 资源

- `scripts/market_watch.py`：生成有界 JSON 证据包。
- `references/market-watch-report.md`：报告结构和主张边界。
