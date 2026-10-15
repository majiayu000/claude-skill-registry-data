---
name: resilience-policy-audit
version: 1.0.0
api_version: data-agent/v2
description: 审核服务或工具操作的单次超时、重试次数、退避、随机抖动、错误分类、熔断器、幂等键、失败补偿和最坏总耗时，适用于可靠性策略发布前检查。
author: data-team
tags: [engineering, resilience, deterministic]
triggers:
  keywords: [韧性策略审计, 重试退避检查, 幂等补偿核验]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: audit_resilience_policy
    description: 检查操作的超时、重试、退避、熔断、幂等和补偿策略
    input_schema: schemas/resilience_input.json
    output_schema: schemas/resilience_output.json
capabilities: [resilience.policy.audit]
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
  execute: tools:audit_resilience_policy
input_schema: schemas/resilience_input.json
output_schema: schemas/resilience_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 韧性策略审计

1. 多次尝试必须明确退避、初始等待和可重试错误，禁止使用匹配全部错误的通配重试。
2. 远程操作缺少随机抖动或熔断器时必须警告，熔断阈值和恢复参数必须为正数。
3. 有副作用的重试必须天然幂等或强制幂等键；非幂等操作还必须声明失败补偿。
4. 按重试次数、单次超时、退避上限和抖动计算最坏总耗时，超过预算时必须失败。
5. 只审核策略对象，不发起外部调用、不执行补偿，也不把高分视为运行时故障已经被处理。
