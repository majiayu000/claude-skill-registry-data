---
name: semantic-normalization
version: 1.0.0
api_version: data-agent/v2
description: 按显式规则统一行式数据中的空值标记、布尔值、日期时区、数值单位和枚举别名，适用于跨来源数据对齐、分析前标准化和迁移数据预处理。
author: data-team
tags: [governance, normalization, deterministic]
triggers:
  keywords: [语义规范化, 数值单位统一, 枚举归一]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: normalize_semantics
    description: 按字段规则规范化空值、布尔、时区、单位和枚举值
    input_schema: schemas/normalization_input.json
    output_schema: schemas/normalization_output.json
capabilities: [data.semantic.normalize]
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
  execute: tools:normalize_semantics
input_schema: schemas/normalization_input.json
output_schema: schemas/normalization_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 语义规范化

1. 只执行调用方明确声明的字段规则，不自动猜测单位、时区、枚举或空值语义。
2. 空值、布尔、时间、缩放和枚举规则逐条应用；无法转换时保留原值并记录行号、字段和原因。
3. 无时区时间必须使用显式来源时区解释，再转换到目标时区并输出带偏移的标准时间。
4. 数值缩放必须排除布尔值，枚举转换必须要求非空映射，禁止静默吞掉未知枚举。
5. 始终深复制输入，返回逐值审计和输出指纹，不修改调用方持有的原始数据。
