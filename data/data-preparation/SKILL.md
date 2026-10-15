---
name: data-preparation
version: 1.0.0
api_version: data-agent/v2
description: 对行式数据执行非破坏式、可审计的数据准备，适用于用户明确要求去重、缺失值填充、类型转换、字段重命名、选列或排序的场景。
author: data-team
tags: [foundation, preparation, deterministic]
triggers:
  keywords: [数据清洗, 数据准备, 类型转换, 去重清洗, 字段重命名, 缺失值填充]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: prepare_data
    description: 按显式白名单步骤转换数据并返回逐步审计记录
    input_schema: schemas/preparation_input.json
    output_schema: schemas/preparation_output.json
capabilities: [data.prepare]
accepts: [database, table_file, timeseries]
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
  max_output_bytes: 4194304
entrypoints:
  execute: tools:prepare_data
input_schema: schemas/preparation_input.json
output_schema: schemas/preparation_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 数据准备

1. 必须由调用方显式给出变换步骤，不根据自然语言猜测破坏性操作。
2. 按声明顺序执行步骤，并为每一步记录前后行数和实际变更。
3. 保持输入数据不变，只返回新的结果行。
4. 字段缺失、目标字段冲突、混合类型不可排序或类型转换失败时立即拒绝。
5. 仅支持清单声明的白名单操作，不执行任意表达式、脚本或文件写入。
