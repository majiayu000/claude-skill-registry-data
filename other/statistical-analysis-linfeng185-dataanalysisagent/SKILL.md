---
name: statistical-analysis
version: 1.0.0
api_version: data-agent/v2
description: 对行式数据执行通用确定性统计，适用于用户明确要求描述统计、相关系数、集中度、趋势或四分位异常分析的场景。
author: data-team
tags: [foundation, statistics, deterministic]
triggers:
  keywords: [确定性统计, 描述统计, 相关系数, 集中度分析, Z-Score, 四分位异常]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: analyze_statistics
    description: 统一执行描述统计、趋势、异常、相关性和集中度计算
    input_schema: schemas/statistics_input.json
    output_schema: schemas/statistics_output.json
capabilities: [statistics.analyze]
accepts: [database, table_file, timeseries]
permissions:
  network: []
  files: none
  datasources: read_only
resources:
  timeout_seconds: 30
  cpu_seconds: 15
  memory_mb: 512
  max_tool_calls: 1
  max_input_bytes: 4194304
  max_output_bytes: 2097152
entrypoints:
  execute: tools:analyze_statistics
input_schema: schemas/statistics_input.json
output_schema: schemas/statistics_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 确定性统计分析

1. 所有数值必须由确定性统计函数计算，模型只可解释结果。
2. 某项分析缺少必要字段时记录跳过原因，不伪造结果。
3. 相关分析必须保留配对样本量，并明确相关性不代表因果。
4. 异常点只表示相对于当前样本偏离，不直接判定为数据错误。
5. 非有限数值必须拒绝，不能让其污染均值、方差或预测结果。
