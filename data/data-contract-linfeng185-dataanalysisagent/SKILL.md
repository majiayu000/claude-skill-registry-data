---
name: data-contract
version: 1.0.0
api_version: data-agent/v2
description: 按显式数据契约校验行式数据的字段存在性、类型、空值、唯一性、枚举、范围、正则和复合主键，适用于数据入库前校验、接口数据验收和质量门禁场景。
author: data-team
tags: [governance, contract, deterministic]
triggers:
  keywords: [数据契约校验, 字段约束审计, 复合键校验]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: validate_data_contract
    description: 校验字段、类型、空值、唯一性、枚举、范围、正则和复合主键约束
    input_schema: schemas/contract_input.json
    output_schema: schemas/contract_output.json
capabilities: [data.contract.validate]
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
  execute: tools:validate_data_contract
input_schema: schemas/contract_input.json
output_schema: schemas/contract_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 数据契约校验

1. 只校验调用方明确传入的行式数据和契约，不读取数据源或推断业务规则。
2. 先检查契约结构，再按字段存在性、类型、空值、枚举、范围、正则和唯一性依次校验。
3. 复合主键中的任一字段为空或组合值重复都必须记录为错误。
4. 违规明细必须受 `max_violations` 限制，同时保留完整违规总数和按代码统计。
5. 不修改原始数据；契约通过只表示满足显式技术约束，不代表业务语义正确。
