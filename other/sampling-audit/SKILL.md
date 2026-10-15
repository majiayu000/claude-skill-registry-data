---
name: sampling-audit
version: 1.0.0
api_version: data-agent/v2
description: 使用固定随机种子执行简单随机、系统、分层或时间窗口抽样，并比较样本与总体的分层占比，适用于可复现样本构造和代表性审计。
author: data-team
tags: [governance, sampling, deterministic]
triggers:
  keywords: [抽样审计, 分层抽样检查, 样本代表性]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: sample_with_audit
    description: 执行可复现抽样并量化样本与总体的分层占比差异
    input_schema: schemas/sampling_input.json
    output_schema: schemas/sampling_output.json
capabilities: [data.sample.audit]
accepts: [database, table_file, timeseries]
permissions:
  network: []
  files: none
  datasources: none
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 1
  max_input_bytes: 2097152
  max_output_bytes: 1048576
entrypoints:
  execute: tools:sample_with_audit
input_schema: schemas/sampling_input.json
output_schema: schemas/sampling_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 抽样与代表性审计

1. 所有随机选择都必须使用调用方传入的固定种子，相同输入和参数必须得到相同样本。
2. 随机抽样不放回，系统抽样使用固定随机起点，分层抽样按总体占比和最大余数法分配样本量。
3. 时间窗口必须按标准时间解析闭区间，窗口内记录超过样本量时再执行固定种子抽样。
4. 提供分层字段时必须报告总体占比、样本占比和最大绝对差，超过一成时给出警告。
5. 样本量超过总体时返回全部记录并明确告警，不复制或修改原始数据。
