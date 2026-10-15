---
name: result-verification
version: 1.0.0
api_version: data-agent/v2
description: 对结构化分析结果执行空结果、行数、必需字段、唯一性、数值范围和汇总明细一致性核验，并审查截断与部分结果状态，适用于结果交付前质量门禁。
author: data-team
tags: [governance, verification, deterministic]
triggers:
  keywords: [结果核验, 汇总明细核对, 截断状态检查]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: verify_result
    description: 执行结果质量规则并判断结果是否完整且通过核验
    input_schema: schemas/verification_input.json
    output_schema: schemas/verification_output.json
capabilities: [result.verify]
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
  execute: tools:verify_result
input_schema: schemas/verification_input.json
output_schema: schemas/verification_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 结果核验

1. 只按显式规则核验调用方传入的明细和汇总，不重新执行原始查询或补造缺失数据。
2. 支持非空、行数、必需字段、字段组合唯一、数值范围以及求和、计数、平均、最小和最大核对。
3. 数值汇总使用显式容差；汇总字段缺失、非数值混入或规则参数不完整都必须明确失败或拒绝。
4. `truncated` 或 `partial` 为真时结果必须标记为不完整，即使所有内容规则通过也不能标记为已验证。
5. 核验通过只说明满足所给规则，不代表上游查询、业务口径或来源数据天然正确。
