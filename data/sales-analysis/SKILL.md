---
name: sales-analysis
version: 1.0.0
description: 销售数据分析 — 指标口径查询、趋势分析、异常检测
author: data-team
tags: [sales, analysis, reporting]

triggers:
  keywords: [销售额, GMV, 客单价, 复购, 转化率, 退款, 毛利, 销售趋势, 品类分析, 同比, 环比, 季度]
  intents: [query, aggregation, trend]
  tables: [orders, order_items, products]

depends_on:
  mcp_servers: []
  skills: []
  python_packages: [pandas]

tools: []
---

# 销售数据分析技能

## 激活条件
用户查询涉及销售指标(GMV/客单价/复购率/转化率/退款率)或分析场景(品类排行/趋势分析/同比环比)。

## 激活后行为
1. 优先从知识库检索指标定义, 确保 SQL 计算口径一致
2. 对时间序列结果自动计算环比增长率
3. 异常指标主动标注 (退款率 > 5%, 转化率 < 60%)
4. 分析完成后推荐 1-2 个下钻分析维度

## 指标速查
| 指标 | 计算公式 | 正常范围 |
|------|---------|---------|
| GMV | SUM(quantity * unit_price) WHERE status IN ('paid','completed') | — |
| 客单价 | GMV / 去重用户数 | 800-3000 |
| 转化率 | 已支付/总下单 | 60%-95% |
| 复购率 | 多次下单用户/总用户 | 20%-50% |
| 退款率 | 退款/总订单 | < 5% |
