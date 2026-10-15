---
name: skill-evaluator
version: 1.0.0
api_version: data-agent/v2
description: 离线评估调用方提供的 Skill 执行记录，检查输出结构定义、期望子集、重复输出确定性、错误和耗时预算并执行最低得分门禁，适用于技能发布前回归验收。
author: data-team
tags: [governance, skill, evaluation]
triggers:
  keywords: [技能质量评测, 技能评测门禁, 确定性评测]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: [jsonschema]
tools:
  - name: evaluate_skill_runs
    description: 基于固定执行记录统计契约、期望、确定性、耗时和最低得分门禁
    input_schema: schemas/evaluator_input.json
    output_schema: schemas/evaluator_output.json
capabilities: [skill.evaluate]
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
  execute: tools:evaluate_skill_runs
input_schema: schemas/evaluator_input.json
output_schema: schemas/evaluator_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 技能质量评测

1. 只评估调用方传入的执行记录和内联输出结构定义，不导入、加载或执行任意待测代码。
2. 每个用例必须检查输出结构、期望子集、重复输出确定性和耗时预算；记录错误时增加执行失败项。
3. 期望对象按递归子集匹配，期望数组中的每个元素必须能在实际数组中找到匹配项。
4. 用例得分按检查项等权计算，全部用例通过且平均分达到门槛时整体门禁才通过。
5. 评测数据必须来自可重复执行或录制响应，不调用真实模型，也不把自然语言逐字一致作为质量标准。
