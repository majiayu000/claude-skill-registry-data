---
name: numeric-integrity-audit
version: 1.0.0
api_version: data-agent/v2
description: 按显式字段规则检查行式数据中的数值类型、非有限值、上下界、整数约束、十进制精度、舍入结果和单位一致性，适用于计算与导出前的数值质量门禁。
author: data-team
tags: [governance, numeric, deterministic]
triggers:
  keywords: [数值完整性审计, 小数精度检查, 单位一致性核验]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: audit_numeric_integrity
    description: 检查数值有限性、类型、范围、精度、舍入和单位规则
    input_schema: schemas/numeric_input.json
    output_schema: schemas/numeric_output.json
capabilities: [data.numeric.integrity]
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
  execute: tools:audit_numeric_integrity
input_schema: schemas/numeric_input.json
output_schema: schemas/numeric_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 数值完整性审计

1. 只按显式字段规则检查数值，不推断货币、单位、精度或合理范围。
2. 布尔值不得当作整数，非有限浮点值、非数值文本和无法转换的十进制值必须报错。
3. 金额默认要求两位小数；其他字段只有声明小数位时才检查舍入，并返回建议值但不修改输入。
4. 声明预期单位时必须同时提供单位字段，缺失或不同单位都必须失败。
5. 问题明细可以截断，但完整错误计数、字段统计和输入未修改声明必须保留。
