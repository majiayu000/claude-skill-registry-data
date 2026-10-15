---
name: schema-linking
version: 1.0.0
api_version: data-agent/v2
description: 将自然语言术语映射为表、字段和关联键候选，适用于用户明确要求字段映射、模式映射、术语对齐或关联路径检查的场景。
author: data-team
tags: [foundation, schema, linking]
triggers:
  keywords: [字段映射, 模式映射, 术语映射, 表字段匹配, 关联路径, Schema映射]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: link_schema
    description: 根据名称、别名和描述生成带分数与原因的模式候选
    input_schema: schemas/linking_input.json
    output_schema: schemas/linking_output.json
capabilities: [schema.link]
accepts: [database, table_file]
permissions:
  network: []
  files: none
  datasources: read_only
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 1
  max_input_bytes: 2097152
  max_output_bytes: 1048576
entrypoints:
  execute: tools:link_schema
input_schema: schemas/linking_input.json
output_schema: schemas/linking_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 模式语义映射

1. 只根据调用方提供的表、字段、别名和描述生成词法候选。
2. 为每个候选保留命中词、分数和评分原因，不把候选描述为已确认语义。
3. 最高候选分数接近时必须返回歧义，不能自行选择。
4. 同名字段只能作为关联键候选；执行连接前必须再经过 `JoinContract` 验证。
5. 没有可靠候选时返回未映射状态，不生成不存在的表或字段。
