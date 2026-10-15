---
name: dataset-diff
version: 1.0.0
api_version: data-agent/v2
description: 按唯一主键确定性比较两版行式数据，识别新增、删除、修改、未变化记录和字段级差异，适用于数据发布验收、回归核对和迁移结果检查。
author: data-team
tags: [governance, diff, deterministic]
triggers:
  keywords: [数据集差异, 行级版本对比, 字段差异统计]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: compare_datasets
    description: 按唯一主键返回有界的行级和字段级差异
    input_schema: schemas/diff_input.json
    output_schema: schemas/diff_output.json
capabilities: [data.diff.compare]
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
  execute: tools:compare_datasets
input_schema: schemas/diff_input.json
output_schema: schemas/diff_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 数据集差异比较

1. 比较前必须验证两侧主键非空且唯一，主键质量不满足时立即拒绝。
2. 未指定比较字段时，使用两侧全部非主键字段的并集并按字段名稳定排序。
3. 数值字段只在绝对差超过显式容差时判为变化，其他值按稳定结构语义比较。
4. 差异明细必须受 `max_details` 限制，但新增、删除、修改和字段变化统计必须保持完整。
5. 不修改输入数据，也不把主键相同解释为记录业务含义相同。
