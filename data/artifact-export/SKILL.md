---
name: artifact-export
version: 1.0.0
api_version: data-agent/v2
description: 将通用分析产物确定性导出为 JSON、CSV 或 Markdown 内存文本，适用于生成 CSV、生成 JSON、生成 Markdown 或结构化结果序列化场景。
author: data-team
tags: [foundation, artifact, export]
triggers:
  keywords: [生成CSV, 生成JSON, 生成Markdown, 下载结构化结果, 序列化产物]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: export_artifact
    description: 将结构化产物导出为标准文本并返回媒体类型、大小和 SHA-256
    input_schema: schemas/export_input.json
    output_schema: schemas/export_output.json
capabilities: [artifact.export]
accepts: [database, table_file, document, timeseries, api, stream]
permissions:
  network: []
  files: none
  datasources: none
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 512
  max_tool_calls: 1
  max_input_bytes: 4194304
  max_output_bytes: 5242880
entrypoints:
  execute: tools:export_artifact
input_schema: schemas/export_input.json
output_schema: schemas/export_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 分析产物导出

1. 只返回内存文本和元数据，不写入宿主文件系统。
2. JSON 使用稳定键顺序，CSV 使用稳定列顺序，保证同一输入可复现。
3. CSV 中以公式控制字符开头的单元格必须中和，避免电子表格公式注入。
4. CSV 只接受对象数组；输入不满足行式结构时明确拒绝。
5. 输出必须包含媒体类型、扩展名、字节数和 SHA-256 校验值。
