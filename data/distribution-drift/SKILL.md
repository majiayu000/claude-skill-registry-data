---
name: distribution-drift
version: 1.0.0
api_version: data-agent/v2
description: 比较基准集与当前集的数值和类别字段分布，计算群体稳定性指数、近似柯尔莫哥洛夫距离、统计量变化和总变差距离，适用于数据质量监控和模型输入漂移检查。
author: data-team
tags: [governance, drift, deterministic]
triggers:
  keywords: [分布漂移, 群体稳定性检查, 类别频率漂移]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: measure_distribution_drift
    description: 测量数值与类别字段的分布变化并按阈值标记漂移
    input_schema: schemas/distribution_input.json
    output_schema: schemas/distribution_output.json
capabilities: [data.distribution.drift]
accepts: [database, table_file, timeseries]
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
  execute: tools:measure_distribution_drift
input_schema: schemas/distribution_input.json
output_schema: schemas/distribution_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 分布漂移测量

1. 数值字段使用基准集分位点定义分箱，计算群体稳定性指数、经验分布最大距离、均值和标准差变化。
2. 类别字段在两侧类别并集上计算总变差距离，空值比例作为独立质量信号返回。
3. 仅当两侧非空值均为数值时采用数值算法；条件不足时降级为类别比较并说明原因。
4. 漂移判断只依据调用方显式阈值，不把统计漂移直接解释为业务异常或因果变化。
5. 所有指标由确定性函数计算，不调用模型，不修改输入数据，也不访问外部数据源。
