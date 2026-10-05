---
name: dw-data-comparison
description: 数仓数据比对流程，适用于新旧表、上下游表、核心金额字段和指标口径差异分析。直接调用命令：/dw-data-comparison。
---

# Step 5: 数据比对

## 执行流程

1. 调用 `data-comparator` subagent 进行新旧表数据对比
2. subagent 在独立 context 运行，只返回差异超过容差的字段
3. 主对话只接收差异摘要

## 推荐提示词

```
用 data-comparator subagent 对比数据：
- 新表: [表名], partition_dt = '[日期]'
- 参考表: [表名], partition_dt = '[日期]'
- 比对字段: [核心金额字段列表]
- 容差: ≤ 0.01%（金额类）
只返回差异超过容差的字段列表及差值。
```

## 比对参数

| 字段类型 | 容差 |
|---------|------|
| 金额类 | ≤ 0.01% |
| 数量类 | ≤ 0.1% |
| 字符串类 | 精确匹配 |

## 输出

由 data-comparator subagent 返回：
- 字段级差异列表
- 差异率
- 差值说明
- 结论（通过/需关注）
