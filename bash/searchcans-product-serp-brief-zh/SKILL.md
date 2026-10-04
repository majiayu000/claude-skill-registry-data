---
name: searchcans-product-serp-brief-zh
description: 使用 SearchCans Google Shopping、Google 网页、Google 图片和明确指定的 Reader 商家 URL 创建地域化商品搜索证据简报。适用于电商品类研究、竞品商品组合发现、商品页规划和市场特定的陈列策略简报。
metadata:
  author: SearchCans
  version: 1.1.0
  tags: [serp-api, google-shopping-api, google-images-api, ecommerce, chinese]
---

# SearchCans 商品 SERP 简报

将一个商品查询转为当前、特定市场的观察包。它并列获取 Shopping、网页和图片结果，便于对比商品列表、商家名称、搜索意图和视觉搜索呈现；不得把它写成完整商品目录或实时价格数据库。

## 定义商品问题

确认查询、目标 `country`、`language` 和所支持的决策。若结果用于商品组合或页面规划，优先使用具体商品/品类查询，而不是宽泛的“最佳”查询。

```bash
python scripts/product_serp_brief.py "便携式意式咖啡机" \
  --country us --language zh --max-products 10 \
  --read-url "https://merchant.example/product" \
  --out product-brief.json
```

`--read-url` 必须明确指定：不得自动抓取 Google Shopping 商品链接或商家页面。只添加本次调查相关、且在来源预算内的 URL。

## 负责任地使用价格和素材

`merchant_observations.observed_numeric_price_range` 仅描述选定市场中一页 Google Shopping SERP 上可解析的展示数值。它有时间戳，未做货币归一化，不保证价格、库存、运费、评分、评价或可用性。

图片 URL 与缩略图只是发现线索；被展示不授予下载、复用、训练或再发布任何素材的权限。

使用 [报告模板](references/product-brief-report.md) 区分：

1. 市场/查询和收集边界。
2. 已观察的商品、商家和价格模式。
3. 网页与视觉结果中的页面类型信号。
4. 由成功 Reader 提取支撑的页面级主张。
5. 商业行动前仍需人工验证的缺口。

## 让账户设置安全范围

默认的 `--account-mode auto` 只检查一次 Account API，估算三次 SERP 调用和明确 Reader URL，在需要时仅收缩来源读取，并让并发不超过报告的 Parallel Lane。任务有不同预算策略时使用 `warn`、`enforce` 或 `off`。JSON 只包含脱敏后的账户保护字段。

## 官网

[SearchCans 官网](https://www.searchcans.com/)

## 资源

- `scripts/product_serp_brief.py`：获取地域化商品证据包。
- `references/product-brief-report.md`：分析简报与注意事项。
