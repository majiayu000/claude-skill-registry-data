---
name: custom-report
version: 1.0.0
api_version: data-agent/v2
description: 将已完成的查询与分析结果确定性渲染为周报或月报，适用于用户明确要求生成周期数据报告的场景。
author: data-team
tags: [foundation, report, deterministic]

triggers:
  keywords: [周报, 月报, 周度报告, 月度报告, 周期数据报告]
  intents: []
  tables: []

depends_on:
  mcp_servers: []
  skills: []
  python_packages: [jinja2]

tools:
  - name: render_report
    description: 用模板渲染数据报告
    input_schema: schemas/render_report_input.json
    output_schema: schemas/render_report_output.json

capabilities: [report.render]
accepts: [database, table_file]
permissions:
  network: []
  files: read_asset_only
  datasources: read_only
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 1
  max_input_bytes: 2097152
  max_output_bytes: 524288
entrypoints:
  execute: tools:render_report
input_schema: schemas/render_report_input.json
output_schema: schemas/render_report_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 自定义周期报告

1. 先完成数据查询和分析，再把已验证的摘要、洞察和指标传给渲染工具。
2. 明确请求月报时使用 `monthly_report`，其他周期报告请求使用 `weekly_report`。
3. 只渲染调用方提供的数据，不补造指标、趋势、异常或行动建议。
4. 输出 Markdown 文本，不写入文件系统；需要落盘或转换格式时交给专用导出能力。
5. 模板渲染失败时保留明确日志，并使用结构稳定的最小 Markdown 回退结果。
