---
name: reproducibility-audit
version: 1.0.0
api_version: data-agent/v2
description: 比较多次执行记录的输入指纹、代码版本、依赖版本、配置指纹、运行环境、随机种子和输出指纹，适用于分析结果复现验收和环境漂移诊断。
author: data-team
tags: [engineering, reproducibility, deterministic]
triggers:
  keywords: [可复现性审计, 重复执行一致性, 运行环境复现]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: audit_reproducibility
    description: 审核重复执行上下文和输出指纹是否保持一致
    input_schema: schemas/reproducibility_input.json
    output_schema: schemas/reproducibility_output.json
capabilities: [execution.reproducibility.audit]
accepts: [document]
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
  execute: tools:audit_reproducibility
input_schema: schemas/reproducibility_input.json
output_schema: schemas/reproducibility_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 可复现性审计

1. 至少使用两次完整执行记录，第一条记录作为比较基准但不视为天然正确。
2. 输入、代码、依赖、配置、环境和随机种子任一变化都必须单独报告上下文漂移。
3. 相同上下文下输出指纹不一致必须使可复现性失败；上下文不同也不能声称输出可比。
4. 所有资产指纹必须是完整小写 SHA-256，依赖必须同时记录名称和版本。
5. 只审核调用记录，不读取环境或重新执行任务，并明确返回未访问文件系统的安全声明。
