---
name: data-profile
version: 1.0.0
api_version: data-agent/v2
description: 为数据库查询结果和结构化文件生成通用数据画像，适用于用户明确要求字段画像、数据概览、候选主键或时间列识别的场景。
author: data-team
tags: [foundation, profiling, deterministic]
triggers:
  keywords: [数据画像, 字段画像, 列画像, 数据概览, 候选主键, 结构画像]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: profile_data
    description: 生成字段类型、空值、唯一性、候选键、时间列、重复行和稳定指纹
    input_schema: schemas/profile_input.json
    output_schema: schemas/profile_output.json
capabilities: [data.profile]
accepts: [database, table_file, timeseries]
permissions:
  network: []
  files: none
  datasources: read_only
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 1
  max_input_bytes: 2097152
  max_output_bytes: 1048576
entrypoints:
  execute: tools:profile_data
input_schema: schemas/profile_input.json
output_schema: schemas/profile_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 数据画像

1. 只分析已授权且已传入的行式数据，不读取额外文件或数据源。
2. 将字段缺失与显式空值统一计入空值率，并保留混合类型警告。
3. 仅把无空值且每行唯一的字段标记为候选主键，不声称它已经满足业务主键语义。
4. 仅在至少八成非空文本可按标准时间解析时标记时间列。
5. 将画像结果作为结构证据，不根据画像结果自动修改原始数据。
