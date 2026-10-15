---
name: timeseries-analysis
version: 1.0.0
api_version: data-agent/v2
description: 对严格有序的单变量时间序列执行趋势、滚动回测、基线模型选择和区间预测，适用于时间序列分析、滚动回测或预测区间场景。
author: data-team
tags: [foundation, timeseries, forecast]
triggers:
  keywords: [时间序列分析, 滚动回测, 预测区间, 单变量预测, 序列趋势, 基线模型]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: [statistical-analysis]
  python_packages: []
tools:
  - name: analyze_timeseries
    description: 校验时间顺序并输出趋势、回测指标、预测值、区间和模型卡
    input_schema: schemas/timeseries_input.json
    output_schema: schemas/timeseries_output.json
capabilities: [timeseries.analyze]
accepts: [database, table_file, timeseries]
permissions:
  network: []
  files: none
  datasources: read_only
resources:
  timeout_seconds: 60
  cpu_seconds: 30
  memory_mb: 512
  max_tool_calls: 1
  max_input_bytes: 4194304
  max_output_bytes: 2097152
entrypoints:
  execute: tools:analyze_timeseries
input_schema: schemas/timeseries_input.json
output_schema: schemas/timeseries_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 时间序列分析

1. 时间列必须严格递增且不能重复，禁止静默重排造成时间泄漏。
2. 数值必须有限，样本不足时拒绝预测。
3. 使用滚动回测比较简单基线，只输出回测支持的模型。
4. 同时输出预测区间、模型卡、时间范围和间隔规则性。
5. 明确预测只基于历史单变量模式，不构成确定性承诺。
