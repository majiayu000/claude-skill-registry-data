---
name: file-ingestion-inspector
version: 1.0.0
api_version: data-agent/v2
description: 检查调用方传入的 Base64 文件样本及归档元数据，识别编码、BOM、分隔符、表头、换行、公式前缀、解压比、宏和外链风险，适用于结构化文件摄取前门禁。
author: data-team
tags: [engineering, ingestion, deterministic]
triggers:
  keywords: [文件摄取检查, 文件编码检测, 归档炸弹风险]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: inspect_file_ingestion
    description: 检查有界文件样本和归档元数据是否适合安全摄取
    input_schema: schemas/ingestion_input.json
    output_schema: schemas/ingestion_output.json
capabilities: [file.ingestion.inspect]
accepts: [table_file]
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
  execute: tools:inspect_file_ingestion
input_schema: schemas/ingestion_input.json
output_schema: schemas/ingestion_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 文件摄取检查

1. 只解码调用方传入的有界 Base64 样本，不接受宿主文件路径或主动解压归档。
2. 优先使用 BOM 和显式编码严格解码；无 BOM 时只按 UTF-8、GB18030 顺序保守推断。
3. 根据多行字段数一致性识别分隔符，并检查空表头、重复表头、混合换行和公式前缀。
4. 归档风险只能依据显式元数据判断，解压比、条目数、加密和宏超过边界时必须阻断。
5. 外部链接只保留风险警告，禁止自动刷新；检查通过不代表文件内容或公式业务安全。
