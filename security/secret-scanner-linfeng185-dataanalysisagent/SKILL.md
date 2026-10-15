---
name: secret-scanner
version: 1.0.0
api_version: data-agent/v2
description: 扫描代码、配置和日志文本中的私钥、签名令牌、云访问键、源码平台令牌、内联连接凭据和敏感字段赋值，适用于提交前与日志交付前的凭据泄露检查。
author: data-team
tags: [security, credential, deterministic]
triggers:
  keywords: [工程凭据扫描, 密钥泄露检查, 连接串凭据检查]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: scan_secrets
    description: 扫描工程文本中的高风险凭据特征并仅返回不可逆指纹
    input_schema: schemas/secret_input.json
    output_schema: schemas/secret_output.json
capabilities: [security.credential.scan]
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
  execute: tools:scan_secrets
input_schema: schemas/secret_input.json
output_schema: schemas/secret_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 工程凭据扫描

1. 只扫描调用方传入的文本，不读取仓库、环境变量、配置文件或版本历史。
2. 对私钥块、签名令牌、访问键、连接地址和敏感字段赋值使用严格特征匹配。
3. 白名单仅接受不可逆指纹，不允许用原始凭据作为忽略规则。
4. 输出只能包含类别、来源定位、字符区间和截断哈希，禁止返回完整或局部凭据。
5. 命中后应撤销并轮换真实凭据；本工具不修改文本、不验证凭据有效性，也不调用外部服务。
