---
name: skill-validator
version: 1.0.0
api_version: data-agent/v2
description: 离线校验 Skill Manifest v2、工具 Schema、权限、资源预算、触发冲突和评测配置，适用于技能校验、清单校验或技能包发布前检查场景。
author: data-team
tags: [foundation, skill, validation]
triggers:
  keywords: [技能校验, Skill校验, 清单校验, Manifest校验, 触发冲突, 技能包检查]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: [jsonschema, pydantic]
tools:
  - name: validate_skill_manifest
    description: 校验调用方提供的清单对象、中文指令和内联 JSON Schema
    input_schema: schemas/validator_input.json
    output_schema: schemas/validator_output.json
capabilities: [skill.validate]
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
  execute: tools:validate_skill_manifest
input_schema: schemas/validator_input.json
output_schema: schemas/validator_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 技能包校验

1. 只校验调用方传入的清单、正文和内联 Schema，不读取任意文件路径。
2. 必须检查名称、语义版本、`data-agent/v2`、能力、资产类型和权限白名单。
3. 必须复用运行时资源上限，并单独限制工具调用次数。
4. 工具 Schema 只能声明在 `schemas/` 相对路径中，禁止绝对路径和目录穿越。
5. 触发重叠作为发布警告返回；结构错误必须使 `valid=false`。
