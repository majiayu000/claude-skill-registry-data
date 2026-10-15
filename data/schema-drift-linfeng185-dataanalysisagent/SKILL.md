---
name: schema-drift
version: 1.0.0
api_version: data-agent/v2
description: 比较两版数据库或文件结构快照，识别表字段增删、类型、可空性、默认值和主键变化并判断兼容性，适用于发布前结构审查和上游变更监控。
author: data-team
tags: [governance, schema, deterministic]
triggers:
  keywords: [结构漂移检查, 结构版本对比, 破坏性结构变化]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: compare_schema_drift
    description: 区分结构版本中的破坏性、兼容性和信息性变化
    input_schema: schemas/drift_input.json
    output_schema: schemas/drift_output.json
capabilities: [schema.drift.compare]
accepts: [database, table_file]
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
  execute: tools:compare_schema_drift
input_schema: schemas/drift_input.json
output_schema: schemas/drift_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 结构漂移检查

1. 只比较调用方传入的两版结构快照，不连接数据库或猜测未声明结构。
2. 删除表、删除字段、收紧可空性、主键变化和非扩宽类型变化必须归为破坏性变化。
3. 新增可空字段或有默认值字段、放宽可空性和受支持的类型扩宽归为兼容变化。
4. 默认值与字段描述变化作为信息性变化返回，仍需由调用方确认业务影响。
5. 任一破坏性变化都必须使整体兼容性为假，并保留变化前后值和判定原因。
