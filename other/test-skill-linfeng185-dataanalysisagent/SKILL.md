---
name: test-skill
description: 销售数据分析专用技能——GMV计算、客户分层、商品排名、品类占比
intents:
  - aggregation
  - ranking
  - proportion
version: "1.0"
author: 测试团队
enabled: true
---

# 销售数据分析技能

## 能力

1. **GMV 计算**：按日/周/月/季/年维度计算 GMV，生成趋势图
2. **客户分层**：按累计消费将客户分为高价值(>10万)、中等(1-10万)、低价值(<1万)
3. **商品排名**：按销售额/销量/利润 Top-N 排名
4. **品类占比**：按商品分类计算销售额占比

## 数据要求

- 需包含 orders + order_items 表
- 客户分析需 customers 表

## 调用示例

```
@gmv 上月 --按分类
```

```
@customer-level --thresholds 100000,10000
```
