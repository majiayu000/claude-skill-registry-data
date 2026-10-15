---
name: provenance-audit
version: 1.0.0
api_version: data-agent/v2
description: 离线审核数据资产指纹、来源定位、工具参数、代码版本和有序变换链连续性，适用于分析结果追溯、制品验收和数据血缘完整性检查。
author: data-team
tags: [governance, provenance, deterministic]
triggers:
  keywords: [来源链审计, 数据血缘核查, 资产指纹审计]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: audit_provenance
    description: 审核资产清单和变换记录能否形成完整可追溯链路
    input_schema: schemas/provenance_input.json
    output_schema: schemas/provenance_output.json
capabilities: [data.provenance.audit]
accepts: [database, table_file, document]
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
  execute: tools:audit_provenance
input_schema: schemas/provenance_input.json
output_schema: schemas/provenance_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 来源链审计

1. 只审核调用方传入的资产和变换记录，不读取文件、代码仓库或外部元数据服务。
2. 每个资产必须有唯一标识和合法的小写 SHA-256 指纹；声明来源时必须同时提供证据定位。
3. 每个变换必须记录唯一步骤、输入资产、输出资产、工具、完整参数对象和代码版本。
4. 按变换数组顺序检查输入是否已经可用，禁止引用尚未产生的资产或重复产生同一输出。
5. 完整性得分只是记录完备程度；发现错误时必须使整体校验失败，不能据此证明数据内容真实。
