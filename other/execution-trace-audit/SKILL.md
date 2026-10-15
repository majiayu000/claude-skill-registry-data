---
name: execution-trace-audit
version: 1.0.0
api_version: data-agent/v2
description: 审计工作流节点跨度的执行顺序、耗时、尝试次数、错误恢复和状态写回，适用于运行轨迹诊断、重试链路验收和节点性能门禁场景。
author: data-team
tags: [engineering, trace, deterministic]
triggers:
  keywords: [执行轨迹审计, 节点耗时审查, 重试链路检查]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: audit_execution_trace
    description: 检查节点跨度顺序、耗时、重试、终态和状态字段写回完整性
    input_schema: schemas/trace_input.json
    output_schema: schemas/trace_output.json
capabilities: [workflow.trace.audit]
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
  execute: tools:audit_execution_trace
input_schema: schemas/trace_input.json
output_schema: schemas/trace_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 执行轨迹审计

1. 只审计调用方传入的节点跨度记录，不连接追踪平台或恢复缺失事件。
2. 按执行序号检查顺序和断档，按节点检查尝试次数连续性、重试上限和最终成功状态。
3. 结束时间早于开始时间必须报错，节点耗时超过预算作为明确警告保留。
4. 预期节点缺失或必需状态字段没有写回记录时必须使整体审计失败。
5. 问题明细必须受上限约束，但错误、警告和总问题数量不得因截断而漏算。
