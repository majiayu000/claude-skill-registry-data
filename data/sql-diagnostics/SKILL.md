---
name: sql-diagnostics
version: 1.0.0
api_version: data-agent/v2
description: 对 SQL 执行只读安全校验、方言兼容性检查、规范化改写和静态复杂度诊断，适用于 SQL 诊断、方言检查或查询复杂度审计场景。
author: data-team
tags: [foundation, sql, diagnostics]
triggers:
  keywords: [SQL诊断, SQL校验, 方言检查, SQL改写, 查询复杂度, 只读检查]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: [sqlglot]
tools:
  - name: diagnose_sql
    description: 校验并静态分析 SQL，返回错误、警告、规范化 SQL、表列和风险标记
    input_schema: schemas/diagnostics_input.json
    output_schema: schemas/diagnostics_output.json
capabilities: [sql.diagnose]
accepts: [database]
permissions:
  network: []
  files: none
  datasources: none
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 1
  max_input_bytes: 1048576
  max_output_bytes: 1048576
entrypoints:
  execute: tools:diagnose_sql
input_schema: schemas/diagnostics_input.json
output_schema: schemas/diagnostics_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# SQL 诊断

1. 只解析和改写 SQL，绝不连接数据库或执行语句。
2. 先经过平台统一只读安全校验，校验失败时不得生成可执行改写结果。
3. 按真实数据库方言解析，保留函数兼容性警告。
4. 静态风险只表示需要进一步检查，性能结论仍需真实 `EXPLAIN` 证据。
5. 输出必须明确 `executed=false`，避免调用方误解为已验证运行结果。
