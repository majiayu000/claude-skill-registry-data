---
name: api-contract-drift
version: 1.0.0
api_version: data-agent/v2
description: 比较两版内联 OpenAPI 文档的路径、操作、认证、参数、请求体、响应状态和嵌套结构，适用于接口发布前的向后兼容性审查。
author: data-team
tags: [engineering, api, deterministic]
triggers:
  keywords: [接口契约漂移, OpenAPI版本对比, 接口破坏性变化]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: compare_api_contracts
    description: 比较两版 OpenAPI 并区分破坏性、兼容性和信息性变化
    input_schema: schemas/api_drift_input.json
    output_schema: schemas/api_drift_output.json
capabilities: [api.contract.drift]
accepts: [api]
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
  execute: tools:compare_api_contracts
input_schema: schemas/api_drift_input.json
output_schema: schemas/api_drift_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 接口契约漂移

1. 只比较调用方传入的 OpenAPI 对象，不访问接口地址或下载外部引用。
2. 仅解析当前文档内的本地引用，引用缺失、循环或嵌套深度超限时必须拒绝。
3. 删除路径、操作、参数、请求字段或响应字段，以及新增必填输入和认证要求必须归为破坏性变化。
4. 新增可选参数、操作、响应或向后兼容字段归为兼容变化，说明文本变化单独记录。
5. 兼容性判断面向协议结构，不替代真实客户端回归、状态码语义或鉴权策略测试。
