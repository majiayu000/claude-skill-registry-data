---
name: data-quality-check
version: 1.0.0
api_version: data-agent/v2
description: 对已授权的行式查询结果执行空值率、重复值和数值异常检查，适用于用户明确要求核查数据质量、完整性、重复记录或异常值的场景。
author: data-team
tags: [foundation, quality, deterministic]

triggers:
  keywords: [数据质量, 空值, 重复, 异常检测, 数据校验, 完整性, 脏数据]
  intents: []
  tables: []

depends_on:
  mcp_servers: []
  skills: []
  python_packages: []

tools:
  - name: check_null_rate
    description: 检查指定列的空值率
    input_schema: schemas/quality_input.json
    output_schema: schemas/quality_output.json
  - name: check_duplicates
    description: 检查指定列的重复值
    input_schema: schemas/quality_input.json
    output_schema: schemas/quality_output.json
  - name: detect_outliers
    description: 用 Z-Score 方法检测异常值
    input_schema: schemas/quality_input.json
    output_schema: schemas/quality_output.json

capabilities: [data.quality]
accepts: [database, table_file]
permissions:
  network: []
  files: none
  datasources: read_only
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 50
  max_input_bytes: 2097152
  max_output_bytes: 524288
entrypoints:
  check_null_rate: tools:check_null_rate
  check_duplicates: tools:check_duplicates
  detect_outliers: tools:detect_outliers
input_schema: schemas/quality_input.json
output_schema: schemas/quality_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 数据质量检查

1. 只检查当前请求已经授权并显式传入的行式数据，不读取额外文件或数据源。
2. 将字段缺失和显式空值统一计入空值率，并同时返回样本总数和空值数量。
3. 重复值检查只统计非空值；异常值检查使用总体标准差和调用方给定的 Z-Score 阈值。
4. 少于八个有效样本时不输出异常值结论，避免把极小样本误判为稳定分布。
5. 将质量结果作为分析证据，不自动修改原始数据，也不把统计异常直接断言为数据错误。
