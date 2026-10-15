---
name: cross-source-fusion
version: 1.0.0
api_version: data-agent/v2
description: 在跨资产连接前检查匹配率、连接基数和结果膨胀风险，适用于跨数据源连接、跨文件核对、匹配率检查或 Join 契约审计场景。
author: data-team
tags: [foundation, join, governance]
triggers:
  keywords: [跨源融合, 跨数据源连接, 跨文件核对, 匹配率检查, Join契约, 连接基数]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: [schema-linking]
  python_packages: []
tools:
  - name: inspect_join
    description: 构造 JoinContract 并在满足安全条件时生成有界内连接预览
    input_schema: schemas/fusion_input.json
    output_schema: schemas/fusion_output.json
capabilities: [data.join.inspect]
accepts: [database, table_file, timeseries, api]
permissions:
  network: []
  files: none
  datasources: read_only
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 512
  max_tool_calls: 1
  max_input_bytes: 4194304
  max_output_bytes: 2097152
entrypoints:
  execute: tools:inspect_join
input_schema: schemas/fusion_input.json
output_schema: schemas/fusion_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 跨源融合检查

1. 必须先检查两侧连接键是否存在，再计算匹配率、基数和膨胀因子。
2. 左侧匹配率低于八成、多对多连接或膨胀超过十倍时默认阻断。
3. 风险连接只有在调用方显式确认后才能生成有界预览。
4. 只返回内连接预览，不修改、覆盖或持久化任何资产。
5. 连接键的词法同名不等于业务语义一致，输出中必须保留该限制。
