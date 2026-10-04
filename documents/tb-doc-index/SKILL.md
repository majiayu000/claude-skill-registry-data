---
name: tb-doc-index
description: Use when locating TBQ3 documentation, function references, examples, or source docs under docs without loading the full corpus; supports rg-based search and curated topic/function indexes.
---

# TBQ3 文档索引

本 skill 用于在 `docs` 中定位资料。默认使用 `rg` 精确搜索，避免把 1000+ 篇文档全部放入上下文。

## 检索流程

1. 先读 `references/topic-index.md` 判断是否已有主题入口。
2. 查函数时读 `references/function-index.md`。
3. 如果索引没有覆盖，用 `rg -n "关键词" docs -g '*.md'` 搜索。
4. 只打开最相关的 1-3 篇原文；长文档先用 `rg -n` 定位小节。
5. 回答或生成代码时，优先引用已查证的函数和文档路径。

## 常用搜索词

- Bar 策略：`策略代码说明|MarketPosition|BuyToCover|BarsSinceEntry`
- 止盈止损：`止盈|止损|AvgEntryPrice|MinMove|PriceScale`
- 资金手数：`固定资金|固定保证金|ContractUnit|BigPointValue|MarginRatio`
- 事件驱动：`OnReady|OnBar|OnOrder|OnPosition|SubscribeBar|Timer`
- 委托交易：`发单|撤单|委托|持仓|成交|A_SendOrder`
- 跨周期多品种：`跨周期|多品种|数据源|套利`
- Plot：`Plot|画板|线型|ICON|颜色|表格`

## 使用边界

索引是入口，不是最终依据。涉及交易函数签名、枚举值、事件参数、结构体字段时，应打开原文确认。
