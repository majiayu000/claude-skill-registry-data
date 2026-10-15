---
name: workflow-state-diff
version: 1.0.0
api_version: data-agent/v2
description: 比较工作流执行前后状态及持久化快照，识别嵌套字段新增、删除、覆盖、保护字段变化和恢复差异，适用于状态写回与持久化边界核验。
author: data-team
tags: [engineering, state, deterministic]
triggers:
  keywords: [工作流状态差异, 状态写回核对, 持久化状态核验]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: compare_workflow_state
    description: 按嵌套字段路径比较执行前后状态和持久化状态
    input_schema: schemas/state_input.json
    output_schema: schemas/state_output.json
capabilities: [workflow.state.diff]
accepts: [stream]
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
  execute: tools:compare_workflow_state
input_schema: schemas/state_input.json
output_schema: schemas/state_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 工作流状态差异

1. 将嵌套对象展平为点分字段路径，数组保持原子值，显式空值必须与字段缺失区分。
2. 忽略字段不参与比较；保护字段发生新增、删除或修改时必须判为违规。
3. 必需后置字段缺失时必须失败，预期变化未发生时单独报告但不伪造状态更新。
4. 提供持久化快照时按指定字段核对写回值和存在性，禁止把空值当作未持久化。
5. 不修改任一状态对象，返回稳定指纹和有界差异明细。
