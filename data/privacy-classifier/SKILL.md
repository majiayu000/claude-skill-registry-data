---
name: privacy-classifier
version: 1.0.0
api_version: data-agent/v2
description: 根据字段名和严格格式确定性识别邮箱、手机号、身份证、银行卡、网络地址、凭据、姓名和地址等敏感信息，适用于数据接入分级和安全策略前置分类，不执行脱敏。
author: data-team
tags: [governance, privacy, deterministic]
triggers:
  keywords: [隐私分类, 敏感字段识别, 凭据字段识别]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: classify_privacy
    description: 分类常见敏感字段和值并仅返回不可逆样例哈希
    input_schema: schemas/privacy_input.json
    output_schema: schemas/privacy_output.json
capabilities: [data.privacy.classify]
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
  execute: tools:classify_privacy
input_schema: schemas/privacy_input.json
output_schema: schemas/privacy_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 隐私分类

1. 使用字段名语义和严格值格式分类敏感信息，身份证与银行卡必须通过校验码后才按值命中。
2. 输出只能包含字段名、类别、敏感级别、置信度、数量、原因和截断哈希，禁止回显敏感原值。
3. 凭据类字段名命中时将其全部非空值视为敏感，不分析或记录凭据内容。
4. 分类结果只提供安全策略输入，不执行脱敏、阻断、授权判断或数据持久化。
5. 未命中不等于数据无风险；自定义行业标识和业务敏感字段仍需由核心安全层配置规则。
